import cv2
import mediapipe as mp
import math
import time
import directkeys as dk

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

def distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    action = "NO HAND"

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            thumb = hand.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            dist = distance(thumb, index)

            if dist > 0.08:
                dk.press_key(dk.RIGHT)
                dk.release_key(dk.LEFT)
                action = "ACCELERATE"
            else:
                dk.press_key(dk.LEFT)
                dk.release_key(dk.RIGHT)
                action = "BRAKE"
    else:
        dk.release_key(dk.RIGHT)
        dk.release_key(dk.LEFT)

    cv2.putText(
        frame,
        action,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Hill Climb Racing Automation", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
