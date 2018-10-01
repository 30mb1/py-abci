
Build blockchain applications in Python for Tendermint

Version
-------
Supports ABCI v0.14.0 and latest Tendermint

Installation
------------
Requires Python >= 3.6.5

``pip install tm-abci``  OR ``python setup.py install``

Generating Protobuf
-------------------
*ONLY* needed for developing this code base, not to create apps.  If you
just want to create apps, goto Getting Started

1. Update all .proto files (protobuf dir)
2. Install protoc
3. Install go
4. Install gogo protobuf via go
5. Run `make gogo`

Or using Docker container:

1. Update all .proto files (protobuf dir)
2. Build image:``sudo docker build -t abcidev .``
3. Run container: ``sudo docker run -it abcidev sh``
4. Inside container run: ``make gogo``

Testing with tm-bench
---------------------
Use this if you want to test throughput of server and application. By default, dummpy app is used,
you can change it in docker-compose.yml, abci command section (before build).

1. Build tm-bench and move to tm-abci directory (you can get it `here <https://github.com/tendermint/tendermint/tree/master/tools/tm-bench>`_)
2. Change testing config in tm-bench command section of docker-compose.yml
3. Run  ``sudo docker-compose -f docker-compose.yml up -d``
4. Wait about minute (or more/less if you changed default) and run ``sudo docker-compose -f docker-compose.yml logs --tail 50 tm-bench``

Getting Started
---------------
1. Extend the BaseApplication class
2. Implement the Tendermint ABCI callbacks - see https://github.com/tendermint/abci
3. Run it

See the example app ``counter.py`` application under the ``examples`` directory
here: https://github.com/SoftblocksCo/tm-abci/blob/master/examples/counter.py
