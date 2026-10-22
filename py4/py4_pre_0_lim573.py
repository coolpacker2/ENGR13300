"""
Course Number: ENGR 13300
Semester: Fall 2026

Description:
    Write a new CSV file, plot two figures using matplotlib, label axis and title

Assignment Information:
    Assignment:     py4 pre 0
    Team ID:        LC5 - 16
    Author:         Stephen Lim, lim573@purdue.edu
    Date:           9/25/2026

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

import matplotlib.pyplot as plt
import pandas as pd


def main():
    csv_file = pd.read_csv('py4_pre_0_data.csv', header= None)
    #: will access all rows of a column and the number will say which column
    day = csv_file.iloc[:, 0]
    quantity_traded = csv_file.iloc[:, 1]
    price = csv_file.iloc[:, 2]

    #set figure size
    plt.figure(figsize=(12, 5))
    
    

    #create csv file
    dollar_volume = (price*quantity_traded).astype(float)
    #dollar_volume should be a float
    new_csv_file = pd.DataFrame({'day': day, 'dollar_volume': dollar_volume})

    new_csv_file.to_csv('py4_pre_0_lim573.csv',index = False, header= None)

    #labels help make the legend
    #split graph 1
    plt.subplot(1, 2, 1)
    #-o tells it to trace the points together
    plt.plot(day,price, '-o', label = 'Price')
    plt.title('Stock Price vs Time')
    plt.xlabel('Time (days)')
    plt.ylabel('Price (USD)')
    plt.legend()

    #split graph 2
    plt.subplot(1, 2, 2)
    plt.title('Dollar Volume vs Time')
    plt.bar(day, dollar_volume, label = 'Dollar Volume')
    plt.xlabel('Time (days)')
    plt.ylabel('Volume (USD)')
    plt.legend()

    #make sure titles and axis labels don't cross
    plt.tight_layout()
    plt.show()

    


if __name__ == "__main__":
    main()
