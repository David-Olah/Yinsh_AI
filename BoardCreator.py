'''
• This will create and edit the boardstate, and save that boardstate along with other information to the library.
• The way in which the proper boardstate is determined is incredibly convoluted due to the variable nature of the format of the
game data text files. All different formats are accounted for, as such there are a lot of checks to make sure the correct
action is taken. There are a number of checks for errors, and the code now runs on all 2006-2023 March files without error.
• If any edits are made to this code it is highly recommended that the game data text files are extensively researched, and
that any error messages are investigated immediately, because sometimes certain formats which cause issues only arise a few times
in all the thousands of games.
• Generally speaking there are 8 situations:
    • "done" = this signifies the end of an action.
        • Sometimes this means that an action is done, so previous action information can be saved, and a new action 
        will be starting that could be part of the same turn.
        • sometimes this means previous set of action information can be entered into a board state and saved as a library entry as
        this is the end of a turn.
    • "move" = this line will hold information about which piece is being moved, the color, from where, and to where. A "move" is a very
    convenient way of conveying a whole turn in a single line (other than the "done" line), so some other types of situations will be
    converted into a "move" format for simplicity.
    • "drop" = indicates that a ring was placed, or "dropped" onto the board. This ring was picked up from a location denoted on the 
    previous "place" line. This is part of what becomes a "move" formatted action.
    • "remove" = indicates that either a ring or a set of 5 markers was removed from the board.
    • "place" = indicates the location that a marker is placed into a ring, and where that ring is then picked up from. This is 
    always followed by a "drop" line. This is part of what becomes a "move" formatted action.
    • "end" = signifies the end of the game.
    • "resign" = when a game ends in a resignation.
    • "skip" = there are a lot of worthless lines of information in the game data text files which are ignored, or skipped over.
'''

import os
from pathlib import Path
from Board import *
from GameData import *
from Library2D import *
import chardet


