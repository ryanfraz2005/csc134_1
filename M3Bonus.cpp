#include <iostream>
#include <cstdlib>
#include <ctime>
#include <string>
#include <algorithm>

static int playerWins = 0;
static int computerWins = 0;
static int ties = 0;

std::string getComputerMove() {
    static bool seeded = false;
    if (!seeded) {
        srand(time(0)); 
        seeded = true;
    }
    int moveIndex = rand() % 3; 
    switch (moveIndex) {
        case 0: return "rock";
        case 1: return "paper";
        case 2: return "scissors";
        default: return "";
    }
}

std::string standardizeMove(std::string move) {
    std::transform(move.begin(), move.end(), move.begin(), 
                   ::tolower);
    if (move == "rock" || move == "paper" || move == "scissors") {
        return move;
    }
    return "invalid"; 
}

void determineWinner(const std::string& playerMove, const std::string& computerMove) {
    
    if (playerMove == computerMove) {
        std::cout << "\nIt's a tie!\n";
        ties++; 
    }
  
    else if (
        (playerMove == "rock" && computerMove == "scissors") ||
        (playerMove == "paper" && computerMove == "rock") ||
        (playerMove == "scissors" && computerMove == "paper")
    ) {
        std::cout << "\nYou win!\n";
        playerWins++;
    }
   
    else {
        std::cout << "\nComputer wins!\n";
        computerWins++; 
    }
}

void displayStats() {
    int totalGames = playerWins + computerWins + ties;
    std::cout << "\n===================================\n";
    std::cout << "           GAME STATISTICS           \n";
    std::cout << "===================================\n";
    std::cout << "Total Games Played: " << totalGames << "\n";
    std::cout << "Your Wins:          " << playerWins << "\n";
    std::cout << "Computer Wins:      " << computerWins << "\n";
    std::cout << "Ties:               " << ties << "\n";
    std::cout << "===================================\n";
}

int main() {
    std::string playerInput = "";
    std::string playerMove = "";
    std::string computerMove = "";
    char playAgain = ' ';

    std::cout << "Welcome to Rock, Paper, Scissors! Best of luck!\n";


    do {
       
        std::cout << "===================================\n";
        std::cout << "Enter your move (Rock, Paper, or Scissors): ";
        std::cin >> playerInput;
        
        playerMove = standardizeMove(playerInput);

   
        if (playerMove == "invalid") {
            std::cout << "\nInvalid choice. Please enter 'Rock', 'Paper', or 'Scissors'.\n";
         
            continue; 
        }

        computerMove = getComputerMove();

        std::cout << "===================================\n";
        std::cout << "\nYou chose: " << playerMove << "\n";
        std::cout << "Computer chose: " << computerMove << "\n";

        determineWinner(playerMove, computerMove);

        displayStats();
        
        std::cout << "Do you want to play again? (y/n): ";
        std::cin >> playAgain;

        playAgain = std::tolower(playAgain);

    } while (playAgain == 'y'); 

    std::cout << "\nThanks for playing! Final Stats:\n";
    displayStats();

    return 0;
}
