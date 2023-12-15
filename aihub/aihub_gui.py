import tkinter as tk
from tkinter import scrolledtext
import subprocess

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("aiHub manager")

        # Text area to display stdout
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10, expand=True, fill="both")

        # Button to start the background app
        self.start_button = tk.Button(root, text="Start aiHub lurking...", command=self.start_background_app)
        self.start_button.pack(pady=10)

        # Button to stop the background app
        self.stop_button = tk.Button(root, text="Stop aiHub", command=self.stop_background_app,
                                     state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        # Store the process and file descriptor
        self.process = None
        self.fd = None

    def start_background_app(self):
        # Disable the button while the app is running
        self.start_button.config(state=tk.DISABLED)
        # Enable the stop button
        self.stop_button.config(state=tk.NORMAL)

        # Start the background app
        self.process = subprocess.Popen(
            ["python", "-u", "aihub.py", "-gui"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        # Get the file descriptor for stdout
        self.fd = self.process.stdout.fileno()

        # Set up a fileevent to monitor the stdout for new data
        self.root.createfilehandler(self.fd, tk.READABLE, self.read_stdout)

    def stop_background_app(self):
        # Terminate the background app
        if self.process:
            self.process.terminate()

        # Enable the start button
        self.start_button.config(state=tk.NORMAL)

        # Disable the stop button
        self.stop_button.config(state=tk.DISABLED)

    def read_stdout(self, *args):
        # Read and display the stdout in real-time
        line = self.process.stdout.readline()
        if line:
            self.update_text_area(line)
        else:
            # The process has finished, enable the button
            self.start_button.config(state=tk.NORMAL)
            # Disable the stop button
            self.stop_button.config(state=tk.DISABLED)

    def update_text_area(self, text):
        # Update the text area in a thread-safe manner
        self.text_area.insert(tk.END, text)
        self.text_area.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
