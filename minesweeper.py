import os
from random import randint
###### Some Game DETAILS #######################################################
# Game levels:
#-Beginner – 9 * 9 Board and 10 Mines
# -Intermediate – 16 * 16 Board and 40 Mines
# -Advanced – 24 * 24 Board and 99 Mines
#
# Probability of finding a mine:
# -Beginner  level –  10/81 (0.12)
# -Intermediate level – 40/256 (0.15)
# -Advanced level – 99 / 576 (0.17)
################################################################################
# Length and width of the square row and column
# row - rows, column - columns
# mines - number of bombs
# starting point of the player 0<= startX < n, 0<= startY < m
dict_t = {"1":(9,9,10),"2":(16,16,40), "3":(24,24,99)}
set_up_value = 0
indexX,indexY = 0,0
print("WELCOME TO A GAME")
print("Please choose level of the game: 1 - Beginner (9x9, 10 mines), 2 - Intermedaite (16x16, 40 mines), 3 - Advanced (24x24, 99 mines)")
while set_up_value == 0:
    set_up_value = input()
    if set_up_value.lower() == "q":
        print('GOODBYE. We will BATLE again!')
        exit()
    else:
        if set_up_value in ['1','2','3']:
            break
        else:
            print("You have entered wrong value. Try again: ",end="")
            set_up_value = 0

row,column= dict_t[set_up_value][0],dict_t[set_up_value][1]
mines = dict_t[set_up_value][2]
mine_list = [] # Needed in case game is lost to reveal of mines on a table
# Creating original [GAME BOARD], and players [GAME BOARD]
# Original table board is board to check player choices
# Player board, to display players board
original_board_table = [["O" for x in range(column)] for acc in range(row)]
player_board_table = [["-" for x in range(column)] for acc in range(row)]

### POPULATING BOARD WITH BOMBS ###
def populate_table_with_mines(table, mine, row, column):
    mine_l = []
    while mine != 0:
        x, y = randint(0,row-1), randint(0, column-1)
        if table[x][y] == "O":
          table[x][y] = "X"
          mine_l.append((x,y))
          mine -= 1
        else:
          continue
    return table, mine_l

### Checking if indexes of rows and columns are valid ###
def is_values_valid(indexX, indexY):
    return 0 <= indexX <= row-1 and 0 <= indexY <= column-1


### Returning VALUE OF THE SQUARE after checking it previouse value ###
# Using in another function to populate the numbers on a board
def return_table_index_value(table, indX, indY):
    if isinstance(table[indX][indY], int):
        return table[indX][indY] + 1
    elif table[indX][indY] == "O":
        return 1
    else:
        return table[indX][indY]

### Populating TABLE BOARD with MINES ###
def populate_table_with_numbers(table, row, column):
    for accX in range(row):
        for accY in range(column):
            if is_values_valid(accX, accY) and table[accX][accY] == "X":
            # Top
                if is_values_valid(accX-1, accY):
                  table[accX-1][accY] = return_table_index_value(table, accX-1, accY)
                # right-Top
                if is_values_valid(accX-1, accY+1):
                  table[accX-1][accY+1] = return_table_index_value(table, accX-1, accY+1)
                # right
                if is_values_valid(accX, accY+1):
                  table[accX][accY+1] = return_table_index_value(table, accX, accY+1)
                # right-Bottom
                if is_values_valid(accX+1, accY+1):
                  table[accX+1][accY+1] = return_table_index_value(table, accX+1, accY+1)
                # Bottom
                if is_values_valid(accX+1, accY):
                  table[accX+1][accY] = return_table_index_value(table, accX+1, accY)
                # left-Bottom
                if is_values_valid(accX+1, accY-1):
                  table[accX+1][accY-1] = return_table_index_value(table, accX+1, accY-1)
                # left
                if is_values_valid(accX, accY-1):
                  table[accX][accY-1] = return_table_index_value(table, accX, accY-1)
                # left-Top
                if is_values_valid(accX-1, accY-1):
                  table[accX-1][accY-1] = return_table_index_value(table, accX-1, accY-1)
    return table

