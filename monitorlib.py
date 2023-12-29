import time
from pynput import keyboard, mouse
import pyautogui
import cv2
import numpy as np
from pathlib import Path

# Future work: 
#   Include hotkeys  https://pynput.readthedocs.io/en/latest/keyboard.html
#   Include PC sound, microphone, webcam
#   Make the same for smartphones

# Problema de nivel 1. Elegir solo los datos necesarios con que entrenar un modelo que resuelta la tarea Z. En lugar de colectarlos todos. 
#  1) Solo grabar screenshot T tiempos antes y despues de que ocurra un evento en el mause y el teclado
#  2) Problema de nivel 2: Grabar los screenshots, asumiendo que grabo todo 
#       1) en iamgenes con sicronia es infeiciente en memoria 29gb en 1hora, 
#       2) en video 1.9gb en 1hora, pero pierdo sincronia, a menos que estampe el tiempo en el frame 

class Monitorpc:
    def __init__(self, Tf):
        self.Tf = Tf  # Total duration in seconds
        self.fps = 30 # frames per second for screenshots
        self.mouse_moves = []
        self.mouse_clicks = [] 
        self.mouse_scrolls = []
        self.keys_pressed = []
        self.screenshots = [] 
        
    # Monitoring
    def start(self):
        height, width, layers = self.capture_screen().shape
        video = cv2.VideoWriter('screencast.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 1/0.0525, (width, height))
        print("Monitoring is working ...")
        self.start_time = time.time()
        with mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as listener_mouse, \
            keyboard.Listener(on_press=self.on_press) as listener_keyboard:
            while time.time() - self.start_time < self.Tf:
                video.write(self.capture_screen())
                time.sleep(1.0/self.fps)
        cv2.destroyAllWindows()
        video.release()
        self.savevents()
        print("Monitoring was ended ...")

    # Monitoring
    def start2(self):
        folder = 'screenshoots/'
        Path(folder).mkdir(exist_ok=True)
        print("Monitoring is working ...")
        self.start_time = time.time()
        with mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as listener_mouse, \
            keyboard.Listener(on_press=self.on_press) as listener_keyboard:
            k, t = 0, 0
            while t < self.Tf:
                t = time.time() - self.start_time
                screenshot = pyautogui.screenshot(folder + 'screen_{:08}_{}.jpg'.format(k, t))
                time.sleep(1.0/self.fps)
                k += 1
        self.savevents()
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
        frame = np.asarray(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
    
    def savevents(self): 
        def writevents(filename, items):
            with open(filename, "w") as file:
                for item in items:
                    file.write(",".join(str(i) for i in item)+"\n")
                    
        writevents("mouse_clicks.txt", self.mouse_clicks)
        writevents("mouse_moves.txt", self.mouse_moves)
        writevents("mouse_scrolls.txt", self.mouse_scrolls)
        writevents("keys_pressed.txt", self.keys_pressed)
        
    