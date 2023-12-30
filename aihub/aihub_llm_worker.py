import argparse
import json
import logging
import time

import grpc
import aihub_pb2
import aihub_pb2_grpc

from google.protobuf import empty_pb2
from aihub import send_request


def main(api):
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
            task = stub.StartGeneratingAnswer(empty)
            if task.id > 0:
                # If this is a valid task, process it.
                print("Received: ", task)
                answer = send_request(task.question, api)
                # task.answer = "This is the answer from LLM"
                task.answer = answer
                task.status = aihub_pb2.ANSWER_AVAILABLE
                print("Adding answer: ", task)
                stub.AddAnswer(task)
            else:
                print("No task to work on!")

            time.sleep(5)

def load_configuration_from_file(self):
    try:
        with open('config.json', 'r') as file:
            config_data = json.load(file)

            # Update StringVar values
            for key, value in config_data.items():
                self.configuration_settings[key].set(value)
    except FileNotFoundError:
        print("Config file not found. Using default values.")

if __name__ == "__main__":
    logging.basicConfig()
    api = ''
    prompt_prefix = ''
    try:
        with open('config.json', 'r') as file:
            config_data = json.load(file)

            # Update StringVar values
            api = config_data['api']
            prompt_prefix = config_data['prompt_prefix']
    except FileNotFoundError:
        print("Config file not found. Using default values.")

    main(api)
