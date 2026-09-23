"""
Course Number: ENGR 13300
Semester: e.g. Spring 2026

Description:
    Today I use Python to check the temperature and pressure of CO2 and ensure that the CO2 is safe to extract.

Assignment Information:
    Assignment:     14.3.1 py2 ind 1
    Team ID:        LC5 - 16
    Author:         Stephen Lim, lim573@purdue.edu
    Date:           09/22/2026

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


def check_status(temp, pres):
    #define constants as variables
    Carbon_Dioxide_Critical_Point_t = 304.2
    Carbon_Dioxide_Critical_Point_p = 73.8
    Maximum_Operating_Specification_t = 344.14
    Maximum_Operating_Specification_p = 137
    #temperature part of if statements
    if temp < Carbon_Dioxide_Critical_Point_t:
        print("CO2 is below the critical temperature.\nIncrease the temperature by at least " + str(f"{round(Carbon_Dioxide_Critical_Point_t-temp,2):.2f}") + " Kelvin.")
    elif temp == Carbon_Dioxide_Critical_Point_t and pres == Carbon_Dioxide_Critical_Point_p:
        print("CO2 is at the critical point.") #only check once
    elif temp>=(95/100) * Maximum_Operating_Specification_t:
        print("Warning! Reduce the temperature!\nDecrease the temperature by at least " +  str(f"{round(temp - (95/100) * Maximum_Operating_Specification_t,2):.2f}") + " Kelvin.") 
    else:
        print("Temperature is within safe operating conditions.")

    #pressure part of if statements
    if pres < Carbon_Dioxide_Critical_Point_p:
            print("CO2 is below the critical pressure.\nIncrease the pressure by at least " + str(f"{round(Carbon_Dioxide_Critical_Point_p-pres,2):.2f}") + " bar.")
    elif pres>=(95/100) * Maximum_Operating_Specification_p:
            print("Warning! Reduce the pressure!\nDecrease the pressure by at least " +  str(f"{round(pres - (95/100) * Maximum_Operating_Specification_p,2):.2f}") + " bar.") 
    elif pres!=Carbon_Dioxide_Critical_Point_p: #prevent it from printing this if it is critical
            print("Pressure is within safe operating conditions.")


def main():
    temperature = float(input("Enter the temperature of carbon dioxide in Kelvin: "))
    #start with temperature, global scope
    if temperature<0:
        print("Error: Please enter a valid temperature.")
    else:   
        #if passes first test, go for second
        pressure = float(input("Enter the pressure of carbon dioxide in bar: "))
        if pressure<0:
            #print message
            print("Error: Please enter a valid pressure.")
        else:
            #every test passed, run code
            check_status(temperature, pressure)


if __name__ == "__main__":
    main()
