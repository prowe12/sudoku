#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 16:16:21 2022

@author: prowe

A class for displaying the Sudoko board

by Penny Rowe
"""

from abc import abstractmethod
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator


class BoardRepresentation():
    """Informal interface for classes that create a board representation,
    e.g. by printing to standard output or plotting the sudoku board
    These are the methods that must be included in the subclasses"""
    
    @abstractmethod
    def __init__(self, grid, techinque):
        """
        Plot the starting sudoku board and set up the class
        @param grid  The current values in the board, list of lists
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, grid, xpos=-1, ypos=-1):
        """Update the Sudoko board plot with the new grid
        @param grid  Grid of Sudoku numbers, list of lists
        @param xpos  x position of changed number
        @param ypos  y position of changed number
        """
        raise NotImplementedError

    @abstractmethod
    def message(self, msg):
        """
        Print a message
        """
        raise NotImplementedError

    @abstractmethod
    def finish(self, success):
        """
        Finished; print final message regarding success
        @param success  True if successful
        """
        raise NotImplementedError



class BoardPrint(BoardRepresentation):
    """A class for printing the Sudoko board to standard output as it changes"""
    def __init__(self, grid, techinque):
        """
        Plot the starting sudoku board and set up the class
        @param grid  The current values in the board, list of lists
        """
        print('Using', techinque)
        for gridrow in grid:
            print(gridrow)
        print()

    def update(self, grid, xpos=-1, ypos=-1):
        """Update the Sudoko board plot with the new grid
        @param grid  Grid of Sudoku numbers, list of lists
        @param xpos  x position of changed number
        @param ypos  y position of changed number
        """
        for gridrow in grid:
            print(gridrow)
        if xpos > 0 and ypos > 0:
            print('Just changed value at: ', xpos, ',', ypos, ':', grid[xpos][ypos])
        print()

    def message(self, msg):
        """
        Print a message
        """
        print(msg, '\n')

    def finish(self, success):
        """
        Finished; print final message regarding success
        @param success  True if successful
        """
        self.message("Success: " + str(success))



class BoardPlot(BoardRepresentation):
    """A class for plotting the Sudoko board as it changes"""
    def __init__(self, grid, technique):
        """
        Plot the starting sudoku board and set up the class
        @param grid  The current values in the board, list of lists
        """

        # Create subplots
        fig, ax = plt.subplots(figsize=(5, 4.5))
        self.ax = ax
        self.fig = fig
        self.fsize = 18
        self.nrow, self.ncol = np.shape(grid)
        self.txt = []

        # Interactive mode
        plt.ion()

        # Add the Sudoku numbers to the plot
        self.add_new_numbers(grid)

        ax.set_xlim([-.5, self.nrow-.5])
        ax.set_ylim([-.5, self.ncol-.5])

        # Make outer box thicker
        for axis in ['top', 'bottom', 'left', 'right']:
            ax.spines[axis].set_linewidth(2.5)

        minor_locator = AutoMinorLocator(3)
        ax.xaxis.set_minor_locator(minor_locator)
        minor_locator = AutoMinorLocator(3)
        ax.yaxis.set_minor_locator(minor_locator)
        plt.grid(which='minor')

        ax.set_xticks([-.5, 2.5, 5.5])
        ax.set_yticks([-.5, 2.5, 5.5])
        ax.set(xticklabels=[])
        ax.set(yticklabels=[])
        ax.tick_params(axis='y', which='both', direction='in')
        ax.tick_params(axis='x', which='both', direction='in')

        plt.grid(b=True, which='major', color='k', linewidth=2)
        plt.grid(b=True, which='minor', color='gray', linewidth=1)

        if technique == 'backtrack':
            plt.title('Sudoku solver with ' + technique, fontsize=12)
        else:
            plt.title('Sudoku solver with Backtracking + AC-3', fontsize=12)


        fig.canvas.draw()
        fig.canvas.flush_events()

        # Optionally, save the frame
        #self.figno = 1
        #plt.savefig('fig001.png')

        # Display
        plt.show()
        plt.pause(.001)


    def remove_old_numbers(self):
        """Remove the old numbers from the Sudoku plot"""
        for plttext in self.txt:
            plttext.remove()
        self.txt = []


    def display_number(self, row, col, num, color='black'):
        """The column corresponds to the x-value, the
                        # row to the y-value
        """
        xloc = col - .25
        yloc = 7.75 - row
        self.txt.append(self.ax.text(xloc, yloc, str(num), fontsize=self.fsize,
                                     color=color))

    def add_new_numbers(self, grid):
        """Add the new numbers to the Sudoku plot
        @param grid  Grid of Sudoku numbers, list of lists
        """
        #  Plot
        for row in range(self.nrow):
            for col, num in enumerate(grid[row]):
                if num > 0:
                    self.display_number(row, col, num)

    def plotsingle(self, grid, xpos, ypos):
        """Add the number at position xpos, ypos to the Sudoku plot in blue
        @param grid  Grid of Sudoku numbers, list of lists
        @param xpos  x position of changed number
        @param ypos  y position of changed number
        """
        if xpos >= 0 and ypos >= 0:
            newnum = str(grid[xpos][ypos])
            self.display_number(xpos, ypos, newnum, 'blue')


    def update(self, grid, xpos=-1, ypos=-1):
        """Update the Sudoko board plot with the new grid
        @param grid  Grid of Sudoku numbers, list of lists
        @param xpos  x position of changed number
        @param ypos  y position of changed number
        """
        #plt.show(block=False)

        self.remove_old_numbers()
        self.add_new_numbers(grid)

        # Plot the number in the indicated position in blue
        self.plotsingle(grid, xpos, ypos)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


        # Optionally, save the frame
        #self.figno += 1
        #figno = str(self.figno).zfill(3)
        #filename = 'fig' + figno +'.png'
        #plt.savefig(filename)

        # Display
        plt.show()
        plt.pause(.001)


    def message(self, msg):
        """
        Print a message on the plot
        @param msg The message to print
        """
        plt.xlabel(msg, fontsize=self.fsize)

        # Optionally, save the frame
        #plt.savefig('fig_final.png' )


    def finish(self, success):
        """
        Wrap up the plot
        success  Wether or not the run was successful
        """

        if success:
            msg = 'Success!'
            self.message(msg)
        plt.pause(10)
