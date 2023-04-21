'''
• Parses a given line using a complex and convoluted set of rules that take into account the variable ways
in which the game data text files are formatted. Then returns the specifics in a Line object which is then
decoded by the caller.
'''

class Line:
    def __init__(self, line: str):
        self.color = None
        self.piece = None
        self.coord = None
        self.second_coord = None
        self.parse_line(line)

    def parse_line(self, data: str):
        if data.lower().find(" done") != -1:
            move_name = " done"
            self.move = "done"
        elif data.lower().find(" move") != -1:
            move_name = " move"
        elif data.lower().find("[move") != -1:
            move_name = "[move"
        elif data.lower().find(" drop board") != -1:
            move_name = " drop"
        elif data.lower().find(" remove") != -1:
            move_name = " remove"
        elif data.lower().find(" place") != -1:
            move_name = " place"
        elif data.find(")") != -1:
            move_name = " end"
            self.move = "end"
        elif data.lower().find(" resign") != -1:
            move_name = " resign"
            self.move = "resign"
        else:
            move_name = " skip"
            self.move = "skip"
            
        if move_name != " done" and move_name != " skip" and move_name != " RE" and move_name != " end" and move_name != " whiteplayer" and move_name != " resign":
            # get color
            if data.find("P0") != -1:
                self.color = "white"
            else:
                self.color = "black"

            # remove the data and the extra space before the move name
            data = data[data.find(move_name) + 1::]
            # remove the ending bracket and everything after it
            data = data[:data.find("]"):]

            # split at the double space (will make a list with one thing in it if there's no double space)
            data = data.split("  ")

            # if we actually split at the double space (drop or place)
            if len(data) == 2:
                # set the move to the first part of the first half of the data
                self.move = data[0].split(" ")[0]

                # set the piece to a marker if the color is only one character, else ring
                self.piece = "marker" if len(data[0].split(" ")[1]) == 1 else "ring"

                # creates a list "coord" with the letter as the first item and the int position as the second item
                self.coord = [data[1].split(" ")[0], int(data[1].split(" ")[1])]

            # if we didn't (move or remove)
            else:
                # split up all the data
                data = data[0].split(" ")

                # first item is the move
                self.move = data[0]
                
                # check marker
                self.piece = "marker" if len(data[1]) == 1 else "ring"
                if self.move == "move":
                    # a move is always a ring
                    self.piece = "ring"
                    # set the first coord
                    self.coord = [data[1], int(data[2])]
                    # set the second coord
                    self.second_coord = [data[3], int(data[4])]
                elif self.piece == "marker":
                    # set the first coord
                    self.coord = [data[2], int(data[3])]
                    # set the second coord
                    self.second_coord = [data[4], int(data[5])]
                else:
                    # only one coord
                    self.coord = [data[2], int(data[3])]
                    
    # overriding the print value when the object is printed
    def __str__(self):
        return f"{self.move} {self.color} {self.piece} {self.coord} {self.second_coord}"
