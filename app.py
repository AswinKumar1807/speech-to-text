import datetime
import os
import threading
import uuid
import customtkinter as ctk
from tkinter import messagebox
from cryptography.fernet import Fernet
from PIL import Image, ImageTk
from http.server import SimpleHTTPRequestHandler, HTTPServer
import webbrowser
import subprocess
import signal

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
        icon_path = "textify/img/icon.ico"
        self.wm_iconbitmap(icon_path)
        
        # Load icon image for the taskbar using Pillow
        icon_image = Image.open(icon_path)
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.iconphoto(True, icon_photo)
        self.geometry("350x100")

        # Set the website URL for the server
        self.website_url = "http://localhost:8000/index.html"

        self.security_key = b'Vv9UHUeTmtcbOc-9gy9Cxy5lY1kE-EkRmMR6m73DtIU='  # Replace with your actual Fernet key
        self.license_gen = LicenseGenerator(self.security_key)

        if not self.validate_license():
            self.prompt_for_license_key()
            if not self.validate_license():
                messagebox.showerror("License Error", "Invalid or missing license key. Exiting the application.")
                self.destroy()
                return

        # Initialize the application
        self.start_server()

    def start_server(self):
        """Start a temporary HTTP server to serve the HTML page."""
        def serve():
            os.chdir(os.path.abspath("."))  # Set working directory
            self.httpd = HTTPServer(("localhost", 8000), SimpleHTTPRequestHandler)
            self.httpd.serve_forever()

        self.server_thread = threading.Thread(target=serve, daemon=True)
        self.server_thread.start()

        # Open the website URL in the browser using subprocess
        # self.browser_process = subprocess.Popen(["python", "-m", "webbrowser", self.website_url])

        # Add a button to open the URL if it's not already opened
        self.open_button = ctk.CTkButton(self, text="Open Textify in Browser", command=self.open_in_browser)
        self.open_button.pack(pady=10)

        # Add a label displaying the website URL
        self.url_label = ctk.CTkLabel(self, text=f"Website URL: {self.website_url}")
        self.url_label.pack(pady=10)

    def open_in_browser(self):
        """Open the website URL in the default web browser."""
        webbrowser.open(self.website_url)

    def stop_server(self):
        """Stop the temporary HTTP server."""
        if self.httpd:
            self.httpd.shutdown()
            self.server_thread.join()

    def stop_browser(self):
        """Close the browser process."""
        if self.browser_process:
            os.kill(self.browser_process.pid, signal.SIGTERM)

    def on_closing(self):
        """Override the default close behavior to stop the server and browser."""
        self.stop_server()
        self.stop_browser()
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
