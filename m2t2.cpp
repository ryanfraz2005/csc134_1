#include <iostream>
using namespace std; 

int main ()
{
    double meal = 5.99;
    double tax_percent = 0.08; 
    double tax_amount = meal * tax_percent;
    double total = meal + tax_amount;

    cout << "Meal: $" << meal << endl;
    cout << "Tax: $" << tax_amount << endl;
    cout << "Total: $" << total << endl;

    return 0;
}