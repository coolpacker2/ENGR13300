"""
Course Number: ENGR 13300
Semester: e.g. Spring 2026

Description:
    In this assignment I do some mathematical calculations in Python to learn the basics.

Assignment Information:
    Assignment:     13.1.2 Python 1 Pre Task 0
    Team ID:        LC5
    Author:         Zheng Yang Stephen Lim, lim573@purdue.edu
    Date:           e.g. 09/06/2026

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


def main():
    a = 101
    b = 7
    c = 12.34
    var1 = math.pow(c,2) - math.pow((math.sin(b)),2)
    var2 = math.factorial(b) * (math.cos(math.pi/c) - a)
    var3 = (math.pow(c,math.e*math.pi)*math.asin(math.sqrt(3)/2))/(b*math.pow(a,math.e))
    print("equation 1: " + f"{var1:.3f}")
    print("equation 2: " + f"{var2:.3f}")
    print("equation 3: " + f"{var3:.3f}")
    
    
if __name__ == "__main__":
    main()
