#include <iostream>
#include <iomanip>
#include <cstdlib>
#include <ctime>
#include <string>
#include <fstream>
using namespace std;


// this game is a fictional board game our teacher came up with

// variables
typedef enum { Normal, Goose, Bridge, Well, Inn, Maze, Dice, Jail, Death } tBox;
const int DIM = 63, PLAYERS = 4, MATCHES = 3, PENALTY_INN = 1, PENALTY_JAIL = 2, PENALTY_WELL = 3;
typedef tBox tBoard[DIM];

// structure types
struct tPlayer {
   int currentBox, turnsToSkip;
};

typedef tPlayer playerArray[PLAYERS];

struct tPlayers {
   int numberOfPlayers;
   playerArray playersInfo;
};

struct tMatch { // numberOfPlayers max 4
   tBoard board;
   bool debugMode;
   int numberOfPlayers, nextPlayer;
   tPlayers playersState;
};

typedef tMatch matchesInfo[MATCHES];

struct tMatches {
    matchesInfo matches; 
    int counter = 0;
};

// prototypes
void nextGoose(const tBoard board, int& position);
int randomDie();
int manualDie();
int whoStarts(int numOfPlayers);
void checkSpecial(tMatch& match);
void checkTurns(tMatch& match);
void changeTurn(tMatch& match);
int getPlayer(const tMatch& match);
tBox stringToBox(string id);
string boxToString(tBox box);
void pause();
void printBoard(const tMatch& match);
bool load(tBoard board, ifstream& file);
void load(tMatches& listOfMatches);
int match(tMatch& match);
void play(tMatch& match);
bool playAgain(const tBoard board, int box);
int nextBox(const tBoard board, int box);
void searchPair(const tBoard board, tBox kind, int& position);
int selectMatch(const tMatches& listOfMatches);
void removeMatch(tMatches& listOfMatches, int index); 
void addMatch(tMatches& listOfMatches, tMatch match);
void loadListOfMatches(tMatches& listOfMatches);

int main() {
    srand(time(NULL)); // seed
    tMatches listOfMatches;
    tMatch matchToPlay;
    tBoard board;
    string fileName;
    bool correctMatch = false, isOpen;
    char choiceSaved, choiceDebug;
    int chosenMatch, numberPlayers, winner, nextPlayerGame;
    
    // ask user if he wants to continue an interrupted game or start a new one
    cout << "(N)ew match or (S)aved match? ";
    cin >> choiceSaved;
    choiceSaved = toupper(choiceSaved);

    // either way, we will need the number of interrupted games so far; we will store it in listOfMatches.counter
    ifstream file3;
    int numberMatches;
    file3.open("matches.txt");
    if(file3.is_open()) {
        file3 >> numberMatches;
        file3.close();
    } 
    if(numberMatches <= 0) {
        listOfMatches.counter = 0;
    } else {
        listOfMatches.counter = numberMatches;
    }

    // if user wants to continue with an interrupted game
    if(choiceSaved == 'S') {
        // only let user continue if there are interrupted games to continue
        if(numberMatches > 0) {
            load(listOfMatches);
            chosenMatch = selectMatch(listOfMatches); // returns index of match chosen
            printBoard(listOfMatches.matches[chosenMatch]); // print board of chosen match
            matchToPlay = listOfMatches.matches[chosenMatch];
            correctMatch = true;
            removeMatch(listOfMatches, chosenMatch); // deletes the old status of the game that will not be continued -> auch wird dadurhc die reihenfolge der matches in matches.txt geändert
        } else {
            cout << "There are no interrupted matches!" << endl;
            correctMatch = false;
        }  
    } else {
         // load the existing interrupted games into listOfMatches; this is necessary for when we want to add the new game to the text file matches.txt
        loadListOfMatches(listOfMatches); 

        // get info about new match
        cout << "Number of players: ";
        cin >> numberPlayers;
        cout << "Name of the file with special boxes: ";
        cin >> fileName;
        cout << "(N)ormal mode or (Debug) mode? ";
        cin >> choiceDebug;
        choiceDebug = toupper(choiceDebug);
            
        // initialize tMatch
        ifstream file; // open file with board info
        file.open(fileName);
        isOpen = load(board, file); // load board
        // only continue with the rest if file could be openend and board could be loaded accordingly
        
        if(isOpen) {
            correctMatch = true;
            bool debugMode = choiceDebug;
            nextPlayerGame = whoStarts(numberPlayers);
            tPlayers playerInfo;

            // initialize tPlayer
            tPlayer p;
            p.currentBox = 1;
            p.turnsToSkip = 0;

            // initialize tPlayers
            playerInfo.numberOfPlayers = numberPlayers;
            for(int i = 0; i < numberPlayers; i++) {
                playerInfo.playersInfo[i] = p;
            }
                
            // further initialize tMatch
            tMatch newMatch;
            for(int i = 0; i < DIM; i++) {
                newMatch.board[i] = board[i];
            }
            newMatch.debugMode = choiceDebug;
            newMatch.nextPlayer = nextPlayerGame;
            newMatch.numberOfPlayers = numberPlayers;
            newMatch.playersState = playerInfo;
            matchToPlay = newMatch;
            printBoard(matchToPlay); // print board of chosen match
        } else {
            cout << "Match could not be loaded!" << endl;
            correctMatch = false;
        }
    }

    // match to play is now stored in matchToPlay
    if(correctMatch) {
        winner = match(matchToPlay);
        // if match was interrupted, add match to the list of matches
        if(winner == -1) {
            addMatch(listOfMatches, matchToPlay); // nextPlayer here holds the number of the nextPlayer, so nextPlayer -1 is the player in turn
        } else {
            cout << "Winner: " << winner << endl;
        }
    } 

    return 0;
}

