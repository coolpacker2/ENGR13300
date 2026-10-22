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

def create_dict():
    dictionary = {}
    #read file and extract the rows
    with open("py4_task3_input.txt", "r") as data:
        file = data.readlines()

    
    for i in range(len(file)):
        #split first
        file_split = file[i].split(":")
        #strip out the dictionary key
        file_param_name = file_split[0].strip()
        #strip out the data that will be appended to the list belonging to the dictionary key.
        file_param_data = file_split[1].strip()
        if file_param_name not in dictionary:
            dictionary[file_param_name] = []


        if file_param_name != 'Name':
            dictionary[file_param_name].append(float(file_param_data))
        else:
            dictionary[file_param_name].append(file_param_data)    
    return dictionary


def absorb_calc(absorbency, length, epsilon):
    #calculation that takes floats
    conc = absorbency/(length*epsilon)
    return conc
    
    

def main():
    dictionary = create_dict()
    print(f"The name of the substance is {dictionary['Name'][0]}")
    for i in dictionary["Absorbency"]: #pass dictionary data through the function for however many absorbencies must be tested.
        c = absorb_calc(length = dictionary["Path Length"][0], epsilon=dictionary["Molar Extinction Coefficient"][0], absorbency=i)
        print(f"For {i:.4f} absorbency value, the concentration is {c:.7f}")    
    
    



if __name__ == "__main__":
    main()
