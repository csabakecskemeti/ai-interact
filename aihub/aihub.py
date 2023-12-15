from PIL import Image, ImageGrab
import pytesseract
import sys
import requests
from pynput.mouse import Listener
from pynput import keyboard
import argparse
import logging
from logging import handlers
import time
import threading


version = '1.0 beta'
COMBINATIONS = [
    {keyboard.Key.shift, keyboard.KeyCode(char='a')},
    {keyboard.Key.shift, keyboard.KeyCode(char='A')},
    {keyboard.Key.shift, keyboard.KeyCode(char='x')},
    {keyboard.Key.shift, keyboard.KeyCode(char='X')}
]
current = set()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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


def system_printer(text, is_gui=False):
    if is_gui:
        print(f'\n{text}')
    else:
        print(f'\n{bcolors.HEADER}{text}{bcolors.ENDC}')


def user_printer(text, is_gui=False):
    if is_gui:
        print(f'\n{text}')
    else:
        print(f'\n{bcolors.WARNING}{text}{bcolors.ENDC}')


def bot_printer(text, is_gui=False):
    if is_gui:
        print(f'\n{text}')
    else:
        print(f'\n{bcolors.OKGREEN}{text}{bcolors.ENDC}')


def spinner():
    symbols = ['-', '\\', '|', '/']
    i = 0
    while True:
        sys.stdout.write('\r' + symbols[i])
        sys.stdout.flush()
        time.sleep(0.1)
        i = (i + 1) % len(symbols)


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


def send_request(user_input:str, host:str, port:int):
    url = f"{host}:{port}/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": [
            {"role": "user", "content": f"### Instruction: {user_input}\n###Response: "}
        ],
        "stop": ["### Instruction:"],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']


def help_me(host:str, port:int, is_gui=False):
    global spinner_thread
    image = capture_screen()
    if image != None:
        text = pytesseract.image_to_string(image)
        # PROMPT_DEFAULT = "Summarize this: \n"
        PROMPT_DEFAULT = "Help me with this: \n"
        prompt = PROMPT_DEFAULT + text
        user_printer('USER:', is_gui)
        user_printer(prompt, is_gui)
        bot_printer('BOT:', is_gui)
        bot_response = ''
        bot_response = send_request(prompt, host, port)
        # try:
        #     bot_printer('BOT:', is_gui)
        #     spinner_thread = threading.Thread(target=spinner)
        #     spinner_thread.start()
        #
        #     bot_response = send_request(prompt, host, port)
        #
        # finally:
        #     # Stop the spinner when the task is done
        #     spinner_thread.join()

        return bot_response
    pass


def main():
    parser = argparse.ArgumentParser(description='aiHub arg parse')
    parser.add_argument('-api', '--llm_api_host', type=str, help='LLM API host', default='http://localhost')
    parser.add_argument('-p', '--port', type=int, help='LLM API port number', default=1234)
    parser.add_argument('-l', '--log_file', type=str, help='Log file for aiHub', default='aihub.log')
    parser.add_argument('-gui', '--gui_printer', action='store_true', help='Using aiHub with aiHubManager GUI')
    args = parser.parse_args()

    system_printer(f'I am © aiHub | version: {version} | © devquasar.com', args.gui_printer)

    def log_setup():
        log_handler = logging.handlers.WatchedFileHandler(args.log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        formatter.converter = time.gmtime  # if you want UTC time
        log_handler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.addHandler(log_handler)
        logger.setLevel(logging.DEBUG)

    def on_press(key):
        if any([key in COMBO for COMBO in COMBINATIONS]):
            current.add(key)
            logging.info(f'key combo pressed: {current}')
            # if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            if any(x in current for x in {keyboard.KeyCode(char='A')}):
                system_printer(f'Make a screenshot: define the screen area by click 2 corners of a rectangle', args.gui_printer)

                bot_response = help_me(args.llm_api_host, args.port, args.gui_printer)
                bot_printer(bot_response, args.gui_printer)
            # if key == keyboard.Key.shift and any(x in current for x in {keyboard.KeyCode(char='X')}):
            if any(x in current for x in {keyboard.KeyCode(char='X')}):
                logging.info('Shift + X pressed. Stopping the listener.')
                listener.stop()

    def on_release(key):
        try:
            if any([key in COMBO for COMBO in COMBINATIONS]):
                current.remove(key)
        except:
            pass

    log_setup()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()