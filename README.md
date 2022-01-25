# sudoku
<img src="./sudoku_easy_looping.gif?raw=true">

Sudoku solver using backtracking and AC-3.
Run from terminal using:

$ python sudoku.py puzzlefilename backtrack

Where 
- puzzlefilename is a file of type ../puzzles/\*.puzz. It is optional. If not included, an empty board or a default board will be used.
- backtrack indicates that backtracking alone should be used. It is also optional. If omitted, backtracking + AC-3 will be used.

Notes:
See solver.py for choice of implementation of method to get the next unassigned variable. Options include:
- Get the next value (get_next_unassigned)
- Use the Minimum Remaining Values heuristic (get_unassigned_using_mrv)
- Use the Minimum Remaining Values heuristic and the degree (get_unassigned_using_mrv_and_degree)

