#include <iostream>
#include <string>
using namespace std;

void menu();
void question1();
void question2();
void question3();

int main () {

menu();

return 0;
}

void menu() {
    cout << "MAIN MENU" << endl;
    cout << "---------" << endl;
    cout << "1 = Question 1 (Rainfall for Months)" << endl;
    cout << "2 = Question 2 (Volume of a Block)" << endl;
    cout << "3 = Question 3 (Number Range)" << endl;
    cout << "7 = All" << endl;
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
    else if (choice == 3) {
        question3();
    }
    else if (choice == 7) {
        question1();
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
if (length <= 0) {
    cout << "Invalid Input." << endl;
    cout << "Input cannot be less than or equal to 0." << endl;
    cin.clear();
    question2();
}
cout << "Enter Width: ";
cin >> width;
if (width <= 0) {
    cout << "Invalid Input." << endl;
    cout << "Input cannot be less than or equal to 0." << endl;
    cin.clear();
    question2();
}
cout << "Enter Height: ";
cin >> height;
if (length <= 0 && width <= 0 && height <=0) {
    cout << "Invalid Input." << endl;
    cout << "Input cannot be less than or equal to 0." << endl;
    cin.clear();
    question2();
}
volume = length * width * height;
cout << "The volume of the block is " << volume << endl;
}

void question3() {
   
    cout << "Enter a number between 1-10: ";
    int num;
    cin >> num;

    if (num == 1) {
        cout << "The roman numeral version of 1 is I" << endl;
    }
    else if (num = 2) {
        cout << "The roman numeral version of 2 is II" << endl;
    }
    else if (num = 3) {
        cout << "The roman numeral version of 3 is III" << endl;
    }
    else if (num = 4) {
        cout << "The roman numeral version of 4 is IV" << endl;
    }
    else if (num = 5) {
        cout << "The roman numeral version of 5 is V" << endl;
    }
    else if (num = 6) {
        cout << "The roman numeral version of 6 is VI" << endl;
    }
    else if (num = 7) {
        cout << "The roman numeral version of 7 is VII" << endl;
    }
    else if (num = 8) {
        cout << "The roman numeral version of 8 is VIII" << endl;
    }
    else if (num = 9) {
        cout << "The roman numeral version of 9 is IX" << endl;
    }
    else if (num = 10) {
        cout << "The roman numeral version of 10 is X" << endl;
    }
    else {
        cout << "Invaid number. Must be a whole number between 1-10." << endl;
        question3();
    }

}