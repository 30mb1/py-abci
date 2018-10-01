
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


Getting Started
---------------
1. Extend the BaseApplication class
2. Implement the Tendermint ABCI callbacks - see https://github.com/tendermint/abci
3. Run it

See the example app ``counter.py`` application under the ``examples`` directory
here: https://github.com/SoftblocksCo/tm-abci/blob/master/examples/counter.py
