"""
Course Number: ENGR 13300
Semester: e.g. Spring 2026

Description:
    Replace this line with a description of your program.

Assignment Information:
    Assignment:     14.3.2 py2 ind 2 main
    Team ID:        LC5 - 16
    Author:         Stephen Lim, lim573@purdue.edu
    Date:           09/23/2026

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

from py2_ind_2_functions_lim573 import standard, ramp, round


def main():
     #put functions in table to call later
    vol_types = {
    "Standard": standard,
    "Ramp": ramp,
    "Round": round
    } 
    vol_type = input("Enter the name of the pool to calculate (Standard, Ramp, or Round): ")
    if not vol_types.get(vol_type): #if not a valid volume type print error
        print("Please run the program again and enter a valid pool name.")
    else:
        vol_l1 = int(input("Enter the surface length or radius. "))
        vol_l2 = int(input("Enter the surface width or bottom radius. "))
        vol_ds = int(input("Enter the shallow end depth. "))
        vol_dd = int(input("Enter the deep end depth. "))
        selected_function = vol_types.get(vol_type)
        print("The volume of the " + vol_type + " pool with your dimensions is " + f"{selected_function(vol_l1, vol_l2, vol_ds, vol_dd):,.2f}" + " gallons.")

   

    
        
    

    


if __name__ == "__main__":
    main()
