"""
Course Number: ENGR 13300
Semester: Fall 2026

Description:
    The goal is to apply gaussian filter instead of a mean filter to a grayscale image to blur it.

Assignment Information:
    Assignment:    7.2.3 tp1 team 3
    Team ID:        LC5 - 16
    Author:        Stephen Lim, lim573@purdue.edu
    Date:          10/17/2026

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
import math

def load_img(OpenImage):
    #convert image to numpy float array
    ArrayImage = np.array(OpenImage, dtype=float)
    #ArrayImage.shape[2] is the amount of channels, [0][1] are height and width
    if len(ArrayImage.shape) == 3 and ArrayImage.shape[2] == 4:
        ArrayImage = ArrayImage[:, :, :3] #convert to 3 channels (rgb)
    #if the max value is not normalized, normalize the array
    NormalArray = []

    if ArrayImage.max() > 1.0:
        NormalArray = ArrayImage/255.0
    else: NormalArray = ArrayImage

    #shortened by hari
    linear_array = np.zeros_like(NormalArray, dtype=np.float32)
    is_dark = NormalArray <= 0.04045
    linear_array[is_dark] = NormalArray[is_dark]/12.92
    linear_array[~is_dark] = ((NormalArray[~is_dark] + 0.055)/1.055)**2.4

    return linear_array

def rgb_to_grayscale(rgb_array):
    #apply formula across channels to produce a 2D array (height, width)
    gray_img = (0.2126 * rgb_array[:, :, 0] + 
                0.7152 * rgb_array[:, :, 1] + 
                0.0722 * rgb_array[:, :, 2])
    return gray_img

def create_gaussian_kernel(sigma):
    #determine odd kernel size
    kernel_size = 2*math.ceil(3*sigma) + 1 #math.ceil to round up
    k_half = int(kernel_size/2)
    
    #create an empty 2d matrix of zeros with the target size
    kernel = np.zeros((kernel_size, kernel_size), dtype=float)
    
    #go through every index in the kernel
    for i in range(kernel_size):
        for j in range(kernel_size):
            #calculate offset from the center (0, 0)
            y = i - k_half
            x = j - k_half
            
            # apply the gaussian formula for this specific cell
            kernel[i, j] = np.exp(-(x**2 + y**2)/(2*sigma**2))
            
    #normalize the kernel so all elements sum to 1
    kernel = kernel/np.sum(kernel)
    
    return kernel

def gaussian_filter(image, sigma):
    #apply gaussian filter using padding and sliding window
    kernel = create_gaussian_kernel(sigma)
    kernel_size = kernel.shape[0]
    pad = int(kernel_size/2)

    #pad the image
    padded_image = np.pad(image, pad, mode='constant', constant_values=0)
    output = np.zeros_like(image, dtype=float)

    #go through each pixel and apply the gaussian filter
    h, w = image.shape
    for i in range(h):
        for j in range(w):
            window = padded_image[i:i+kernel_size, j:j+kernel_size]
            output[i, j] = np.sum(window*kernel)

    #convert to uint8 if it is an int array and return it
    if np.issubdtype(image.dtype, np.integer):
        return np.round(output, 6).astype(image.dtype) #round to 6 to fix the weird autograder - credit to ai (claude)
    return output

def main():
    #get filename from user
    file_path = input("Enter the path to the image file: ")
    
    #open and load image
    OpenImage = Image.open("ref_images/" + file_path)
    img = load_img(OpenImage)
    gray_img = rgb_to_grayscale(img)
    
    #apply gaussian filter
    sigma = 1.0
    smoothed_img = gaussian_filter(gray_img, sigma)
    #the file name should be the suggested name under image tests
    #split name before saving as well
    file_name = file_path.split(".png")
    out_filename = f"{file_name[0]}_smooth.png"
    #save result
    plt.imsave(out_filename, smoothed_img, cmap='gray')
    #display image
    plt.figure()
    plt.imshow(smoothed_img, cmap='gray')
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    main()