void nextGoose(const tBoard board, int& position) { // returns position of next Goose, if current box is a Goose
    position = nextBox(board, position);
}


int randomDie() { // returns random number 1-6; will be called when program is not in debug mode
    int randomNumber;

    randomNumber = 1 + rand() % (6 - 1 + 1);

    return randomNumber;
}


int manualDie() { // ask user for input >=1; will be called when program is in debug mode
    int die;

    cout << "Enter die roll: ";
    cin >> die;

    return die;
}


int whoStarts(int numOfPlayers) { // returns player who starts randomly
    int whoStartsGame;

    whoStartsGame = 1 + rand() % (numOfPlayers - 1 + 1);

    return whoStartsGame; 
}


void checkSpecial(tMatch& match) { // checks if current box is a special box 
    int currentPlayer = getPlayer(match);
    int boxNumber = match.playersState.playersInfo[currentPlayer - 1].currentBox; 
    tBox boxPosition = match.board[boxNumber - 1];
    string boxName = boxToString(boxPosition);
    
    if(boxName == "Goose") {
        int oldBox = boxNumber; 
        nextGoose(match.board, boxNumber);
        match.playersState.playersInfo[currentPlayer - 1].currentBox = boxNumber;
        int newBox = match.playersState.playersInfo[currentPlayer - 1].currentBox;
        if(oldBox != newBox) {
            cout << "From goose to goose and roll again with no excuse!" << endl;
            cout << "Jumping to next goose (box " << newBox << ")" << endl;
        }
        //match.playersState.playersInfo[currentPlayer - 1].turnsToSkip = 0; überall weggemacht, richtig?
    } else if(boxName == "Bridge") {
        int oldBox = boxNumber;
        searchPair(match.board, stringToBox("Bridge"), boxNumber);
        match.playersState.playersInfo[currentPlayer - 1].currentBox = boxNumber;
        int newBox = match.playersState.playersInfo[currentPlayer - 1].currentBox;
        if(oldBox != newBox) {
            cout << "From bridge to bridge and roll again down the ridge" << endl;
            cout << "Jumping to next bridge (box " << newBox << ")" << endl;
        }
    } else if(boxName == "Dice") {
        int oldBox = boxNumber;
        searchPair(match.board, stringToBox("Dice"), boxNumber);
        match.playersState.playersInfo[currentPlayer - 1].currentBox = boxNumber;
        int newBox = match.playersState.playersInfo[currentPlayer - 1].currentBox;
        if(oldBox != newBox) {
            cout << "From dice to dice and roll again with no price!" << endl;
            cout << "Jumping to next dice (box " << newBox << ")" << endl;
        }
    } else if(boxName == "Maze") {
        cout << "Go back 12 boxes!" << endl;
        match.playersState.playersInfo[currentPlayer - 1].currentBox = boxNumber - 12;
    } else if(boxName == "Death") {
        cout << "You're dead!!! Starting over ..." << endl;
        match.playersState.playersInfo[currentPlayer - 1].currentBox = 1;
    } else if(boxName == "Inn") {
        cout << "Relaxing at the Inn!" << endl << "Skipping "  << PENALTY_INN << " turn(s)" << endl;
        match.playersState.playersInfo[currentPlayer - 1].turnsToSkip += PENALTY_INN;
    } else if(boxName == "Jail") {
        cout << "In Jail! " << PENALTY_JAIL << " skipped  turn(s)" << endl;
        match.playersState.playersInfo[currentPlayer - 1].turnsToSkip += PENALTY_JAIL;
    } else if(boxName == "Well") {
        cout << "Into the Well! Skipping " << PENALTY_WELL << " turn(s)" << endl;
        match.playersState.playersInfo[currentPlayer - 1].turnsToSkip += PENALTY_WELL;
    }
}


