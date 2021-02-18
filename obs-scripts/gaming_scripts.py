import re
import sys

import win32api as win32
import win32con

# https://stackoverflow.com/questions/42007272/screen-rotation-in-windows-with-python

def rotate_screen(x, rotation_val):
    device = win32.EnumDisplayDevices(None,x)
    dm = win32.EnumDisplaySettings(device.DeviceName,win32con.ENUM_CURRENT_SETTINGS)
    if((dm.DisplayOrientation + rotation_val)%2==1):
        dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth   
    dm.DisplayOrientation = rotation_val

    win32.ChangeDisplaySettingsEx(device.DeviceName,dm)

def spin_screen(x, rotation_val):
    pass

def scramble_keys():
    pass

def screen_mayham():
    pass

def percentage_mayham():
    pass