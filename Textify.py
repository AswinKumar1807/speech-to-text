import datetime
import os
import sys
import threading
import uuid
import webbrowser
import customtkinter as ctk
from tkinter import messagebox
from cryptography.fernet import Fernet
from PIL import Image, ImageTk
from flask import Flask, render_template, send_from_directory

class LicenseGenerator:
    def __init__(self, security_key: bytes):
        self.cipher_suite = Fernet(security_key)

    def generate_license(self, mac_address: str, expiry_date: datetime.date) -> str:
        license_data = f"{mac_address}|{expiry_date.isoformat()}"
        encrypted_license = self.cipher_suite.encrypt(license_data.encode())
        return encrypted_license.decode()

    def validate_license(self, license_key: str) -> bool:
        try:
            decrypted_data = self.cipher_suite.decrypt(license_key.encode()).decode()
            mac_address, expiry_date = decrypted_data.split("|")
            expiry_date = datetime.date.fromisoformat(expiry_date)

            current_mac = self.get_mac_address()
            if current_mac != mac_address:
                messagebox.showerror("Validation Error", "MAC address mismatch.")
                return False

            if datetime.date.today() > expiry_date:
                messagebox.showerror("Validation Error", "License has expired.")
                return False

            return True
        except Exception as e:
            messagebox.showerror("Validation Failed", f"Error: {e}")
            return False

    @staticmethod
    def get_mac_address() -> str:
        mac = uuid.getnode()
        return ':'.join(("%012X" % mac)[i:i + 2] for i in range(0, 12, 2))

class LicenseDialog(ctk.CTkToplevel):
    def __init__(self, master, mac_address, callback):
        super().__init__(master)
        self.callback = callback
        
        self.title("Enter License Key")
        self.geometry("400x200")
        self.resizable(False, False)

        self.mac_label = ctk.CTkLabel(self, text=f"Your MAC Address: {mac_address}")
        self.mac_label.pack(pady=10)

        self.license_entry = ctk.CTkEntry(self, placeholder_text="Enter your license key")
        self.license_entry.pack(pady=10)

        self.copy_button = ctk.CTkButton(self, text="Copy MAC Address", command=self.copy_mac_id)
        self.copy_button.pack(pady=10)

        self.ok_button = ctk.CTkButton(self, text="OK", command=self.on_ok)
        self.ok_button.pack(pady=10)

    def copy_mac_id(self):
        mac_address = self.mac_label.cget("text").split(": ")[1]
        self.clipboard_clear()
        self.clipboard_append(mac_address)
        messagebox.showinfo("Copied", "MAC Address copied to clipboard!")

    def on_ok(self):
        license_key = self.license_entry.get()
        self.callback(license_key)
        self.destroy()

class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title('Textify')
        # icon_path = 'static\img\icon.ico'
        icon_path = os.path.join(sys._MEIPASS, 'static', 'img', 'icon.ico')
        self.wm_iconbitmap(icon_path)
        
        # Load icon image for the taskbar using Pillow
        icon_image = Image.open(icon_path)
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.iconphoto(True, icon_photo)
        self.geometry("350x100")

        # Flask app initialization
        self.flask_app = Flask(__name__)
        self.setup_routes()

        # Set the Flask server URL
        self.website_url = "http://localhost:8000"

        self.security_key = b'Vv9UHUeTmtcbOc-9gy9Cxy5lY1kE-EkRmMR6m73DtIU='  # Replace with your actual Fernet key
        self.license_gen = LicenseGenerator(self.security_key)

        # Validate the license
        if not self.validate_license():
            self.prompt_for_license_key()
            if not self.validate_license():
                messagebox.showerror("License Error", "Invalid or missing license key. Exiting the application.")
                self.destroy()
                return

        # Start the Flask server
        self.start_flask_server()

        # Add UI elements
        self.open_button = ctk.CTkButton(self, text="Click Here To Open Textify In The Browser", command=self.open_in_browser)
        self.open_button.pack(pady=30)

        # # Add a label displaying the website URL
        # self.url_label = ctk.CTkLabel(self, text=f"Website URL: http://localhost:8000")
        # self.url_label.pack(pady=10)

    def setup_routes(self):
        """Define Flask routes for serving files."""
        @self.flask_app.route('/')
        def index():
            return render_template('index.html')

    def start_flask_server(self):
        """Start the Flask server in a separate thread."""
        def run():
            self.flask_app.run(host='localhost', port=8000, debug=False, use_reloader=False)

        self.flask_thread = threading.Thread(target=run, daemon=True)
        self.flask_thread.start()

    def open_in_browser(self):
        """Open the Flask server URL in the default web browser."""
        webbrowser.open(self.website_url)

    def on_closing(self):
        """Override the default close behavior."""
        self.destroy()

    def get_mac_address(self) -> str:
        return LicenseGenerator.get_mac_address()

    def validate_license(self) -> bool:
        license_key = self.read_license_key_from_file("license.txt")
        if not license_key:
            return False

        return self.license_gen.validate_license(license_key)

    def read_license_key_from_file(self, filename: str) -> str:
        try:
            with open(filename, "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            print(f"License file '{filename}' not found.")
            return ""

    def prompt_for_license_key(self) -> str:
        mac_address = self.get_mac_address()
        dialog = LicenseDialog(self, mac_address, self.on_license_key_entered)
        self.wait_window(dialog)
        return getattr(dialog, 'license_key', "")

    def on_license_key_entered(self, license_key: str):
        with open("license.txt", "w") as file:
            file.write(license_key)


if __name__ == "__main__":
    app = App()
    app.eval("tk::PlaceWindow . center")
    app.mainloop()