void checkTurns(tMatch& match) { // increases turns to play for current player
    int currentPlayer = getPlayer(match);
    int currentBox = match.playersState.playersInfo[currentPlayer - 1].currentBox;
    tBox currentBoxOnBoard = match.board[currentBox - 1];
    string boxName = boxToString(currentBoxOnBoard);

    if(boxName == "Bridge" || boxName == "Dice" || boxName == "Goose") {
        // increase skips of everyone else so that current player can play again
        for(int i = 0; i < match.numberOfPlayers; i++) {
            if(i + 1 != currentPlayer) {
                match.playersState.playersInfo[i].turnsToSkip += 1;
            }
        }
    }
}

void changeTurn(tMatch& match) { 
    if(match.nextPlayer == match.numberOfPlayers) {
        match.nextPlayer = 1;
    } else {
        match.nextPlayer ++;
    }
}

bool load(tBoard board, ifstream& file) { 
    bool correct = false, isOpen = false;
    int counterDice = 0, counterBridge = 0;

    for(int i = 0; i < DIM; i++) {
        board[i] = stringToBox("Normal");
    }

    if(file.is_open()) {
        isOpen = true;
        int box;
        file >> box;
        while(box != 0) {
            string name;
            file >> name;
            board[box-1] = stringToBox(name);
            if(boxToString(board[box-1]) == "Dice") {
                counterDice++;
            } else if(boxToString(board[box-1]) == "Bridge") {
                counterBridge++;
            }
            file >> box;
        }
        file.close();
    } 

    // check if there are exactly two bridges and two dices
    if(isOpen && counterDice == 2 && counterBridge == 2) {
        correct = true;
    }
  
    return correct;
}