### Edit TABLE BOARD if bomb is on a first try ###
def edit_table_if_mine_is_on_first_try(table, rowx, columny, row, column):
    for accx in range(row):
        for accy in range(column):
            if table[accx][accy] != "X":
                table[accx][accy] = "X"
                table[rowx][columny] = "O"
                return table, (accx,accy)

### Printing the table ###
def print_board(board_table, row, column):
    counter = 0
    print(f'{"":-^{column*3+column+5}}')
    print(f'{"Nr.":^5}', end='')
    for i in range(row):
         print(f'{i:^4}', end='')
    print()
    print(f'{"":-^{column*3+column+5}}')
    for acc in board_table:
        print(f'{counter:^4}|', end='')
        counter += 1
        for val in acc:
            print(f"{val:^3}|",end="")
        print()
    print()

# xx = '\u2588'
# for accx in range(10):
#     for accy in range(10):
#         print(f"{xx:^2}",end="")
#     print()
# ^^^^^^^^^^^^^^^^ Above code should be deleted after bottom implementation

### GETTING indexes of SQUARES TO OPEN and put in a player table ###
def return_paths(table, indexX, indexY):
    to_go_list = []
    no_go_further_list = []
    # Checking all nine sqaures if choisen index is not equal "1", if it is equal to "1"
    # simply return that value and no go search further
    if is_values_valid(indexX,indexY):
        if isinstance(table[indexX][indexY], int) or table[indexX][indexY] == "X":
            no_go_further_list.append((indexX,indexY))
            return no_go_further_list, to_go_list
        else:
            # Top
            if is_values_valid(indexX-1,indexY):
                if table[indexX-1][indexY] == "O":
                    to_go_list.append((indexX-1,indexY))
                else:
                    no_go_further_list.append((indexX-1,indexY))
            # Right
            if is_values_valid(indexX,indexY+1):
                if table[indexX][indexY+1] == "O":
                    to_go_list.append((indexX,indexY+1))
                else:
                    no_go_further_list.append((indexX,indexY+1))
            # Bottom
            if is_values_valid(indexX+1,indexY):
                if table[indexX+1][indexY] == "O":
                    to_go_list.append((indexX+1,indexY))
                else:
                    no_go_further_list.append((indexX+1,indexY))
            # Left
            if is_values_valid(indexX,indexY-1):
                if table[indexX][indexY-1] == "O":
                    to_go_list.append((indexX,indexY-1))
                else:
                    no_go_further_list.append((indexX,indexY-1))
            # right-Top
            if is_values_valid(indexX-1,indexY+1):
                if table[indexX-1][indexY+1] == "O":
                    to_go_list.append((indexX-1,indexY+1))
                else:
                    no_go_further_list.append((indexX-1,indexY+1))
            # right-Bottom
            if is_values_valid(indexX+1,indexY+1):
                if table[indexX+1][indexY+1] == "O":
                    to_go_list.append((indexX+1,indexY+1))
                else:
                    no_go_further_list.append((indexX+1,indexY+1))
            # left-Bottom
            if is_values_valid(indexX+1,indexY-1):
                if table[indexX+1][indexY-1] == "O":
                    to_go_list.append((indexX+1,indexY-1))
                else:
                    no_go_further_list.append((indexX+1,indexY-1))
            # left-Top
            if is_values_valid(indexX-1,indexY-1):
                if table[indexX-1][indexY-1] == "O":
                    to_go_list.append((indexX-1,indexY-1))
                else:
                    no_go_further_list.append((indexX-1,indexY-1))
            return no_go_further_list, to_go_list
    else:
        return no_go_further_list, to_go_list

### REVEAL PLAYERS TABLE SQUARES ###
def reveal_players_table(table_g, table_p, f_list):
    # print(len(f_list))
    for acc in f_list:
        table_g[acc[0]][acc[1]] = table_p[acc[0]][acc[1]]
    return table_g

