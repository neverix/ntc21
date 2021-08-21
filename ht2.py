import serial
import time
import cv2
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)
d = []

cap = cv2.VideoCapture(0)
while True:
    cv2.waitKey(1)
    # name = 'cam'
    _, image = cap.read()
    try:
        c = []
        for _ in range(3):
            n = int(arduino.readline())
            if n > 0:
                continue
            a = -n - 1
            b = int(arduino.readline())
            c.append((a, b))
        d.append(dict(c))
    except ValueError:
        pass
    cv2.imshow("img", cv2.flip(annotated_image, 1))