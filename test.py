
import pydirectinput
import pyautogui


def clickmouse(x, y, button, pressed):
    try:
        pydirectinput.moveRel(0, 10)
    except:
        print(f'未知鼠标操作')


while True:
    pydirectinput.moveRel(0, 10)
    pydirectinput.doubleClick()
