#include <iostream>
#include <string>
using namespace std;

void question1();

int main () {

question1();

return 0;
}

void question1() {
string month1, month2, month3;
double rain1, rain2, rain3, average;

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