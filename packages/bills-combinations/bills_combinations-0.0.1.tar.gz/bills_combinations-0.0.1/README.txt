# bills_combinations

This is an example project demonstrating how to publish a python module to PyPI.

the function calculates all possible "bills" combinations in a "wallet" when given the amount of "money" that is desired.


# Installation

Run the following to install:

open Windows PowerShell (Fn+Alt+F12) and enter --> pip install bills_combinations


# Usage

from bills_combinations import bills_combinations

bills_in_wallet = [20, 20, 20, 10, 10, 10, 10, 10, 5, 5, 1, 1, 1, 1, 1]  # each number stands as a bill
print(bills_combinations(bills_in_wallet, 100))  # calling the function

output:

there are 5 combinations possible and they are [
					[20, 20, 20, 10, 10, 10, 10],
 					[20, 20, 20, 10, 10, 10, 5, 5],
 					[20, 20, 10, 10, 10, 10, 10, 5, 5],
 					[20, 20, 20, 10, 10, 10, 5, 1, 1, 1, 1, 1],
 					[20, 20, 10, 10, 10, 10, 10, 5, 1, 1, 1, 1, 1]]



