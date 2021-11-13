#!/bin/bash

# protobuff and grpc generator: 
# "-I": include directory
# "--python_out" specify python protobuf interface output file
# "--grpc_python_out" specify python grpc interface output file
python -m grpc_tools.protoc -I=. --python_out=../src --grpc_python_out=../src actuator_server.proto
python -m grpc_tools.protoc -I=. --python_out=../src --grpc_python_out=../src master_server.proto