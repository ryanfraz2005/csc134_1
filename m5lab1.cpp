#include <iostream>
using namespace std;

int getPlayerChoice(int maxChoice);
void showChoices(string choice1, string choice2, string choice3);
void game_start();
const int MAX = 3;
void gameOver();

int main() {

    game_start();

    /*
    int choice;
    int max = 3;
    showChoices("1", "2","3")
    choice = getPlayerChoice(max);
    cout << "You choose: " << choice << endl;

    return 0;
    */
}

int getPlayerChoice(int maxChoice) {
    int choice;
    while (true) {
        cout << "Your choice: ";
        cin >> choice;

        if (choice >= 1 && choice <= maxChoice) {
            return choice;
        }

        cout << "Please choose between 1 and " << maxChoice;
    }
}

void showChoices(string choice1, string choice2, string choice3) {
    cout << endl;
    cout << "---- MAKE YOUR CHOICE ----" << endl;
    int num = 1;
    cout << num << ". " << choice1 << endl;
    num++;

    if (choice2 != "") {
        cout << num << ". " << choice2 << endl;
        num++;
    }
    if (choice3 != "") {
        cout << num << ". " << choice3 << endl;
        num++;
    }
}

void game_start() {
  int choice;
// R for Raw -- Print every line as is until it ends
  cout << R"(You wake up in a dark haunted house, confused of how you got there.)" << endl;
  cout << R"(You hear footsteps walking down the hallway. What do you do?)";

  showChoices("Try and exit through the window.", "Hide under the bed.", "Hide in the closet.");

  getPlayerChoice(MAX);
  if (choice == 1) {
    cout << R"(At first, the window won't budge. But eventually you successfully open it, but you find youself several stories up.)" << endl;
    cout << R"(With no way out, you are caught.)" << endl;
    gameOver();
  }
  if (choice == 2) {
    
  }
}

void gameOver() {
    cout << endl;
    cout << " - - - -  G A M E   O V E R  - - - - " << endl;
}