"""
Course Number: ENGR 13300
Semester: e.g. Spring 2026

Description:
    Replace this line with a description of your program.

Assignment Information:
    Assignment:     15.1.2 py3 ind task 0
    Team ID:        LC5 - 16
    Author:         Stephen Lim, lim573@purdue.edu
    Date:           9/20/2026

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

""" Write any import statements here (and delete this line)."""

#two parameters, width and length
def build_matrix(w, l):
    matrix = []
    num = 0
    # two variables that track the matrix number and data that don't reset
    for num_l in range(l):
        row = []
        # reset the row everytime it goes to a new row
        for num_w in range(w):
            num+=1 #add to the number
            row.append(num)
        matrix.append(row) #add the finished row into the matrix

    return matrix

def traverse_with_for(X):
    print("FOR loop traversal:")
    for row in range(len(X)):
        for ind_comp in range(len(X[row])):
            print("X[" + str(row) + "," + str(ind_comp) + "] = " + str(X[row][ind_comp]))

def traverse_with_while(X, stop):
    print("WHILE loop traversal: ")
    row = 0
    
    while row in range(len(X)):
        ind_comp = 0
        while ind_comp in range(len(X[row])):
            if X[row][ind_comp] < stop:
                print("X[" + str(row) + "," + str(ind_comp) + "] = " + str(X[row][ind_comp]))
            else:
                break
            ind_comp+=1
        row+=1
def main():
    print("Enter Matrix Dimensions")
    user_w = int(input("Enter rows: "))
    user_l = int(input("Enter columns: "))
    traverse_with_for(build_matrix(user_w, user_l))
    print("\n" + "Enter Matrix Dimensions")    
    user_w = int(input("Enter rows: "))
    user_l = int(input("Enter columns: "))
    user_stop = int(input("Enter Stop Value: "))
    traverse_with_while(build_matrix(user_w, user_l), user_stop)
if __name__ == "__main__":
    main()
