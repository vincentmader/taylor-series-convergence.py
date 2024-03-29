import os
import pathlib
from pathlib import Path


PATH_TO_PROJECT = pathlib.Path(__file__).parent.resolve()
PATH_TO_PLOTS = os.path.join(PATH_TO_PROJECT, "../plots")

MPL_THEME = Path("..", "lib", "mpl-styles", "dark.mplstyle")
