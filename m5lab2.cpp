#include <iostream>
using namespace std;

double getLength();
double getWidth();
double getArea(double length, double width);
void   displayData(double length, double width, double area);
void menu_area();
void menu_main();

int main() {
 
    menu_main();

    return 0;
}

void menu_main() {
    cout << "MAIN MENU" << endl;
    cout << "---------" << endl;
    cout << "1. Area of Rectangle" << endl;
    cout << "2. Exit" << endl;
    cout << endl;
    cout << "Enter choice: ";
    int choice;
    cin >> choice;

    if (choice == 1) {
        menu_area();
    }
    else if (choice == 2) {
        cout << "Goodbye" << endl;
    }
    else {
        cout << "Invalid choice." << endl << endl;
        cin.clear();
        menu_main();
    }
} 

void menu_area() {
    double length,
           width,
           area;

    length = getLength();

    width = getWidth();

    area = getArea(length, width);

    displayData(length, width, area);

}
double getLength() {
    double length;
    cout << "What is the length? ";
    cin >> length;
    return length;
}

double getWidth() {
    double width;
    cout << "What is the width? ";
    cin >> width;
    return width;
}

double getArea(double length, double width) {
    double area;
    area = length * width;
    return area;
}

void   displayData(double length, double width, double area) {
    cout << "Rectangle is " << length << " by " << width << "." << endl;
    cout << "Area is: " << area << endl;
    return;
}