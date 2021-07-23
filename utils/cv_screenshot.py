# USAGE
# python take_screenshot.py

import numpy as np
import pyautogui  # 用于截图
import imutils
import cv2

import win32con
import win32api

import easyocr

import time

reader = easyocr.Reader(['en'])


try:
    f = open("./settings/weapon_config.json", "a")
    f.write("Now the file has more content!")
    f.close()

    # open and read the file after the appending:
    f = open("./settings/weapon_config.json", "r")
    print(f.read())
except:
    print("Couldn't open file")


# 获取屏幕截图并存储在内存中
# 然后将PID/Pillow图像转换成 opencv可处理的numpy数组，并存储到磁盘


def capture_screen():

    y_start_offset = None,
    y_end_offset = None,
    x_start_offset = None,
    x_end_offset = None

    # 数字键1 & 数字键2
    key_one = win32api.GetKeyState(0x31)
    key_two = win32api.GetKeyState(0x32)

    if(key_one < 0 or key_two < 0):
        time.sleep(1.70)

        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        #
        cv2.imwrite("temp/in_memory_to_disk.png", image)

        # TODO: 未必需要用这个
        # # 屏幕截图并直接保存到磁盘
        # pyautogui.screenshot("temp/straight_to_disk.png")

        # 加载屏幕截图
        # image = cv2.imread("straight_to_disk.png")
        sp = image.shape

        if __debug__:
            print("height,width,dimensions")
            print(sp)

        # Full Screen Image Size:
        full_height = sp[0]
        full_width = sp[1]

        y_start = full_height - 95
        y_end = full_height - 50

        x_start = full_width - 210
        y_end = full_width - 50

        cropped = image[y_start:y_end,
                        x_start:y_end]  # Cropping Area: [y_start:y_end, x_start:y_end]

        cv2.imwrite("cropped.png", cropped)

        # cv2.imshow("Screenshot", imutils.resize(image, width=600))
        result = reader.readtext(
            'cropped.png', allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. ')
        try:
            print('weapon:')
            weapon = result[0][1]
            print(weapon)

            return weapon
        except:
            print('error')
            __debug__ and print(result)

        cv2.waitKey(0)


def main():
    while True:
        capture_screen()


if __name__ == '__main__':
    main()
