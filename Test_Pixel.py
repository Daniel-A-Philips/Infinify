import pyautogui as gui
import time
from PIL import ImageGrab as grabber

image = grabber.grab()
while True:
    time.sleep(0.1)
    positions = (gui.position()[0],gui.position()[1])
    print(type(positions))

    print(image.getpixel(positions))