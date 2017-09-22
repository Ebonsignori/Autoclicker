import pyautogui as pag
from tkinter import filedialog
import random
import time


class ImageNotFoundEx(Exception):
    """ Custom Exception for returning screenshot that can't be found """
    def __init__(self, screenShotArguments):
        Exception.__init__(self, screenShotArguments)
        self.screenShotArguments = screenShotArguments


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
        raise ImageNotFoundEx(img1)
    pag.moveTo(x, y, vartime_move)
    pag.PAUSE = vartime_move_and_click
    pag.click()
    try:
        x, y = pag.locateCenterOnScreen(img1, minSearchTime=4,
                                        region=(region2[0], region2[1],
                                                region2[2], region2[3]))
    except TypeError:
        raise ImageNotFoundEx(img2)
    pag.moveTo(x, y, vartime_move)
    pag.PAUSE = vartime_move_and_click
    pag.click()
    time_taken = time.time() - time_taken
    print("Click cycle completed. Time taken = ", time_taken)