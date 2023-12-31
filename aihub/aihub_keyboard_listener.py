import argparse
import logging
from pynput.mouse import Listener
from pynput import keyboard
from PIL import Image, ImageGrab
import pytesseract

import grpc
import aihub_pb2
import aihub_pb2_grpc

COMBINATIONS = [
    {keyboard.Key.shift, keyboard.Key.f1},
    {keyboard.Key.shift, keyboard.Key.f12}
]
current = set()

class ClickListener:
    def __init__(self):
        self.coordinates = None
        self.keep_listening = True


    def on_click(self, x, y, button, pressed):
        if pressed:
            self.coordinates = int(x), int(y)
            self.keep_listening = False
            return False  # Stop the listener


    def get_coordinates(self):
        with Listener(on_click=self.on_click) as listener:
            listener.join()  # This will block until on_click returns False
        return self.coordinates


def capture_screen():
    # Create an instance of ClickListener
    click_listener = ClickListener()

    # Get the mouse coordinates after the first click
    x1, y1 = click_listener.get_coordinates()
    x2, y2 = click_listener.get_coordinates()

    logging.info(f'Rectangle: x1: {x1} y1: {y1} x2: {x2} y2: {y2}')
    try:
        image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    except:
        return None
    return image

def capture():
    text = ''
    image = capture_screen()
    if image != None:
        text = pytesseract.image_to_string(image)
    return text


def main():
    parser = argparse.ArgumentParser(description="aiHub keyboard listener arg parse")
    parser.add_argument(
        "-t", "--host", type=str, help="Task manager host.", default="localhost"
    )
    parser.add_argument(
        "-p", "--port", type=int, help="Task manager port.", default=50051
    )
    args = parser.parse_args()

    def on_press(key):
        if any([key in COMBO for COMBO in COMBINATIONS]):
            current.add(key)
            logging.info(f'key combo pressed: {current}')
            # if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            # if any(x in current for x in {keyboard.KeyCode(char='A')}):
            if any(keypressed in current for keypressed in {keyboard.Key.f1}):
                stub.AddNewTask(aihub_pb2.Task(question=capture()))
            # if key == keyboard.Key.shift and any(x in current for x in {keyboard.KeyCode(char='X')}):
            if any(keypressed in current for keypressed in {keyboard.Key.f12}):
                logging.info('Shift + F12 pressed. Stopping the listener.')
                listener.stop()

    def on_release(key):
        try:
            if any([key in COMBO for COMBO in COMBINATIONS]):
                current.remove(key)
        except:
            pass
    # This should have a main loop waiting for shorcut pressed, when it happens
    # it should call teserac, and create a new task with the following call.
    with grpc.insecure_channel("{}:{}".format(args.host, args.port)) as channel:
        stub = aihub_pb2_grpc.AIHubStub(channel)
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()


        # stub.AddNewTask(aihub_pb2.Task(question="This is the question about the teserac utility. How to use it?"))


if __name__ == "__main__":
    logging.basicConfig()
    main()
