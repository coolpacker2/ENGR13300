"""
Course Number: ENGR 13300
Semester: Fall 2026

Description:
    Take a template image and find it in a more broad image. Print out the location of the template and highlight on a plot the location of the template.

Assignment Information:
    Assignment:     17.2.1 py5 ind 2
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
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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
    else: NormalArray = ArrayImage
        
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

def ssd(grayscale_scene, grayscale_temp):
    scene_h = len(grayscale_scene)
    scene_w = len(grayscale_scene[0])

    temp_h = len(grayscale_temp)
    temp_w = len(grayscale_temp[0])
        
    
    #make sure temp doesn't exceed scene size
    out_h = scene_h - temp_h + 1
    out_w = scene_w - temp_w + 1
    #initialize a blank array
    R = np.zeros((out_h, out_w))
    
    #iterate through each pixel
    for i in range(out_h):
        for j in range(out_w):
            #take out regions of the scene that are the same size as the template
            region = grayscale_scene[i:i+temp_h, j:j+temp_w]
            
            R[i, j] = np.sum((region - grayscale_temp) ** 2)
            
    return R

def draw_rectangle(scene_rgb, temp_rgb, R):
    #get template dimensions
    temp_h = len(temp_rgb)
    temp_w = len(temp_rgb[0])
    #setup mins
    min_val = R[0][0]
    x_min = 0
    y_min = 0
    
    for i in range(len(R)):
        for j in range(len(R[0])):
            if R[i][j] < min_val:
                min_val = R[i][j]
                x_min = j  
                y_min = i
    #display the original scene image and draw a red rectangle at (x, y)
    plt.figure()
    plt.imshow(scene_rgb)
    
    #add the rectangle patch
    #matplotlib wants (x, y) coordinates for the rectangle origin
    plt.gca().add_patch(Rectangle((x_min, y_min), width=temp_w, height=temp_h, edgecolor='red', facecolor='none', lw=2))
    
    plt.axis('off')
    plt.show()
    
    return x_min, y_min

def main():
    #ask user for file paths
    scene_path = input("Enter the path of the scene image you want to load: ")
    temp_path = input("Enter the path of the template image you want to load: ")
    
    #load color image arrays
    scene_rgb = load_img(scene_path)
    temp_rgb = load_img(temp_path)
    
    #convert to grayscale arrays
    scene_gray = rgb_to_grayscale(scene_rgb)
    temp_gray = rgb_to_grayscale(temp_rgb)
    
    #call ssd to obtain the output map
    R_map = ssd(scene_gray, temp_gray)
    
    #display image and retrieve x, y coordinates
    x, y = draw_rectangle(scene_rgb, temp_rgb, R_map)
    print(f"The template is located at ({x}, {y})")
    


if __name__ == "__main__":
    main()
