#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 09:39:43 2022

@author: prowe
"""


import imageio
import os
import numpy as np

fignames = []
fnames = os.listdir()
for fname in fnames:
    if fname[:3] == 'fig' and fname[-4:] == '.png':
        fignames.append(fname)
fignames = np.sort(fignames)


with imageio.get_writer('mygif.gif', mode='I') as writer:
    for filename in fignames:
        image = imageio.imread(filename)
        writer.append_data(image)
