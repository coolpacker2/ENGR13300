"""
Course Number: ENGR 13300
Semester: e.g. Spring 2026

Description:
    In this task, I will be writing a UDF to perform specific calculations in Python.

Assignment Information:
    Assignment:     14.1.2. Task 0 py2 pre 0
    Team ID:        LC5
    Author:         Stephen Lim, lim573@purdue.edu
    Date:           9/11/2026

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
#define calc_perform function as stated by the assignment instructions, with parameters a, b, and c
def calc_perform(a, b, c):
    if a>4:
        return (a**2 + math.cos(b) - math.log(c))/(b-c*a)
       #is a<4
    else:
        #return alternate result if a is less than or equal to 4
        return math.sqrt(a+b)/(math.factorial(c)+math.sin(b))

def main():
    #define variables to make it more flexible when changing paramaters of the calculation function
    a = float(input("Input a number for variable a: "))
    b = 135
    c = 3
    #print the results of the calculation
    print("The result of the function was " + str(round(calc_perform(a=a,b=b,c=c), 2)))


if __name__ == "__main__":
    main()
