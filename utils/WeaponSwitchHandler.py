
import cv2
import easyocr
import pyautogui  # 用于截图

import win32api
import time

import json

GAME = "RAINBOW_SIX_SIEGE"

reader = easyocr.Reader(['en'])


class WeaponSwitchHandler:

    def __init__(self):
        self.current_weapon = "R4-C"
        self.primary_weapon = "R4-C"
        self.secondary_weapon = "M45 MEUSOC"
        # y_start_offset = None,
        # y_end_offset = None,
        # x_start_offset = None,
        # x_end_offset = None

        self.reader = easyocr.Reader(['en'])
        self.jsonfile = open("./files/json_update_test.json", "w+")

    def detect_weapon(self):
        print("Detect Weapons")

    def load_weapon_config(self, weapon_config):
        print("loading weapon config")

    def capture_screen():
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

    def updateJsonFile(self, weapon, direction, value):
        jsonfile = self.jsonfile

        try:
            # Open the JSON file for reading
            jsonFile = open("./files/json_update_test.json", "r")
            data = json.load(jsonFile)  # Read the JSON into the buffer
            jsonFile.close()  # Close the JSON file
        except:
            jsonFile = open("./files/json_update_test.json", "w")
            print("Failed to open the file")

        data[weapon][direction] = value

        try:
            # Save our changes to JSON file
            jsonfile = open("./files/json_update_test.json", "w+")
        except:
            print("can't modify the file")

        json_data = json.dumps(data)
        print(json_data)
        jsonfile.write(json_data)
        jsonfile.close()

    # def
