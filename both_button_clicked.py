import win32api
import time

width = win32api.GetSystemMetrics(0)
height = win32api.GetSystemMetrics(1)
midWidth = int((width + 1) / 2)
midHeight = int((height + 1) / 2)

# Left button up = 0 or 1. Button down = -127 or -128
state_left = win32api.GetKeyState(0x01)

# Left button up = 0 or 1. Button down = -127 or -128
state_right = win32api.GetKeyState(0x02)

while True:
    l = win32api.GetKeyState(0x01)
    r = win32api.GetKeyState(0x02)
    if l < 0 and r < 0:
        print('Both Button Pressed')
    else:
        pass
    time.sleep(0.001)
