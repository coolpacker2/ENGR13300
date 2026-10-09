"""
Course Number: ENGR 13300
Semester: Fall 2026

Description:
    Replace this line with a description of your program.

Assignment Information:
    Assignment:     17.2.3 Py5 Team 3
    Team ID:        LC5 - 16 
    Author:         Zane Danger Clark, clar1439@purdue.edu
    Date:           10/09/2026

Contributors:
    Nathan Crute, ncrute@purdue.edu
    Hari Ghatpande, sghatpan@purdue.edu
    Stephen Lim, lim573@purdue.edu

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


from PIL import Image, ImageOps

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

                            

    return TempArray, OpenImage #returns the PIL image from before so I can get its size later


def resize_image(original_image_array, new_size): 

    #inputs: np.array of original image (from the load_img), and tuple of size (width,height) for resized image 

    #outputs: resized img as a np array

    pil_img = Image.fromarray(original_image_array) #converts np array back to PIL array so we can use .resize() on it

    resized_img = pil_img.resize(new_size) #resizes using PIL's Image.resize() which only works on PIL images, not np arrays

    resized_np_array = np.array(resized_img) #converts resized PIL Image back to np array

    return resized_np_array


def pad_image(resized_img_array, target_size):

    #inputs: np array of resized image (from resize_image() function), and tuple of size(width, height) for padded image

    #outputs: padded img as a np array

    pil_img = Image.fromarray(resized_img_array) #converts

    padded_img = ImageOps.pad(pil_img, target_size, color=(0,0,0)) #pads image to target_size with black bars

    padded_np_array = np.array(padded_img)

    return padded_np_array

    



def main():

    file_path = input("Enter the path of the image you want to clean: ")

    img_array, img_PIL = load_img(file_path)

    img_array = (img_array * 255).astype(np.uint8) #converts the img_array from a bunch of floats in the [0.1,1.0] range to uint8 numbers in the [0,255] range because thats what resize_image() uses


    #prompts user to give width and height, then turns that into a tuple

    target_size_input = input("Enter the target width and height: ")

    w_and_h = [int(target_size_input.split(", ")[0]), int(target_size_input.split(", ")[1])] #splits the one input into a list of two specifications

    target_size_tuple = tuple(w_and_h) #tuple


    #check and accomodate for the aspect ratios and change values to prevent distortion

    original_ratio = img_PIL.size[0] / img_PIL.size[1] #divides width by height to get aspect ratio

    target_ratio = target_size_tuple[0] / target_size_tuple[1]

    if original_ratio >= target_ratio:

        intermediate_dimensions = [int(target_size_tuple[0] / original_ratio), int(target_size_tuple[1])] #list to be made into tuple

    else:

        intermediate_dimensions = [int(target_size_tuple[0]), int(target_size_tuple[1] / original_ratio)]

    

    intermediate_size = tuple(intermediate_dimensions) #tuple


    resized_array = resize_image(img_array, intermediate_size)

    padded_image = pad_image(resized_array, target_size_tuple)

    print(f"Image shape before cleaning: {img_array.shape[:2]}")

    print(f"Image shape after resizing: {resized_array.shape[:2]}")

    print(f"Image shape after cleaning: {padded_image.shape[:2]}") 


    #display image
    plt.figure()
    if padded_image.ndim == 2:
        plt.imshow(padded_image, cmap='gray')
    else:
        plt.imshow(padded_image)
    plt.axis('off')
    plt.show()


if __name__ == "__main__":

    main()
