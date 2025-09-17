/*
CSC 134
M3T1 - Area of Rectangles
Simple Comparison
Ryan Frazee
9/17/25
*/

#include <iostream>
using namespace std;

int main()
{
    double length1, length2, width1, width2;
    double area1, area2;
    cout << "Enter the length and width of two rectangles." << endl;
    cout << "First rectangle." << endl;
    cout << "Length: ";
    cin >> length1;
    cout << "Width: ";
    cin >> width1;
    cout << "Second rectangle." << endl;
    cout << "Length: ";
    cin >> length2;
    cout << "Width: ";
    cin >> width2;

    area1 = length1 * width1;
    area2 = length2 * width2;




    return 0;
}