from ast import arg
from email.policy import default
import sys  # Get command line arguments
import time  # analytics
from optparse import OptionParser

import cv2  # Video reading with opencv
import mediapipe as mp  # Mediapipe for the Blazepose (and other stuff)

KEY_ESC = 27

# MEDIA PIPE BLAZEPOSE PREP
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

parser = OptionParser()
parser.add_option("-s", "--start", type="int", dest="start",
                  help="start frame", default=0)

(options, arguments) = parser.parse_args()
flip = False
print(options)
print(arguments)

# Open video
if len(arguments) >= 2:
    print('in ' + arguments[0]+' out ' + arguments[1])
    cap = cv2.VideoCapture(arguments[0])
else:
    # webcam
    cap = cv2.VideoCapture(0)
    flip = True

len_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# start frame
cap.set(cv2.CAP_PROP_POS_FRAMES, options.start if options.start > 0 else 0)

# List codec options
output = None
if len(arguments) >= 2:
    output = cv2.VideoWriter(arguments[1], cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), int(cap.get(
        cv2.CAP_PROP_FPS)), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

count = 0
process_time = 0.0

with mp_pose.Pose(
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75,
        model_complexity=2
) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            continue

        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # processing time
        t0 = time.time()
        results = pose.process(frame)
        # analytics
        process_time += time.time() - t0

        frame.flags.writeable = True
        image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
        )

        if results.pose_landmarks:
            hr = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
            hl = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
            # print("Right hip %f, %f z=%f, Left hip %f, %f z=%f" % (hr.x, hr.y, hr.z, hl.x, hl.y, hl.z))

        # flip on selfie
        image = image if not flip else cv2.flip(image, 1)

        # cv2.circle(image, (int(width * (1.0 - g_hands[0])), int(height * g_hands[1])), 5, (255, 0, 0), 3)

        if output:
            output.write(image)

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Pose', image)
        count = count + 1

        if output and count >= len_frames:
            break

        if cv2.pollKey() == KEY_ESC:
            break

if count > 0:
    print("Avg. processing time: %.2f ms/frame" %
          (1000 * process_time / count,))

cap.release()
if output:
    output.release()

cv2.destroyAllWindows()
