/*
CSC 134
M5T1
Ryan Frazee
10/22/25

Purpose: Demo void and value-returning functions.
*/

#include <iostream>
using namespace std;

// Function Declares (Definitions are at the bottom)
void say_hello(); // says hi

int get_the_answer(); // provides the answer to everything

double double_a_number(double); // num times two

int main() {
    // this program does nothing useful
    double my_num;
    int another_num;

   say_hello();
    cout << "Please enter a number (with or without a decimal point)" << endl;
    cin >> my_num;
    my_num = double_a_number(my_num);
    cout << "Double the number is: " << my_num << endl;
    cout << "But the only answer you need is: ",
    cout << get_the_answer() << endl;

}

// Function Definitons (the whole function!) goes here
void say_hello() {
    // says hi
    cout << "Welcome to the best program ever!" << endl;
}

int get_the_answer() {
    // provides the answer to everything
    return 42;
}

double double_a_number(double the_num) {
    // num times two
    double answer = the_num * 2;
    return answer;
}