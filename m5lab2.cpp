#include <iostream>
using namespace std;

double getLength();
double getWidth();
double getArea(double length, double width);
void   displayData(double length, double width, double area);

int main() {
    double length,
           width,
           area;

    length = getLength();

    width = getWidth();

    area = getArea(length, width);

    displayData(length, width, area);

    return 0;
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