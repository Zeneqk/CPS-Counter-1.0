
import time
import threading
from collections import deque
from pynput import mouse
import tkinter as tk

left_clicks = deque()
right_clicks = deque()

LOCK = threading.Lock()

def on_click(x, y, button, pressed):
    if not pressed:
        return
    now = time.time()
    with LOCK:
        if button == mouse.Button.left:
            left_clicks.append(now)
        elif button == mouse.Button.right:
            right_clicks.append(now)

def get_cps(clicks_deque):
    now = time.time()
    cutoff = now - 1.0
    while clicks_deque and clicks_deque[0] < cutoff:
        clicks_deque.popleft()
    return len(clicks_deque)

def start_listener():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

def gui_loop():
    root = tk.Tk()
    root.title("CPS")
    root.geometry("200x60")
    root.resizable(False, False)

    root.attributes("-topmost", True)

    label = tk.Label(root, font=("Consolas", 14))
    label.pack(expand=True)

    def update_label():
        with LOCK:
            l_cps = get_cps(left_clicks)
            r_cps = get_cps(right_clicks)
        label.config(text=f"LPM: {l_cps} | PPM: {r_cps}")
        root.after(100, update_label)

    update_label()
    root.mainloop()

if __name__ == "__main__":
    t = threading.Thread(target=start_listener, daemon=True)
    t.start()
    gui_loop()
