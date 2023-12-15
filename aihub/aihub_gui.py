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
        root.resizable(True, True)

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
                self.update_text_area(line)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
