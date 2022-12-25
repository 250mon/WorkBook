import pyautogui
import time
import datetime
import sys

waiting = 0.2

def imgFileName(imgFile):
    return 'res\\' + imgFile


def clickImg(img, *args):
    loc = pyautogui.locateCenterOnScreen(img)
    while loc is None:
        return None
    else:
        pyautogui.moveTo(loc, duration=0.05)
        pyautogui.click(loc)
    if args:



def mustClickImg(img_):
    while clickImg(img_) is None:
        time.sleep(waiting)


def refresh():
    pyautogui.click(1390,150)
    while pyautogui.locateOnScreen(imgFileName('refresh_check_btn.png')) is None:
        time.sleep(waiting)
    pyautogui.click(960,700)


def main():
    refresh()
    while (clickImg(imgFileName('book_possible.png')) is None):
        refresh()
    mustClickImg(imgFileName('select_btn.png'))
    mustClickImg(imgFileName('booking_complete_btn.png'))
    mustClickImg(imgFileName('apply_btn.png'))


if __name__ == '__main__':
    pyautogui.FAILSAFE = True
    try:
        main()
    except KeyboardInterrupt:
        print('Terminated\n')
