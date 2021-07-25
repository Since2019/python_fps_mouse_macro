
# For OCR purposes
import json
import time
import win32api
import cv2
import easyocr
import numpy as np

import pyautogui  # 用于截图
reader = easyocr.Reader(['en'])

# Key Listener


# Different games requires different screenshot area
GAME = "RAINBOW_SIX_SIEGE"


class WeaponSwitchHandler:

    def __init__(self):
        # TODO 作为一个指针，用于指向
        self.current_weapon = {"name:": "R4-C"}

        # TODO: 格式必须要规定好
        self.primary_weapon_config = {"name": "R4-C",
                                      "offset_horizontal": int(-1),
                                      "offset_vertical": int(8)
                                      }

        self.secondary_weapon_config = {"name:": "M45 MEUSOC",
                                        "offset_horizontal": int(0),
                                        "offset_vertical": int(8)
                                        }

        # y_start_offset = None,
        # y_end_offset = None,
        # x_start_offset = None,
        # x_end_offset = None

        self.reader = easyocr.Reader(['en'])
        self.current_game = "R6S"
        self.current_game_json = {}

        try:
            # TODO 目录不存在 files/
            self.jsonfile = open("json_update_test.json", "r")
        except:
            self.jsonfile = None

    def detect_weapon(self):
        print("Detect Weapons")

    #
    def __read_weapon_json(self, game):
        __debug__ and print(f"reading file for game: {game}")
        # 读取文件
        try:
            # Open the JSON file for reading
            jsonFile = open(f"{game}_weapon_config.json", "r")
            weapon_json = json.load(jsonFile)  # Read the JSON into the buffer
            jsonFile.close()  # Close the JSON file
            return weapon_json
        except:
            jsonFile = open(f"{game}_weapon_config", "w+")
            print("Failed to open the file so I created a new one.")
            return None

    # 保存数据
    def _save_weapon_config(self):
        __debug__ and print("Saving Weapon Config")

        current_weapon = self.current_weapon

        if(self.current_gamecurrent_game_json):
            current_game_json = self.current_game_json
        else:
            self.__read_weapon_json(self.current_game)

        # current_game_json[current_weapon]['verticle'] =

        # 读取文件
        try:
            # Open the JSON file for reading
            # TODO 目录不存在 files/
            jsonFile = self.jsonfile
            weapon_json = json.load(jsonFile)  # Read the JSON into the buffer
            jsonFile.close()  # Close the JSON file
        except:
            jsonFile = open("json_update_test.json", "w+")
            print("Failed to open the file")

    def _read_weapon_config(self, game, weapon_name):
        __debug__ and print(f"reading file for game: {game}")
        # - 1.试着读取文件
        # - 2.并且读取具体的武器
        # - 3.return 一个武器所对应的 JSON 变量
        try:
            # Open the JSON file for reading
            # TODO 目录不存在 files/
            jsonFile = open(f"{game}_weapon_config.json", "r")
            weapon_json = json.load(jsonFile)  # Read the JSON into the buffer
            jsonFile.close()  # Close the JSON file

            try:
                __debug__ and print(weapon_json)
                __debug__ and print(weapon_json[weapon_name])

                weapon_config = weapon_json[weapon_name]  # DONE:- 2.并且读取具体的武器
                return weapon_config                     # DONE:- 3.return 一个武器所对应的 JSON 变量

            except:
                print("cannot find such a weapon")

        except:
            jsonFile = open(f"{game}_weapon_config.json", "w+")
            print("Failed to open the file so I created a new one.")

    def _capture_screen(self):

        y_start_offset = None,
        y_end_offset = None,
        x_start_offset = None,
        x_end_offset = None

        # 数字键1 & 数字键2
        key_one = win32api.GetKeyState(0x31)
        key_two = win32api.GetKeyState(0x32)

        if(key_one < 0 or key_two < 0):
            time.sleep(1.4)

            image = pyautogui.screenshot()
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

            #
            # cv2.imwrite("temp/in_memory_to_disk.png", image)

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

            y_start = full_height - 85
            y_end = full_height - 50

            x_start = full_width - 230
            x_end = full_width - 50

            cropped = image[y_start:y_end,
                            x_start:x_end]  # Cropping Area: [y_start:y_end, x_start:y_end]

            cv2.imwrite("cropped.png", cropped)

            # cv2.imshow("Screenshot", imutils.resize(image, width=600))
            result = reader.readtext(
                'cropped.png', allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. ')
            try:
                print('weapon:')
                weapon = result[0][1]
                print(weapon)

                return weapon, True
            except:
                print('error')
                __debug__ and print(result)
                return None, False

        return None, False

    def _update_json_file(self, game, weapon, direction, value):
        jsonfile = self.jsonfile

        # - 1.读取json文件
        # - 2.更改json变量（内存）
        # - 3.写回json文件
        try:
            # Open the JSON file for reading
            jsonFile = open(f"{game}_weapon_config.json", "r")
            data = json.load(jsonFile)  # Read the JSON into the buffer
            jsonFile.close()  # Close the JSON file
        except:
            jsonFile = open(f"{game}_weapon_config.json", "w")
            # data = json.dumps({})
            data = dict()
            print("Failed to open the file")

        # 2.更改json变量（内存）
        try:
            print(f"json_data:\n{data}")
            print(
                f"GAME:{game}, Weapon:{weapon}, Direction:{direction}, Value:{value}")

            # weapon_direction = {direction: value}
            # weapon_data = {weapon: weapon_direction}
            # print(weapon_data)
            # data.update(weapon_data)

            # data['test'] = 100
            # data['testing'] = 1000
            # data["test"]["testing"] = 19999
            # if data[weapon]["horizontal"] and data[weapon]["vertical"]:
            #     data[weapon][direction] = value
            # elif direction == "horizontal":
            #     data[weapon]["horizontal"] = value
            # elif direction == "vertical":
            #     data[weapon]["vertical"] = value
            # else:
            print("data.get(weapon)")
            print(data.get(weapon))
            if(not data.get(weapon)):
                print('not in it!')
                data[weapon] = {"horizontal": 0, "vertical": 0}

            if((data.get(weapon).get('horizontal') != None) and (data.get(weapon).get('vertical') != None)):
                print(
                    "data[weapon].get(horizontal) and data[weapon].get('vertical')")
                print(data.get(weapon).get(direction))
                if direction == "horizontal":
                    data[weapon] = {
                        "horizontal": value, "vertical": data.get(weapon).get("vertical")}
                elif direction == "vertical":
                    data[weapon] = {
                        "horizontal": data.get(weapon).get("horizontal"), "vertical": value}

        except:
            print(data)
            print("can't create json'")
            pass

        try:
            # Save our changes to JSON file
            jsonfile = open(f"{game}_weapon_config.json", "w+")
        except:
            print("can't modify the file")

        json_data = json.dumps(data)
        print(json_data)
        jsonfile.write(json_data)
        jsonfile.close()

    # def
