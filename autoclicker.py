import pyautogui as pag
import winsound as ws
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import sys
import random
import time

root = tk.Tk()
root.withdraw()


class ImageNotFound(Exception):
    def __init__(self, screenShotArguments):
        Exception.__init__(self, screenShotArguments)
        self.screenShotArguments = screenShotArguments


def get_position_of_image(imagefile):
    try:
        x, y = pag.locateOnScreen(imagefile)
    except TypeError:
        print("Image not found on page")
        return -1
    pag.moveTo(x, y)
    return pag.position()


def get_image_dimmensions(image):
    left, top, width, height = pag.locateOnScreen(image)
    width += 2
    height += 2
    return [left, top, width, height]


def move_2(iterations, move_independence):
    print("Select first screenshot")
    img1 = filedialog.askopenfilename()
    print("Select second screenshot")
    img2 = filedialog.askopenfilename()
    region1 = get_image_dimmensions(img1)
    if move_independence is False:
        region2 = [-1, -1, -1, -1]
    else:
        region2 = get_image_dimmensions(img2)
    for i in range(iterations):
        try:
            move_2_mouse(img1, region1, img2, region2)
        except ImageNotFound as inf:
            ws.PlaySound("sounds/bad_beep_2.wav", ws.SND_FILENAME)
            print("Unable to locate image from screenshot, \"{0}\"".format(inf.args[0]))
        except KeyboardInterrupt:  # Cntr + C on the command line
            print("Autoclicking Stopped")
            break


def move_2_mouse(img1, region1, img2, region2):
    time_taken = time.time()  # for calculating time after execution
    vartime_move = random.uniform(.2, 1)  # random num between .2 and 1.2
    vartime_click_and_move = random.uniform(.2, 1)  # further randomizing
    vartime_move_and_click = random.uniform(.2, 1)
    pag.PAUSE = vartime_click_and_move
    try:
        x, y = pag.locateCenterOnScreen(img1, minSearchTime=4,
                                        region=(region1[0], region1[1],
                                                region1[2], region1[3]))
    except TypeError:
        raise ImageNotFound(img1)
    pag.moveTo(x, y, vartime_move)
    pag.PAUSE = vartime_move_and_click
    pag.click()

    # IMPORTANT! Image recongnition needs time to locate pop up screen
    try:
        if (region2[0]) is -1:
            x, y = pag.locateCenterOnScreen(img2, minSearchTime=4)
        else:
            x, y = pag.locateCenterOnScreen(img1, minSearchTime=4,
                                            region=(region2[0], region2[1],
                                                    region2[2], region2[3]))
    except TypeError:
        raise ImageNotFound(img2)
    pag.moveTo(x, y, vartime_move)
    pag.PAUSE = vartime_move_and_click
    pag.click()
    time_taken = time.time() - time_taken
    print("Click cycle completed. Time taken = ", time_taken)


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

try:
    move_number = int(input("How many images are you moving between?"))
    move_independence = input("Are the images independent of another? \n \
                              1 for Yes 0 for No")
    iterations = int(input("Loop for?"))

except Exception:
    print("Invalid Input")
    sys.exit("Input error")

if move_number is 2:
    move_2(iterations, str2bool(move_independence))
else:
    print("Currently only 2 images supported")

ws.PlaySound("sounds/correct_2.wav", ws.SND_FILENAME)
print("Finished")
