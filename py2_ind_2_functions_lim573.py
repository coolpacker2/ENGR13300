"""
Course Number: ENGR 13300
Semester: e.g. Spring 2026

Description:
    The script to store the function of calculated volumes for the 3 different pool shapes (standard, ramp, round). 

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

import math

#split all volumes into different volumes to make it easier to read.
#volume conv converts to gallons

def volume_conv(value):
    return (value*(12**3))/231

def standard(l1, l2, ds, dd):
    volume_of_both_parrallelograms = (l1/3)*(ds+dd)*l2 #(l1/3)*(ds+dd)*l2 combines the shapes together and then calculate volume, so ds and dd can be added and multiplied by length then width
    volume_of_rectangular_prism = ds*(l1/3)*l2
    volume =  volume_conv(volume_of_both_parrallelograms + volume_of_rectangular_prism)
    if l1 < 0 or l2 < 0 or ds < 0 or dd < 0:
        print("Please enter valid dimensions.")
    else:
        return volume

def ramp(l1, l2, ds, dd):
    volume_of_triangle = (1/2)*(ds)*(l1/3)*(l2)
    volume_of_rectangular_prism = (ds)*(l1/3)*(l2)
    volume_of_parrallelogram = (1/2)*(ds+dd)*(l1/3)*(l2)
    volume = volume_conv(volume_of_triangle+volume_of_rectangular_prism+volume_of_parrallelogram)
    if l1 < 0 or l2 < 0 or ds < 0 or dd < 0:
        print("Please enter valid dimensions.")
    else:
        return volume

def round(l1, l2, ds, dd):
    volume_of_cylinder = ds*math.pi*l1**2
    volume_of_cone = (1/3)*math.pi*(dd-ds)*((l1**2) + (l1*l2) + (l2**2)) #volume of conical frustum (bottom part of pool) according to google.
    volume = volume_conv(volume_of_cylinder + volume_of_cone)
    if l1 < 0 or l2 < 0 or ds < 0 or dd < 0:
        print("Please enter valid dimensions.")
    else:
        return volume