int match(tMatch& match) { 
    bool isWinner = false, playerChange = false, newGame = true, exit = false, firstRound = true, canPlay = true;
    int winner = -1, i = 0, currentPlayer, nextPlayer, storageOfCurrentPlayer;
    char continueOrExit = 'C';

    // identify if it is a new game
    while(newGame && i < match.numberOfPlayers) {
        if(match.playersState.playersInfo[i].currentBox > 1 || match.playersState.playersInfo[i].turnsToSkip > 1) {
            newGame = false;
        }
        i++;
    } 

    if(newGame) {
        currentPlayer = whoStarts(match.numberOfPlayers);
        if(currentPlayer == match.numberOfPlayers) {
            match.nextPlayer = 1;
        } else {
            match.nextPlayer = currentPlayer + 1;
        }
    } else {
        currentPlayer = getPlayer(match);
        bool allHavePenalties = true, allHaveSkipps = true;
        int i = 0;
        // if not all other players stand on a penalty-box, but all other players have skipps, the previous player may play again
        while(i < match.numberOfPlayers && allHavePenalties) { // check, if any player does not have a penalty
            if(i != currentPlayer -1) {
                if(boxToString(match.board[match.playersState.playersInfo[i].currentBox - 1]) != "Well" && boxToString(match.board[match.playersState.playersInfo[i].currentBox - 1]) != "Death" && boxToString(match.board[match.playersState.playersInfo[i].currentBox - 1]) != "Inn") {
                    allHavePenalties = false;
                }
            }
            i++;
        }
        i = 0;
        while(i < match.numberOfPlayers && allHaveSkipps) { // check if any player does not have skipps
            if(i != currentPlayer -1) {
                if(match.playersState.playersInfo[i].turnsToSkip == 0) { 
                    allHaveSkipps = false;
                }
            }
            i++;
        }
        if(!allHavePenalties && allHaveSkipps) {
            playerChange = false;
        } else {
            playerChange = true;
        }
    }

    cout << endl << "Game starts with Player " << currentPlayer << "..." << endl;
        
    // let the game begin
    while(!isWinner && !exit) {
        currentPlayer = getPlayer(match);
        storageOfCurrentPlayer = currentPlayer;

        // create output for currentPlayer
        if(playerChange && !firstRound) {
            cout << endl << "Turn for Player " << currentPlayer << endl;
        } 

        if(!firstRound) {
            if(!playerChange) {
                cout << endl;
            }
            cout << "(C)ontinue or (E)xit? ";
            cin >> continueOrExit;
            continueOrExit = toupper(continueOrExit);
        }       

        if(continueOrExit == 'C') {
            // if user wants to continue...
            if(playerChange) { // if the previous currentPlayer does not have one more turn
                if(match.playersState.playersInfo[currentPlayer - 1].turnsToSkip > 0) {
                    if(match.playersState.playersInfo[currentPlayer - 1].turnsToSkip == 1) {
                        cout << "Player " << currentPlayer << " can't play until the next turn" << endl;
                    } else {
                        cout << "Player " << currentPlayer << " can't play and still has " << match.playersState.playersInfo[currentPlayer - 1].turnsToSkip << " more turn(s) to skip" << endl;
                    }
                    match.playersState.playersInfo[currentPlayer - 1].turnsToSkip -= 1;
                    canPlay = false;
                } else {
                    cout << "Player " << currentPlayer << endl << "Current box: " << match.playersState.playersInfo[currentPlayer - 1].currentBox << endl;
                    canPlay = true;
                }
            } else { // if the previous currentUser has one more turn
                cout << "Player " << currentPlayer << endl << "Current box: " << match.playersState.playersInfo[currentPlayer - 1].currentBox << endl;
                canPlay = true;
                if(!firstRound || (firstRound && !newGame)) {
                    for(int i = 0; i < match.numberOfPlayers; i++) { // reduce the skipps of all other player by one, since the currentPlayer now got his additional turn
                        if(i + 1 != currentPlayer) {
                            match.playersState.playersInfo[i].turnsToSkip -= 1;
                        }
                    }
                }
            }
            firstRound = false;
            newGame = false;
        

            if(canPlay) {
                // let current Player play, if he does not have to skip
                play(match);

                //exit loop, if there is one winner
                if(match.playersState.playersInfo[currentPlayer - 1].currentBox >= 63) {
                    isWinner = true;
                    winner = currentPlayer;
                }

                // look for next Player in turn
                int skippsNextPlayer = match.playersState.playersInfo[match.nextPlayer - 1].turnsToSkip;
                checkTurns(match); // updates turns
                int updatedSkippsNextPlayer = match.playersState.playersInfo[match.nextPlayer - 1].turnsToSkip;
                if(skippsNextPlayer != updatedSkippsNextPlayer) { // if the currentPlayer gets one more turn, let him play again in the next round
                    playerChange = false;
                } else {
                    playerChange = true;
                }
            }

            // if the currentPlayer does not get an additional turn, identify next Player
            if(playerChange) {
                changeTurn(match);
                if(match.nextPlayer == 1) {
                    currentPlayer = 4;
                } else {
                    currentPlayer -= 1;
                }
            }
            
        // if user does not want to continue...
        } else {
            exit = true;
        }
    }

    return winner;
}


void play(tMatch& match) { // let's player play one round
    int die, currentPlayer;

    currentPlayer = getPlayer(match);
    if(match.debugMode) {
        die = manualDie();
    } else {
        die = randomDie();
    }
    cout << "Die: " << die << endl;
    match.playersState.playersInfo[currentPlayer - 1].currentBox += die;
    cout << "Next box: " << match.playersState.playersInfo[currentPlayer - 1].currentBox << endl;
    if(match.playersState.playersInfo[currentPlayer - 1].currentBox < 63) {
        checkSpecial(match);
    }
    printBoard(match);
}

