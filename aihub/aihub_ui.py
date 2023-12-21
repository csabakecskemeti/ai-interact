import argparse
import logging
import time

import grpc
import aihub_pb2
import aihub_pb2_grpc

from google.protobuf import empty_pb2


def main():
    parser = argparse.ArgumentParser(description="aiHub keyboard listener arg parse")
    parser.add_argument(
        "-t", "--host", type=str, help="Task manager host.", default="localhost"
    )
    parser.add_argument(
        "-p", "--port", type=int, help="Task manager port.", default=50051
    )
    args = parser.parse_args()

    empty = empty_pb2.Empty()
    with grpc.insecure_channel("{}:{}".format(args.host, args.port)) as channel:
        stub = aihub_pb2_grpc.AIHubStub(channel)
        while True:
            processed_task = stub.RemoveProcessedQuestion(empty)
            if processed_task.id > 0:
                # If this is a valid task, show it on UI.
                print("Received: ", processed_task)
            else:
                print("No new processed task to show on UI!")

            time.sleep(5)


if __name__ == "__main__":
    logging.basicConfig()
    main()
