"""
Course Number: ENGR 13300
Semester: Fall 2026

Description:
    We use python to normalize image bit values and then linearize those values and print out the mean of those linearized values.

Assignment Information:
    Assignment:     17.1.2 Py5 pre 0 (for Python 5 Pre Task 0)
    Team ID:        LC5 - 16
    Author:         Stephen Lim, lim573@purdue.edu
    Date:           10/03/2026

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

import numpy as np
from PIL import Image

def normalize_image(ImageArray):
    #RGB values range from 0 to 255, dividing a value by 255 gives us a list between 0 to 1
    return ImageArray / 255.0

def linearize_image(NormalArray):
    TempArray = np.zeros_like(NormalArray)
    
    # if the image is grayscale (2 dimensions)
    if NormalArray.ndim == 2:
        for r in range(len(NormalArray)):
            for g in range(len(NormalArray[r])):
                v = NormalArray[r, g]
                if v <= 0.04045:
                    TempArray[r, g] = v / 12.92
                else:
                    TempArray[r, g] = ((v + 0.055) / 1.055) ** 2.4
                    
    # if the image is color (3 dimensions)
    else:
        for r in range(len(NormalArray)):
            for g in range(len(NormalArray[r])):
                for b in range(len(NormalArray[r][g])):
                    v = NormalArray[r][g][b]
                    if v <= 0.04045:
                        TempArray[r][g][b] = v / 12.92
                    else:
                        TempArray[r][g][b] = ((v + 0.055) / 1.055) ** 2.4
                        
    return TempArray


def mean_channel(LinearArray, channel_index): 
    #if the array only has 2 dimensions, it is grayscale, return 0
    if LinearArray.ndim == 2:
            return 0
    else:
        Channel = np.mean(LinearArray[:, :, channel_index])      
        return Channel




def main():
    #ask the user for the image filename
    filename = input("Enter the filename of the image: ")
    
    # open the image using PIL
    OpenImage = Image.open(filename)

    #turn the PIL image into a NumPy float array
    ImageArray = np.array(OpenImage, dtype=float)
    #restrict the pixel values to the range [0.0, 1.0]
    NormalArray = normalize_image(ImageArray)
    LinearArray = linearize_image(NormalArray)
    print(f"Image: {filename}")
    print(f"Red Channel Mean: {mean_channel(LinearArray,0):.2f}")
    print(f"Green Channel Mean: {mean_channel(LinearArray,1):.2f}")
    print(f"Blue Channel Mean: {mean_channel(LinearArray,2):.2f}")

if __name__ == "__main__":
    main()