## Number of not revealed squares ##
def not_revealed_squares(table):
    counter = 0
    for acc in table:
        counter += acc.count("-")
    return counter

# Reavealign MINES if game is lost, or if game is ended
def reveal_mines_on_loose(table_p, table_g, mine_l):
    for acc in mine_l:
        table_p[acc[0]][acc[1]] = table_g[acc[0]][acc[1]]
    return table_p

# Get Values from the user
def get_indexes_from_user():
    while True:
        indexX = input(f"Enter ROW Value [0,{row-1}]: ")
        if indexX.lower() == "q":
            print('GOODBYE. We will BATLE again!')
            exit()
        elif indexX.isdigit() and is_values_valid(int(indexX),0):
            indexX = int(indexX)
        else:
            print(f"Entered value {indexX} does not fit requested internal for rows and columns. Try again")
            continue

        indexY = input(f"Enter COLUMN Value [0,{column-1}]: ")
        if indexY.lower() == "q":
            print('GOODBYE. We will BATLE again!')
            exit()
        elif indexY.isdigit() and is_values_valid(0,int(indexY)):
            indexY = int(indexY)
            return indexX,indexY
        else:
            print(f"Entered value {indexX} does not fit requested internal for rows and columns. Try again")
            continue


################################ GAME STARTING #################################
# os.system("cls") # Clear Screen in windows terminal not so much working with ATOM

print("GAME STARTED PRINTING A TABLE:")

## Preparation for the first player move and EDITING ORIGINAL BOARD IF NEEDED
original_board_table, mine_list = populate_table_with_mines(original_board_table, mines, row, column)
print("Number of not revealed squares: ", not_revealed_squares(player_board_table), "Number of mines in the game: ", mines)
print_board(player_board_table, row, column)
indexX,indexY = get_indexes_from_user()

# os.system('clear')
if is_values_valid(indexX, indexY):
    if original_board_table[indexX][indexY] == "X":
        print("Changed:")
        original_board_table, tuple_x = edit_table_if_mine_is_on_first_try(original_board_table, indexX, indexY, row, column)
        original_board_table = populate_table_with_numbers(original_board_table, row, column)
        mine_list.remove((indexX,indexY))
        mine_list.append(tuple_x)
    else:
        print("NOT Changed")
        original_board_table = populate_table_with_numbers(original_board_table, row, column)

## Game continues after the first move
full_list = []
end_game = False
while True:
    if is_values_valid(indexX, indexY):
        full_list.extend([(indexX, indexY)])
        temp_f, temp_g = return_paths(original_board_table,indexX, indexY)
        full_list.extend(temp_f)
        if (len(temp_g)==0):
            full_list = list(set(full_list))
            set_for = full_list[0]
            if original_board_table[set_for[0]][set_for[1]] == "X":
                end_game = True
        else:
            while len(temp_g) != 0:
                for acc in temp_g:
                    if acc not in full_list:
                        full_list.append(acc)
                        temp_g.remove(acc)
                        temp_f, temp_gf = return_paths(original_board_table,acc[0], acc[1])
                        full_list.extend(temp_f)
                        temp_g.extend(temp_gf)
                    else:
                        temp_g.remove(acc)

            full_list = list(set(full_list))
        # os.system('clc')
        player_board_table = reveal_players_table(player_board_table, original_board_table, full_list)
        print("Number of not revealed squares: ", not_revealed_squares(player_board_table), "Number of mines in the game: ", mines)
        print_board(player_board_table, row, column)
        full_list = []
        if end_game:
            print("Number of not revealed squares: ", not_revealed_squares(player_board_table), "Number of mines in the game: ", mines)
            player_board_table = reveal_mines_on_loose(player_board_table,original_board_table,mine_list)
            print_board(player_board_table,row,column)
            print("## You have LOST. Better luck next time")
            break
        elif not_revealed_squares(player_board_table) == mines:
            print("## Congratulations! You have WON the game.")
            break
        indexX,indexY = get_indexes_from_user()
