'''
• This program only uses an already trained XGBoost model and a Library2D object with Yinsh board states
to test the model upon the test set. It gives an accuracy and a graph, with options to uncomment code to
print more information.
• This program requires a pickled XGBoost model, and a pickled Library2D object from other parts of this repo.
• Some preprocessing is done. The random state used is is consistent with other times train/test splits are done.
'''

import pickle
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from Library2D import *
from Board import *
from xgbmain import *
from collections import defaultdict
import matplotlib.pyplot as plt
import xgboost as xgb

def main():
    # Load the model and library
    with open('xgb_model.pkl', 'rb') as f:
        model = pickle.load(f)
        
    with open('yinsh_library_2D.pkl', 'rb') as f:
        library_2D = pickle.load(f)

    X = []  # Features
    y = []  # Labels
    
    # Extract information from library
    for entry in library_2D.entries:
        board = entry['boardstate']
        outcome = 0 if entry['outcome'] == -1 else 1
        turn = entry['turn']
        
        features = board_to_features(board)
        X.append(features)
        y.append(outcome)

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Overall accuracy
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("\nOverall accuracy: ", accuracy)

    # Create a dictionary to store the results for each turn
    results_by_turn = defaultdict(dict)

    # Evaluate the model for each turn in the test set and store the results
    for i in range(len(X_test)):
        board = library_2D.entries[i]['boardstate']
        turn = library_2D.entries[i]['turn']
        prediction = model.predict(X_test[i].reshape(1, -1))
        outcome = y_test[i]

        # Store the prediction and outcome in the dictionary for this turn
        results_by_turn[turn]['predictions'] = results_by_turn[turn].get('predictions', []) + [prediction]
        results_by_turn[turn]['outcomes'] = results_by_turn[turn].get('outcomes', []) + [outcome]

    # Sort the results by turn in ascending order
    sorted_results = sorted(results_by_turn.items())
    
    # Evaluate the model for each turn in the test set and print the results
    for turn, results in sorted_results:
        predictions = np.array(results['predictions'])
        outcomes = np.array(results['outcomes'])
        accuracy = accuracy_score(outcomes, predictions)
        #precision = precision_score(outcomes, predictions)
        #recall = recall_score(outcomes, predictions)
        #f1 = f1_score(outcomes, predictions)

        # Print each result if you want
        #print(f"Results for turn {turn}:")
        #rint(f"Accuracy: {accuracy}")
        
        # Other printing options
        #print(f"Precision: {precision}")
        #print(f"Recall: {recall}")
        #print(f"F1 score: {f1}")
        #print()
        
    # Save the accuracy scores for each turn
    accuracies = [accuracy_score(np.array(results['outcomes']), np.array(results['predictions'])) for _, results in sorted_results]
    turns = [turn for turn, _ in sorted_results]

    # Create a line graph of the accuracy scores by turn
    plt.plot(turns, accuracies)
    plt.xlabel('Turn')
    plt.ylabel('Accuracy')
    plt.title('Accuracy by Turn')
    
    # Add a horizontal line at y=0.712
    plt.axhline(y=0.712, color='r', linestyle='--')
    
    plt.show()

if __name__ == "__main__":
    main()











'''
import pickle
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from Library2D import *
from Board import *
from xgbmain import *

import xgboost as xgb

def main():
    with open('xgb_model.pkl', 'rb') as f:
        model = pickle.load(f)
        
    with open('yinsh_library_2D.pkl', 'rb') as f:
        library_2D = pickle.load(f)
        
    X = []  # Features
    y = []  # Labels
    
    print("\nnew5")
    for entry in library_2D.entries:
        board = entry['boardstate']
        outcome = 0 if entry['outcome'] == -1 else 1
        
        features = board_to_features(board)
        X.append(features)
        y.append(outcome)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Print the results
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 score:", f1)

if __name__ == "__main__":
    main()
    '''
