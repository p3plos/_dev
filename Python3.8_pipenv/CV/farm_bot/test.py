import numpy as np
import cv2
from mss.linux import MSS as mss
from PIL import Image
import time
import pyautogui as pg
import cv2
import mss
import numpy

template = cv2.imread("bobber.png", cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]

color_yellow = (0,255,255)

with mss.mss() as sct:
    monitor = {"top": 40, "left": 0, "width": 800, "height": 640}

    while "Screen capturing":
        last_time = time.time()
        img = numpy.array(sct.grab(monitor))
        cv2.imshow("OpenCV/Numpy normal", img)
        print("fps: {}".format(1 / (time.time() - last_time)))
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.7)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
            for p in img:
                pts = (pt[0], pt[1])
                x = (pt[0])
                y = (pt[1])
                print(x)
                cv2.circle(template, pts, 5, (200, 0, 0), 2)
                cv2.putText(img, "%d-%d" % (x, y), (x + 10, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)

        cv2.imshow("Frame", img)
        key = cv2.waitKey(1)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break