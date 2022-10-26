import numpy as np
import cv2
from mss.linux import MSS as mss
from PIL import Image
import time
import pyautogui as pg
import imutils
import mss
import numpy
import pyautogui
from random import randint

template = cv2.imread("bobber.png", cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]

color_yellow = (0, 255, 255)

mon = {'top': 80, 'left': 400, 'width': 100, 'height': 100}


def process_image(original_image):
    # processed_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    # processed_image = cv2.Canny(processed_image, threshold1=200, threshold2=300)
    processed_image = cv2.Canny(original_image, threshold1=200, threshold2=300)
    return processed_image


def ss():
    op = 0
    with mss.mss() as sct:

        monitor = {"top": 50, "left": 0, "width": 1400, "height": 850}

        while "Screen capturing":
            last_time = time.time()

            img = numpy.array(sct.grab(monitor))

            gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= 0.7)
            op += 1
            print(op)
            for pt in zip(*loc[::-1]):
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
                for _ in img:
                    # pts = (pt[0], pt[1])
                    x = (pt[0])
                    # y = (pt[1])
                    print(x)
                    if 220 < x < 372:
                        pyautogui.mouseDown(button='left')
                        time.sleep(1.2)
                        pyautogui.mouseUp(button='left')
                        x = 0
                    elif 140 < x < 219:
                        pyautogui.mouseDown(button='left')
                        time.sleep(3.2)
                        pyautogui.mouseUp(button='left')
                        x = 0
                    else:
                        continue
                    break
                else:
                    continue
                break
            # key = cv2.waitKey(1)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
            if op > 8:
                return


def screen_record():
    sct = mss.mss()
    last_time = time.time()

    while True:
        img = sct.grab(mon)
        print(f'Петля заняла {time.time() - last_time} секунд')
        last_time = time.time()

        img = np.array(img)
        processed_image = process_image(img)
        # cv2.imshow("Зона наблюдения", processed_image)
        mean = np.mean(processed_image)
        print('Среднее значение = ', mean)

        if mean <= float(0.11):
            print('ПОПЛАВОК ИСЧЕЗ ')
            pyautogui.click(button='left')
            break
            # return
        else:
            time.sleep(0.02)
            continue
        # return
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        return

while True:
    time.sleep(1)
    pyautogui.moveTo(431, 175, duration=1)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(450, 220, duration=1)
    pyautogui.mouseUp(button='left')
    time.sleep(1)
    screen_record()
    time.sleep(0.01)
    ss()
