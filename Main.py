'''
This program will traverse through a directory (found in BoardCreator.py), folder by folder, file by file, reading in and parsing the
game data in order to populate the libraries.
'''

from Board import *
from BoardCreator import *
from GameData import *
from pathlib import Path
import os
from Library2D import *
import numpy as np
import pickle


# Main function.
def main():

    empty_library = Library2D()
    empty_library_ties = Library2D()
    yinsh_library_2D, yinsh_library_2D_ties = BoardCreator.populate_library(empty_library, empty_library_ties)

    yinsh_library_1D = {}
    BS_counter = 0 # Board state counter

    for i, entry in enumerate(yinsh_library_2D.entries):
        # flatten the 2D array
        flattened_array = np.array(entry['boardstate'].data).flatten()
        # create a new dictionary entry for the flattened array and add it to the new library
        new_entry = {'turn': entry['turn'], 'boardstate': flattened_array, 'filename': entry['filename'], 'outcome': entry['outcome']}
        yinsh_library_1D[i] = new_entry
        BS_counter += 1
        
    yinsh_library_1D_ties = {}
    BS_ties_counter = 0
        
    for i, entry in enumerate(yinsh_library_2D_ties.entries):
        # flatten the 2D array of ties
        flattened_array = np.array(entry['boardstate'].data).flatten()
        # create a new dictionary entry for the flattened array and add it to the new library
        new_entry = {'turn': entry['turn'], 'boardstate': flattened_array, 'filename': entry['filename'], 'outcome': entry['outcome']}
        yinsh_library_1D_ties[i] = new_entry
        BS_ties_counter += 1

    # Pickle all the different libraries
    with open('yinsh_library_1D.pkl', 'wb') as f:
        pickle.dump(yinsh_library_1D, f)

    with open('yinsh_library_2D.pkl', 'wb') as f:
        pickle.dump(yinsh_library_2D, f)
        
    with open('yinsh_library_1D_ties.pkl', 'wb') as f:
        pickle.dump(yinsh_library_1D_ties, f)

    with open('yinsh_library_2D_ties.pkl', 'wb') as f:
        pickle.dump(yinsh_library_2D_ties, f)
    
    print("\n\n", BS_counter, "\n\n", BS_ties_counter)
    
if __name__ == "__main__":
    main()