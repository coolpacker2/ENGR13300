"""
Course Number: ENGR 13300
Semester: Fall 2026

Description:
    Team task 2 part b program

Assignment Information:
    Assignment:     13.2.2 Team task 2
    Team ID:        LC5 - 16
    Author:         Zheng Yang Stephen Lim, lim573@purdue.edu
    Date:           09/11/2026

Contributors:
    Nathan Crute, ncrute@purdue.edu
    Zane Clark, clar1439@purdue.edu
    Hari Ghatpande, sghatpan@purdue.edu

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


string_1 = input("Enter the first string: ")
string_2 = input("Enter the second string: ")
char_1 = []
char_2 = []

#turn str 1 into char list
char_1 = list(dict.fromkeys(string_1.lower()))
#turn str 2 into char list
char_2 = list(dict.fromkeys(string_2.lower()))


#extract similarities using set intersection
similarities = list(set(char_1) & set(char_2))
#extract differences in char_1 using set difference
diff_char_1 = list(set(char_1) - set(char_2))
#extract differences in char_2 using set difference
diff_char_2 = list(set(char_2) - set(char_1))
#sort all
char_1.sort()
char_2.sort()
similarities.sort()
diff_char_1.sort()
diff_char_2.sort()

print("Characters in first string:" + "\n" +  str(char_1))
print("Characters in second string:" + "\n" + str(char_2))
print("Characters in both strings:" + "\n" + str(similarities))
print("Characters in the first string but not the second:" + "\n" + str(diff_char_1))
print("Characters in the second string but not the first:" + "\n" + str(diff_char_2))