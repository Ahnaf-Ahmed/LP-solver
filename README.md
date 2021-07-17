# LP-solver

## Brief Overview
This program is written in python 3 and only requires the numpy and sys library. It takes input from standard input and outputs to standard output It can be run by typing python main.py into the command line. Python3 main.py may be required if you have python 2 installed

This program creates a dictionary from the values given and uses the simplex algorithm to pivot and find the optimal value. In the case it is optimal it will outpul optimal, then the optimal value on the next line, then all the x values needed to attain that optimal value in one line on the line after. 

In the case that the dictionary is unbounded or infeasible it will output unbounded or infeasible respectively.

## Description
The program solves LPs by using the dictionary based simplex algorithm.

Once the dictionary is created the program will first check for infeasibility and if it seems initially infeasible, a dual dictionary will be created. This dual will first be checkeed for bounds, in the case it is unbounded the program will return that the original LP is infeasible. if it isnt unbounded it will be checked for feasibility. If it is infeasible, the objective row of the original LP will be turned to zeroes and the dual will be reconstructed. The simplex method will be run on the dual LP with the leaving and entering variables being switched before fed into the pivot method for the primal LP. This will loop until no entering variables are found at which point the primal LP will be optimal and returned.

In the event that it is not infeasible, the program will check the bounds. After it will find the proper entering and leaving variables using hte largest coefficient method, AKA Dantzig's rule. Then it will start hte pivoting process. At the start of the pivoting it will record the objective value and then compare it to the objective value after pivoting. If they are the same then a global degenerate flag will be set and the next time entering and leaving variables are found, it will use Bland's rule instead of Dantzig's to prevent cycling. This process repeats until no entering and leaving variables are returned, at which point the dictionary has reached its optimal state.

## Extra features
The extra feature chosen is the Primal-Dual Methods where a dual LP is constructed and used instead of solving for an auxillary problem.