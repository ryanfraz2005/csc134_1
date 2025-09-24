#include <iostream>
using namespace std;
// ========== FUNCTION PROTOTYPES ==========
// Declare all your "rooms" up here
void tavern(); // Starting location
void forest(); // A possible path
void trail1();
void trail2();
void village();
void castle1(); // Another path
void castle2();
void gameOver(); // An ending
void victory(); // Another ending
// ========== MAIN FUNCTION ==========
int main()
{
cout << "==================================" << endl;
cout << " WELCOME TO YOUR ADVENTURE " << endl;
cout << "==================================" << endl;
cout << endl;
// Start the adventure!
tavern();
cout << "\n=== THE END ===" << endl;
return 0;
}
// ========== LOCATION FUNCTIONS ==========
// Each function is one "node" in your story
void tavern()
{
cout << "\nYou wake up in a dusty tavern." << endl;
cout << "The bartender tells you about the trouble in the kingdom. A group of people are invading the castle." << endl;
cout << "Will you help? (1 = Yes, 2 = No): ";
int choice;
cin >> choice;
if (choice == 1)
{
cout << "\n'Brave soul! Head to the forest!'" << endl;
forest(); // Go to forest function
}
else
{
cout << "\n'Coward! Get out of my tavern!'" << endl;
gameOver(); // Go to game over
}
}
void forest()
{
// TODO: Add your forest scene here!
cout << "\nYou find a crossroad in the forrest." << endl;
cout << "Where will you go? (1 = Right, 2 = Left): ";
int choice;
cin >> choice;
if (choice == 1)
{
    cout << "\nYou go down the path on the right" << endl;
    trail1();
}
else
{
    cout << "\nYou go down the path on the left" << endl;
    trail2();
}
}
void trail1()
{
    cout << "\nDeadend. Go back." << endl;
    forest();
}
void trail2()
{
    cout << "\nAfter a long walk, you eventually find your way into the kingdom." << endl;
    cout << "Enter the castle? (1 = Yes, 2 = No): " << endl;
    int choice;
    cin >> choice;
    if (choice == 1)
    {
        cout << "\nYou enter into the castle." << endl;
        castle1();
    }
    else 
    {
        cout << "\nYou decide not enter the castle yet." << endl;
        cout << "You continue your previous path and find your way into a village." << endl;
        village();
    }

}
void village()
{
    cout << "You tell the villagers there is trouble at the castle." << endl;
    cout << "They come up with a plan to save the kingdom. Will you help? (1 = Yes, 2 = No): " << endl;
    int choice;
    cin >> choice;
    if (choice == 1)
    {
        cout << "\nYou accompany the armed villagers back to the kingdom and into the castle." << endl;
       castle2();
    }
    else 
    {
        cout << "\nThe villagers call you a coward." << endl;
        gameOver();
    }
   
}
void castle1()
{
// TODO: Add your castle scene here!
cout << "\nYou enter into the castle and are attacked by a group of people who were invading the castle." << endl;
cout << "You were no match." << endl;
gameOver();
}
void castle2()
{
    cout << "\nYou make your way back to the castle." << endl;
    cout << "You all were attacked by the invaders. You fight back and after a long battle you emerge victorious!" << endl;
    victory();
}
void gameOver()
{
cout << "\n💀 GAME OVER 💀" << endl;
cout << "Your adventure ends here." << endl;
}
void victory()
{
cout << "\n💀 VICTORY! 💀" << endl;
cout << "You saved the kingdom!" << endl;
}