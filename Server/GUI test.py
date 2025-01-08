import tkinter
import tkinter.messagebox
import customtkinter
import subprocess

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.line_tracking_process = None  # Houd het line-tracking proces bij

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Button to start Line Tracking
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Line Tracking", command=self.run_script)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        # Button to stop Line Tracking
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Stop Line Tracking", command=self.stop_script)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        # Button to capture an image
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Capture Image", command=self.capture_image)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        # Textbox for logging
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # Other widgets and settings (omitted for brevity, but include all widgets from your original code)

    def run_script(self):
        """Start het line-tracking script."""
        if self.line_tracking_process and self.line_tracking_process.poll() is None:
            self.log_to_textbox("Line Tracking is al actief.")
            return
        try:
            self.line_tracking_process = subprocess.Popen(
                ["sudo", "python3", "/home/pi/Server/Line_Tracking.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.log_to_textbox("Line Tracking gestart.")
        except Exception as e:
            error_message = f"Fout bij het starten van line tracking: {e}"
            self.log_to_textbox(error_message)
            tkinter.messagebox.showerror("Error", error_message)

    def stop_script(self):
        """Stop het line-tracking script."""
        if self.line_tracking_process and self.line_tracking_process.poll() is None:
            self.line_tracking_process.terminate()
            self.line_tracking_process.wait()  # Zorg ervoor dat het proces volledig wordt gestopt
            self.line_tracking_process = None
            self.log_to_textbox("Line Tracking gestopt.")
        else:
            self.log_to_textbox("Line Tracking is niet actief.")

    def capture_image(self):
        """Maak een foto."""
        try:
            command = ["libcamerastill", "-o", "image.jpg"]
            subprocess.run(command, check=True, text=True, capture_output=True)
            self.log_to_textbox("Afbeelding succesvol vastgelegd.")
        except subprocess.CalledProcessError as e:
            error_message = f"Fout bij het vastleggen van de afbeelding: {e.stderr}"
            self.log_to_textbox(error_message)
            tkinter.messagebox.showerror("Error", error_message)
        except Exception as e:
            error_message = f"Unexpected error: {e}"
            self.log_to_textbox(error_message)
            tkinter.messagebox.showerror("Unexpected Error", error_message)

    def log_to_textbox(self, message):
        """Log een bericht in de textbox."""
        self.textbox.insert("end", message + "\n")
        self.textbox.see("end")  # Scroll naar het einde van de textbox

    def sidebar_button_event(self):
        """Placeholder voor een andere functionaliteit."""
        self.log_to_textbox("Sidebar button event aangeroepen.")

    def open_input_dialog_event(self):
        """Open een invoerdialoog."""
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        self.log_to_textbox(f"Invoer ontvangen: {dialog.get_input()}")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

        # ... (bestaande code blijft ongewijzigd)

        # Button to start Ultrasonic
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Ultrasonic", command=self.start_ultrasonic)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)

        self.ultrasonic_process = None  # Procesbeheer voor de ultrasone functionaliteit

    def start_ultrasonic(self):
        """Start de ultrasone functionaliteit."""
        if self.ultrasonic_process and self.ultrasonic_process.is_alive():
            self.log_to_textbox("Ultrasonic is al actief.")
            return
        try:
            self.ultrasonic_process = multiprocessing.Process(target=self.run_ultrasonic)
            self.ultrasonic_process.start()
            self.log_to_textbox("Ultrasonic gestart.")
        except Exception as e:
            error_message = f"Fout bij het starten van ultrasonic: {e}"
            self.log_to_textbox(error_message)
            tkinter.messagebox.showerror("Error", error_message)

    def stop_ultrasonic(self):
        """Stop de ultrasone functionaliteit."""
        if self.ultrasonic_process and self.ultrasonic_process.is_alive():
            self.ultrasonic_process.terminate()
            self.ultrasonic_process.join()
            self.ultrasonic_process = None
            self.log_to_textbox("Ultrasonic gestopt.")
        else:
            self.log_to_textbox("Ultrasonic is niet actief.")

    @staticmethod
    def run_ultrasonic():
        """Roep de `run`-functie van de Ultrasone klasse aan."""
        ultrasonic = Ultrasonic()
        ultrasonic.run()
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
