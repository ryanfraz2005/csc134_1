#include <iostream>
using namespace std;

int main () {
    int maxHP = 100;
    int hp = 30;
    const int healing = 10;
    string empty = "🟥";
    string full = "🟩";

    cout << "Resting until healed." << endl;
    while (hp < maxHP) {
        hp += healing;
        
        cout << "[";
        for (int i=0 ; i < hp/10; i++){
            cout << full;
        }
        for (int i=0; i < (100-hp)/10; i++){
         cout << empty;
        }
        cout << "]" << endl;
         cout << "HP: " << hp << "/" << maxHP << endl;
    }
    
    cout << "Fully rested." << endl;
}