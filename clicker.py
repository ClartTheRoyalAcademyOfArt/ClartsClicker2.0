import ctypes
import threading
import time
from pynput.keyboard import Listener
from tkinter import *
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Variable setup
        self.is_clicking = False
        self.click_thread = None
        self.click_delay = 0.1
        self.selected_key = '`'
        self.min_click_delay = 0.001

        # Window setup
        self.title("Clart's Clicker 2")
        self.iconbitmap("ClartsClicker2/icon.ico")
        self.geometry("300x225")
        self.resizable(False, False)

        # Frames defined
        self.frameB1 = ctk.CTkFrame(self, 300, 100)
        self.frameB1.pack(pady=10)
        self.frameB2 = ctk.CTkFrame(self, 200, 25)
        self.frameB2.pack(pady=0)

        self.frame1 = ctk.CTkFrame(self.frameB1, 150, 100)
        self.frame1.grid(column=0, row=0, padx=10, pady=10)
        self.frame2 = ctk.CTkFrame(self.frameB1, 150, 100)
        self.frame2.grid(column=1, row=0, padx=10, pady=10)

        # Frame1 items
        self.start_button = ctk.CTkButton(self.frame1, 100, 25, text="Start", font=("Helvetica", 12, "bold"), command=self.start_clicking)
        self.start_button.pack(padx=10, pady=10)
        self.stop_button = ctk.CTkButton(self.frame1, 100, 25, state="disabled", text="Stop", font=("Helvetica", 12, "bold"), command=self.stop_clicking)
        self.stop_button.pack(padx=10, pady=10)
        self.option_dropdown = ctk.CTkOptionMenu(self.frame1, 100, 25, values=["Left Click", "Right Click"], font=("Helvetica", 12, "bold"),)
        self.option_dropdown.pack(padx=10, pady=10)
        
        # Frame2 items
        self.delay_entry = ctk.CTkEntry(self.frame2, 100, 25, placeholder_text="100", font=("Helvetica", 12, "bold"),)
        self.delay_entry.pack(padx=10, pady=10)
        self.set_delay_button = ctk.CTkButton(self.frame2, 100, 25, text="Set Delay (ms)", font=("Helvetica", 12, "bold"), command=self.set_delay)
        self.set_delay_button.pack(padx=10, pady=10)
        self.set_delay_default_button = ctk.CTkButton(self.frame2, 100, 25, text="Set Default", font=("Helvetica", 12, "bold"), command=self.set_delay_default)
        self.set_delay_default_button.pack(padx=10, pady=10)

        # Frame3 items
        self.iL1 = ctk.CTkLabel(self.frameB2, text="Click ( ` ) to toggle clicking\nClart's Clicker v2.1.1", font=("Helvetica", 12, "bold"))
        self.iL1.pack(padx=65, pady=5)
        
        # Key listener setup
        self.listener_thread = threading.Thread(target=self.start_listener, daemon=True)
        self.listener_thread.start()

    def start_listener(self):
        with Listener(on_press=self.on_press) as listener:
            listener.join()

    def start_clicking(self):
        if not self.is_clicking:
            self.is_clicking = True
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.click_thread = threading.Thread(target=self.click_loop)
            print("START")
            self.click_thread.start()

    def stop_clicking(self):
        if self.is_clicking:
            self.is_clicking = False
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            print("STOP")
            self.click_thread.join()

    def set_delay(self):
        try:
            delay = int(self.delay_entry.get())

            self.click_delay = max(delay / 1000, self.min_click_delay)
        except ValueError:
            pass
    
    def set_delay_default(self):
        self.click_delay = 0.1
        self.delay_entry.delete(0, 'end')
        self.delay_entry.configure(placeholder_text="100")

    def on_press(self, key):
        if hasattr(key, 'char') and key.char == self.selected_key:
            if self.is_clicking:
                self.stop_clicking()
            else:
                self.start_clicking()

    def click_loop(self):
        while self.is_clicking:
            if self.option_dropdown.get() == "Left Click":
                ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)  # left down
                ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)  # left up
            elif self.option_dropdown.get() == "Right Click":
                ctypes.windll.user32.mouse_event(0x0008, 0, 0, 0, 0)  # right down
                ctypes.windll.user32.mouse_event(0x0010, 0, 0, 0, 0)  # right up
            time.sleep(self.click_delay)



if __name__ == "__main__":
    app = App()
    app.mainloop()
