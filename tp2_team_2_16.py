"""
Course Number: ENGR 13300
Semester: Fall 2026

Description:
    Our goal is to extract features from images (hue_mean,hue_std,saturation_mean,saturation_std, etc) and save them in a CSV file. 

Assignment Information:
    Assignment:    8.2.3 tp2 team 2
    Team ID:       LC5 - 16
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
import pandas as pd
import matplotlib.pyplot as plt
import math
import cv2
import os
from pathlib import Path
#---------------------------------old functions
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


def pad_image(resized_img_array, size_increase):
    #inputs: np array of resized image (from resize_image() function), and tuple of size(width, height) for padded image
    #outputs: padded img as a np array
    
    padded_np_array = np.pad(resized_img_array, size_increase)
    return padded_np_array

def rgb_to_hsv(R,G,B):
    #Normalize RGB values to values between 0 and 1
    normal_R = R/255
    normal_G = G/255
    normal_B = B/255
    
    #calculate hue_prime
    max_component = max(normal_R, normal_G, normal_B)
    min_component = min(normal_R, normal_G, normal_B)
    component_delta = max_component - min_component
    if component_delta == 0:
        hue_prime = 0
    else:
        if max_component == normal_R:
            hue_prime = (60 * ((normal_G - normal_B) / component_delta) + 360) % 360 #campus wire comment (Brianna Lewis)
        elif max_component == normal_G:
            hue_prime = (60 * ((normal_B - normal_R) / component_delta) + 120) % 360
        elif max_component == normal_B:
            hue_prime = (60 * ((normal_R - normal_G) / component_delta) + 240) % 360

    #calculate saturation_prime
    if max_component == 0:
        saturation_prime = 0
    else:
        saturation_prime = component_delta / max_component

    #calculate value_prime
    value_prime = max_component

    #rescale values to be from 0 to 255
    hue = hue_prime * 255 / 360 #campus wire comment (Brianna Lewis)
    saturation = (saturation_prime * 255)
    value = (value_prime * 255)
    return (hue,saturation,value)

def convert_to_hsv(rgb_image):
    hsv_image = np.array([[rgb_to_hsv(r,g,b) for r, g, b in row] for row in rgb_image], dtype=np.uint8)
    return hsv_image

def resize_image(original_image_array, new_size): 
    #inputs: np.array of original image (from the load_img), and tuple of size (width,height) for resized image 
    #outputs: resized img as a np array
    if original_image_array.dtype != np.uint8: #PIL can't handle float arrays
        original_image_array = (original_image_array * 255).astype(np.uint8)
    pil_img = Image.fromarray(original_image_array) #converts np array back to PIL array so we can use .resize() on it
    resized_img = pil_img.resize(new_size, resample=2) #resizes using PIL's Image.resize() which only works on PIL images, not np arrays
    resized_np_array = np.array(resized_img) #converts resized PIL Image back to np array
    return resized_np_array


def sobel_filter(image):
    # initialize sobel x and y
    sobelx = np.array([[-1, 0, 1],[-2, 0, 2],[-1,0,1]],dtype=float)
    sobely = np.array([[-1,-2,-1],[0,0,0],[1,2,1]],dtype=float)
    image_arr = np.array(image,dtype=float)
    # we know the kernel size because we are given the kernels
    kernel_size = 3
    # just one pixel of padding
    pad = 1

    padded_image = np.pad(image_arr, pad, mode='constant',constant_values=0)
    output = np.zeros_like(image_arr,dtype=np.uint8)
    threshold = 50
    # apply the kernel
    h, w = image_arr.shape
    gradient_min = 10000
    gradient_max = 0
    for i in range(h):
        for j in range(w):
            window = padded_image[i:i+kernel_size,j:j+kernel_size]

            gx = np.sum(window*sobelx)
            gy = np.sum(window*sobely)
            # multiply by 255 to de-normalize
            gradient_magnitude = math.sqrt(gx**2 + gy**2)
            
            if (gradient_magnitude >= threshold):
                output[i,j] = 255
            else:
                output[i,j] = 0
    return output

#------------------------------new functions
def detect_circle(gray_img):
    """Detects if a large circle is present. Returns 1 if found, 0 otherwise."""
    # Hough Circles works best on a grayscale, slightly blurred image

    blurred_img = gaussian_filter(gray_img, sigma=1.5) #Use gaussian_filter with sigma=1.5 to blur the input image
    blurred_img_array = np.array(blurred_img)  # Convert to NumPy array for processing with cv2
    blurred_img_array = blurred_img_array.astype(np.uint8)  #cv2.HoughCircles requires an 8-bit image

    # Detect circles
    circles = cv2.HoughCircles(
        blurred_img_array,
        cv2.HOUGH_GRADIENT,
        dp=1.2,  # Inverse ratio of accumulator resolution
        minDist=50,  # Minimum distance between centers of detected circles
        param1=100,  # Upper threshold for the internal Canny edge detector
        param2=30,  # Threshold for center detection
        minRadius=20,  # Minimum circle radius to detect
        maxRadius=50  # Maximum circle radius to detect
    )
    if circles is None:
        return 0
    else:
        return 1

def detect_triangle(gray_img):
    """Detects if a triangle is present. Returns 1 if found, 0 otherwise."""
    blurred = gaussian_filter(gray_img, sigma=1.0)
    edges = sobel_filter(blurred)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 3 and cv2.contourArea(approx) > 625:
            return 1
    return 0

def count_lines(gray_img):
    """Counts the number of lines in an image using Hough Line Transform."""
    # Edge detection via sobel filtering is a prerequisite for Hough Lines
    edges = sobel_filter(gray_img) #Use sobel_filter on the input grayscale image

    # Detect lines using the edge map
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=30, maxLineGap=10)

    if lines is None: #if no lines are detected return 0
        return 0
    return len(lines) #return the number of lines detected

def extract_features(img_array):
    #inputs: np array of the resized and padded RGB image (100x100x3)
    #outputs: list of the nine features in the required order
    
    #convert the rgb image to hsv
    hsv_img = convert_to_hsv(img_array)

    #calculate the mean and standard deviation of each hsv channel
    hue_mean = np.mean(hsv_img[:, :, 0])
    hue_std = np.std(hsv_img[:, :, 0])
    saturation_mean = np.mean(hsv_img[:, :, 1])
    saturation_std = np.std(hsv_img[:, :, 1])
    value_mean = np.mean(hsv_img[:, :, 2])
    value_std = np.std(hsv_img[:, :, 2])

    #convert the rgb image to grayscale for the shape based features
    gray_img = rgb_to_grayscale(img_array)

    #calculate the shape based features
    number_lines = int(count_lines(gray_img))
    has_circle = int(detect_circle(gray_img))
    has_triangle = int(detect_triangle(gray_img))

    #return all nine features in the required order
    return [hue_mean, hue_std, saturation_mean, saturation_std, value_mean, value_std,
            number_lines, has_circle, has_triangle]

def main():
    folder_name = input("Enter the name of the dataset folder:\n")
    meta_data_name = input("Enter the name of the metadata file:\n")
    csv_features_name = input("Enter the name of output csv features file:\n")
    loaded_csv = pd.read_csv(meta_data_name)
    print("\nTraining Metadata DataFrame:")
    print(loaded_csv.head())

    #column names for the final feature dataset
    feature_columns = ["hue_mean", "hue_std", "saturation_mean", "saturation_std", "value_mean", "value_std", "number_lines", "has_circle", "has_triangle", "Path", "ClassId"]

    feature_rows = []
    if Path(csv_features_name).exists():
        feature_df = pd.read_csv(csv_features_name)
    #process each row of the metadata dataframe
    else:
        for index, row in loaded_csv.iterrows():
            image_path = row["Path"]
            class_id = row["ClassId"]
            full_path = os.path.join(folder_name, image_path)
            linear_img = load_img(Image.open(full_path))
            uint8_img = (linear_img * 255).astype(np.uint8)
            resized_img = resize_image(uint8_img, (100, 100))
            padded_img = pad_image(resized_img, ((0, 0), (0, 0), (0, 0)))
            features = extract_features(padded_img)
            feature_rows.append([float(f) for f in features] + [image_path, class_id])

        feature_df = pd.DataFrame(feature_rows, columns=feature_columns)
        feature_df[feature_columns[:9]] = feature_df[feature_columns[:9]].astype(float)
        feature_df.to_csv(csv_features_name, index=False)

    print(f"\nFeatures have been extracted and saved to {csv_features_name}")

    #print the shape and head of the final dataset
    print("\nFeature Dataset Shape:")
    print(feature_df.shape)
    print("\nFeature Dataset Head:")
    print(feature_df.head())
    print("")
    image_name = input("Enter the Path of the image you want to display the features for:\n")
    #filter the dataframe for the row matching the image path and print it
    print(f"\nFeatures for {image_name}:")
    print(feature_df[feature_df["Path"] == image_name])


if __name__ == "__main__":
    main()