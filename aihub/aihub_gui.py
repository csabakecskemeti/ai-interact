import time
import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("aiHub Manager")

        # Create a grid with a single row and column
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Text area to display stdout
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.text_area.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Button to start the background app
        self.start_button = tk.Button(root, text="Start aiHub lurking...", command=self.start_background_app)
        self.start_button.grid(row=1, column=0, pady=10)

        # Button to stop the background app
        self.stop_button = tk.Button(root, text="Stop aiHub", command=self.stop_background_app, state=tk.DISABLED)
        self.stop_button.grid(row=2, column=0, pady=10)

        # Allow resizing of the window
        root.geometry("400x300")
        self.default_color = "lightgray"
        self.load_color = '#856ff8'
        root.resizable(True, True)
        self.stop_spinner_flag = False
        # self.spinner_line_number = None


    def change_color(color):
        root.configure(bg=color)

    # def run_spinner(self):
    #     symbols = ['-', '\\', '|', '/']
    #     i = 0
    #
    #     while not self.stop_spinner_flag:
    #         spinner_text = '\r' + symbols[i]
    #         if self.spinner_line_number is not None:
    #             # Update the existing line
    #             self.update_spinner_text_area(spinner_text, line_number=self.spinner_line_number)
    #         else:
    #             # Insert a new line
    #             self.update_spinner_text_area(spinner_text)
    #             self.spinner_line_number = self.text_area.index(tk.END).split('.')[0]
    #
    #         time.sleep(0.1)
    #         i = (i + 1) % len(symbols)
    #
    #
    # def start_spinner(self):
    #     # Start the spinner in a separate thread
    #     self.thread = threading.Thread(target=self.run_spinner)
    #     self.thread.start()
    #
    # def stop_spinner(self):
    #     # Set the flag to stop the spinner
    #     self.stop_spinner_flag = True

    def start_background_app(self):
        # Disable the start button while the app is running
        self.start_button.config(state=tk.DISABLED)

        # Enable the stop button
        self.stop_button.config(state=tk.NORMAL)

        # Start the background app in a separate thread
        self.thread = threading.Thread(target=self.run_background_app)
        self.thread.start()

    def run_background_app(self):
        try:
            # Replace 'your_background_app.py' with the actual file name of your background app
            self.process = subprocess.Popen(["python", "-u", "aihub.py", "-gui"], stdout=subprocess.PIPE, text=True, bufsize=1)

            # Read and display the stdout in real-time
            for line in iter(self.process.stdout.readline, ""):
                if len(line) > 0:
                    self.update_text_area(line)
                    if "BOT:" in line:
                        # self.start_spinner()
                        # self.update_text_area(root.cget("bg"))
                        root.configure(bg=self.load_color)
                    else:
                        # self.stop_spinner()
                        root.configure(bg='systemWindowBackgroundColor')

            # Wait for the process to complete and get the return code
            return_code = self.process.wait()

            # Enable the start button after the app is done
            self.start_button.config(state=tk.NORMAL)

            # Disable the stop button
            self.stop_button.config(state=tk.DISABLED)

            # Optionally, you can print the return code
            print("Background App exited with return code:", return_code)

        except Exception as e:
            print("Error:", e)

    def stop_background_app(self):
        # Terminate the background app
        if hasattr(self, 'process') and self.process.poll() is None:
            self.process.terminate()

        # Enable the start button
        self.start_button.config(state=tk.NORMAL)

        # Disable the stop button
        self.stop_button.config(state=tk.DISABLED)

    def update_text_area(self, text):
        # Update the text area in a thread-safe manner
        self.text_area.insert(tk.END, text)
        self.text_area.yview(tk.END)

        # Force the GUI to update in real-time
        self.root.update_idletasks()


    def update_spinner_text_area(self, text, line_number=None):
        # Update the text area in a thread-safe manner
        if line_number is not None:
            self.text_area.delete(f"{line_number}.0", f"{line_number + 1}.0")
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.yview(tk.END)

        # Force the GUI to update in real-time
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
