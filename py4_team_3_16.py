"""
Course Number: ENGR 13300
Semester: Fall 2026

Description:
    Calculate concentration from a given list of values (length, epsilon, absorbancy) in an input txt file.

Assignment Information:
    Assignment:     16.2.3 Py4 Team 3 (for Python 4 Team task 3)
    Team ID:        LC5 - 16
    Author:         Stephen Lim, lim573@purdue.edu
    Date:           10/01/2026

Contributors:
    Nathan Crute, ncrute@purdue.edu
    Hari Ghatpande, sghatpan@purdue.edu
    Zane Danger Clark, clar1439@purdue.edu

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


#read file and extract the rows
with open("py4_task3_input.txt", "r") as data:
    file = data.readlines()
#define data read from the file
length = file[1]
episilon = file[2]
absorbancy1 = file[3]
absorbancy2 = file[4]
absorbancy3 = file[5]


def absorb_calc(length, epsilon, absorbancy):
    #first data filter is split
    f1l = length.split(":")
    f1e = epsilon.split(":")
    f1a = absorbancy.split(":")
    #second filter is strip and turn into float
    f2l = float(f1l[1].strip())
    f2e = float(f1e[1].strip())
    f2a = float(f1a[1].strip())
    conc = f2a/(f2l*f2e)
    data = [f2a, conc]
    #return a list of data
    return data
    
    

def main():
    print("The name of the substance is Glucose Oxidase")
    #concentration calculations with parameters put in
    c1 = absorb_calc(length = length, epsilon=episilon, absorbancy=absorbancy1)
    c2 = absorb_calc(length = length, epsilon=episilon, absorbancy=absorbancy2)
    c3 = absorb_calc(length = length, epsilon=episilon, absorbancy=absorbancy3)
    #print results and draw data out of the list.
    print(f"For {c1[0]:.4f} absorbency value, the concentration is {c1[1]:.7f}")
    print(f"For {c2[0]:.4f} absorbency value, the concentration is {c2[1]:.7f}")
    print(f"For {c3[0]:.4f} absorbency value, the concentration is {c3[1]:.7f}")



if __name__ == "__main__":
    main()
