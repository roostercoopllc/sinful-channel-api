import time
import rotatescreen
import keyboard

def screen_flip(duration, angle):
    screen = rotatescreen.get_primary_display()
    screen.rotate_to(angle)
    time.sleep(duration)
    screen.rotate_to(0)

def grey_grumpkin():
    pass

def brightness_blass():
    pass

def crazy_keys():
    pass

def camera_whirl():
    pass

def mic_mute():
    pass