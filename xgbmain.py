'''
• This program will train an XGBoost model.
• A pickled Library2D object is required. This can be obtained from elsewhere in this repo.
'''

import pickle
import numpy as np
from Library2D import *
from Board import *
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import xgboost as xgb



def main():
    
    # load the library
    with open('yinsh_library_2D.pkl', 'rb') as f:
        library_2D = pickle.load(f)
    
    X = []  # Features
    y = []  # Labels
    
    # Extract data from library
    for entry in library_2D.entries:
        board = entry['boardstate']
        outcome = 0 if entry['outcome'] == -1 else 1
        
        features = board_to_features(board)
        X.append(features)
        y.append(outcome)
    
    # Split the data for training
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the XGBoost model
    model = xgb.XGBClassifier()
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    # Save the trained model to a file
    with open('xgb_model.pkl', 'wb') as f:
        pickle.dump(model, f)
        
    # Load the saved model from a file (this is just done for testing and should be able to be safely removed)
    with open('xgb_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    # Make predictions for some test examples (this part is just for testing, and to show it working)
    for i in range(10):
        test_features = X_test[i]
        test_label = y_test[i]
        prediction = model.predict(test_features.reshape(1, -1))
        print(f"Example {i+1}: Predicted label {prediction}, actual label {test_label}")
        
    print("\n\n Final results: ", accuracy, "\n", precision, "\n", recall, "\n", f1)
        
        
def board_to_features(board):
    # Convert the board state to a feature vector
    return np.array(board.data).flatten()        

if __name__ == "__main__":
    main()