int getPlayer(const tMatch& match) {
    int currentPlayer;
    
    if(match.nextPlayer == 1) {
        currentPlayer = match.numberOfPlayers;
    } else {
        currentPlayer = match.nextPlayer - 1;
    }

    return currentPlayer;
}

bool playAgain(const tBoard board, int box) {
    bool anotherTurn = false;
    tBox boxPosition = board[box-1];
    string boxName = boxToString(boxPosition);

    if(boxName == "Goose" || boxName == "Dice" || boxName == "Bridge") {
        anotherTurn = true;
    } 

    return anotherTurn;
}

int nextBox(const tBoard board, int box) { // called for special boxes
    int nextBox = box, index = box;
    tBox boxPosition = board[nextBox - 1];
    string boxName = boxToString(boxPosition); 

    if(boxName == "Bridge") {
        while(nextBox == box && index <= 62) {
            if(boxToString(board[index]) == "Bridge") { 
                nextBox = index + 1;
            } else {
                index += 1;
            }
        }
    } else if(boxName == "Goose") {
        while(nextBox == box && index <= 62) {
            if(boxToString(board[index]) == "Goose") {
                nextBox = index + 1;
            } else {
                index += 1;
            }
        }
    } else if(boxName == "Maze") {
        while(nextBox == box && index <= 62) {
            if(boxToString(board[index]) == "Maze") {
                nextBox = index + 1;
            } else {
                index += 1;
            }
        }
    } else if(boxName == "Dice") {
        while(nextBox == box && index <= 62) {
            if(boxToString(board[index]) == "Dice" ) {
                nextBox = index + 1;
            } else {
                index += 1;
            }
        }
    } 

    return nextBox;
}

// changes value of position, if currentBox is not the last Dice / Bridge on the Board
void searchPair(const tBoard board, tBox kind, int& position) {
    string boxName = boxToString(kind);
    int box = position;
    int index = position;

    if(boxName == "Dice") {
        while(position == box && index <= 62) {
            if(boxToString(board[index]) == "Dice") {
                position = index + 1 ; 
            } else {
                index += 1;
            }
        }
    } else if(boxName == "Bridge") {
        while(position == box && index <= 62) {
            if(boxToString(board[index]) == "Bridge") {
                position = index + 1 ;
            } else {
                index += 1;
            }
        }
    }
}


tBox stringToBox(string id) {
   tBox kind = Normal;

   if (id == "Goose")
      kind = Goose;
   else if (id == "Dice")
      kind = Dice;
   else if (id == "Bridge")
      kind = Bridge;
   else if (id == "Inn")
      kind = Inn;
   else if (id == "Death")
      kind = Death;
   else if (id == "Maze")
      kind = Maze;
   else if (id == "Well")
      kind = Well;
   else if (id == "Jail")
      kind = Jail;

   return kind;
}

string boxToString(tBox box) {
   string str;

   switch (box) {
   case Normal:
      str = "";
      break;
   case Goose:
      str = "Goose";
      break;
   case Dice:
      str = "Dice";
      break;
   case Bridge:
      str = "Bridge";
      break;
   case Inn:
      str = "Inn";
      break;
   case Death:
      str = "Death";
      break;
   case Maze:
      str = "Maze";
      break;
   case Well:
      str = "Well";
      break;
   case Jail:
      str = "Jail";
      break;
   }

   return str;
}

void pause() {
   cout << "   Press any key to continue...";
   cin.get();
}

