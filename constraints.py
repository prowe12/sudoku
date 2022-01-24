#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 07:01:49 2021

@author: prowe
"""

def qc_board_and_constraints(board, constraints):
    """
    Purpose: When the board first comes in, do a check to see if any of the
    fixed values are duplicates
    @param board  The Sudoku board: A list of lists of variable class instances
    @param constraints  The unallowed values for each cell, list of tuples
    """
    i = 0
    while i < len(constraints):
        ([irow, icol], [jrow, jcol]) = constraints[i]
        xi = board[irow][icol]
        xj = board[jrow][jcol]
        if xi.fixed and xj.fixed and xi.get_only_value() == xj.get_only_value():
            return constraints, False

        if xi.fixed:
            # Remove this constraint; don't update i
            constraints.pop(i)
        elif not xi.fixed:
            # update i
            i += 1

    return constraints, True



def final_constraints(board, constraints):
    """
    Purpose: When the board is finished, do a final check to see if any of
    the values are duplicates
    @param board  The Sudoku board: A list of lists of variable class instances
    @param constraints  The unallowed values for each cell, list of tuples
    """
    while constraints:
        ([irow, icol], [jrow, jcol]) = constraints.pop()
        xi = board[irow][icol]
        xj = board[jrow][jcol]
        if not xi.get_only_value() or not xj.get_only_value():
            return False
        if xi.get_only_value() == xj.get_only_value():
            return False

    return True



def get_all_constraints(max_domain_val):
    """
    Purpose: get all binary constraints of the form xi,xj and put them in
    a list. To save space, we just put the row and column indices in the
    list.
    @param max_domain_val  int, The dimensions of each side of the square board
    @return constraints  list of tuples containing 2 lists with 2 elements each:
                     [([xi_row, xi_col],[xj_row,xj_col]), ... ]

    A Sudoku board has 9 rows and 9 columns, and is divided into 3x3 boxes.
    For each cell (row & column), there are therefore:
        Constraints per cell:
            8 for the row
            8 for the column
            4 for the box
            ---------------
            20 constraints / cell

        There are 81 cells, so 81*20 = 1620 constraints total. Note that we
        only include 4 constraints for the box because we have already
        counted the other 4: 2 in the row and 2 in the column.

        We can also exclude any fixed cells from the list of constraints,
        since (1) we pre-check for consistency, ans (2) they cannot change.
        But we do that in another function, just to keep things simple.

    Notes:
        1) There are a lot of nested loops here. However, this code is only
           run once and it has to cover all squares. We could flatten the
           Sudoku board to a 1x81 array (instead of 9x9) but it's probably not
           worth the trouble.
    """

    constraints = []
    list_rows = range(max_domain_val)
    list_cols = range(max_domain_val)


    for irow in list_rows:
        for icol in list_cols:

            # .. Row: Add all column indices to row, except the variable's
            for jcol in range(max_domain_val):
                if jcol != icol:
                    constraints.append(([irow, icol], [irow, jcol]))

            # .. Column
            for jrow in range(max_domain_val):
                # Add all rows of this column, except the variable's column
                if jrow != irow:
                    constraints.append(([irow, icol], [jrow, icol]))

            # .. Box
            #    Add all row,column sets that share the box,
            #    except the variable's row, column
            #    and the ones that have already been one
            ibox_row = int(irow/3) * 3
            ibox_col = int(icol/3) * 3

            irows = list(range(ibox_row, irow)) + list(range(irow, ibox_row+3))
            icols = list(range(ibox_col, icol)) + list(range(icol, ibox_col+3))
            #irows = [i for i in range(ibox_row, irow)] \
            #         + [i for i in range(irow, ibox_row+3)]
            #icols = [i for i in range(ibox_col, icol)] \
            #         + [i for i in range(icol, ibox_col+3)]

            for jrow in irows:
                for jcol in icols:
                    if jrow != irow and jcol != icol:
                        constraints.append(([irow, icol], [jrow, jcol]))
    return constraints



def reverse_constraints(irow, icol, max_domain_val):
    """
    Get the reverse contraints
    @param irow  Index to row
    @param icol  Index to column
    @param max_domain_val  The dimensions of each side of the square board, int
    """
    xj_constraints = []


    # .. Row: Add all column indices to row, except the variable's
    for jcol in range(max_domain_val):
        if jcol != icol:
            xj_constraints.append(([irow, jcol], [irow, icol]))

    # .. Column
    for jrow in range(max_domain_val):
        # Add all rows of this column, except the variable's column
        if jrow != irow:
            xj_constraints.append(([jrow, icol], [irow, icol]))

    # .. Box
    #    Add all row,column sets that share the box,
    #    except the variable's row, column
    #    and the ones that have already been one
    ibox_row = int(irow/3) * 3
    ibox_col = int(icol/3) * 3

    irows = list(range(ibox_row, irow)) + list(range(irow, ibox_row+3))
    icols = list(range(ibox_col, icol)) + list(range(icol, ibox_col+3))

    for jrow in irows:
        for jcol in icols:
            if jrow != irow and jcol != icol:
                xj_constraints.append(([jrow, jcol], [irow, icol]))

    return xj_constraints
