import serial
import time
# import cv2
arduino = serial.Serial(port='/dev/cu.SLAB_USBtoUART',
                        baudrate=1000000)
d = []
#sudo chmod a+rw /dev/ttyACM0


try:
    # cap = cv2.VideoCapture(0)
    while True:
        # cv2.waitKey(1)
        # name = 'cam'
        # _, image = cap.read()
        try:
            c = {i: e for i, e in enumerate(list(map(int, arduino.readline().decode(
                'utf-8').strip().split(';'))))}
            c.append(("time", time.time()))
            d.append((dict(c)))
        except TypeError:
            pass
        except ValueError:
            pass
        # cv2.imshow("img", cv2.flip(annotated_image, 1))
except KeyboardInterrupt:
    import pandas as pd
    pd.DataFrame(d).set_index("time",).sort_index(axis=1).to_csv("ardata.csv")
