#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

const int MAX = 3;
void showChoices(string choice1, string choice2, string choice3);
void room1();
void room_1();
void room2();
void room_2();
void room__2();
void room3();
void exit();


int main() {
    cout << " - - - - Escape Room - - - - " << endl;
    cout << "Welcome to the escape room! Where would you like to search first?" << endl;
    room1();

    return 0;
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
    cout << "Choose!" << endl;
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

void room1() {
    int choice;
    showChoices("Door", "Bookshelf", "Table");
    choice = getPlayerChoice(MAX);
  if (choice == 1) {
  cout << endl;
  cout << "The door is locked." << endl;
  room1();
  }
  if (choice == 2) {
  cout << endl;
  cout << "You searched the bookshelf... and you found a key in a book!" << endl;
  room_1();
  }
  if (choice == 3) {
  cout << endl;
  cout << "You searched the tables... and you found nothing." << endl;
  room1();
  }
}

void room_1() {
    int choice;
    showChoices("Door", "Bookshelf", "Table");
    choice = getPlayerChoice(MAX);
  if (choice == 1) {
  cout << endl;
  cout << "You unlocked the door!" << endl;
  room2();
  }
  if (choice == 2) {
  cout << endl;
  cout << "Nothing else to search for." << endl;
  room_1();
  }
  if (choice == 3) {
  cout << endl;
  cout << "Nothing else to search for." << endl;
  room_1();
  }
}

void room2() {
    int choice;
    cout << endl;
    cout << "You enter the next room. Where will you look in here?" << endl;
    showChoices("Door", "Cabinets", "Drawers");
    choice = getPlayerChoice(MAX);
  if (choice == 1) {
  cout << endl;
  cout << "The door is locked." << endl;
  room2();
  }
  if (choice == 2) {
  cout << endl;
  cout << "You searched through the cabinets... and you found a note!" << endl;
  cout << endl;
  cout << "The note reads: 'There is a hidden compartment in one of the drawers.' " << endl;
  room_2();
  }
  if (choice == 3) {
  cout << endl;
  cout << "You searched through the drawers... and you found nothing." << endl;
  room2();
  }

}

void room_2() {
    int choice;
    cout << endl;
    showChoices("Door", "Cabinets", "Drawers");
    choice = getPlayerChoice(MAX);
  if (choice == 1) {
  cout << endl;
  cout << "The door is locked." << endl;
  room_2();
  }
  if (choice == 2) {
  cout << endl;
  cout << "Nothing else to search for here." << endl;
  room_2();
  }
  if (choice == 3) {
  cout << endl;
  cout << "You searched through the drawers... and you found a hidden compartment with a key!" << endl;
  room__2();
  }

}

void room__2() {
   int choice;
    cout << endl;
    showChoices("Door", "Cabinets", "Drawers");
    choice = getPlayerChoice(MAX);
  if (choice == 1) {
  cout << endl;
  cout << "You unlocked the door!" << endl;
  room3();
  }
  if (choice == 2) {
  cout << endl;
  cout << "Nothing else to search for." << endl;
  room__2();
  }
  if (choice == 3) {
  cout << endl;
  cout << "Nothing else to search for." << endl;
  room__2();
  } 

}

void room3() {
    string riddle;
    cout << "This next room only requires you to solve this riddle." << endl;
    cout << endl;
    cout << "What comes up but never comes down? ";
    cin >> riddle;
    std::transform(riddle.begin(), riddle.end(), riddle.begin(),
    [](unsigned char c){ return std::tolower(c); });

    if (riddle == "rain"){
        cout << "Correct! You may exit!" << endl;
        exit();
    }
    else {cout << "Incorrect. Try again." << endl;
        room3(); 
}
}

void exit() {
    cout << endl;
    cout << "Congrats! You have escaped!" << endl;
}