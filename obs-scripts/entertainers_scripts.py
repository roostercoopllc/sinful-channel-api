import time
import rotatescreen
import keyboard

def camera_whirl():
    screen = rotatescreen.get_primary_display()
    start_pos = screen.current_orientation

    for i in range(1, 5):
        pos = abs((start_pos - i*90) % 360)
        screen.rotate_to(pos)
        time.sleep(1.5)