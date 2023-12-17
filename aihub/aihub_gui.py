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
        self.text_area.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        self.start_stop_button = tk.Button(root, text="Start aiHub lurking...", command=self.toggle_background_app)
        self.start_stop_button.grid(row=1, column=0, pady=10)

        # Button to clear the text area
        self.clear_button = tk.Button(root, text="Clear Text", command=self.clear_text_area)
        self.clear_button.grid(row=1, column=1, pady=10)

        # Canvas for the status "light"
        self.status_light_canvas = tk.Canvas(root, width=15, height=15, highlightthickness=0)
        self.status_light_canvas.grid(row=1, column=2, pady=10, padx=10)

        # Initialize the circle on the canvas
        self.status_light_circle = self.status_light_canvas.create_oval(1, 1, 15, 15, fill="red", outline="")

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

        # Flag to track whether the background app is currently running
        self.background_app_running = False


    def toggle_background_app(self):
        if hasattr(self, 'process') and self.process.poll() is None:
            # Background app is running, stop it
            self.stop_background_app()
        else:
            # Background app is not running, start it
            self.start_background_app()


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
            # 'shortcut': self.configuration_settings['shortcut'].get(),
            'prompt_prefix': self.configuration_settings['prompt_prefix'].get()
        }

        with open('config.json', 'w') as file:
            json.dump(config_data, file, indent=4)


    def save_configuration(self, api, prompt_prefix, config_window):
        # Store the configuration settings in variables
        self.configuration_settings['api'].set(api)
        # self.configuration_settings['shortcut'].set(shortcut)
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

        # shortcut_label = tk.Label(config_window, text="Shortcut:")
        # shortcut_entry = tk.Entry(config_window, textvariable=self.configuration_settings['shortcut'])

        prompt_label = tk.Label(config_window, text="Prompt prefix:")
        prompt_entry = tk.Entry(config_window, textvariable=self.configuration_settings['prompt_prefix'])

        # Grid layout for labels and entry widgets
        api_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        api_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # shortcut_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        # shortcut_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        prompt_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        prompt_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Button to save configuration settings and close the window
        # save_button = tk.Button(config_window, text="Save",
        #                         command=lambda: self.save_configuration(api_entry.get(), shortcut_entry.get(),
        #                                                                 prompt_entry.get(), config_window))
        save_button = tk.Button(config_window, text="Save",
                                command=lambda: self.save_configuration(api_entry.get(),
                                                                        prompt_entry.get(), config_window))
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

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


    def stop_background_app(self):
        # Terminate the background app
        if hasattr(self, 'process') and self.process.poll() is None:
            self.process.terminate()

        # Enable the start/stop button
        self.start_stop_button.config(text="Start aiHub lurking...", command=self.start_background_app)
        # Update the flag
        self.background_app_running = False

        # Update the status "light" color
        self.status_light_canvas.itemconfig(self.status_light_circle, fill="red", outline="")

    def start_background_app(self):
        if not self.background_app_running:

            # Start the background app in a separate thread
            self.thread = threading.Thread(target=self.run_background_app)
            self.thread.start()

            # Update the command attribute for the button
            self.start_stop_button.config(text="Stop aiHub", command=self.stop_background_app)

            # Update the flag
            self.background_app_running = True

            # Update the status "light" color
            self.status_light_canvas.itemconfig(self.status_light_circle, fill="green", outline="")

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
                        self.status_light_canvas.itemconfig(self.status_light_circle, fill="orange", outline="")
                    else:
                        self.status_light_canvas.itemconfig(self.status_light_circle, fill="green", outline="")

            # Wait for the process to complete and get the return code
            return_code = self.process.wait()

            # # Enable the start button after the app is done
            # self.start_button.config(state=tk.NORMAL)
            #
            # # Disable the stop button
            # self.stop_button.config(state=tk.DISABLED)

            # Optionally, you can print the return code
            print("Background App exited with return code:", return_code)

        except Exception as e:
            print("Error:", e)


    def clear_text_area(self):
        # Keep the first two lines and clear the rest
        text_content = self.text_area.get("1.0", "2.0")
        self.text_area.delete("3.0", tk.END)
        self.text_area.insert(tk.END, text_content)


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
