/*
M3T2 - Craps Part 1
CSC 134
Ryan Frazee
9/22/25
Beginning of the craps game.
*/

#include <iostream>
#include <cstdlib> // for rand() and srand()
#include <ctime> // for time()
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
   int roll1;
   int roll2;
   int point;

   srand(0);

   roll1 = roll();
   roll2 = roll();
   int sum = roll1+roll2;
   cout << "ROLL: " << sum << endl;

   if ( (sum == 7) || (sum == 11) )
   {
    cout << "Seven or Eleven -- You win!" << endl;
   }
   else if ( (sum == 2) || (sum == 3) || (sum == 12) ) 
   {
    cout << "2,3,12 -- Sorry, you lose." << endl;
   }
   else
   {
    point = sum;
    cout << "Rolled a point." << endl;
    cout << "Your point is: " << point << endl;
   }

    return 0;
}

// DEFINE Helper Functions
int roll()
{
    int my_roll;
    my_roll = (rand() % 6) + 1; //1-6
    return my_roll;
}