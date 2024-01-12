# MonitorPC
 This python module stores events from mouse and keyboard, and saves screenshots.

 Note: It was tested only on Ubuntu. 

### Install virtual environment 
conda create --name automat python==3.10
conda activate automat
pip install pyautogui pynput jupyterlab opencv-python keyboard

### Usage
1. Clone this repository
2. Activate the environment: conda activate automat
3. Check the python path by: which python
4. In your terminal: sudo [your python path here] monitor.py 
5. Press the ESC key to start recording. And don't forget to press again the ESC key to terminate the recording. 