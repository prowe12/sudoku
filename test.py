#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 19:52:42 2022

@author: prowe
"""

from backtrack import getsquarevals

def test_getsquarevals():
    """Test of getsquarevals"""
    grid = [[0, 2, 2, 1, 8, 3, 6, 0, 3],
            [3, 1, 7, 2, 9, 9, 8, 7, 5],
            [5, 2, 1, 2, 0, 5, 8, 0, 8],
            [0, 2, 1, 9, 6, 3, 8, 4, 7],
            [7, 8, 6, 5, 3, 5, 0, 4, 8],
            [5, 5, 9, 8, 1, 5, 8, 2, 8],
            [3, 1, 2, 0, 8, 9, 6, 8, 1],
            [4, 8, 5, 2, 3, 0, 3, 4, 6],
            [2, 9, 1, 5, 7, 6, 3, 9, 4]]

    # First 3 rows and columns
    for i in range(3):
        for j in range(3):
            assert(getsquarevals(grid, i, j)) == [0, 2, 2, 3, 1, 7, 5, 2, 1]

    # Second 3 rows and first 3 columns
    for i in range(3, 6):
        for j in range(3):
            assert(getsquarevals(grid, i, j)) == [0, 2, 1, 7, 8, 6, 5, 5, 9]

    # Last 3 rows and first 3 columns
    for i in range(6, 9):
        for j in range(3):
            assert(getsquarevals(grid, i, j)) == [3, 1, 2, 4, 8, 5, 2, 9, 1]


    # First 3 rows and second 3 columns
    for i in range(3):
        for j in range(3, 6):
            assert(getsquarevals(grid, i, j)) == [1, 8, 3, 2, 9, 9, 2, 0, 5]

    # Second 3 rows and second 3 columns
    for i in range(3, 6):
        for j in range(3, 6):
            assert(getsquarevals(grid, i, j)) == [9, 6, 3, 5, 3, 5, 8, 1, 5]

    # Last 3 rows and second 3 columns
    for i in range(6, 9):
        for j in range(3, 6):
            assert(getsquarevals(grid, i, j)) == [0, 8, 9, 2, 3, 0, 5, 7, 6]

    # Second 3 rows and last 3 columns
    for i in range(3, 6):
        for j in range(6, 9):
            assert(getsquarevals(grid, i, j)) == [8, 4, 7, 0, 4, 8, 8, 2, 8]
