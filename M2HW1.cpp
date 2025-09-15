/*
CSC 134
M2HW1 -
Ryan Frazee
9/15/25
*/
#include <iostream>
#include <iomanip>
using namespace std;

void question1()
{
    cout << "Question 1" << endl;

    double Balance, 
    Deposit, 
    Withdrawl,
    Final_Balance;

    string Name;

    cout << "Enter Name: ";
    cin >> Name;

     cout << setprecision(2) << fixed;
     cout << "Enter account balance: $";
     cin >> Balance;
     cout << "Enter amount deposited: $";
     cin >> Deposit;
     cout << "Enter amount withdrawn: $";
     cin >> Withdrawl;

     Final_Balance = Balance + Deposit - Withdrawl;

     cout << "Account name: " << Name << endl;
     cout << "Account number: 649174290" << endl;
     cout << "Final account balance: " << Final_Balance << endl;


}
void question2()
{
    cout << "Question 2" << endl;
}

int main ()
{
    // Call each question as its own function

    question1();
    question2();



    return 0;
}