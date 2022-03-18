import numpy as np
import matplotlib.pyplot as plt

from vang import *
import pos_explore

# dataset for bbox cropping
dataset = "pajulahti_3"

L_POINT_HIP = 3
L_POINT_KNEE = 5
L_POINT_SHOULDER = 1
L_POINT_ANKLE = 7
L_POINT_TOE = 9

R_POINT_HIP = 4
R_POINT_KNEE = 6
R_POINT_ANKLE = 8

LEFT_SIDE = [
    L_POINT_SHOULDER, L_POINT_HIP, L_POINT_KNEE,
    L_POINT_ANKLE, L_POINT_TOE]

RIGHT_SIDE = [R_POINT_HIP, R_POINT_KNEE, R_POINT_ANKLE]

def _pick_lm(x, n_frame, i_lms):
    return np.array([getvec(x, point)[n_frame, 0:2] for point in i_lms])


def stick_fig(x, n_frame):
    left_lm_xys = _pick_lm(x, n_frame, LEFT_SIDE)
    right_lm_xys = _pick_lm(x, n_frame, RIGHT_SIDE)
    plt.plot(right_lm_xys[:, 0], right_lm_xys[:, 1], '-', color="silver", linewidth=1.0)
    plt.plot(left_lm_xys[:, 0], left_lm_xys[:, 1], '-', color="k", linewidth=1.25)


num_stick_figs = 14


def draw_stick_figs(ax, x, run_num=None):
    if run_num is not None:
        plt.title("Veto " + str(run_num))
    step = int(x.shape[0] / num_stick_figs)
    for i in range(0, x.shape[0], step):
        stick_fig(x, i)
    ax.set_aspect('equal')


if __name__ == "__main__":
    for run_num in range(29, 36):
        x = pos_explore.qread(run_num)
        x = pos_explore.crop_by_dataset(x, dataset)

        lhip = getvec(x, L_POINT_HIP)
        lknee = getvec(x, L_POINT_KNEE)
        lshoul = getvec(x, L_POINT_SHOULDER)
        lankle = getvec(x, L_POINT_ANKLE)
        ltoe = getvec(x, L_POINT_TOE)

        t = x[:, 0] / 190
        theta_hip = np.array([r2d(vang(a, b))
                              for a, b in zip(lshoul-lhip, lknee-lhip)])
        theta_knee = np.array([r2d(vang(a, b))
                               for a, b in zip(lhip-lknee, lankle-lknee)])
        theta_ankle = np.array([r2d(vang(a, b))
                                for a, b in zip(lknee-lankle, ltoe-lankle)])

#        plt.figure()
        f, (a0, a1, a2, a3) = plt.subplots(4, 1,
                                           gridspec_kw={
                                               'height_ratios': [1, 1, 1, 2]},
                                           figsize=(9, 8))
        plt.suptitle("Nivelkulmat, veto " + str(run_num))

        a0.plot(t, theta_hip, label="Lantio")
        a0.set_ylabel("astetta")
        a0.legend()
        a0.grid()
        a1.plot(t, theta_knee, label="Polvi")
        a1.set_ylabel("astetta")
        a1.legend()
        a1.grid()
        a2.plot(t, theta_ankle, label="Nilkka")
        a2.set_ylabel("astetta")
        a2.legend()
        a2.grid()

        draw_stick_figs(a3, x, run_num=run_num)
        figfname = "output/kinematiikka_%d.png" % (run_num,)
        f.savefig(figfname)

        f2 = pos_explore.pplot(x, h="Veto " + str(run_num))
        f2.savefig("output/kinematiikka_lantio_%d.png" % (run_num,))

        # compute mean velocity
        delta = x[-1] - x[0]
        v = delta[1] / (10 * delta[0])
        sec,ms = divmod(v, 1.0)
        print("mean velocity;%d;%d,%03d" % (run_num, sec,int(ms*1000)))
