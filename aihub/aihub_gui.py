import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import json

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

        # Create the menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Create the menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Create the File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Add the "Configuration" menu item
        file_menu.add_command(label="Configuration", command=self.open_configuration_window)

        # Add a separator
        file_menu.add_separator()

        # Add the "About" menu item
        file_menu.add_command(label="About", command=self.show_about)

        # ... (unchanged code)

        # Variable to store configuration settings
        self.configuration_settings = {
            'api': tk.StringVar(),
            'shortcut': tk.StringVar(),
            'prompt_prefix': tk.StringVar()
        }

        # Load configuration from file
        self.load_configuration_from_file()

        # Allow resizing of the window
        root.geometry("400x300")
        self.default_color = "lightgray"
        self.load_color = '#856ff8'
        root.resizable(True, True)
        self.stop_spinner_flag = False
        # self.spinner_line_number = None

    def load_configuration_from_file(self):
        try:
            with open('config.json', 'r') as file:
                config_data = json.load(file)

                # Update StringVar values
                for key, value in config_data.items():
                    self.configuration_settings[key].set(value)
        except FileNotFoundError:
            print("Config file not found. Using default values.")

    def save_configuration_to_file(self):
        config_data = {
            'api': self.configuration_settings['api'].get(),
            'shortcut': self.configuration_settings['shortcut'].get(),
            'prompt_prefix': self.configuration_settings['prompt_prefix'].get()
        }

        with open('config.json', 'w') as file:
            json.dump(config_data, file, indent=4)


    def save_configuration(self, api, shortcut, prompt_prefix, config_window):
        # Store the configuration settings in variables
        self.configuration_settings['api'].set(api)
        self.configuration_settings['shortcut'].set(shortcut)
        self.configuration_settings['prompt_prefix'].set(prompt_prefix)

        # Save configuration to file
        self.save_configuration_to_file()

        # Close the configuration window
        config_window.destroy()


    def open_configuration_window(self):
        # Create a new Toplevel window for configuration settings
        config_window = tk.Toplevel(self.root)
        config_window.title("Configuration Settings")

        # Labels and entry widgets for configuration settings
        api_label = tk.Label(config_window, text="API:")
        api_entry = tk.Entry(config_window, textvariable=self.configuration_settings['api'])

        shortcut_label = tk.Label(config_window, text="Shortcut:")
        shortcut_entry = tk.Entry(config_window, textvariable=self.configuration_settings['shortcut'])

        prompt_label = tk.Label(config_window, text="Prompt prefix:")
        prompt_entry = tk.Entry(config_window, textvariable=self.configuration_settings['prompt_prefix'])

        # Grid layout for labels and entry widgets
        api_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        api_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        shortcut_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        shortcut_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        prompt_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        prompt_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Button to save configuration settings and close the window
        save_button = tk.Button(config_window, text="Save",
                                command=lambda: self.save_configuration(api_entry.get(), shortcut_entry.get(),
                                                                        prompt_entry.get(), config_window))
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About")

        # Read content from the readme.md file
        try:
            with open('readme.md', 'r', encoding='utf-8') as file:
                readme_content = file.read()

            # Create a scrolled text widget to display the content
            readme_text = scrolledtext.ScrolledText(about_window, wrap=tk.WORD, width=60, height=20)
            readme_text.insert(tk.END, readme_content)
            readme_text.config(state=tk.DISABLED)
            readme_text.pack(expand=True, fill='both')
        except FileNotFoundError:
            readme_text = tk.Label(about_window, text="readme.md not found.")
            readme_text.pack()

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
            self.process = subprocess.Popen(["python", "-u", "aihub.py", "-gui",
                                             '-api', self.configuration_settings['api'].get(),
                                             '-pp', self.configuration_settings['prompt_prefix'].get()],
                                            stdout=subprocess.PIPE, text=True, bufsize=1)

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