void printBoard(const tMatch& match) { // prints board
   const int COL = 9; // 9 boxes per row
   typedef int tRow[COL]; // Box number in each 9 columns

   tRow row;
   ifstream file;
   string border; // Horizontal borders with graphical characters read from the file
   int num;

   cout << endl;
   file.open("boardinfo.txt");
   getline(file, border);
   cout << "   " << border << endl; // Uppermost border
   for (int i = 1; i <= 8; i++) { // 8 rows of boxes
      for (int col = 0; col < COL; col++) // Box numbers for the row
         file >> row[col];
      cout << "   " << '\xba'; // Vertical border
      for (int col = 0; col < COL; col++) {
         if (row[col] == -1) // No box
            if (row[col + 1] == -1)
               cout << "       "; // If there is no box next, no vertical border
            else
               cout << "      " << '\xba';
         else
            cout << setw(6) << right << row[col] << '\xba'; // Box number and vertical border
      }
      cout << endl << "   " << '\xba'; // Rightmost vertical border
      for (int col = 0; col < COL; col++) {
         if (row[col] == -1)
            if (row[col + 1] != -1)
               cout << "      " << '\xba';
            else
               cout << "       ";
         else // Special box names are diplayed in green
            cout << "\033[32m" << setw(6) << right << boxToString(match.board[row[col] - 1]) << "\033[0m" << '\xba';
      }
      cout << endl << "   " << '\xba'; // Rightmost vertical border
      for (int col = 0; col < COL; col++) {
         cout << " ";
         num = 0;
         cout << "\033[31m"; // Player numbers are displayed in red
         for (int p = 0; p < match.numberOfPlayers; p++)
            if (match.playersState.playersInfo[p].currentBox - 1 == row[col] - 1) {
               cout << p + 1;
               num++;
            }
         cout << "\033[0m";
         cout << setw(5 - num) << " ";
         if (row[col] == -1)
            if (row[col + 1] != -1)
               cout << '\xba';
            else
               cout << " "; // If there is no box next, no vertical border
         else
            cout << '\xba';
      }
      cout << endl;
      file.get();
      getline(file, border);
      cout << "   " << border << endl;
   }
   if (match.debugMode == false)
      pause();
   cout << endl;
}

void load(tMatches& listOfMatches) { // shows interrupted matches
    ifstream file;
    tBoard board;
    string name;
    char debug;
    int numberOfMatches, numberOfPlayers, box, skipps, boardBox, nextPlayer;

    file.open("matches.txt");
    if(file.is_open()) {
        file >> numberOfMatches;
        listOfMatches.counter = numberOfMatches;

        // load playerInfo for each match
        for(int i = 1; i <= numberOfMatches; i++) {
            file >> numberOfPlayers;
            listOfMatches.matches[i - 1].numberOfPlayers = numberOfPlayers;
            listOfMatches.matches[i - 1].playersState.numberOfPlayers = numberOfPlayers;
            cout << i << ": " << numberOfPlayers << " players -";
            for(int j = 1; j <= numberOfPlayers; j++) {
                file >> box >> skipps;
                cout << " " << box;
                listOfMatches.matches[i - 1].playersState.playersInfo[j - 1].turnsToSkip = skipps;
                listOfMatches.matches[i - 1].playersState.playersInfo[j - 1].currentBox = box;
            }

            // load board for each match
            file >> boardBox;
            while(boardBox != 0) {
                file >> name;
                listOfMatches.matches[i - 1].board[boardBox - 1] = stringToBox(name);
                file >> boardBox;
            }
            
            file >> nextPlayer;
            listOfMatches.matches[i - 1].nextPlayer = nextPlayer;
            file >> debug;
            debug = toupper(debug);
            if(debug == 'D') {
                cout << " (debug mode)" << endl;
                listOfMatches.matches[i - 1].debugMode = true;
            } else {
                cout << endl;
                listOfMatches.matches[i - 1].debugMode = false;
            }
        }
    file.close();
    }
}

int selectMatch(const tMatches& listOfMatches) { // select match to continue
    int result, chosen;

    cout << "Match to play: ";
    cin >> chosen;
    while(chosen > listOfMatches.counter) {
        cout << "The game you chose does not exist! Please select new game..." << endl;
        cin >> chosen;
    }
    cout << endl;
    result = chosen - 1;

    return result; // returns -1 in case there are no matches
}

