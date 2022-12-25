import pyautogui
import time
import sys
from PIL import ImageGrab

waiting = 0.1
zero_loc = (466, 246)
horz_interval = 166
vert_interval = 90
first_cell_btn_loc = (zero_loc[0] + 145, zero_loc[1] + 84)
horz, vert = 1, 1

refresh_btn_loc = (zero_loc[0] + 924, zero_loc[1] - 100)
complete_btn_loc = (zero_loc[0] + 537, zero_loc[1] + 694)
scan_ready_loc = (zero_loc[0] + 334, zero_loc[1] + 54)
cell_btn_loc = (first_cell_btn_loc[0] + horz_interval * horz, first_cell_btn_loc[1] + vert_interval * vert)
check_btn_loc = (960, 700)

check_btn_screen = {'loc':(974, 591), 'expectedRGB':(34, 34, 34)}
scan_ready = {'loc':scan_ready_loc, 'expectedRGB':(243, 248, 253)}
cell_btn = {'loc':cell_btn_loc, 'expectedRGB':(0, 119, 185)}
select_btn = {'loc':(1000, 700), 'expectedRGB':(0, 125, 180)}
complete_btn = {'loc':complete_btn_loc, 'expectedRGB':(0, 125, 180)}
apply_btn = {'loc':(1000, 700), 'expectedRGB':(0, 125, 180)}

cell_1_btn_loc = (first_cell_btn_loc[0], first_cell_btn_loc[1] + vert_interval * 0)
cell_1_btn = {'loc':cell_1_btn_loc, 'expectedRGB':(0, 119, 185)}
cell_2_btn_loc = (first_cell_btn_loc[0], first_cell_btn_loc[1] + vert_interval * 1)
cell_2_btn = {'loc':cell_2_btn_loc, 'expectedRGB':(0, 119, 185)}
cell_3_btn_loc = (first_cell_btn_loc[0], first_cell_btn_loc[1] + vert_interval * 2)
cell_3_btn = {'loc':cell_3_btn_loc, 'expectedRGB':(0, 119, 185)}
cell_4_btn_loc = (first_cell_btn_loc[0], first_cell_btn_loc[1] + vert_interval * 3)
cell_4_btn = {'loc':cell_4_btn_loc, 'expectedRGB':(0, 119, 185)}
cell_btns = [cell_1_btn, cell_2_btn, cell_3_btn, cell_4_btn]

def isOn(pointToCheck):
    screen_ = ImageGrab.grab()
    return screen_.getpixel(pointToCheck['loc']) == pointToCheck['expectedRGB']


def isReady(pointToCheck):
    while True:
        if isOn(pointToCheck):
            break;
        time.sleep(waiting)
    return True;


def refresh():
    pyautogui.click(refresh_btn_loc)
    isReady(check_btn_screen)
    pyautogui.click(check_btn_loc)


def main():
    while True:
        refresh()
        if isReady(scan_ready) and isOn(cell_btn):
            break;
    pyautogui.click(cell_btn['loc'])

    #     if isReady(scan_ready):
    #         found = False
    #         for cell in cell_btns:
    #             if isOn(cell):
    #                 temp_cell_btn = cell
    #                 found = True
    #                 break;
    #         if found:
    #             break
    # pyautogui.click(temp_cell_btn['loc'])

    isReady(select_btn)
    pyautogui.click(select_btn['loc'])
    isReady(scan_ready)
    pyautogui.click(complete_btn_loc)
    isReady(apply_btn)
    pyautogui.click(apply_btn['loc'])
    #pyautogui.moveTo(apply_btn['loc'])


if __name__ == '__main__':
    pyautogui.FAILSAFE = True
    try:
        main()
    except KeyboardInterrupt:
        print('Terminated\n')
