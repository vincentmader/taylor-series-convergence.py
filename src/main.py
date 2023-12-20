#!/usr/bin/env python3
from math import pi as PI
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from config import PATH_TO_PLOTS
from config import MPL_THEME


FIGSIZE = (12, 6)
X_MIN, X_MAX = -15, 15
X_0 = 0
N_X = 1000
N = 20

plt.style.use(MPL_THEME)
# mpl.rcParams["text.usetex"] = True
# mpl.rcParams["text.latex.preamble"] = ["\\usepackage{amsmath}"] # This is needed for `\text` command.


def factorial(x): 
    return x*factorial(x-1) if x != 0 else 1


def cos_taylor(x, x_0, n):
    return (-1)**n * (x-x_0)**(2*n) / factorial(2*n)


def sin_taylor(x, x_0, n):
    return (-1)**n * (x-x_0)**(2*n+1) / factorial(2*n+1)


def arcsin_taylor(x, x_0, n):
    return factorial(2*n) / (4**n * (factorial(n))**2 * (2*n+1)) * (x-x_0)**(2*n+1)


def arccos_taylor(x, x_0, n):
    return PI/2 - arcsin_taylor(x, x_0, n)


def exp_taylor(x, x_0, n):
    return (x-x_0)**n / factorial(n)


def sinh_taylor(x, x_0, n):
    return (x-x_0)**(2*n+1) / factorial(2*n+1)


def cosh_taylor(x, x_0, n):
    return (x-x_0)**(2*n) / factorial(2*n)


def arcsinh_taylor(x, x_0, n):
    return (-1)**n * factorial(2*n) / (4**n*(factorial(n)**2) * (2*n+1)) * (x-x_0)**(2*n+1)


def arctanh_taylor(x, x_0, n):
    return (x-x_0)**(2*n+1) / (2*n+1)


def foo(title, func, func_taylor, ylims):
    print(f"Plotting {title} taylor from n=0 to n={N}")
    os.system(f"mkdir -p {PATH_TO_PLOTS}/{title}")
    os.system(f"rm {PATH_TO_PLOTS}/{title}/* 2> /dev/null")

    x = np.linspace(X_MIN, X_MAX, N_X)
    y = np.zeros(N_X)
    label = r"$\mathrm{" + title + "}(x)$"

    for n in tqdm(range(N)):
        a = func_taylor(x, X_0, n)
        y = y + a

        fig = plt.figure(figsize=FIGSIZE)

        plt.plot(x, func(x), 'w', label=f"original function {label}")
        plt.plot(x, y, 'g', linewidth=2, label=f"Taylor series up to $N={n}$")

        plt.xlim(X_MIN, X_MAX)
        plt.ylim(ylims[0], ylims[1])

        plt.xlabel("$x$")
        plt.ylabel("$f(x)$")

        plt.legend(loc="upper left")

        path_to_savefiles = os.path.join(PATH_TO_PLOTS, title)
        if not os.path.exists(path_to_savefiles):
            os.mkdir(path_to_savefiles)
        filename = f"{zero_pad_num(n, len(str(N)))}.png"
        path_to_savefile = os.path.join(path_to_savefiles, filename)
        plt.savefig(path_to_savefile)
        plt.close()


def main():
    FUNCS = [
        ("sin", np.sin, sin_taylor, [-1.1, 1.1]),
        ("cos", np.cos, cos_taylor, [-1.1, 1.1]),
        ("exp", np.exp, exp_taylor, [-2, 5]),
        ("sinh", np.sinh, sinh_taylor, [-5000, 5000]),
        ("cosh", np.cosh, cosh_taylor, [0, 10000]),
        ("arctanh", np.arctanh, arctanh_taylor, [-PI, PI]),
        ("arcsinh", np.arcsinh, arcsinh_taylor, [-PI/2, PI/2]),
        ("arcsin", np.arcsin, arcsin_taylor, [-PI/2, PI/2]),

        # # # # ("arccos", np.arccos, arccos_taylor, [-0, PI]),
    ]

    for title, func, func_taylor, ylims in FUNCS:
        foo(title, func, func_taylor, ylims)


def zero_pad_num(x, N):
    while len(str(x)) < N:
        x = f"0{x}"
    return x


def create_videos():
    SLOW_DOWN_FACTOR = 4

    print("Creating videos...")
    # loop over all plot-directories
    for directory in tqdm(os.listdir(PATH_TO_PLOTS)):
        path_to_dir = os.path.join(PATH_TO_PLOTS, directory)
        if not os.path.isdir(path_to_dir):
            continue

        # get path-to-video, delete if existing
        video_filename = f"{directory}.mp4"
        path_to_vid = os.path.join(PATH_TO_PLOTS, video_filename)

        # create video
        os.system(f"ffmpeg \
            -y \
            -hide_banner -loglevel error \
            -pattern_type glob \
            -i '{path_to_dir}/*.png' \
            -vcodec libx264 \
            -pix_fmt yuv420p \
            \"{path_to_vid}\""
                  )

        # change playback speed (slow-down)
        os.system(f"ffmpeg \
            -i \"{path_to_vid}\" \
            -hide_banner -loglevel error \
            -filter:v \"setpts={SLOW_DOWN_FACTOR}*PTS\" \
            \"{path_to_vid}_copy.mp4\"")
        os.system(f"mv \"{path_to_vid}_copy.mp4\" \"{path_to_vid}\"")


if __name__ == "__main__":
    main()
    create_videos()
