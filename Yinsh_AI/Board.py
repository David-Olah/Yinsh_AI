'''
• This is the data structure, a 2D array, that holds the information about the board in integers.
    • 8 = nothingness, the board does not exist here, and it can be used to determine where the edges of the board are.
    • 0 = empty spaces that exist on the board.
    • 1/-1 = white/black markers respectively.
    • 2/-2 = white/black rings respectively.
'''

SIZE = 11 # An attempt at generalization which never got developed due to the complexity of the board.


class Board:
    def __init__(self):
        self.rows = SIZE
        self.cols = SIZE
        out_of_bounds_indicies = [
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 10),
            (1, 0), (1, 1), (1, 2), (1, 3),
            (2, 0), (2, 1), (2, 2), 
            (3, 0), (3, 1), 
            (4, 0), 
            (5, 0), (5, 10), 
            (6, 10), 
            (7, 9), (7, 10), 
            (8, 8), (8, 9), (8, 10), 
            (9, 7), (9, 8), (9, 9), (9, 10), 
            (10, 0), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10)
            ]
        self.data = [[8 if (i, j) in out_of_bounds_indicies else 0 for j in range(self.cols)] for i in range(self.rows)]



    def __getitem__(self, index):
        return self.data[index[0]][index[1]]
    
    def __setitem__(self, index, value):
        self.data[index[0]][index[1]] = value
    
    def __str__(self):
        return '\n'.join([' '.join([str(self.data[i][j]) for j in range(self.cols)]) for i in range(self.rows)])

    def __getdata__(self):
        return self.data

    def invert_values(self):
        inverted_data = [[0 for j in range(self.cols)] for i in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                if self[i, j] == 1:
                    inverted_data[i][j] = -1
                elif self[i, j] == -1:
                    inverted_data[i][j] = 1
                elif self[i, j] == 2:
                    inverted_data[i][j] = -2
                elif self[i, j] == -2:
                    inverted_data[i][j] = 2
                else:
                    inverted_data[i][j] = self[i, j]
        inverted_board = Board()
        inverted_board.data = inverted_data
        return inverted_board