/*
M3T2 - Craps Part 1
CSC 134
Ryan Frazee
9/22/25
Beginning of the craps game.
*/

#include <iostream>
#include <cstdlib>
#include <time>

using namespace std;

// Helper functions (todo)
int roll();

// main
int main()
{
    //int num = roll();
    //cout << num << endl;
    // MAIN CRAPS CYCLE
    // For Now;
    /*
    - roll 2d6 (2-12)
    - branch based on win, lose, or point
    - rest comes later
    */
   int roll1 = 2;
   int roll2 = 5;

   int sum = roll1+roll2;

   if (sum == 7)
   {
    cout << "Lucky Seven -- You win!" << endl;
   }
   else
    {
    cout << "Did not roll a seven." << endl;
   }

    return 0;
}

// DEFINE Helper Functions
int roll()
{
    // rolls a six sided die
    // TODO
    return 6;
}