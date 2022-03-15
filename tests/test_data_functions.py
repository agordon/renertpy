"""
RenertPy Python Package
Copyright (C) 2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""
import unittest
import renertpy
from renertpy import *
from ipycanvas import Canvas
import PIL

class DataFunctionsTest(unittest.TestCase):

    def test_parrot_rgb_data(self):
        x = get_data_parrot_rgb()
        self.assertIsInstance(x,list)
    
    def test_parrot_bw_data(self):
        x = get_data_parrot_bw()
        self.assertIsInstance(x,list)
    
    def test_butterfly_rgb_data(self):
        x = get_data_butterfly_rgb()
        self.assertIsInstance(x,list)

    def test_butterfly_bw_data(self):
        x = get_data_butterfly_bw()
        self.assertIsInstance(x,list)

if __name__ == '__main__':
    unittest.main()
