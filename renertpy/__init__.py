"""
RenertPy Python Package
Copyright (C) 2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""

from .list_plots import (bar_plot,
                         line_plot,
                         greyscale_plot,
                         greyscale_2d_plot,
                         colorname_plot,
                         rgb_plot,
                         rgb_2d_plot)

from .list_audio import (play_frequencies,
        play_frequencies_durations)

from .data import (load_picture_data,
                  get_data_parrot_rgb,
                  get_data_parrot_bw,
                  get_data_butterfly_rgb,
                  get_data_butterfly_bw)

# Try to load the version string.
# the 'version.py' file is auto-generated by 'setup.py'.
# if it is not found, this module is being used without
# proper installation.
try:
    from .version import __version__
except ImportError as e:
    __version__ = "0.0.0+BAD.VERSION"

load_picture_data()
