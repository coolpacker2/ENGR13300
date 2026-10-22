"""
Course Number: ENGR 13300
Semester: Fall 2026

Description:
    Replace this line with a description of your program.

Assignment Information:
    Assignment:     17.2.2 Py5 Team 2
    Team ID:        LC5 - 16 
    Author:         Stephen Lim, lim573@purdue.edu
    Date:           10/08/2026

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

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def load_img(file_path):
    #open image with PIL
    OpenImage = Image.open(file_path)
    #convert image to numpy float array
    ArrayImage = np.array(OpenImage, dtype=float)
    #ArrayImage.shape[2] is the amount of channels, [0][1] are height and width
    if len(ArrayImage.shape) == 3 and ArrayImage.shape[2] == 4:
        ArrayImage = ArrayImage[:, :, :3] #convert to 3 channels (rgb)
    #if the max value is not normalized, normalize the array
    NormalArray = []

    if ArrayImage.max() > 1.0:
        NormalArray = ArrayImage / 255.0
        
    TempArray = np.zeros_like(NormalArray)
    
    #if the image is grayscale (2 dimensions)
    if NormalArray.ndim == 2:
        for r in range(len(NormalArray)):
            for g in range(len(NormalArray[r])):
                v = NormalArray[r, g]
                if v <= 0.04045:
                    TempArray[r, g] = v / 12.92
                else:
                    TempArray[r, g] = ((v + 0.055) / 1.055) ** 2.4
                    
    #if the image is color (3 dimensions)
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

def rgb_to_grayscale(rgb_array):
    #apply formula across channels to produce a 2D array (height, width)
    gray_img = (0.2126 * rgb_array[:, :, 0] + 
                0.7152 * rgb_array[:, :, 1] + 
                0.0722 * rgb_array[:, :, 2])
    return gray_img
    

def main():
    #ask the user for the image file path and load it
    file_path = input("Enter the path of the image you want to load: ")
    image_array = load_img(file_path)
    
    #check if the image is RGB (has 3 dimensions and 3 channels)
    
    if len(image_array.shape) == 3 and image_array.shape[2] == 3:
        choice = input("Would you like to convert to grayscale? ")
        if choice == 'yes':
            image_array = rgb_to_grayscale(image_array)
            plt.imshow(image_array, cmap='gray')
    else:
        plt.imshow(image_array, cmap='gray')
    #display the image
        
        
    plt.axis('off')  #hide axis ticks 
    plt.show()


if __name__ == "__main__":
    main()
