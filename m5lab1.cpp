#include <iostream>
using namespace std;

int getPlayerChoice(int maxChoice);

void main() {
    int choice;
    int max = 3;
    cout << "TESTING: Choose 1, 2, or 3." << endl;
    choice = getPlayerChoice(max);
    cout << "You choose: " << choice << endl;
}

int getPlayerChoice(int maxChoice) {
    int choice;
    while (true) {
        cout << "Your choice: ";
        cin >> choice;

        if (choice >= 1 && choice <= maxChoice) {
            return choice;
        }

        cout << "Please choose between 1 and " << maxChoice
    }
}