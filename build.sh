#!/bin/bash

python -m grpc_tools.protoc -I. --python_out=./aihub --pyi_out=./aihub --grpc_python_out=./aihub aihub.proto
