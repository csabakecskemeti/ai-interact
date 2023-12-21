import argparse
from concurrent import futures
import logging

import grpc
import aihub_pb2
import aihub_pb2_grpc


class IdGenerator(object):
    def __init__(self):
        self._id = 0

    def new_id(self):
        # TODO: Generate UUID or something similar.
        self._id += 1
        return self._id


class TaskManager(aihub_pb2_grpc.AIHubServicer):
    def __init__(self, id_gen):
        self._tasks = {}
        self._id_gen = id_gen

    def AddNewTask(self, request, context):
        # TODO: Check if `question` is peresent, if not return error status.
        request.id = self._id_gen.new_id()
        request.status = aihub_pb2.NEW
        self._tasks[request.id] = request
        print("AddNewTask", self._tasks, request)
        return request

    def StartGeneratingAnswer(self, request, context):
        new_tasks = [
            task_id
            for task_id, task in self._tasks.items()
            if task.status == aihub_pb2.NEW
        ]

        # TODO: Handle this properly.
        if not new_tasks:
            return aihub_pb2.Task()

        new_task = self._tasks[new_tasks[0]]
        new_task.status = aihub_pb2.GENERATING_ANSWER
        print("StartGeneratingAnswer", self._tasks, new_task)
        return new_task

    def AddAnswer(self, request, context):
        # TODO: Handle this properly.
        if not request.id in self._tasks:
            return aihub_pb2.Task()

        task = self._tasks[request.id]
        task.status = aihub_pb2.ANSWER_AVAILABLE
        task.answer = request.answer
        print("AddAnswer", self._tasks, task)
        return task

    def RemoveProcessedQuestion(self, request, context):
        processed_tasks = [
            task_id
            for task_id, task in self._tasks.items()
            if task.status == aihub_pb2.ANSWER_AVAILABLE
        ]

        # TODO: Handle this properly.
        if not processed_tasks:
            return aihub_pb2.Task()

        processed_task = self._tasks[processed_tasks[0]]
        del self._tasks[processed_task.id]
        print("RemoveProcessedQuestion", self._tasks, processed_task)
        return processed_task


def main():
    parser = argparse.ArgumentParser(description="aiHub task manager arg parse")
    parser.add_argument(
        "-p", "--port", type=int, help="Task manager port.", default=50051
    )
    args = parser.parse_args()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    aihub_pb2_grpc.add_AIHubServicer_to_server(TaskManager(IdGenerator()), server)
    server.add_insecure_port("[::]:{}".format(args.port))
    server.start()
    print("Task manager started, listening on {}".format(args.port))
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    main()
