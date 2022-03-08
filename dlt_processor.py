import numpy as np
import cv2  # Video reading with opencv
import mediapipe as mp  # Mediapipe for the Blazepose (and other stuff)

from dltx import DLTcalib, DLTrecon

__all__ = ["DLTProcesor"]

Landmark = mp.solutions.pose.PoseLandmark

BLUE = (255, 0, 0)
RED = (0, 0, 255)
YELLOW = (0, 255, 255)
GREEN = (0, 255, 0)
GRAY_DARK = (32, 32, 32)


def distance(p1, p2):
    if p1 is None:
        return None

    if p2 is None:
        return None

    return np.sqrt(((p1[0]-p2[0])**2) + ((p1[1]-p2[1])**2) + ((p1[2]-p2[2])**2))


class DLTProcessor:
    def __init__(self, cameras, world_positions, n_dim=3, world_unit=1000.0):
        """
        Params:
            cameras         : list;
            world_positions : list;
            n_dim           : int; number of world dimensions
        """
        self.prev_state = {
            "t": 0,
            "t_start": None,
            "t_end": None,
            "pos_hip": None,
            "pos_hip_start": None,
            "s_total": None,
            "v_total": None,
        }

        self.n_dim = n_dim
        self.cameras = cameras
        self.world_unit = world_unit
        self.pos_data = []

        # dlt camera transform array
        self.L_arr = []

        # calibrate all cameras
        for i, cam in enumerate(cameras):
            L, err = DLTcalib(n_dim, world_positions, np.array(cam))
            self.L_arr.append(L)
            self.calibration_error = err
            print("Error of the calibration of camera %i (in pixels): %.3f" % (i, err))

    def _draw_calibration_pos(self, camera, image):
        for idx, p in enumerate(camera):
            pos = (int(p[0]), int(p[1]))
            cv2.circle(image, pos, 10, YELLOW, 4)
            cv2.putText(image, str(idx), (pos[0] - 10, pos[1] + 40), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, YELLOW, 2, cv2.LINE_AA)

    def _display_metrics(self, image, t_total, s_total, v, t=None, fps=100.0):
        LINE_HEIGHT = 40
        CHAR_WIDTH = 20

        texts = []
        if t is not None:
            texts.append('t: %3.3f s' % (t,))

        if v is not None:
            texts.append('v: %5.2f m/s (frame)' % (v,))

        if s_total:
            texts.append('s: %5.2f m (total)' % (s_total / self.world_unit,))

        if s_total and t_total:
            texts.append('v: %5.2f m/s (total)' %
                         (fps * s_total / (t_total * self.world_unit),))

        if len(texts) == 0:
            return

        # draw
        max_chars = max([len(ln) for ln in texts])

        cv2.rectangle(image, (20, 10), (30 + CHAR_WIDTH * max_chars, 25 + len(texts) * LINE_HEIGHT),
                      GRAY_DARK, cv2.FILLED)

        for i_line, text in enumerate(texts):
            ty = 40 + LINE_HEIGHT * i_line
            cv2.putText(image, text, (40, ty), cv2.FONT_HERSHEY_SIMPLEX,
                        1, GREEN, 1, cv2.LINE_AA)

    def get_analysis(self):
        fps = self.prev_state["fps"]
        s = self.prev_state["s_total"] / self.world_unit if self.prev_state["s_total"] else None
        t = self.prev_state["t_total"]
        v = None if not t or not s else fps * s / t

        return {
            "v": v,
            "s": s
        }

    def get_position(self, screen_positions):
        return DLTrecon(self.n_dim, len(self.cameras),
                        self.L_arr, screen_positions)

    def process(self, images, pose_results, frame_params={}):
        w = frame_params["width"]
        h = frame_params["height"]
        fps = frame_params["fps"]

        # store fps for analysis
        self.prev_state["fps"] = fps

        # draw calibration markers
        for (image, camera) in zip(images, self.cameras):
            self._draw_calibration_pos(camera, image)

        world_pos = None

        if pose_results:
            screen_positions = []
            for (image, results, camera) in zip(images, pose_results, self.cameras):
                hr = results.pose_landmarks.landmark[Landmark.RIGHT_HIP]
                hl = results.pose_landmarks.landmark[Landmark.LEFT_HIP]

                # hip center
                mx = w * (hr.x + hl.x) / 2
                my = h * (hr.y + hl.y) / 2
                screen_positions.append([mx, my])

                # draw
                cv2.circle(image, (int(mx), int(my)), 5, BLUE, 3)

            # solve world positions
            world_pos = self.get_position(screen_positions)

        v = None
        s = None

        if self.prev_state["pos_hip"] is not None and world_pos is not None:
            # distance since prev frame
            s = distance(self.prev_state["pos_hip"], world_pos)
            v = (fps * s) / self.world_unit  # --> m/s

        t = self.prev_state["t"]
        t_start = self.prev_state["t_start"]
        pos_start = self.prev_state["pos_hip_start"]

        if world_pos is not None:
            self.pos_data.append([t, *world_pos])

        s_total = distance(pos_start, world_pos)
        print("pos_start", pos_start, "t_start", t_start, "t", t, "pos_cur", world_pos)
        if (s is not None and v is not None and s_total is not None):
            print("     s=%.2f" % (s,), "v=%.2f" % (v,), "s_tot=%.2f"%(s_total,))
        t_total = (t - t_start) if t_start is not None else None

        for image in images:
            self._display_metrics(image, t_total, s_total, v, t/fps)

        # update state
        if self.prev_state["t_start"] is None and world_pos is not None:
            # first frame with detected position
            self.prev_state["t_start"] = t

        if self.prev_state["pos_hip_start"] is None:
            self.prev_state["pos_hip_start"] = world_pos

        if s_total:
            self.prev_state["s_total"] = s_total

        self.prev_state["pos_hip"] = world_pos
        self.prev_state["t"] = t + 1
        self.prev_state["t_total"] = t_total
