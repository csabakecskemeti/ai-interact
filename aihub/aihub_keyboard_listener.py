import argparse
import logging

import grpc
import aihub_pb2
import aihub_pb2_grpc


def main():
    parser = argparse.ArgumentParser(description="aiHub keyboard listener arg parse")
    parser.add_argument(
        "-t", "--host", type=str, help="Task manager host.", default="localhost"
    )
    parser.add_argument(
        "-p", "--port", type=int, help="Task manager port.", default=50051
    )
    args = parser.parse_args()

    # This should have a main loop waiting for shorcut pressed, when it happens
    # it should call teserac, and create a new task with the following call.
    with grpc.insecure_channel("{}:{}".format(args.host, args.port)) as channel:
        stub = aihub_pb2_grpc.AIHubStub(channel)
        stub.AddNewTask(aihub_pb2.Task(question="This is the question from teserac."))


if __name__ == "__main__":
    logging.basicConfig()
    main()
