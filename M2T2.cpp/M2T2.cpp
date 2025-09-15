/*
M2T2 - Restaurant Reciept
Ryan Frazee
9/15/25
*/

#include <iostream>
#include <iomanip>
using namespace std;

int main()
{
    string item = "Burger";
    double menu_price = 5.99;
    double tax_percent = 0.08;
    double tax_amount;
    double total_price;

    cout << "Order up" << endl;
    cout << item << " (x1)";
    cout << "\t$" << menu_price << endl;

    tax_amount = menu_price + tax_percent;
    total_price = menu_price + tax_amount;

    cout << setprecision(2) << fixed;
    cout << "Tax:   \t\t$" << tax_amount << endl;
    cout << "Total: \t\t$" << total_price << endl;

    return 0;
}