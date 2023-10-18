#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys

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
    """Takes a board and returns solved board."""
    # initialize domain to keep track of possible solutions for a slot
    domains = __initDomains()
    # first look at other slots in same box
    for box in BOXES:
        for slot in box:
            # if slot is already assigned a val, continue
            if board[slot] != 0: continue
            # parse missing nums in box
            for num in __missingNums(box, board):
                # if num does not violate constraints for row and col add to domain of slot
                if __isValidRow(slot[0], board, num) and __isValidCol(slot[1], board, num):   
                    domains[slot].append(num)
        # check all slots in box again
        # if only 1 possible val in domain, write it in and forward check
        # after forward checking backtrack board again
        for slot in box:
            if len(domains[slot]) == 1 and board[slot] == 0:
                board[slot] = domains[slot][0]
                __forwardChecking(box, slot, board[slot], domains)
                backtracking(board)
    board, domains = __tryTwos(domains, board)
    #__mrv(domains, board)
    # after we write in all slots that have 1 possible val we need to try and fill other slots using mrv heuristic

    return board

def __tryTwos(domains, board):
    for box in BOXES:
        for slot in box:
            if len(domains[slot]) == 2:
                print("domain of ", slot, ": ", domains[slot])
                for candidate in domains[slot]:
                    print("trying ", candidate)
                    candidateWorks = __candidateWorks(candidate, slot, board.copy(), box, domains.copy())
                    print("domain: ", domains[slot])
                    #if candidateWorks is not None:
                        #board, domains = candidateWorks
                        #break
    return  board, domains

def __candidateWorks(candidate, slot, board, box, domains):
    

def __initDomains():
    domains = {}
    for i in ROW:
        for j in COL:
            slot = i+j
            # init empty domain 
            if board[slot] == 0: 
                domains[slot] = []
            # add val to domain
            else:
                domains[slot] = [board[slot]]
    return domains

def __missingNums(box, board):
    # return nums that box is missing
    nums = []
    for slot in box:
        nums.append(board[slot])
    missingNums = []
    for num in range(1,10):
        if num not in nums:
            missingNums.append(num)
    return missingNums

def __isValidRow(rowNum, board, candidate) -> bool:
    row = []
    for i in COL:
        row.append(board[rowNum+i])
    if candidate in row: return False
    return True

def __isValidCol(colNum, board, candidate) -> bool:
    col = []
    for i in ROW:
        col.append(board[i+colNum])
    if candidate in col: return False
    return True

def isSolution(board):
    if not __checkRows(board): return False
    if not __checkCols(board): return False
    if not __checkBoxes(board): return False
    return True

def __checkRows(board) -> bool:
    for i in ROW: 
        row = []
        for j in COL:
            row.append(board[i+j])
        if not __checkRow(row): 
            print("row is WRONG")
            print(row)
            return False
    return True
        
def __checkRow(row) -> bool:
    for num in range(1,10):
        if num not in row: 
            print(num, " not in row")
            return False
    return True

def __checkCols(board) -> bool:
    for i in COL:
        col = []
        for j in ROW:
            col.append(board[j+i])
        if not __checkCol(col): 
            print("col is WRONG")
            print(col)
            return False
    return True

def __checkCol(col) -> bool:
    for num in range(1,10):
        if num not in col: return False
    return True

def __checkBoxes(board) -> bool:
    vals = []
    for box in BOXES:
        for slot in box:
            vals.append(board[slot])
        for num in range(1,10):
            if num not in vals: 
                print(num, " not in box ", box)
                return False
    return True

def __forwardChecking(box, assignedSlot, val, domains):
    # check box for inconsistencies
    for slot in box:
        if val in domains[slot]:
            if len(domains[slot]) == 1:
                return False
            domains[slot].remove(val)
    row = assignedSlot[0]
    col = assignedSlot[1]
    # check row for inconsistencies
    for i in COL:
        slot = row+i
        if val in domains[slot]:
            if len(domains[slot]) == 1:
                return False
            domains[slot].remove(val)
    # check col for inconsistencies
    for j in ROW:
        slot = j+col
        if val in domains[slot]:
            if len(domains[slot]) == 1:
                return False
            domains[slot].remove(val)
    return True

if __name__ == '__main__':
    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
        print("starter board")
        print_board(board)
        solved_board = backtracking(board)
        if isSolution(board): print("YAY SOLUTION")
        else: print("returning wrong solution...")
        print_board(solved_board)
        
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
            if isSolution(board): print("YAY SOLUTION")
            else: print("returning wrong solution...")

            # Print solved board. TODO: Comment this out when timing runs.
            print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        print("Finishing all boards in file.")