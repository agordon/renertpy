"""
RenertPy Python Package
Copyright (C) 2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""

from .utils import load_image_as_2d_rgb_list,rgb_list_to_gray_scale
import os

parrot_rgb = None
parrot_bw = None
butterfly_rgb = None
butterfly_bw = None

def load_picture_data():
    global parrot_rgb, parrot_bw
    global butterfly_rgb, butterfly_bw

    rootdir = os.path.abspath(os.path.dirname(__file__))
    datadir = os.path.join(rootdir,"data")
    parrot_rgb = load_image_as_2d_rgb_list( os.path.join(datadir,"parrot.jpg") )
    butterfly_rgb = load_image_as_2d_rgb_list( os.path.join(datadir,"butterfly.jpg") )

    parrot_bw = rgb_list_to_gray_scale(parrot_rgb)
    butterfly_bw = rgb_list_to_gray_scale(butterfly_rgb)

def get_data_parrot_rgb():
    return parrot_rgb

def get_data_parrot_bw():
    return parrot_bw

def get_data_butterfly_rgb():
    return butterfly_rgb

def get_data_butterfly_bw():
    return butterfly_bw
