import time
from pynput import keyboard, mouse
import pyautogui
import cv2
import numpy as np
from pathlib import Path
import os
import re
import keyboard as kb

# Future work: 
#   Grabar cuando se clicks se sostienen y los botones. 
#   Grabar solo cuando hay eventos como la camara Imou
#   Make easy installation for windows users and avoid adsminitrator permissions. 
#   Include hotkeys  https://pynput.readthedocs.io/en/latest/keyboard.html
#   Include PC sound, microphone, webcam
#   Make the same for smartphones
# Resolver el problma de memoria de la base de datos 


# Problema de nivel 1. Elegir solo los datos necesarios con que entrenar un modelo que resuelta la tarea Z. En lugar de colectarlos todos. 
#  1) Solo grabar screenshot T tiempos antes y despues de que ocurra un evento en el mause y el teclado
#  2) Problema de nivel 2: Grabar los screenshots, asumiendo que grabo todo 
#       1) en iamgenes con sicronia es infeiciente en memoria 29gb en 1hora, 
#       2) en video 1.9gb en 1hora, pero pierdo sincronia, a menos que estampe el tiempo en el frame 

#filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg" Hace muy lenta los FPS para el screensaving

class Monitorpc:
    def __init__(self):
        self.fps = 30 # frames per second for screenshots
        self.mouse_moves = []
        self.mouse_clicks = [] 
        self.mouse_scrolls = []
        self.keys_pressed = []
        self.screenshots = [] 
        self.base_folder = 'data/'
        self.sample_folder = self.create_incremented_folder(self.base_folder) + '/'     
        
    # Monitoring (No used)
    def start_wvideo(self):
        height, width, layers = self.capture_screen().shape
        video = cv2.VideoWriter(self.sample_folder + 'screencast.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 1/0.0525, (width, height))
        print("Monitoring is working ...")
        self.running = True
        self.start_time = time.perf_counter()
        with mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as listener_mouse, \
            keyboard.Listener(on_press=self.on_press) as listener_keyboard:
            while self.running:
                video.write(self.capture_screen())
                time.sleep(1.0/self.fps)
        cv2.destroyAllWindows()
        video.release()
        self.savevents()
        print("Monitoring was ended ...")

    # Monitoring
    def start(self):
        print("Waiting for activation with ESC key ...")
        kb.wait('esc')

        print("Monitoring is working ...")
        self.running = True
        self.start_time = time.perf_counter()
        with mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as listener_mouse, \
            keyboard.Listener(on_press=self.on_press) as listener_keyboard:
            t, k = 0, 0
            while self.running:
                t = time.perf_counter() - self.start_time
                screenshot = pyautogui.screenshot(self.sample_folder + '{:010}_{}.jpg'.format(k,t))
                k += 1
                time.sleep(1.0/self.fps)

        self.savevents()
        print("Monitoring was ended ...")

            
    # Stores mouse events
    def on_move(self, x, y):
        self.mouse_moves.append((time.perf_counter() - self.start_time, x, y)) 
    def on_click(self, x, y, button, pressed):
        if pressed:
            self.mouse_clicks.append((time.perf_counter() - self.start_time, x, y, button))
    def on_scroll(self, x, y, dx, dy):
        self.mouse_scrolls.append((time.perf_counter() - self.start_time, x, y, dx, dy))
    
    # Stores keyboard events 
    def on_press(self, key):
        self.keys_pressed.append((time.perf_counter() - self.start_time, str(key).strip("'")))
        if key == keyboard.Key.esc: 
            self.running = False
            
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
                    
        writevents(self.sample_folder + "mouse_clicks.txt", self.mouse_clicks)
        writevents(self.sample_folder + "mouse_moves.txt", self.mouse_moves)
        writevents(self.sample_folder + "mouse_scrolls.txt", self.mouse_scrolls)
        writevents(self.sample_folder + "keys_pressed.txt", self.keys_pressed)
        
    def create_incremented_folder(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        # Find the highest number
        dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        highest_num = 0
        for dir_name in dirs:
            match = re.match(r"sample(\d+)", dir_name)
            if match:
                highest_num = max(highest_num, int(match.group(1)))
        # Create new folder
        new_folder_name = f"sample{highest_num + 1}"
        new_folder_path = os.path.join(path, new_folder_name)
        os.makedirs(new_folder_path)
        return new_folder_path