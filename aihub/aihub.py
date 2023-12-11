from PIL import Image, ImageGrab
import pytesseract
import pyautogui
import requests
from pynput.mouse import Listener
from pynput import keyboard


version = 'beta'
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


def capture_screen():
    # Create an instance of ClickListener
    click_listener = ClickListener()

    # Get the mouse coordinates after the first click
    x1, y1 = click_listener.get_coordinates()
    x2, y2 = click_listener.get_coordinates()

    # Print the coordinates
    # print("First click coordinates:", x1, y1)
    print(f'Rectangle: x1: {x1} y1: {y1} x2: {x2} y2: {y2}')
    try:
        image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    except:
        return None
    return image

def send_request(user_input):
    url = f"http://localhost:1234/v1/chat/completions"
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


def help_me():
    image = capture_screen()
    if image != None:
        text = pytesseract.image_to_string(image)
        # PROMPT_DEFAULT = "Summarize this: \n"
        PROMPT_DEFAULT = "Help me with this: \n"
        prompt = PROMPT_DEFAULT + text
        print(f'\n{bcolors.WARNING}USER:{bcolors.ENDC}')
        print(f'{bcolors.WARNING}{prompt}{bcolors.ENDC}')
        return send_request(prompt)
    pass


def main():
    print(f'{bcolors.HEADER}I am © aiHub | version: {version} | © devquasar.com{bcolors.ENDC}')

    def on_press(key):
        if any([key in COMBO for COMBO in COMBINATIONS]):
            current.add(key)
            print(current)
            # if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            if any(x in current for x in {keyboard.KeyCode(char='A')}):
                print('Make a screenshot: define the screen area by click 2 corners of a triange')

                bot_response = help_me()
                print(f'\n{bcolors.OKGREEN}BOT:{bcolors.ENDC}')
                print(f'{bcolors.OKGREEN}{bot_response}{bcolors.ENDC}')
            # if key == keyboard.Key.shift and any(x in current for x in {keyboard.KeyCode(char='X')}):
            if any(x in current for x in {keyboard.KeyCode(char='X')}):
                print('Shift + X pressed. Stopping the listener.')
                listener.stop()

    def on_release(key):
        try:
            if any([key in COMBO for COMBO in COMBINATIONS]):
                current.remove(key)
        except:
            pass

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()