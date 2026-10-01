"""
Course Number: ENGR 13300
Semester: Fall 2026

Description:
    Using a python program to estimate integrals using the McLauren Series Formula and loops. 

Assignment Information:
    Assignment:     15.3.2 py3 ind 2 
    Team ID:        LC5 - 16
    Author:         Stephen Lim, lim573@purdue.edu
    Date:           9/29/2026

Contributors:
    Name, login@purdue [repeat for each]

    My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.

Academic Integrity Statement:
    I have not used source code obtained from any unauthorized
    source, either modified or unmodified; nor have I provided
    another student access to my code.  The project I am
    submitting is my own original work.
"""

import math
import numpy as np
def calculate_integral(a,b,dec,un):
    sum = 0
    for i in range(un+1): #this +1 fixes the delay by making n=0 actually loop 1 time
        #below we calculate the integral approximation
        sum += np.power(-1,i)*(np.power(b,(2*i+1))-np.power(a,(2*i+1)))/((2*i+1)*(math.factorial(2*i+1)))
    return f"{sum:.{dec}f}" #set it to the amount of decimal places requested


    
def main():
    user_a = float(input("Enter the lower limit of integration: "))
    user_b = float(input("Enter the upper limit of integration: "))
    user_dec = int(input("Enter the number of decimal places for convergence: "))
    user_terms = int(input("Enter the maximum number of terms: "))
    
    last_num = 0
    count = 0
    # if the user put in a negative amount of terms, warn them
    if user_terms < 0:
        print("Error: Input a positive integer")
        return
    else:
        print("\nApproximations:")
        for i in range(user_terms):
            if last_num == calculate_integral(user_a, user_b, user_dec, i):
                count+=1 #track repeats
            else:
                count = 0 #reset counter
            if count!=3:
                print("n = " + str(i) + ": sum = " + str(calculate_integral(user_a, user_b, user_dec, i)))
                last_num = calculate_integral(user_a, user_b, user_dec, i) #set the last num to the new number
            else: #series converged
                print("The integral from " + str(user_a) + " to " + str(user_b) + " is estimated to be " + str(last_num) + ".")
                print("Total number of terms: " + str(i))
                return
    #if the count is less than 3, warn that the series did not converge fully yet to that many decimals
    if count < 3:
        print("Error: The approximation did not converge to " + str(user_dec) + " decimal places with only " + str(user_terms) + " terms.")
        
if __name__ == "__main__":
    main()
