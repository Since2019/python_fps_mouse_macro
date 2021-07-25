

from pynput import mouse


import win32con

import win32api

import time
import pyautogui
import pydirectinput
from os import _exit
from signal import signal, SIGINT

from utils.WeaponSwitchHandler import WeaponSwitchHandler

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
    is_activated: bool

    # negative👈 👉positive
    offset_horizontal: int
    # negative👆 👇positive
    offset_vertical: int

    def __init__(self):
        self.current_weapon = "R4-C"

    def _load_weapon_config(self, weapon_config):
        __debug__ and print("loading weapon config")
        __debug__ and print(f"weapon_config:\n{weapon_config}")
        try:
            tmp_offset_horizontal = self.offset_horizontal
            tmp_offset_vertical = self.offset_vertical
            # 装载参数
            self.offset_horizontal = int(weapon_config['horizontal'])
            self.offset_vertical = int(weapon_config['vertical'])
        except:
            self.offset_horizontal = tmp_offset_horizontal
            self.offset_vertical = tmp_offset_vertical
            #

    def __init__(self):
        self.is_ads = False
        self.is_activated = True
        self.offset_horizontal = -2
        self.offset_vertical = 15

    def _change_compensation_raw(self):
        ctrl = win32api.GetKeyState(0x11)

        up = win32api.GetKeyState(win32con.VK_UP)
        down = win32api.GetKeyState(win32con.VK_DOWN)

        left = win32api.GetKeyState(win32con.VK_LEFT)
        right = win32api.GetKeyState(win32con.VK_RIGHT)

        key_c = win32api.GetKeyState(0x43)
        key_alt = win32api.GetKeyState(win32con.VK_MENU)  # ALT

        key_backspace = win32api.GetKeyState(win32con.VK_BACK)

        # 用于判断是否有return 数值
        # direction = None
        value = None

        # print('scroll')
        # print(scroll)

        # Combination Key: ctrl + ↑ / ↓
        if key_backspace < 0:
            self.is_activated = not self.is_activated
            print(self.is_activated and "activated" or "deactivated")
            time.sleep(0.5)

        elif ctrl < 0:
            # 按下Ctrl之后
            if up < 0:
                self.offset_vertical += CONST_DELTA_VAL
                __debug__ and (
                    print('up'),
                    print(f"suppression Pixel Per Loop{self.offset_vertical}")
                )

            elif down < 0:
                # 判断Limit
                if(self.offset_vertical > CONST_DELTA_VAL):
                    self.offset_vertical -= CONST_DELTA_VAL

                __debug__ and (
                    print('down'),
                    print(f"suppression Pixel Per Loop{self.offset_vertical}")
                )

            elif left < 0:
                self.offset_horizontal -= CONST_DELTA_VAL
                __debug__ and (
                    print('left'),
                    print(
                        f"suppression Pixel Per Loop{self.offset_horizontal}")
                )

            elif right < 0:
                self.offset_horizontal += CONST_DELTA_VAL
                __debug__ and (
                    print('right'),
                    print(
                        f"suppression Pixel Per Loop{self.offset_horizontal}")
                )

            elif key_c < 0:
                _exit(SIGINT)

            # ctrl 按下之后都没有碰其他的键 就没有改变compensation值
            else:
                return False, None, None

            # 改变了，所以return True
            time.sleep(0.14)
            return True, ((left < 0 or right < 0) and 'horizontal') or ((up < 0 or down < 0) and 'vertical'), ((left < 0 or right < 0) and self.offset_horizontal) or ((up < 0 or down < 0) and self.offset_vertical)

        return False, None, None

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
    bool_captured = False

    recoil_controller = RecoilController()

    weapon_switch_handler = WeaponSwitchHandler()

    print('Running. Press CTRL-C to _exit.')

    while True:
        # Ctrl+C = Exit Program (组合键退出)
        signal(SIGINT, handler)

        #
        ret_weapon, ret_bool_cap = weapon_switch_handler._capture_screen()  # OCR detect weapon
        if (ret_weapon != None and ret_bool_cap == True):
            weapon = ret_weapon
            bool_captured = ret_bool_cap
        else:
            bool_captured = False

        (weapon != None and bool_captured) and __debug__ and print(
            f"Modified config for: {weapon}")  # 打印weapon名

        # 选择的是什么游戏
        game = weapon_switch_handler.current_game

        # - 读取weapon config (WeaponSwitchHandler)
        # - 装载weapon config (RecoilController)
        if(weapon != None and bool_captured):
            retval = weapon_switch_handler._read_weapon_config(game, weapon)
            recoil_controller._load_weapon_config(retval)

        # ctrl + ↑/↓/←/→ To change suppression power
        # ctrl 和 方向键 的组合用于调节压枪力度
        # bool_changed 用于判断是否进行了改动
        bool_changed, direction, value = recoil_controller._change_compensation_raw()
        (bool_changed == True) and print(
            bool_changed, direction, value, f"weapon{weapon}")

        if(bool_changed):
            weapon_switch_handler._update_json_file(
                game, weapon, direction, value)

        if(recoil_controller.check_ads_raw()):

            if recoil_controller.is_activated:
                pydirectinput.moveRel(
                    xOffset=recoil_controller.offset_horizontal,
                    yOffset=recoil_controller.offset_vertical,
                    relative=True,
                    _pause=True,
                    duration=1
                )
