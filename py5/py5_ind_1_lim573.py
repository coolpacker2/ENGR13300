"""
Course Number: ENGR 13300
Semester: Fall 2026

Description:
    Develop a Python program that produces a color distribution histogram of a user selected image to aid in image analysis. The program should allow the user to select from a list of all images in their images folder.

Assignment Information:
    Assignment:     17.3.1 py5 ind 1
    Team ID:        LC5 - 16
    Author:         Stephen Lim, lim573@purdue.edu
    Date:           10/13/2026

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

from PIL import Image
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

def linearize_image(image_array):
    temp_array = image_array.copy() #copy array
    if image_array.ndim == 2:
            for r in range(len(image_array)):
                for g in range(len(image_array[r])):
                    v = image_array[r, g]
                    if v <= 0.04045:
                        temp_array[r, g] = v / 12.92
                    else:
                        temp_array[r, g] = ((v + 0.055) / 1.055) ** 2.4
                        
        #if the image is color (3 dimensions)
    else:
        for r in range(len(image_array)):
            for g in range(len(image_array[r])):
                for b in range(len(image_array[r][g])):
                    v = image_array[r][g][b]
                    if v <= 0.04045:
                        temp_array[r][g][b] = v / 12.92
                    else:
                        temp_array[r][g][b] = ((v + 0.055) / 1.055) ** 2.4
    return temp_array

def load_image(file_path):
    #open image with PIL
    OpenImage = Image.open(file_path)
    image = np.array(OpenImage)
    #only unsigned 8-bit images are allowed
    if image.dtype != np.uint8:
        raise ValueError("The image datatype is not unsigned 8-bit integer")
    #convert image to numpy float array
    ArrayImage = np.array(OpenImage, dtype=float)
    #ArrayImage.shape[2] is the amount of channels, [0][1] are height and width
    if len(ArrayImage.shape) == 3 and ArrayImage.shape[2] == 4:
        ArrayImage = ArrayImage[:, :, :3] #convert to 3 channels (rgb)
                            
    return ArrayImage / 255.0

def calculate_luminance(rgb_array):
    #getheight and width ofimage
    height = rgb_array.shape[0]
    width = rgb_array.shape[1]
    total_luminance = 0
    num_pixels = 0
    #loop through 2d array
    if rgb_array.ndim == 2:
        for i in range(height):
            for j in range(width):
                #for grayscale, the pixel value itself is the luminance
                pixel_lum = rgb_array[i][j]
                total_luminance += pixel_lum
                num_pixels += 1
    else:
        for i in range(height):
            for j in range(width):
                #get r, g, b values for the current pixel
                r = rgb_array[i][j][0]
                g = rgb_array[i][j][1]
                b = rgb_array[i][j][2]
                #calculate luminance for this pixel
                pixel_lum = (0.2126*r) + (0.7152*g) + (0.0722*b)
                #add it to total
                total_luminance += pixel_lum
                num_pixels += 1
            
    #divide total by the num of pixels for the average
    average_luminance = total_luminance/num_pixels
    
    return np.float32(average_luminance)

def plot_pixel_intensity(image_array):
    #2 subplots
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    #first subplot, the linearized image
    axes[0].imshow(image_array, cmap = 'gray')
    axes[0].set_title("Linearized image")
    axes[0].axis('off')
    
    #second subplot, intensity histogram
    #is it grayscale?
    if image_array.ndim == 2:
        #turn 2D to 1D array
        channel_vals = image_array.flatten()
        axes[1].hist(channel_vals, bins=256, color='gray', alpha=0.5)
        axes[1].set_title("Grayscale Intensity Histogram")
    else:
        colors = ['red', 'green', 'blue']
        for i, color in enumerate(colors):
            #turn each channel's 2D array to a 1D array
            channel_vals = image_array[:, :, i].flatten()
            axes[1].hist(channel_vals, bins=256, color=color, alpha=0.5)
        axes[1].set_title("RGB Intensity Histogram")
    
    axes[1].set_xlabel("Pixel Value")
    axes[1].set_ylabel("Quantity")

    plt.tight_layout()
    plt.show()

def main():
    path = Path('images')
    files = list(path.iterdir())
    #put all the images in a dictionary to make it easier to check
    file_dict = {}
    print("Available images:")
    for i, image in enumerate(files):
            file_dict[i+1] = image
    for i in file_dict:
        if '.jpg' in file_dict[i].name or '.jpeg' in file_dict[i].name or '.png' in file_dict[i].name:
            print(f"{i}. {file_dict[i].name}")
    file_number = input("Select an image (q to quit): ")
    #ask the user for the image file path and load it
    if file_number == "q":
        return
    else:
        try:
            #try to convert the input string to an integer
            number = int(file_number)
            #check that the number is even in the dict
            if number in file_dict:
                image_array = load_image(files[number-1])
                lin_array = linearize_image(image_array)
                print(f"The average luminance of the image: {calculate_luminance(lin_array):.3f}")
                plot_pixel_intensity(lin_array)
                print()
                main()
            else:
                print("Invalid choice, please try again.")
                print()
                main()
        except ValueError:
            print("Invalid choice, please try again.")
            print()
            main()
        

if __name__ == "__main__":
    main()
