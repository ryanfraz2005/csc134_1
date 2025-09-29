/*
M3LAB2 - Letter Grade (changed to Game Mechanics Test)
CSC 134
Ryan Frazee
9/29/25
*/

#include <iostream>
#include <cstdlib> // for rand() and srand()
#include <ctime> // for time()

using namespace std;

void letter_grader();
void combat();
int roll();

int main() 
{
    letter_grader();
    combat();

    return 0;
}

// DEFINE the other functions here

void letter_grader()
{
    // input a number grade
    // respond with a letter grade

    double num_grade;
    string letter_grade;
    // constants for grade breakpoints
    const double A_GRADE = 90;
    const double B_GRADE = 80;
    const double C_GRADE = 70;
    const double D_GRADE = 60;

    cout << "Enter a number grade 0-100: ";
    cin >> num_grade;

    // Create the if statements
    if (num_grade >= A_GRADE){
        letter_grade = "A";
    }
    else if (num_grade >= B_GRADE){
        letter_grade = "B";
    }
    else if (num_grade >= C_GRADE){
        letter_grade = "C";
    }
    else if (num_grade >= D_GRADE){
        letter_grade = "D";
    }
    else {
        // must be under a D...
        letter_grade = "F";
    }


    // Output the answer
    cout << "A number grade of " << num_grade << " is: " << letter_grade;
    cout << endl << endl;

}

void combat () {
    /*
    A simple D&D style combat demo
    Attack roll + bonus >= armor class? The hit, else
    */
   // variables
   int attack_roll, attack_bonus, enemy_armor;
   srand(time(0));

   cout << "You are fighting a goblin." << endl;
   cout << "Enter your roll: ";
   cin >> attack_roll;
   cout << "Enter attack bonus: ";
   cin >> attack_bonus;
   cout << "Enter armor class: ";
   cin >> enemy_armor;

   // Roll to hit
   attack_roll = roll();
   cout << "Roll: " << attack_roll << " + " << attack_bonus << " = " << attack_roll+attack_bonus << endl;
   if (attack_roll + attack_bonus >= enemy_armor) {
    cout << "Hit!" << endl;
   }
   else {
    cout << "Miss!" << endl;
   }

   // try again?
   cout << "Again? (y/n): ";
   string again;
   cin >> again;
   if (again == "y") {
    // just call the function again!
    combat();
   }

}

int roll() {
    const int SIDES = 20;
    int my_roll;
    my_roll = (rand() % SIDES) + 1;
    return my_roll;
   }
