import time  # analytics
from contextlib import ExitStack

import numpy as np
import cv2  # Video reading with opencv
import mediapipe as mp  # Mediapipe for the Blazepose (and other stuff)


# key constants
KEY_ESC = 27

# MEDIA PIPE BLAZEPOSE PREP
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def start_capture(inputs, outfile=None, processors=[], start=0, skip=0, cut=-1):
    print('Inputs:', ",".join(inputs))
    print("Output:", outfile)
    print("Start:", start)

    caps = [cv2.VideoCapture(input) for input in inputs]

    len_frames = sorted([int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                         for cap in caps])[0]

    widths = [int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) for cap in caps]
    heights = [int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) for cap in caps]
    fps = int(caps[0].get(cv2.CAP_PROP_FPS))

    # start frame
    skip1 = (start if start > 0 else 0) + skip
    skip2 = (-start if start < 0 else 0) + skip
    print("Skips", skip1, skip2)
    caps[0].set(cv2.CAP_PROP_POS_FRAMES, skip1)
    caps[1].set(cv2.CAP_PROP_POS_FRAMES, skip2)

    # List codec options
    output = None
    if outfile:
        output = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(
            'm', 'p', '4', 'v'), fps, (sum(widths), heights[0]))

    count = 0
    process_time = 0.0

    pose_args = {
        "min_detection_confidence": 0.75,
        "min_tracking_confidence": 0.50,
        "model_complexity": 2
    }

    poses = (
        mp_pose.Pose(**pose_args),
        mp_pose.Pose(**pose_args)
    )

    with ExitStack() as exit_stack:
        for pose in poses:
            exit_stack.enter_context(pose)

        while caps[0].isOpened() and caps[1].isOpened():
            images = []
            pose_results = []
            num_read_ok = 0

            # process each input stream
            for cap, pose in zip(caps, poses):
                ret, frame = cap.read()

                if not ret:
                    break
                else:
                    # succesfully read frame from capture source
                    num_read_ok += 1

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
                    pose_results.append(results)
                images.append(image)

            # hook processor
            has_all_results = len(pose_results) == len(images)
            # apply all combined processors
            for processor in processors:
                processor.process(images,
                                  pose_results if has_all_results else None,
                                  frame_params={
                                      "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                      "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                                      "fps": fps,
                                  })

            # output image

            if len(images) == 2:
                combined_image = cv2.hconcat(images)

                if output:
                    output.write(combined_image)

                cv2.imshow('Pose detection - %s' % (inputs[0],) , combined_image)
                count = count + 1

            if output and count >= len_frames:
                break
        
            if cut > 0 and count > cut:
                break

            if cv2.pollKey() == KEY_ESC:
                break

    if count > 0:
        print("Avg. processing time: %.2f ms/frame" %
              (1000 * process_time / count,))

    caps[0].release()
    if output:
        output.release()

    cv2.destroyAllWindows()
