"""
ABCI TCP server
Tendermint connects to this server over 3 different connections:
 - mempool: used for check_tx
 - consensus: used for the begin_block -> deliver_tx -> end_block -> commit flow
 - query: used to query application state

This can be a bit confusing in the app since gevent spawns a greenlet for each
connection.  If one crashes you will not have full connectivity to Tendermint
"""

import signal
from io import BytesIO
import asyncio
from contextlib import suppress


from .encoding import read_messages, write_message
from .utils import get_logger
from .application import BaseApplication

from .types_pb2 import (
    Request, Response, ResponseEcho,
    ResponseFlush, ResponseException
)

log = get_logger()


class ProtocolHandler:
    """ Internal handler called by the server to process requests from
    Tendermint.  The handler delegates call to your application"""

    def __init__(self, app):
        self.app = app

    def process(self, req_type, req):
        handler = getattr(self, req_type, self.no_match)
        return handler(req)

    def echo(self, req):
        msg = req.echo.message
        response = Response(echo=ResponseEcho(message=msg))
        return write_message(response)

    def flush(self, req):
        response = Response(flush=ResponseFlush())
        return write_message(response)

    def info(self, req):
        result = self.app.info(req.info)
        response = Response(info=result)
        return write_message(response)

    def set_option(self, req):
        result = self.app.set_option(req.set_option)
        response = Response(set_option=result)
        return write_message(response)

    def check_tx(self, req):
        result = self.app.check_tx(req.check_tx.tx)
        response = Response(check_tx=result)
        return write_message(response)

    def deliver_tx(self, req):
        result = self.app.deliver_tx(req.deliver_tx.tx)
        response = Response(deliver_tx=result)
        return write_message(response)

    def query(self, req):
        result = self.app.query(req.query)
        response = Response(query=result)
        return write_message(response)

    def commit(self, req):
        result = self.app.commit()
        response = Response(commit=result)
        return write_message(response)

    def begin_block(self, req):
        result = self.app.begin_block(req.begin_block)
        response = Response(begin_block=result)
        return write_message(response)

    def end_block(self, req):
        result = self.app.end_block(req.end_block)
        response = Response(end_block=result)
        return write_message(response)

    def init_chain(self, req):
        result = self.app.init_chain(req.init_chain)
        response = Response(init_chain=result)
        return write_message(response)

    def no_match(self, req):
        response = Response(exception=ResponseException(error="ABCI request not found"))
        return write_message(response)


def handler(signum, frame):
    raise Exception

signal.signal(signal.SIGQUIT, handler)
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)


class ABCIServer:
    def __init__(self, port=26658, app=None):
        if not app or not isinstance(app, BaseApplication):
            log.error("Application missing or not an instance of Base Application")
            raise TypeError("Application missing or not an instance of Base Application")
        self.port = port
        self.protocol = ProtocolHandler(app)

        self.loop = asyncio.get_event_loop()
        coro = asyncio.start_server(self.__handle_connection, '0.0.0.0', 26658, loop=self.loop)
        self.server = self.loop.run_until_complete(coro)

    def run(self):
        """Option to calling manually calling start()/stop(). This will start
        the server and watch for signals to stop the server"""
        log.info(" ABCIServer started on port: {}".format(self.port))
        try:
            self.loop.run_forever()
        except Exception:
            pass

        pending = asyncio.Task.all_tasks()
        list(map(lambda task: task.cancel(), pending))
        with suppress(asyncio.CancelledError):
            self.loop.run_until_complete(asyncio.gather(*pending))

        # Close the server
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())
        log.info("Shutting down server")
        self.loop.close()


    # TM will spawn off 3 connections: mempool, consensus, query
    # If an error happens in 1 it still leaves the others open which
    # means you don't have all the connections available to TM
    async def __handle_connection(self, reader, writer):
        addr = writer.get_extra_info('peername')
        log.info(f' ... Connection from Tendermint: {addr[0]}:{addr[1]} ...')
        data = BytesIO()
        last_pos = 0

        while True:

            # Create a new buffer every time there is the possibility.
            # This avoids having a never ending buffer.
            if last_pos == data.tell():
                data = BytesIO()
                last_pos = 0

            inbound = await reader.read(1024 * 8)
            data.write(inbound)

            if not len(inbound):
                break

            # Before reading the messages from the buffer, position the
            # cursor at the end of the last read message.
            data.seek(last_pos)
            messages = read_messages(data, Request)

            for message in messages:
                req_type = message.WhichOneof('value')
                response = self.protocol.process(req_type, message)
                writer.write(response)
                await writer.drain()
                last_pos = data.tell()

        writer.close()
