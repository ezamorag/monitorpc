# MonitorPC
 This python module stores events from mouse and keyboard, and saves screenshots.

 Note: It was tested only on Ubuntu 20.04 and Windows 11. 

### Install virtual environment 
```
conda create --name automat python==3.10
conda activate automat
pip install pyautogui pynput jupyterlab opencv-python keyboard pandas
```

### Usage
1. Clone this repository
2. Activate the environment: conda activate automat
3. In your terminal, check the python path by: ```which python``` (Ubuntu) or ```where python``` (Windows)
4. Ubuntu: ```sudo [your python path here] monitor.py```. Windows: ```python monitor.py```
5. Press the ESC key to start recording. And don't forget to press again the ESC key to terminate the recording. 