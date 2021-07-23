

from pynput import mouse


import win32con

import win32api

import time
import pyautogui
import pydirectinput
from os import _exit
from signal import signal, SIGINT

from utils import WeaponSwitchHandler

import utils.cv_screenshot as cv_screenshot
# import _thread
# import threading

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1

screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()

pyautogui.MINIMUM_SLEEP = 0.1
pydirectinput.MINIMUM_SLEEP = 0.1


CONST_DELTA_VAL = 1


class RecoilController:
    is_ads: bool
    is_activated: bool = True

    # negative👈 👉positive
    offset_horizontal = -2
    # negative👆 👇positive
    offset_vertical = 15

    current_mouse = set()

    def load_weapon_config(self, weapon_config):
        print("loading weapon config")
        # 装载参数
        self.offset_horizontal = weapon_config['offset_horizontal']
        self.offset_vertical = weapon_config['offset_vertical']

    def __init__(self):
        self.is_ads = False

    def clickmouse(self, x, y, button, pressed):
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        try:
            self.is_ads = self.on_click_ads(x, y, button, pressed)

        except:
            print(f'{now}未知鼠标操作')

    def change_compensation_raw(self):
        ctrl = win32api.GetKeyState(0x11)

        up = win32api.GetKeyState(win32con.VK_UP)
        down = win32api.GetKeyState(win32con.VK_DOWN)

        left = win32api.GetKeyState(win32con.VK_LEFT)
        right = win32api.GetKeyState(win32con.VK_RIGHT)

        key_c = win32api.GetKeyState(0x43)

        key_backspace = win32api.GetKeyState(win32con.VK_BACK)

        # print('scroll')
        # print(scroll)

        # Combination Key: ctrl + ↑ / ↓
        if key_backspace < 0:
            self.is_activated = not self.is_activated
            print(self.is_activated and "activated" or "deactivated")
            time.sleep(0.5)

        if ctrl < 0:
            # 按下Ctrl之后
            if up < 0:
                print('up')
                self.offset_vertical += CONST_DELTA_VAL
                print(f"suppression Pixel Per Loop{self.offset_vertical}")

            elif down < 0:
                print('down')
                # 判断Limit
                if(self.offset_vertical > CONST_DELTA_VAL):
                    self.offset_vertical -= CONST_DELTA_VAL
                    print(f"suppression Pixel Per Loop{self.offset_vertical}")
            elif left < 0:
                print("left")
                # 判断Limit
                if(self.offset_horizontal > CONST_DELTA_VAL):
                    self.offset_horizontal -= CONST_DELTA_VAL

            elif right < 0:
                print("right")
                # 判断Limit
                if(self.offset_horizontal > CONST_DELTA_VAL):
                    self.offset_horizontal += CONST_DELTA_VAL

            elif key_c < 0:
                _exit(SIGINT)

            time.sleep(0.06)

    def change_compensation(self, x, y, dx, dy):
        if dy > 0:
            print('上滑')
            self.offset_vertical += 5.43561
        elif dy < 0:
            if(self.offset_vertical > 0):
                self.offset_vertical -= 5.43561
            print('下滑')

    def check_ads_raw(self):
        l = win32api.GetKeyState(0x01)
        r = win32api.GetKeyState(0x02)

        if l < 0 and r < 0:
            # print('Both Button Pressed')
            return True
        else:
            return False
        time.sleep(0.001)

    def recoil_control(self, x, y, button, pressed):
        print("in recoil control")
        if self.is_ads:
            if button == mouse.Button.left and pressed:
                print("压枪")
                # pyautogui.moveRel(0, 10)
                pydirectinput.moveRel(0, 10)


def handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. _exiting gracefully')
    _exit(0)


if __name__ == '__main__':

    weapon = 'ak47'

    recoil_controller = RecoilController()

    # weapon_switch_handler = WeaponSwitchHandler()

    print('Running. Press CTRL-C to _exit.')

    while True:
        # Ctrl+C = Exit Program (组合键退出)
        signal(SIGINT, handler)

        weapon = cv_screenshot.capture_screen()
        (weapon != None) and print(weapon)

        # Scroll to change supression
        recoil_controller.change_compensation_raw()

        # weapon_switch_handler.c

        if(recoil_controller.check_ads_raw()):

            if recoil_controller.is_activated:
                pydirectinput.moveRel(
                    xOffset=recoil_controller.offset_horizontal,
                    yOffset=recoil_controller.offset_vertical,
                    relative=True,
                    _pause=True,
                    duration=1
                )
