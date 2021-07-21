
import pynput
from pynput import mouse
from pynput.mouse import Button, Controller
from pynput import keyboard

import win32con

import win32api

import time
import pyautogui
import pydirectinput
from os import _exit
from signal import signal, SIGINT
# import _thread
# import threading

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1

screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()

pyautogui.MINIMUM_SLEEP = 0.1
pydirectinput.MINIMUM_SLEEP = 0.1


# The key combination to check
#
# 左右键一起按下时
COMBN_SUPPRESSOR_ENB = {mouse.Button.right, mouse.Button.left}

#
COMBN_ADJUST_SUP = {keyboard.Key.ctrl, mouse.Button.left}

CONST_DELTA_VAL = 1


class RecoilController:
    is_ads: bool
    is_activated: bool = True
    offset_val = 15

    current_mouse = set()

    def __init__(self):
        self.is_ads = False

    def clickmouse(self, x, y, button, pressed):
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        try:
            self.is_ads = self.on_click_ads(x, y, button, pressed)

        except:
            print(f'{now}未知鼠标操作')

    def onpress(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key))
            if key == keyboard.Key.esc:
                # Stop listener
                # self.is_activated = not self.is_activated

                print(self.is_activated)
            elif key == keyboard.Key.backspace:
                self.is_activated = not self.is_activated
                # _exit(SIGINT)

        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def change_compensation_raw(self):
        ctrl = win32api.GetKeyState(0x11)
        up = win32api.GetKeyState(win32con.VK_UP)
        down = win32api.GetKeyState(win32con.VK_DOWN)

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
            if up < 0:
                print('up')
                self.offset_val += CONST_DELTA_VAL
                print(f"suppression Pixel Per Loop{self.offset_val}")

            elif down < 0:
                print('down')
                # 判断Limit
                if(self.offset_val > CONST_DELTA_VAL):
                    self.offset_val -= CONST_DELTA_VAL
                    print(f"suppression Pixel Per Loop{self.offset_val}")

            elif key_c < 0:
                _exit(SIGINT)

            time.sleep(0.06)

    def change_compensation(self, x, y, dx, dy):
        if dy > 0:
            print('上滑')
            self.offset_val += 5.43561
        elif dy < 0:
            if(self.offset_val > 0):
                self.offset_val -= 5.43561
            print('下滑')
        # if dx:
        #     print(f"滑轮在({x}, {y})处向{'右' if dx > 0 else '左'}滑")
        # else:

        #     print(f"滑轮在({x}, {y})处向{'上' if dy > 0 else '下'}滑")

    def on_click_ads(self, x, y, button, pressed):
        # 按下左右键
        mouse = Controller()
        # mouse.position = (512, 450)

        if button in COMBN_SUPPRESSOR_ENB and pressed:
            self.current_mouse.add(button)
            print(button)
            if self.is_activated:
                if all(btn in self.current_mouse for btn in COMBN_SUPPRESSOR_ENB):
                    # if all(btn in self.current_mouse for btn in COMBN_SUPPRESSOR_ENB):
                    print('All modifiers active!')
                    # mouse.move(None, 800)

                    # pydirectinput.moveRel(
                    #     xOffset=0, yOffset=self.offset_val, _pause=True)

                    # pydirectinput.move(
                    #     xOffset=0, yOffset=1, _pause=True)

                    # pydirectinput.moveTo(
                    #     x=960, y=540, duration=0.0, _pause=False)

                    # pydirectinput.moveTo(
                    #     x=960, y=540, duration=0.0, _pause=False)

                    pydirectinput.moveRel(
                        xOffset=0, yOffset=self.offset_val, relative=True, _pause=False, duration=0.1)

                    button = None
                    # pyautogui.moveRel(-55, 555.21)
                    # pyautogui.tripleClick()
                    # return True
        else:
            self.current_mouse.remove(button)
            return False

    def check_ads_raw(self):
        l = win32api.GetKeyState(0x01)
        r = win32api.GetKeyState(0x02)

        if l < 0 and r < 0:
            # print('Both Button Pressed')
            return True
        else:
            return False
        time.sleep(0.001)

    def check_ads(self, x, y, button, pressed):
        try:
            # 按下:
            if pressed:

                # 是右键:
                if button == mouse.Button.right:
                    print("开镜了")
                    self.recoil_control(button, pressed)
                    return True
            # 松手:
            else:
                print("没有开镜")
                return False

        except:
            print('未知鼠标操作')

    def recoil_control(self, x, y, button, pressed):
        print("in recoil control")
        if self.is_ads:
            if button == mouse.Button.left and pressed:
                print("压枪")
                # pyautogui.moveRel(0, 10)
                pydirectinput.moveRel(0, 10)

    def run_thread_two(self):
        on_click_func = self.check_ads
        pynput.mouse.Listener(on_click=on_click_func).run()


def handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. _exiting gracefully')
    _exit(0)


if __name__ == '__main__':

    recoil_controller = RecoilController()

    # t = threading.Thread(target=send_click, name='recoil_controller',args)

    # t = threading.Thread(
    #     target=recoil_controller.run_thread_two, name='recoil_controller', args=())

    # t.start()

    # m_listener = pynput.mouse.Listener(
    #     on_click=recoil_controller.clickmouse,
    #     on_scroll=recoil_controller.change_compensation
    # ).start()

    # k_listener = pynput.keyboard.Listener(
    #     on_press=recoil_controller.onpress
    # )

    # k_listener.start()

    print('Running. Press CTRL-C to _exit.')
    while True:
        # Ctrl+C = Exit Program (组合键退出)
        signal(SIGINT, handler)

        # Scroll to change supression
        recoil_controller.change_compensation_raw()

        currentX, currentY = pydirectinput.position()
        if(recoil_controller.check_ads_raw()):
            if recoil_controller.is_activated:
                pydirectinput.moveRel(
                    xOffset=0, yOffset=recoil_controller.offset_val, relative=True, _pause=True, duration=1)

            # pydirectinput.tripleClick(x=currentX, y=currentY, interval=0.0, button=pydirectinput.LEFT,
            #                           duration=0.0, tween=None, logScreenshot=None, _pause=True)

    # try:
    #     _thread.start_new_thread(
    #         run_thread_two, ("Thread1", recoil_controller.clickmouse)
    #     )
    # except:
    #     print("Error: 无法启动线程")

    # _thread.start_new_thread(run_thread_two, (recoil_controller))
