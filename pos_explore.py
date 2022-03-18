import os
import re
import numpy as np
from pylab import plot, show, legend, figure, subplot, ylabel, xlabel, grid, title, suptitle

from datasets import load_dataset


def get_bbox(coords):
    """Compute bbox from calibration_coords.world_positions
    """
    cx = np.array(coords)
    bbox = list(zip(cx.min(0), cx.max(0)))
    return bbox


def mean_v(fname, type="text", fps=100, unit=1000):
    x = read_arr(fname, type=type)
    d = np.sqrt(((x[0, 1:]-x[-1, 1:])**2).sum())
    t = x[-1, 0] - x[0, 0]
    return (d * fps) / (t * unit)


def read_arr(fname, type="text", n_landmarks=11):
    d = np.fromfile(fname, sep=";") if type == "text" else np.fromfile(fname)
    # num columns
    cols = 1 + n_landmarks * 3
    return d.reshape([int(len(d)/cols), cols])


def pplot(x, fps=100.0, unit=1000.0, h="Veto"):
    # plot
    fig = figure()
    suptitle("Lantion keskipiste: %s" % (h,))
    legends = ["x", "y", "z"]

    for dim in range(3):
        subplot(2, 2, 1 + dim)
        plot(x[:, 0]/fps, x[:, (1+dim)], label=legends[dim])
        ylabel("mm")
        xlabel("s")
        grid()
        legend()

    d = x[1:, :4]-x[:-1, :4]  # delta
    ds = np.sqrt((d[:, 1:4]**2).sum(1))
    subplot(2, 2, 4)
    title("Juoksunopeus")
    plot(x[1:, 0]/fps, fps*ds/unit, '--', label="v")
    ylabel("m/s")
    xlabel("s")
    legend()
    return fig


def crop_bbox(bbox, x, n_landmarks=11):
    """crop data to fit into bbox
    """
    to_take = np.ones(x.shape[0])

    for i_landmark in range(n_landmarks):
        for dim in range(3):
            i_dim = 1 + 3 * i_landmark + dim 
            to_take = to_take * (x[:, i_dim] >= bbox[dim][0]) * (x[:, i_dim] < bbox[dim][1])

    # return data points inside bbox
    return x[to_take == 1]


def qread(run_num, n_landmarks=11):
    filename = "_%d.array" % (run_num,)
    path = os.path.join("output", filename)
    return read_arr(path, n_landmarks=n_landmarks)

def crop_by_dataset(x, dataset_name, n_landmarks=11):
    if dataset_name:
        ds = load_dataset(dataset_name)
        world_positions = ds[1]
        bbox = get_bbox(world_positions)
        return crop_bbox(bbox, x, n_landmarks=n_landmarks)
    else:
        return x

def qplot(run_num, n_landmarks=11, dataset=None):
    """Quick plot by run number.
    """
    data = qread(run_num)

    # apply dataset calibration frame bbox crop
    data = crop_by_dataset(data, dataset, n_landmarks=n_landmarks)

    plot_headning = "Veto " + str(run_num)
    pplot(data, h=plot_headning)
    show()


if __name__ == "__main__":
    qplot(32, dataset="pajulahti_3")
