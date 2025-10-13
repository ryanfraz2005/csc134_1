#include <iostream>
#include <string>
#include <algorithm>
#include <cctype>
using namespace std;

void example1();
void example2();
void question2();

int main () {

example1();
example2();

return 0;

}

void example1() {
    string answer;
    cout << "Hello, I'm a C++ program!" << endl;
    cout << "Do you like me? Please type yes or no: ";
    cin >> answer;
    std::transform(answer.begin(), answer.end(), answer.begin(),
    [](unsigned char c){ return std::tolower(c); });

    if (answer == "yes"){
        cout << "That's great! I'm sure we'll get along." << endl;
    }
    else if (answer == "no"){
       cout << "Well, maybe you'll learn to like me later." << endl;
    }
    else {cout << "If you're not sure... that's ok." << endl;}
}

void example2() {
cout << endl;
cout << "You find yourself attempting to escape a dungeon" << endl;
cout << "Eventually you find your way to a set of doors. Will you enter door 1 or 2? (Type 1 or 2) ";
int choice;
cin >> choice;
if (choice == 1){
    cout << endl;
    cout << "You enter door 1. Unfortunately, the room is filled with armed guards. You lose." << endl;
    cout << "-----GAME OVER-----" << endl;
}
else if (choice == 2){
  question2();
}
else {
    cout << endl;
    cout << "Try again." << endl;
    example2();
}
}

void question2() {
    cout << endl;
    cout << "You find the exit of the dungeon, however you must now find the exit to the castle." << endl;
    cout << "You find yourself infront of another set of doors. Door 1 or 2? ";
    int choice;
    cin >> choice;
    if (choice == 1){
    cout << endl;
    cout << "You entered door 1 and were caught. You lose." << endl;
    cout << "-----GAME OVER-----" << endl;
}
else if (choice == 2){
  cout << endl;
  cout << "You entered door 2. You found the exit!" << endl;
  cout << "-----YOU WIN!-----" << endl;
}
else {
    cout << endl;
    cout << "Try again." << endl;
    question2();
}


}