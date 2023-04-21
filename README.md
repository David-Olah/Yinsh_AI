YinshPredict

A machine learning based boardstate analysis model that will predict which player will win a game of Yinsh.

This project is divided into 3 different programs, Main.py, xgbmain.py, and YinshPredict.py

Main.py:
This program is going to read all the game data text files, parse the lines within them, and create
various libraries of boardstates.

xgbmain.py:
This program will use the libraries from Main.py and train a XGBoost model, then test that model, and give back an
accuracy score, among other scores.

YinshPredict.py:
This program will do a similar thing to xgbmain.py, but will instead load a XGBoost model that has been previously trained,
such as the one trained and saved by xgbmain.py. This will also calculate and produce a chart of the model accuracy by turn.

Important note:
Inside of BoardCreator.py (currently on line 122), there is a directory that points to my local folder, so that has to be
editted if anyone wants to run this code.

Notes:
1. The game data text files are zipped and must first be unzipped.

2. The libraries could not be included on github as they were too large and could not be compressed. As such, you will have to
download and unzip the game files and run Main.py first to create those libraries before the model can be utilized.

2. The directory of game data text files was downloaded from the following website: http://boardspace.net/yinsh/yinshgames/

3. This code will function for all game data text files between 2006 - March 2023, so if you download your own set of
games, then they should be within that range, unless you are ready to do testing and making certain everything functions
correctly. Games in the 2005 folder (there is nothing earlier than this in the source directory) will not work. And
currently it is April 2023, and all testing was performed on files up until March (and some in  April). Since this website
has before and could update their formatting again, anything after March may not work.
