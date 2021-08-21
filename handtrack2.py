import numpy as np
import cv2
import mediapipe as mp
from pykeyboard import PyKeyboard
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
drawing_styles = mp.solutions.drawing_styles
# help(mp_hands.Hands)
import time


min_curl, max_curl = 10, 0
def proc(x):
    return min(max((x - min_curl) / (max_curl - min_curl), 0), 1)


k = PyKeyboard()

# Run MediaPipe Hands.
dataset = []
try:
    with mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=2,
            min_detection_confidence=0.7) as hands:
        cap = cv2.VideoCapture(0)
        # arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.
        fings = [0. for _ in range(6)]
        while True:
            cv2.waitKey(16)

            name = 'cam'
            _, image = cap.read()
            # print(image)
            # Convert the BGR image to RGB, flip the image around y-axis for correct
            # handedness output and process it with MediaPipe Hands.
            results = hands.process(cv2.flip(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), 1))

            # cv2.imshow("src", image)

            # Print handedness (left v.s. right hand).
            # print(f'Handedness of {name}:')
            # print(results.multi_handedness)

            if not results.multi_hand_landmarks:
                continue
            # Draw hand landmarks of each hand.
            # print(f'Hand landmarks of {name}:')
            image_hight, image_width, _ = image.shape
            annotated_image = cv2.flip(image.copy(), 1)
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Print index finger tip coordinates.
                # print(
                #     f'Index finger tip coordinate: (',
                #     f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
                #     f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_hight})'
                # )
                cor = lambda z: (lambda o: np.array([o.x, o.y, o.z]))(hand_landmarks.landmark[mp_hands.HandLandmark
                                                                      .__getattr__(z.upper())])
                norm = lambda x: x / (x ** 2).sum()
                org = cor("wrist")
                cr = norm(np.cross(norm(cor("index_finger_mcp")-cor("wrist")), norm(cor("pinky_mcp") - cor("wrist"))))
                # dev = lambda x: np.dot(norm(norm(cor(f"{x}_tip") - cor(f"{x}_mcp")) - norm(cor(f"{x}_mcp") - cor("wrist"))), cr)
                dev = lambda x: np.dot(norm(cor(f"{x}_tip") - cor(f"{x}_mcp")), norm(cor(f"{x}_mcp") - cor("wrist")))
                # print(dev("index_finger"), dev("middle_finger"), dev("ring_finger"), dev("pinky"))
                # print(cr)
                # print(list(results.multxi_handedness)[i].classification)
                # is_right = results.multic_handedness[i].label == "Right"
                is_right = "Right" in str(results.multi_handedness[i])
                # print(results.multi_handedness)
                for j, f in enumerate(["index", "middle", "ring"]):
                    fings[int(is_right) * 3 + j] = proc(dev(f"{f}_finger"))
                '''
                mp_drawing.draw_landmarks(
                    annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    drawing_styles.get_default_hand_landmark_style(),
                    drawing_styles.get_default_hand_connection_style())
                    '''
            # print('\r' + str(fings), end='')
            # hand_flexed = any(x >= 0.5 for x in fings)
            # print('\r' + str(hand_flexed), end='')
            dataset.append(tuple(x >= 0.5 for x in fings))
            '''
            for i, j in zip((k.right_key, k.up_key, k.left_key, 'x', k.down_key, 'c'), fings):
                if j >= 0.5:
                    k.press_key(i)
                else:
                    k.release_key(i)
                    '''
            # if fings[0] >= 0.5 or fings[4] >= 0.5:
            #     k.tap_key(k.up_key)
            cv2.imshow("five", cv2.flip(annotated_image, 1))
except KeyboardInterrupt:
    import pandas as pd
    pd.DataFrame(dataset).to_hdf("data.hdf")