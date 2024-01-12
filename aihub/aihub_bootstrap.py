import argparse
import logging
import signal
import subprocess
import sys
import time


class SignalHandler:
  def __init__(self):
    self.run = True
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self, signum, frame):
    self.run = False


def main():
    parser = argparse.ArgumentParser(description="aiHub bootstrap arg parse")
    parser.add_argument(
        "-p", "--port", type=int, help="Task manager port.", default=50051
    )
    args = parser.parse_args()
    port = args.port

    # Start processes.
    modules_to_run = [
        "aihub_task_manager",
        "aihub_keyboard_listener",
        "aihub_llm_worker",
        "aihub_gui",
    ]
    processes = []
    for module_name in modules_to_run:
        process = subprocess.Popen(
            [sys.executable, "-m", module_name, "-p", str(port)],
            stdout=subprocess.PIPE, text=True)
        print(module_name, process.pid)
        processes.append(process)

    # Handle termination signals gracefully and stop the started background
    # processes.
    signal_handler = SignalHandler()
    while signal_handler.run:
        # Wait for signal to exit.
        time.sleep(2)

    print("Terminating processes!")
    for process in processes:
        process.terminate()
        print(process.pid, "terminated.")

if __name__ == "__main__":
    logging.basicConfig()
    main()
