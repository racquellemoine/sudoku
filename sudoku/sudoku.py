#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import copy

# for purposes of box org, have groupings of rows asnd cols per box
# boxes will be numbered as followed 
# 1 2 3
# 4 5 6
# 7 8 9
BOX1 = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]
BOX2 = ["A4", "A5", "A6", "B4", "B5", "B6", "C4", "C5", "C6"]
BOX3 = ["A7", "A8", "A9", "B7", "B8", "B9", "C7", "C8", "C9"]
BOX4 = ["D1", "D2", "D3", "E1", "E2", "E3", "F1", "F2", "F3"]
BOX5 = ["D4", "D5", "D6", "E4", "E5", "E6", "F4", "F5", "F6"]
BOX6 = ["D7", "D8", "D9", "E7", "E8", "E9", "F7", "F8", "F9"]
BOX7 = ["G1", "G2", "G3", "H1", "H2", "H3", "I1", "I2", "I3"]
BOX8 = ["G4", "G5", "G6", "H4", "H5", "H6", "I4", "I5", "I6"]
BOX9 = ["G7", "G8", "G9", "H7", "H8", "H9", "I7", "I8", "I9"]
BOXES = [BOX1, BOX2, BOX3, BOX4, BOX5, BOX6, BOX7, BOX8, BOX9]
ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)

def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def backtracking(board):
    # initialize domain with initial board values
    domains = __initDomains(board)
    return __backtrack(board, domains)

def __initDomains(board):
    domains = {}
    for r in ROW:
        for c in COL:
            slot = r+c
            # init empty domain or write in number
            if board[slot] == 0: domains[slot] = []
            else: domains[slot] = [board[slot]]
    return __fillDomains(board, domains)

def __fillDomains(board, domains):
    # add all possible candidates to domain
    for box in BOXES:
        for tile in box:
            if board[tile] == 0:
                domains[tile] = __getCandidates(tile, box, board)
    return domains  

def __getCandidates(tile, box, board):
    # helper to fillDomains()
    candidates = []
    row, col = tile[0], tile[1]
    for num in range(1,10):
        if not __isInBox(box, num, board) and not __isInRow(row, num, board) and not __isInCol(col, num, board):
            candidates.append(num)
    return candidates

def __backtrack(board, domains):
    # base case
    if __everyTileFilled(board): return board
    tile = __getUnassignedTile(board, domains)
    # if no more unassigned tiles
    if tile == None: return None
    for candidate in domains[tile]:
        if __isConsistent(candidate, tile, board):
            newDomains = __forwardChecking(tile, candidate, copy.deepcopy(domains))
            if newDomains == None: 
                # results in empty domain
                continue
            board[tile] = candidate
            result = __backtrack(board.copy(), newDomains)
            if __resultWorks(result): 
                return result
            # if result is not valid, back track tile
            board[tile] = 0

def __everyTileFilled(board) -> bool:
    # tells us if we are done filling board!
    for key in board:
        if board[key] == 0: return False
    return True

def __getUnassignedTile(board, domains):
    # use mrv to get unassigned tile
    for num in range(1,10):
        unassignedTile = __getDomainOfSize(num, domains, board)
        if unassignedTile is not None: return unassignedTile

def __getDomainOfSize(size, domains, board):
    # helper to getUnassignedTile()
    for box in BOXES:
        for tile in box:
            if len(domains[tile]) == size and board[tile] == 0: return tile
    return None  

def __isConsistent(candidate, tile, board) -> bool:
    # tells us if candidate creates inconsistencies in board if placed at tile
    box = __getBox(tile)
    return not __isInBox(box, candidate, board) and not __isInCol(tile[1], candidate, board) and not __isInRow(tile[0], candidate, board)

def __forwardChecking(assignedSlot, val, domains):
    # check box then row then column
    box = __getBox(assignedSlot)
    for tile in box:
        if tile == assignedSlot: continue
        if val in domains[tile]:
            if len(domains[tile]) == 1: return None
            domains[tile].remove(val)
    row, col = assignedSlot[0], assignedSlot[1]
    for c in COL:
        if row+c == assignedSlot: continue
        if val in domains[row+c]:
            if len(domains[row+c]) == 1: return None
            domains[row+c].remove(val)
    for r in ROW:
        if r+col == assignedSlot: continue
        if val in domains[r+col]:
            if len(domains[r+col]) == 1: return None
            domains[r+col].remove(val)
    return domains

def __resultWorks(result) -> bool:
    if result == None: 
        # back tracking did not produce result
        return False
    for box in BOXES:
        # check for duplicates in boxes
        if not __boxWorks(box, result): return False
    for col in COL:
        # check for duplicates in columns
        if not __colWorks(col, result): return False
    for row in ROW:
        # check for duplicates in rows
        if not __rowWorks(row, result): return False
    return True

def __boxWorks(box, result) -> bool:
    # check for duplicate in single box
    boxVals = []
    for tile in box: 
        boxVals.append(result[tile])
    for num in range(1,10):
        if boxVals.count(num) > 1: return False
    return True

def __colWorks(col, result) -> bool:
    # check for duplicate in single col
    column = []
    for r in ROW:
        column.append(result[r+col])
    for num in range(1,10):
        if column.count(num) > 1: return False
    return True

def __rowWorks(r, result) -> bool:
    # check for duplicate in single row
    row = []
    for c in COL:
        row.append(result[r+c])
    for num in range(1,10):
        if row.count(num) > 1: return False
    return True

def __getBox(tile):
    # returns box that tile belongs to 
    if tile in BOX1: return BOX1
    if tile in BOX2: return BOX2
    if tile in BOX3: return BOX3
    if tile in BOX4: return BOX4
    if tile in BOX5: return BOX5
    if tile in BOX6: return BOX6
    if tile in BOX7: return BOX7
    if tile in BOX8: return BOX8
    if tile in BOX9: return BOX9

def __isInBox(box, num, board) -> bool:
    # tells us if tile is in box
    for tile in box:
        if board[tile] == num: 
            return True

def __isInRow(row, num, board) -> bool:
    # tells us if tile is in row
    for c in COL:
        if board[row+c] == num: return True

def __isInCol(col, num, board) -> bool:
    # tells us if tile is in col
    for r in ROW:
        if board[r+col] == num: return True

if __name__ == '__main__':
    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
        
        solved_board = backtracking(board)
        
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            print_board(board)

            # Solve with backtracking
            solved_board = backtracking(board)

            # Print solved board. TODO: Comment this out when timing runs.
            print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        print("Finishing all boards in file.")
