/*
CSC 124
M4LAB2 - Nested Loops and Rectangles
Ryan Frazee
10/8/25

Task: Draw a rectangle.
*/

#include <iostream>
using namespace std;

int main () {

    int length = 10, height = 10;
    string tile = "🟦";

    cout << "Draw a Rectangle" << endl;
    cout << endl;
    cout << "Length? ";
    cin >> length;
    cout << "Height? ";
    cin >> height;
    cout << endl;
    cout << "Rectangle" << " = " << length << " x " << height << endl;

    for (int i = 0; i < height; i++) {
        for (int j = 0; j < length; j++) {
            cout << tile;
        }
        cout << endl;
    }

    return 0;
}