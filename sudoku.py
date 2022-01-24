#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 11:58:44 2021

@author: prowe

Solving Sudoku using
a constraint satisfaction problem with AC-3 and Backtracking

This is the main program that loads in, displays the board and
calls the solver.

by Penny Rowe
2021/03/11
For AI with Prof. Chambers
at the University of Puget Sound
Spring 2021

"""
# Built-in modules
import sys
from os.path import exists
from numpy import loadtxt

# Sudoku modules
from backtrack import backtracker                      # Backtrack
from solver import solve                               # Backtrack + AC-3
from board_plotter import BoardPlot                    # Include graphics

# For debugging, use this instead of the above to turn off graphics
#from board_plotter import BoardPrint as BoardPlot      # No graphics

def load_starting_vals(filename=''):
    """
    Load in the incompleted Sudoku puzzle, or use default
    @param filename  Name of puzzle file to load in
    @return grid  The grid of numbers; list of lists
    @raises NameError  If filename is not '' and does not exist
    """


    if filename == '':
        # Use default grid
        grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]]
        return grid

    if not exists(filename):
        raise NameError('Puzzle file: ' + filename + ' not found.')

    grid = [[0 for i in range(9)] for j in range(9)]
    orig_vals = loadtxt(filename, dtype=int, ndmin=2)
    for row in orig_vals:
        grid[int(row[0]-1)][int(row[1]-1)] = int(row[2])

    return grid


def main(filename='', technique=''):
    """Run Sudoku solver
    filename  Filename to run, string
    technique  Technique to use. If not 'backtrack', will use backtrack + AC-3

    sample inputs
    technique = 'both'
    filenames = ["",
                 "puzzles/bad.puzz",
                 "puzzles/easy.puzz",
                 "puzzles/evil.puzz",
                 "puzzles/hard.puzz",
                 "puzzles/medium.puzz",
                 "puzzles/one.puzz",
                 "puzzles/puzzle1.puzz",
                 "puzzles/solved.puzz"
                 ]
    filename = filenames[8]
    """


    if technique == 'backtrack':
        solver = backtracker
    else:
        solver = solve

    # Set up the board
    originalgrid = load_starting_vals(filename)
    boardPlot = BoardPlot(originalgrid, technique)

    # Solve the sudoku board using Backtracking or AC-3 and Backtracking
    _, success = solver(originalgrid, boardPlot)

    # Pause the plot for a bit
    boardPlot.finish(success)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        raise ValueError('Please include 0-2 inputs, optionally filename and technique')
