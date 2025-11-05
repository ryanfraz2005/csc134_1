#include <iostream>
using namespace std;

int getPlayerChoice(int maxChoice);
void showChoices(string choice1, string choice2, string choice3);
void game_start();
const int MAX = 3;

int main() {
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
  cout << R"()";

  showChoices(" ");

  getPlayerChoice(MAX);
  if (choice == 1) {
    cout << " " << endl;
  }
}