#include <iostream>
#include <string>
#include <iomanip>
using namespace std;

void exercise1_healthRegen();
void exercise2_levelUpStats();
void exercise3_inventorySystem();

int main() {

int choice;


cout << "==================================" << endl;
cout << "    LAB 7: LOOP FUNDAMENTALS      " << endl;
cout << "==================================" << endl;
cout << "1. Exercise 1: Health Regeneration" << endl;
cout << "2. Exercise 2: Level Up Stats" << endl;
cout << "3. Exercise 3: Inventory System" << endl;
cout << "4. Run All Exercises" << endl;
cout << "5. Exit" << endl;
cout << "==================================" << endl;
cout << "Choice: ";
cin >> choice;

switch(choice)
{
    case 1:
        exercise1_healthRegen();
        break;
    case 2:
        exercise2_levelUpStats();
        break;
    case 3:
        exercise3_inventorySystem();
        break;
    case 4:
        exercise1_healthRegen();
        cout << endl;
        exercise2_levelUpStats();
        cout << endl;
        exercise3_inventorySystem();
        break;
    case 5:
        cout << "Goodbye!" << endl;
        break;
    default:
        cout << "Invalid choice!" << endl;
}

return 0; 

}

void exercise1_healthRegeb() {
    cout << "\n=== EXERCISE 1: HEALTH REGENERATION ===" << endl;

int health = 30;
int maxHealth = 100;

cout << "Starting health: " << health << "/" << maxHealth << endl;
cout << "Resting to recover health..." << endl << endl;

while ( health < maxHealth) {
    health = health + 10;
    cout << "Health: " << health << "/" << maxHealth << endl;
}

cout << "Fully Recovered!" << endl;
}

void exercise2_levelUpStats() {
cout << "\n=== EXERCISE 2: LEVEL UP STATS ===" << endl;

// Base stats at level 0
const int BASE_STR = 10;
const int BASE_DEX = 8;
const int BASE_INT = 12;

// TODO: Display table header
cout << "Level |  STR  |  DEX  |  INT" << endl;
cout << "------|-------|-------|-------" << endl;

// TODO: Implement your for loop here
// HINT: for (int level = 1; level <= 10; level++)
// {
//     Calculate current stats based on level
//     Display formatted row
// }



// TODO: Calculate and display total growth
// (Level 10 stats - Level 1 stats)
}

void exercise3_inventorySystem() {

}


