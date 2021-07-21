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
    a = win32api.GetKeyState(0x01)
    if a != state_left:  # Button state changed
        state_left = a
        print(a)
        if a < 0:
            print('Left Button Pressed')
        else:
            print('Left Button Released')
            # win32api.SetCursorPos((midWidth, midHeight))

    b = win32api.GetKeyState(0x02)
    if b != state_right:  # Button state changed
        state_right = b
        print(b)
        if b < 0:
            print('Right Button Pressed')
        else:
            print('Right Button Released')
            # win32api.SetCursorPos((midWidth, midHeight))

    c = win32api.GetKeyState(0x04)
    if c != state_right:  # Button state changed
        state_mid_pressed = c
        print(c)
        if c > 0:
            pass
        else:
            print('Mid Button Pressed')
    time.sleep(0.001)
