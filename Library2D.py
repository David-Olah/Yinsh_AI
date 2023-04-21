'''
• This is the data structure that holds information about the board state and the boardstate itself.
• turn = turn number in a specific game.
• boardstate =  2d array of numbers that each represent something on the board.
    • 8 = nothingness, the board does not exist here, and it can be used to determine where the edges of the board are.
    • 0 = empty spaces that exist on the board.
    • 1/-1 = white/black markers respectively.
    • 2/-2 = white/black rings respectively.
• filename = name of the file this data was extracted from.
• outcome = which color/player won the game.
'''

import copy

class Library2D:
    def __init__(self):
        self.entries = []

    def add_entry(self, turn, boardstate, filename, outcome):
        new_entry = {'turn': turn, 'boardstate': copy.deepcopy(boardstate), 'filename': filename, 'outcome': outcome}
        self.entries.append(new_entry)

    def print_boardstates(self):
        for entry in self.entries:
            print(f"Boardstate for {entry['filename']}:")
            print(entry['boardstate'])

    def print_boardstate(self, index):
        if index >= len(self.entries):
            print(f"Index {index} out of range")
        else:
            entry = self.entries[index]
            print(f"Boardstate for entry {index}:")
            print(entry['boardstate'])