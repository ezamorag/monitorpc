import time
from pynput import keyboard, mouse
import pyautogui
import cv2
import numpy as np

# Future work: 
#   Include hotkeys  https://pynput.readthedocs.io/en/latest/keyboard.html
#   Include PC sound

class Monitorpc:
    def __init__(self, Tf):
        self.Tf = Tf  # Total duration in seconds
        self.Tp = 1/30 # Sampling interval in seconds for screenshots
        self.mouse_moves = []
        self.mouse_clicks = [] 
        self.mouse_scrolls = []
        self.keys_pressed = []
        self.screenshots = [] 
        
    # Monitoring
    def start(self):
        print("Monitoring is working ...")
        self.start_time = time.time()
        with mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as listener_mouse, \
            keyboard.Listener(on_press=self.on_press) as listener_keyboard:
            while time.time() - self.start_time < self.Tf:
                self.screenshots.append(self.capture_screen())
                time.sleep(self.Tp)
        self.savedata()
        print("Monitoring was ended ...")
            
    # Stores mouse events
    def on_move(self, x, y):
        self.mouse_moves.append((time.time() - self.start_time, x, y)) 
    def on_click(self, x, y, button, pressed):
        if pressed:
            self.mouse_clicks.append((time.time() - self.start_time, x, y, button))
    def on_scroll(self, x, y, dx, dy):
        self.mouse_scrolls.append((time.time() - self.start_time, x, y, dx, dy))
    
    # Stores keyboard events 
    def on_press(self, key):
        self.keys_pressed.append((time.time() - self.start_time, key))
            
    # Stores screenshots  
    def capture_screen(self):
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
    
    def savedata(self): 
        def writedata(filename, items):
            with open(filename, "w") as file:
                for item in items:
                    file.write(",".join(str(i) for i in item)+"\n")
                    
        writedata("mouse_clicks.txt", self.mouse_clicks)
        writedata("mouse_moves.txt", self.mouse_moves)
        writedata("mouse_scrolls.txt", self.mouse_scrolls)
        writedata("keys_pressed.txt", self.keys_pressed)
        
        height, width, layers = self.screenshots[0].shape
        video = cv2.VideoWriter('screencast.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 1.0/self.Tp, (width, height))
        for img in self.screenshots:
            video.write(img)
        cv2.destroyAllWindows()
        video.release()
    