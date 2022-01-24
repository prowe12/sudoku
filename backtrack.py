#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 11:27:10 2021

@author: prowe

Solve Sudoku with backtracking

Inspired by code here:
https://www.geeksforgeeks.org/building-and-visualizing-sudoku-game-using-pygame/
"""


def getsquarevals(grid, row, col):
    """
    Get all the numbers from the 3x3 square including the row and the column
    """
    irow = row//3
    icol = col//3
    return [grid[i][j] for i in range(irow * 3, irow * 3 + 3) \
            for j in range(icol * 3, icol * 3 + 3)]


def alreadythere(grid, row, col, val):
    """
    Check if the value entered in board is already in the row or column
    @param grid  The current numbers of the Sudoku board, list of lists
    @param row
    @param col
    @param val
    """

    # Is the value already in the row?
    if val in grid[row]:
        return True

    # Is the value already in the column?
    colvals = [grid[i][col] for i in range(9)]
    if val in colvals:
        return True

    # Is the value in the 3x3 square?
    if val in getsquarevals(grid, row, col):
        return True

    return False


def backtrack(grid, boardRep, row, col):
    """
    Solve the sudoku board using ONLY Backtracking
    @param grid  The current numbers of the Sudoku board, list of lists
    @param boardRep  The class for printing or plotting the board
    @param row  Index to row
    @param col  Index to col
    """

    while grid[row][col] > 0:
        if row < 8:
            row += 1
        elif row == 8 and col < 8:
            row = 0
            col += 1
        elif row == 8 and col == 8:
            # Exit condition
            return grid, True

    for testnum in range(1, 10):
        if not alreadythere(grid, row, col, testnum):
            grid[row][col] = testnum

            boardRep.update(grid, row, col)
            grid, success = backtrack(grid, boardRep, row, col)
            if success:
                # This is the exit condition
                return grid, True

            grid[row][col] = 0
            boardRep.update(grid)

    return grid, False


def quality_check(grid):
    """
    Make sure that the board is valid
    @param grid  The current numbers of the Sudoku board, list of lists
    """
    for row in range(9):
        for col in range(9):
            val = grid[row][col]
            if val == 0:
                continue
            grid[row][col] = 0
            if alreadythere(grid, row, col, val):
                raise ValueError('Duplicate value in row:', row, ', col:', col)
            grid[row][col] = val


def backtracker(grid, boardRep):
    """
    Solve the sudoku board using ONLY Backtracking
    @param grid  The current numbers of the Sudoku board, list of lists
    @param boardRep  The class for printing or plotting the board
    """

    # Check the starting grid
    quality_check(grid)

    grid, success = backtrack(grid, boardRep, 0, 0)

    # Final test
    if success:
        quality_check(grid)

    return grid, success
