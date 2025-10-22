#include <iostream>
using namespace std;

int main() {
    int firstNum, secondNum, answer;
    cout << "Enter a number from 1-12: ",
    cin >> firstNum;
   
    for (int i=1; i<= firstNum; i++) {
        answer = firstNum * i;
        cout << firstNum << " times " << i << " is " << answer << endl;
    }

    return 0;
}


