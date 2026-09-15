"""
Course Number: ENGR 13300
Semester: e.g. Spring 2026

Description:
    I am calculating the total capacitance of 2 capacitors (1 is input) in series and parallel using a Python Program.
Assignment Information:
    Assignment:     py1 ind 2
    Team ID:        LC5 - 16
    Author:         Stephen Lim, lim573@purdue.edu
    Date:           9/13/2026

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
    u1 = float(input("Input the capacitance of the first capacitor [μF]: "))
    #little bonus, don't let u1 be 0

    if u1 <= 0:
        print("The first capacitor cannot be 0 μF. Please enter a valid capacitance.")
        return    
    u2 = math.exp(3)*math.sqrt(5)
    # Calculate the total capacitance for series and parallel
    series = 1/(1/u1 + 1/u2)
    parallel = u1 + u2
    
    # Format the values with the µF symbol first to avoid confusion in print statement
    u1_str = f"{u1:.1f} µF"
    u2_str = f"{u2:.1f} µF"
    series_str = f"{series:.1f} µF"
    parallel_str = f"{parallel:.1f} µF"


    #< and > are used to align the text in the output, the number is the amount of characters that the output will be forced into
    # Print headers and formatted rows (12-space width for number columns)
    print(f"{'Type':<8}{'First':>12}{'Second':>12}{'Total':>12}")
    print(f"{'Series':<8}{u1_str:>12}{u2_str:>12}{series_str:>12}")
    print(f"{'Parallel':<8}{u1_str:>12}{u2_str:>12}{parallel_str:>12}")
    #1f obviously sets it to one decimal place

if __name__ == "__main__":
    main()
