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

void exercise1_healthRegen() {
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

const int BASE_STR = 10;
const int BASE_DEX = 8;
const int BASE_INT = 12;
int str, dex, intel;

cout << "Level |  STR  |  DEX  |  INT" << endl;
cout << "------|-------|-------|-------" << endl;

for (int level = 1; level <= 10; level++) {
    str = BASE_STR + (level * 2);
    dex = BASE_DEX + (level * 3);
    intel = BASE_INT + (level * 1);
cout << "  " << level << "   |  " << str << "   |  " << dex << "   |  " << intel << endl;
}
}

void exercise3_inventorySystem() {
cout << "\n=== EXERCISE 3: INVENTORY SYSTEM ===" << endl;

string equipment[5] = {
    "Iron Sword",
    "Leather Armor",
    "Health Potion",
    "Magic Ring",
    "Rope"
};

cout << "=== YOUR INVENTORY ===" << endl;

for (int i = 0; i < 5; i++)
{
    cout << (i + 1) << ". " << equipment[i] << endl;
}

cout << "======================" << endl << endl;

string searchTerm;
cout << "Enter item to search for: ";
cin.ignore(); 
getline(cin, searchTerm);

string searchItem;
bool found = false;
int position = -1;

for (int i = 0; i < 5; i++)
{
    if (equipment[i] == searchItem)
    {
        cout << "Found " << searchItem << " at slot " << (i+1) << endl;
        found = true;
    }
}
if (found)
{
    cout << "Found \"" << searchTerm << "\" in slot " 
         << (position + 1) << "!" << endl;
}
else
{
    cout << "\"" << searchTerm << "\" not found in inventory." << endl;
}
}