class BoardCreator:

    def _convert_to_2d_array_coords(number_coord, letter_coord):
        x_coord = abs(number_coord - 11)
        y_coord = ord(letter_coord) - 65
        return x_coord, y_coord

    def _get_2d_array_coords_between(fx, fy, sx, sy):

        between_coordinates = []
        number_of_spaces_between = max((abs(fx - sx) - 1), (abs(fy - sy) - 1))

        # Vertical lines.
        if fx != sx and fy == sy:
            if fx < sx:
                for i in range(number_of_spaces_between):
                    between_coordinates.append((fx + i + 1, fy))
            else:
                for i in range(number_of_spaces_between):
                    between_coordinates.append((fx - i - 1, fy))
        # Horizontal lines.
        elif fx == sx and fy != sy:
            if fy < sy:
                for i in range(number_of_spaces_between):
                    between_coordinates.append((fx, fy + i + 1))
            else:
                for i in range(number_of_spaces_between):
                    between_coordinates.append((fx, fy - i - 1))
        # Diagonal lines.
        elif fx < sx and fy < sy:
            for i in range(number_of_spaces_between):
                    between_coordinates.append((fx + i + 1, fy + i + 1))
        elif fx < sx and fy > sy:
            for i in range(number_of_spaces_between):
                    between_coordinates.append((fx + i + 1, fy - i - 1))
        elif fx > sx and fy < sy:
            for i in range(number_of_spaces_between):
                    between_coordinates.append((fx - i  - 1, fy + i + 1))
        elif fx > sx and fy > sy:
            for i in range(number_of_spaces_between):
                    between_coordinates.append((fx - i - 1, fy - i - 1))
        
        return between_coordinates
        
    # Winner is being found by looking at which player made the last move by finding the last "done" line.
    # A resign is found in two ways, if there is a "resign" line, or if there are 2 "done" lines in a row by the same player.
    def _find_winner(root, file):
        first_done_found = False
        
        with open(os.path.join(root, file), 'rb') as f:
            content = f.read()
            encoding = chardet.detect(content)['encoding']

        with open(os.path.join(root, file), "r", encoding=encoding) as f:
            content = f.read() # read entire file into memory
            lines = content.splitlines() # split into lines
            
            for line in reversed(lines): # iterate through lines in reverse order
                if 'resign' in line.lower():
                    return 0
                elif 'done' in line.lower():
                    if first_done_found:
                        return 0
                    first_done_found = True
                elif 'remove br' in line.lower():
                    return -1
                elif 'remove wr' in line.lower():
                    return 1
            
        return -100

    def _invert_outcome(outcome):
        if outcome == 0:
            return 0
        elif outcome == 1:
            return -1
        elif outcome == -1:
            return 1
        else:
            print("ERROR IN _invert_outcome")


    @classmethod
    def populate_library(cls, library, library_ties):

        # The directory will have to be changed if you want this code to run on your computer
        directory = 'C:/Users/David\YINSH_AI_Project/Yinsh_AI/YinshGames/'
        for root, dirs, files in os.walk(directory):
            for file in files:
                filename = os.path.basename(file)
                if 'B' not in filename[:4]:
                    outcome = cls._find_winner(root, file)
                    turn_counter  = 0
                    skip_next_done = False
                    type_of_change = None
                    start_piece = 0
                    end_piece = 0
                    board = Board()
                    with open(os.path.join(root, file), 'rb') as f:
                        content = f.read()
                        encoding = chardet.detect(content)['encoding']
                    f = open(os.path.join(root, file), "r", encoding = encoding)
                    for next_line in f:
                        line = Line(next_line)                        
                        
                        if line.move == "place":
                            skip_next_done = False
                            if line.piece == "marker":
                                type_of_change = "move"
                                first_coord_letter = line.coord[0]
                                first_coord_number = line.coord[1]
                                if line.color == "white":
                                    start_piece = 1
                                elif line.color == "black":
                                    start_piece = -1
                                else:
                                    print("ERROR IN PLACE>MARKER")
                            elif line.piece == "ring":
                                type_of_change = "place ring"
                                first_coord_letter = line.coord[0]
                                first_coord_number = line.coord[1]
                                if line.color == "white":
                                    start_piece = 2
                                elif line.color == "black":
                                    start_piece = -2
                                else:
                                    print("ERROR IN PLACE>RING")
                            else:
                                print("ERROR IN PLACE")

                        elif line.move == "drop":
                            skip_next_done = False
                            second_coord_letter = line.coord[0]
                            second_coord_number = line.coord[1]
                            if line.color == "white":
                                end_piece = 2
                            elif line.color == "black":
                                end_piece = -2
                            else:
                                print("ERROR IN DROP")

                        elif line.move == "move":
                            skip_next_done = False
                            type_of_change = "move"
                            first_coord_letter = line.coord[0]
                            first_coord_number = line.coord[1]
                            second_coord_letter = line.second_coord[0]
                            second_coord_number = line.second_coord[1]
                            if line.color == "white":
                                start_piece = 1
                                end_piece = 2
                            elif line.color == "black":
                                start_piece = -1
                                end_piece = -2
                            else:
                                print("ERROR IN MOVE")

                        elif line.move == "remove":
                            skip_next_done = False
                            first_coord_letter = line.coord[0]
                            first_coord_number = line.coord[1]
                            if line.piece == "ring":
                                type_of_change = "remove ring"
                            elif line.piece == "marker":
                                type_of_change = "remove markers"
                                second_coord_letter = line.second_coord[0]
                                second_coord_number = line.second_coord[1]
                            else:
                                print("ERROR IN REMOVE")

                        elif line.move == "done" and not skip_next_done:
                            if type_of_change == "move":
                                first_xcoord, first_ycoord = cls._convert_to_2d_array_coords(first_coord_number, first_coord_letter)
                                second_xcoord, second_ycoord = cls._convert_to_2d_array_coords(second_coord_number, second_coord_letter)
                                board[first_xcoord, first_ycoord] = start_piece
                                board[second_xcoord, second_ycoord] = end_piece

                                # Flip all markers between those two points
                                between_coords = cls._get_2d_array_coords_between(first_xcoord, first_ycoord, second_xcoord, second_ycoord)
                                for x, y in between_coords:
                                    if board[x, y] == 1:
                                        board[x, y] = -1
                                    elif board[x, y] == -1:
                                        board[x, y] = 1
                                
                            elif type_of_change == "place ring":
                                first_xcoord, first_ycoord = cls._convert_to_2d_array_coords(first_coord_number, first_coord_letter)
                                board[first_xcoord, first_ycoord] = start_piece
                            elif type_of_change == "remove ring":
                                first_xcoord, first_ycoord = cls._convert_to_2d_array_coords(first_coord_number, first_coord_letter)
                                board[first_xcoord, first_ycoord] = 0
                            elif type_of_change == "remove markers":
                                first_xcoord, first_ycoord = cls._convert_to_2d_array_coords(first_coord_number, first_coord_letter)
                                second_xcoord, second_ycoord = cls._convert_to_2d_array_coords(second_coord_number, second_coord_letter)
                                board[first_xcoord, first_ycoord] = 0
                                board[second_xcoord, second_ycoord] = 0
                                
                                # remove all markers between those two coordinates
                                between_coords = cls._get_2d_array_coords_between(first_xcoord, first_ycoord, second_xcoord, second_ycoord)
                                for x, y in between_coords:
                                    board[x, y] = 0
                            else:
                                print(file)
                                print(turn_counter)
                                print("ERROR IN DONE")
                                print(type_of_change)

                            turn_counter += 1
                            
                            if type_of_change != None and type_of_change != "remove markers":
                                if outcome == 0:
                                    library_ties.add_entry(turn_counter, board, filename, outcome)
                                    library_ties.add_entry(turn_counter, board.invert_values(), filename, outcome)
                                else:
                                    library.add_entry(turn_counter, board, filename, outcome)
                                    library.add_entry(turn_counter, board.invert_values(), filename, cls._invert_outcome(outcome))
                                    
                                type_of_change = None
                                start_piece = 0
                                end_piece = 0
                        
                        elif line.move == "resign":
                            skip_next_done = True

        return library, library_ties
