"""
Course Number: ENGR 13300
Semester: Fall 2026

Description:
    Team task 2 part b program. We aim to test random seeds and sum numbers of different types.

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

# """ Write any import statements here (and delete this line)."""
import random
from fractions import Fraction

def main():
    random.seed(int(input("Input the seed: ")))

    var_1 = round(random.random() * 100,3)
    var_2 = round(10 + random.random() * 40,3)
    var_3 = round(20 + random.random() * 20,3)
    var_4 = round(100 + random.random() * 100,3)
    var_1_frac = Fraction(var_1).limit_denominator(1000)
    var_2_frac = Fraction(var_2).limit_denominator(1000)
    var_3_frac = Fraction(var_3).limit_denominator(1000)
    var_4_frac = Fraction(var_4).limit_denominator(1000)

    var_sum_float = var_1 + var_2 + var_3 + var_4
    var_sum_fractions = Fraction.limit_denominator(var_1_frac + var_2_frac + var_3_frac + var_4_frac, 1000)
    print(f"First Random Number : {var_1}")
    print(f"Second Random Number : {var_2}")
    print(f"Third Random Number : {var_3}")
    print(f"Fourth Random Number : {var_4}")
    print(f"Sum from decimals: {var_1} + {var_2} + {var_3} + {var_4} = {var_sum_float}")
    print(f"Sum from fractions: {var_1_frac} + {var_2_frac} + {var_3_frac} + {var_4_frac} = {var_sum_fractions}")
if __name__ == "__main__":
     main()