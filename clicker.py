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
        self.title("Clart's Clicker 2.1")
        self.geometry("293x180")
        self.resizable(False, False)

        # Frames defined
        self.frame1 = ctk.CTkFrame(self)
        self.frame1.grid(column=0, row=0, padx=10, pady=10)
        self.frame2 = ctk.CTkFrame(self)
        self.frame2.grid(column=1, row=0, padx=10)

        # Frame1 items
        self.start_button = ctk.CTkButton(self.frame1, 100, 25, text="Start", command=self.start_clicking)
        self.start_button.grid(column=0, row=0, padx=10, pady=10)
        self.stop_button = ctk.CTkButton(self.frame1, 100, 25, state="disabled", text="Stop", command=self.stop_clicking)
        self.stop_button.grid(column=0, row=1, padx=10, pady=10)
        self.option_dropdown = ctk.CTkOptionMenu(self.frame1, 100, 25, values=["Left Click", "Right Click"])
        self.option_dropdown.grid(column=0, row=2, padx=10, pady=10)

        # Frame2 items
        self.delay_entry = ctk.CTkEntry(self.frame2, 100, 25, placeholder_text="100")
        self.delay_entry.grid(column=0, row=0, padx=10, pady=10)
        self.delay_info = ctk.CTkLabel(self.frame2, 100, 25, text="delay in ms")
        self.delay_info.grid(column=0, row=1, padx=10, pady=10)
        self.set_delay_button = ctk.CTkButton(self.frame2, 100, 25, text="Set Delay", command=self.set_delay)
        self.set_delay_button.grid(column=0, row=2, padx=10, pady=10)

        # Info blocks
        self.i1 = ctk.CTkLabel(self, text="The built in keybind is `")
        self.i1.grid(column=0, row=2, padx=10)
        self.i2 = ctk.CTkLabel(self, text="clart's clicker v2.1")
        self.i2.grid(column=1, row=2)

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