void removeMatch(tMatches& listOfMatches, int index) {
    ofstream file;

    for(int i = index; i < listOfMatches.counter - 1; i++) {
        listOfMatches.matches[i] = listOfMatches.matches[i + 1];
    }
    listOfMatches.counter -= 1;

    // update matches.txt
    file.open("matches.txt");
    if(file.is_open()) {
        int counter = listOfMatches.counter;
        file << listOfMatches.counter << endl << endl;
        // display info for each match
        for(int i = 0; i < listOfMatches.counter; i++) {
            file << listOfMatches.matches[i].numberOfPlayers << endl;

            // print info for each player of the match
            for(int j = 0; j < listOfMatches.matches[i].numberOfPlayers; j++) {
                file << listOfMatches.matches[i].playersState.playersInfo[j].currentBox << " " << listOfMatches.matches[i].playersState.playersInfo[j].turnsToSkip << endl;
            }
            // display board info for each match
            for(int j = 0; j < DIM; j++) {
                // if box is a special box, display info
                if(boxToString(listOfMatches.matches[i].board[j]) != "") {
                    file << j + 1 << " " << boxToString(listOfMatches.matches[i].board[j]) << endl;
                }
            }
            file << 0 << endl << listOfMatches.matches[i].nextPlayer << endl;
            if(listOfMatches.matches[i].debugMode == true) {
                file << 'D' << endl << endl;
            } else {
                file << 'N' << endl << endl;
            }
        }
        file.close();
    }

}

void addMatch(tMatches& listOfMatches, tMatch match) {
    ofstream file;
    int counter;

    file.open("matches.txt");
    if(file.is_open()) {
        counter = listOfMatches.counter;
        // add match to the list of matches
        if(listOfMatches.counter == MATCHES) {
            removeMatch(listOfMatches, 0);
            listOfMatches.counter += 1;
            listOfMatches.matches[listOfMatches.counter - 1] = match;
        } else {
            listOfMatches.matches[listOfMatches.counter] = match;
            listOfMatches.counter += 1;
        }
        file << listOfMatches.counter << endl << endl;
        // display info for each match
        for(int i = 0; i < listOfMatches.counter; i++) {
            file << listOfMatches.matches[i].numberOfPlayers << endl;

            // print info for each player of the match
            for(int j = 0; j < listOfMatches.matches[i].numberOfPlayers; j++) {
                file << listOfMatches.matches[i].playersState.playersInfo[j].currentBox << " " << listOfMatches.matches[i].playersState.playersInfo[j].turnsToSkip << endl;
            }
            // display board info for each match
            for(int j = 0; j < DIM; j++) {
                // if box is a special box, display info
                if(boxToString(listOfMatches.matches[i].board[j]) != "") {
                    file << j + 1 << " " << boxToString(listOfMatches.matches[i].board[j]) << endl;
                }
            }
            file << 0 << endl << listOfMatches.matches[i].nextPlayer << endl;
            if(listOfMatches.matches[i].debugMode == true) {
                file << 'D' << endl << endl;
            } else {
                file << 'N' << endl << endl;
            }
        }
        file.close();
    }
}

void loadListOfMatches(tMatches& listOfMatches) { // loads interrupted matches into listOfMatches
    ifstream file;
    tBoard board;
    string name;
    char debug;
    int numberOfMatches, numberOfPlayers, box, skipps, boardBox, nextPlayer;

    file.open("matches.txt");
    if(file.is_open()) {
        file >> numberOfMatches;

        // load playerInfo for each match
        for(int i = 0; i < listOfMatches.counter; i++) {
            file >> numberOfPlayers;
            listOfMatches.matches[i].numberOfPlayers = numberOfPlayers;
            listOfMatches.matches[i].playersState.numberOfPlayers = numberOfPlayers;
            for(int j = 0; j < numberOfPlayers; j++) {
                file >> box >> skipps;
                listOfMatches.matches[i].playersState.playersInfo[j].turnsToSkip = skipps;
                listOfMatches.matches[i].playersState.playersInfo[j].currentBox = box;
            }

            // load board for each match
            for(int j = 0; j < DIM; j++) {
                listOfMatches.matches[i].board[j] = stringToBox(""); // initialize board
            }
            file >> boardBox;
            while(boardBox != 0) {
                file >> name;
                listOfMatches.matches[i].board[boardBox - 1] = stringToBox(name);
                file >> boardBox;
            }
            
            // load next player and debug mode
            file >> nextPlayer;
            listOfMatches.matches[i].nextPlayer = nextPlayer;
            file >> debug;
            debug = toupper(debug);
            if(debug == 'D') {
                listOfMatches.matches[i].debugMode = true;
            } else {
                cout << endl;
                listOfMatches.matches[i].debugMode = false;
            }
        }
    file.close();
    }
}
