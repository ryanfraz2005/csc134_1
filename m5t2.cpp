#include <iostream>
#include <math.h>
using namespace std;

void printResult(int number, int result) {
    cout << number << " Squared = " << result << endl;
}

int growth(int number) {
    int result = 2 ^ number;
    return result;
}
int main() {
    int number, result;
    number = 2;
    result = growth(number);
    printResult(number, result);
}