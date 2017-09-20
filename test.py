import pyautogui as pag

x, y = pag.locateCenterOnScreen("osrs_x_bow_spell.PNG")
pag.moveTo(x, y)
print(pag.position())
