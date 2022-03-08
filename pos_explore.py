import os
import numpy as np
from pylab import plot, show, legend, figure, subplot, ylabel, xlabel, grid, title, suptitle


def mean_v(fname, type="text", fps=100, unit=1000):
    x = read_arr(fname, type=type)
    d = np.sqrt(((x[0, 1:]-x[-1, 1:])**2).sum())
    t = x[-1, 0] - x[0, 0]
    return (d * fps) / (t * unit)


def read_arr(fname, type="text"):
    d = np.fromfile(fname, sep=";") if type == "text" else np.fromfile(fname)
    return d.reshape([int(len(d)/4), 4])


def pplot(x, fps=100.0, unit=1000.0, h="Veto"):
    # plot
    figure(1)
    suptitle("Lantion keskipiste: %s" % (h,))
    legends = ["x", "y", "z"]
    for dim in range(3):
        subplot(2, 2, 1 + dim)
        plot(x[:, 0]/fps, x[:, (1+dim)], label=legends[dim])
        ylabel("mm")
        xlabel("s")
        grid()

        legend()
    d = x[1:, :]-x[:-1, :]  # delta
    ds = np.sqrt((d[:, 1:]**2).sum(1))
    subplot(2, 2, 4)
    title("Juoksunopeus")
    plot(x[1:, 0]/fps, fps*ds/unit, '--', label="v")
    ylabel("m/s")
    xlabel("s")
    # show
    legend()
    show()


def qplot(run_num):
    """Quick plot by run number.
    """
    filename = "_%d.array" % (run_num,)
    path = os.path.join("output", filename)
    pplot(read_arr(path), h="Veto " + str(run_num))


if __name__ == "__main__":
    qplot(30)
