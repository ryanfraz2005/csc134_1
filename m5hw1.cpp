#include <iostream>
#include <string>
using namespace std;

void menu();
void question1();
void question2();

int main () {

menu();

return 0;
}

void menu() {
    cout << "MAIN MENU" << endl;
    cout << "---------" << endl;
    cout << "1 = Question 1" << endl;
    cout << "2 = Question 2" << endl;
    cout << endl;
    cout << "Enter choice: ";
    int choice;
    cin >> choice;

    if (choice == 1) {
        question1();
    }
    else if (choice == 2) {
        question2();
    }
    else {
        cout << "Invalid choice." << endl << endl;
        cin.clear();
        menu();
    }
}

void question1() {
string month1, month2, month3;
double rain1, rain2, rain3, average;

cout << endl;
cout << "Enter first month: ";
cin >> month1;
cout << "Enter rainfall for " << month1 << ": ";
cin >> rain1;
cout << "Enter second month: ";
cin >> month2;
cout << "Enter rainfall for " << month2 << ": ";
cin >> rain2;
cout << "Enter third month: ";
cin >> month3;
cout << "Enter rainfall for " << month3 << ": ";
cin >> rain3;
average = (rain1 + rain2 + rain3) / 3;

cout << "The average rainfall for " << month1 << ", " << month2 << ", and " << month3 << " is " << average << endl;
}

void question2() {
double length, width, height, volume;

cout << endl;
cout << "Finding the volume of a block." << endl;
cout << "Enter Length: ";
cin >> length;
cout << "Enter Width: ";
cin >> width;
cout << "Enter Height: ";
cin >> height;
volume = length * width * height;

if (length <= 0, width <= 0, height <= 0) {
    cout << "Invalid Input." << endl;
    cout << "Input cannot be less than 0." << endl;
    question2();
}

}