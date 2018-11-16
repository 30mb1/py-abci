
reset_tm:
	rm -Rf .test_pyabci
	tendermint --home .test_pyabci init

dev-install:
	pip install --editable .

gogo:
	protoc protobuf/github.com/gogo/protobuf/gogoproto/gogo.proto --python_out=./
	protoc protobuf/github.com/tendermint/tendermint/libs/common/types.proto --python_out=./
	protoc protobuf/github.com/tendermint/tendermint/crypto/merkle/merkle.proto --python_out=./
	protoc protobuf/types.proto --python_out=abci/
	mv abci/protobuf/types_pb2.py abci/types_pb2.py

clean:
	rm -Rf dist/
	rm -Rf abci.egg-info
