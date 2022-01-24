#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 12:05:35 2021

@author: prowe

Purpose:
    Solve a Sudoku puzzle as a Constraint Satisfaction Problem (CSP), using
    Arc Consistency 3 (AC-3) and Backtracking

By Penny Rowe
2021/03/10
AI with Prof. America Chambers, Spring 2021
"""

from copy import deepcopy

from variable import Variable
from constraints import get_all_constraints, qc_board_and_constraints
from constraints import reverse_constraints, final_constraints

# Choose how to get the next unassigned variable
#from get_unassigned_variable import get_next_unassigned as get_unassigned
#from get_unassigned_variable import get_unassigned_using_mrv as get_unassigned
from get_unassigned_variable import get_unassigned_using_mrv_and_degree as get_unassigned




def get_board(grid, nside=9):
    """
    Create the board has a list of lists of each cell, where each cell is a
    class containing a domain and a set of constraints
    @param grid  The Numbers in the Sudoku board, as a list of list of int
    @param nside  Elements in a side of the board; default 9
    """
    board = [[[] for i in range(nside)] for j in range(nside)]

    board = [[Variable(i, j, nside) for i in range(nside)] for j in range(nside)]

    for i, row_vals in enumerate(grid):
        for j, val in enumerate(row_vals):
            if val == 0:
                board[i][j] = Variable(i, j, nside)
            else:
                board[i][j] = Variable(i, j, nside, {val}, fix=True)
    return board



def get_grid(board):
    """
    Get the grid for the board
    @param board ???
    """
    if board == -1:
        return None
    nrows = len(board)
    ncols = len(board[0])

    grid = [[0 for i in range(ncols)] for j in range(nrows)]
    for i in range(nrows):
        for j in range(ncols):
            if board[i][j].get_domain_size() == 1:
                grid[i][j] = board[i][j].get_only_value()
            elif board[i][j].get_domain_size() == 0:
                grid[i][j] = -1
            else:
                grid[i][j] = 0

    return grid




def is_complete(board):
    """
    Check if the board is complete, where complete means each cell has
    only one value. Note that checking for consistency is not done here.
    @param board: List of lists of class instance for cell of Sudoku board
    @return True if the board is complete, False otherwise
    """
    if board == -1:
        return False
    for row in board:
        for var in row:
            if var.get_domain_size() > 1:
                return False
    return True



def solve(original, boardPlot):
    """
    Solve Sudoku given a set of cells with fixed values
    @param original Starting grid, with zeros for unknown values, as
                    llist of lists of integers
    @param boardPlot Class for plotting the board
    @return  The solved Sudoku grid
    """

    max_domain_val = len(original)
    board = get_board(original, max_domain_val)   # list of lists of Variables

    # .. Get the starting constraints
    constraints = get_all_constraints(board[0][0].max_domain_val)

    # .. Check if the fixed values are inconsistent
    #    and remove them from the board
    constraints, success = qc_board_and_constraints(board, constraints)
    if not success:
        boardPlot.message('Starting board is not valid.')
        return get_grid(board), False

    # .. Try AC-3 alone first
    board = arc_consistency3(board, deepcopy(constraints), boardPlot)
    if is_complete(board):
        return get_grid(board), True

    # .. If it isn't solved, using backtracking with AC-3
    board = backtrack(deepcopy(board), constraints, original, boardPlot)

    # .. Final check: check all constraints again, even the fixed ones
    constraints = get_all_constraints(max_domain_val)
    constraints, success = qc_board_and_constraints(board, constraints)
    if not success:
        print('Something went wrong')
    if not final_constraints(board, constraints):
        success = False
        print('Something is wrong with your board!')

    return get_grid(board), success



def backtrack(assignment, constraints, original, boardPlot):
    """
    Backtracking search algorithm
    @param assignment
    @param constraints
    @param original
    @param boardPlot  Class for plotting the board
    """

    if is_complete(assignment):                 # Exit condition: board done!
        return assignment
    unasgn = get_unassigned(assignment)
    domain = deepcopy(unasgn.get_domain())

    for d in domain:
        # Replace the domain of x with d in the assignment
        assignment[unasgn.row][unasgn.col].replace(d)       # replace domain of x with d

        boardPlot.update(get_grid(assignment), unasgn.row, unasgn.col)
        temp_board = deepcopy(assignment)

        if arc_consistency3(temp_board, deepcopy(constraints), boardPlot) != -1:

            result = backtrack(temp_board, constraints, original, boardPlot)
                                                  #   assignment is returned
            if result != -1:                      #   If it worked:
                return result                     #      return it to solve


        # The is no need to remove d from domain, because the next time
        # around we will just reset it, and if we run out of values, we
        # will return FAIL (-1)
        # assignment[x.row,x.col] = d             #   remove d from domain
        # But we do need it for the graphics
        boardPlot.update(get_grid(temp_board), unasgn.row, unasgn.col)

    return -1   # Fail



def arc_consistency3(assignment, constraints, boardPlot):
    """
    arc_consistency3
    @param assignment
    @param constraints
    @param boardPlot
    """

    while constraints:
        [irow, icol], [jrow, jcol] = constraints.pop(0)
        xi = assignment[irow][icol]
        xj = assignment[jrow][jcol]

        # .. Check if xi is fixed. It shouldn't be because we already removed
        #    it from the constraints
        if xi.fixed:
            continue

        if remove_values(xi, xj, get_grid(assignment), boardPlot):
            # .. Removed a value from domain of xi based on constraint with xj.
            #    Return FAIL if nothing is left in the domain of x.
            #    Then we need to check every variable that xi has a constraint
            #    with, to see if those constraints are still satisfied or if
            #    we can simplifiy their domains based on the new domain of xi.
            #    Example: If xi has a constraint with some xk:
            #       - If the domain of xi is now {3}, and the domain of xk is
            #         also {3}, then return FAIL so we can back up.
            #       - If the domain of xi is now {3}, and the domain of xk is
            #         {1,3}, we will be able to reduce the domain of xk to {1}
            #    But note that those may already be on the queue, so now
            #    they'll be looped over twice.
            #    Those will be done in another loop around. For now, just
            #    add them to the queue
            if xi.get_domain_size() == 0:
                # CSP cannot be solved
                return -1
            new_constraints = reverse_constraints(xi.row, xi.col, xi.max_domain_val)
            constraints += new_constraints

    return assignment



def remove_values(xi, xj, tempgrid, boardPlot):
    """
    Remove values from the domain
    @param xi
    @param xj
    @param tempgrid
    @param boardPlot
    """
    modified = False

    # We can only remove values if the domain of y has only one value
    # and the domain of x is not fixed.
    # (If x and y are both fixed and equal, that should have been caught
    # previously)
    if xj.get_domain_size() == 1:
        q = xj.get_only_value()
        if q in xi.domain:
            # Remove p from Dx.
            # Note: xi points to an element of assignment, so this will also
            # remove p from xi in assignment.
            xi.remove(q)

            # Update graphics
            if xi.get_domain_size() == 1:
                tempgrid[xi.row][xi.col] = xi.get_only_value()
                boardPlot.update(tempgrid)
            modified = True
    return modified
