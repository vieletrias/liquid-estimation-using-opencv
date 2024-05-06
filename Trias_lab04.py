#Lab 4
#Importing libraries
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

# Image preprocessing 
def imagepreprocess(image):
    #Converts the images to black and white
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    #Once converted, thresholding to seprate the white and black colors, to distinguish the liquid area
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    
    #Display the original and thresholded images
    # plt.figure(figsize=(8, 4))
    # plt.subplot(1, 2, 1)
    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.title('Original Image')
    # plt.axis('off')
    
    # plt.subplot(1, 2, 2)
    # plt.imshow(thresh, cmap='gray')
    # plt.title('Thresholded Image')
    # plt.axis('off')
    
    # plt.show()
    
    #Return the thresholding values
    return thresh


# Function to read images and extract features for different liquid volumes
def volumeprocess(location):
   
    #makes array to contain all features from all images and all labels
    pixelcountlist = []
    volumelabel = []


    #since file names are named after volume numbers, increments each iteration to the volume corresponding the file name
    for volume in range(50, 351, 50):   

        #makes the folder pathnto access the image according to the file name which is also th volume
        folderloc = os.path.join(location, f'{volume}ml') 
        #gets the list of image file names 
        images = os.listdir(folderloc)

        #iterates through the list of fole names 
        for i in images:

            #joins the folder path and file name
            imagepath = os.path.join(folderloc, i)

            #reads the images presented
            image = cv2.imread(imagepath)

            #calls the image to preprocess it by converting it to black and white
            preprocessimage = imagepreprocess(image)

            #gets the area where the liquid is supposed to be
            pixels = countpixel(preprocessimage)

            #append the features in the array 
            pixelcountlist.append(pixels)

            #append the volume in the array
            volumelabel.append(volume)

    #returns all the features 
    return pixelcountlist, volumelabel

# Function to read images and calculate average features for guess subfolders
def predictvolume(location):
    
    #gets the folder path of the file name that is to be guessed 
    guessfolder = os.path.join(location, 'guess')
    
    #intitiate the subfolders which is A, B, and C
    subfolders = ['A', 'B', 'C']

    #makes an array for the average guesses
    meanpredict = []

    #for loop to get the images in the subfolders
    for subfolder in subfolders:
        subfolderloc = os.path.join(guessfolder, subfolder)
        images = os.listdir(subfolderloc)

        #initialize subfolder features array
        sfolderfeat = []

        for i in images:
            imagepath = os.path.join(subfolderloc, i)
            
            #reads each image in each subfolder
            image = cv2.imread(imagepath)

            #preprocess the folder once more
            preprocessimage = imagepreprocess(image)

            #extract the features
            pixels = countpixel(preprocessimage)

            #appends the features in the array
            sfolderfeat.append(pixels)
    
        #averages or calculates the mean of the average feature
        meanfeature = np.mean(sfolderfeat)

        #appends the guessed feature
        meanpredict.append(meanfeature)
    return meanpredict, subfolders

# performs linear regression to all features and labels and the guessed features 
def volumepredict(countpixel, volumelabel, meanpredict):
    #set degree to 1
    degree = 1
    #run polyfgit for linear regression with degree 1 
    coefficients = np.polyfit(countpixel, volumelabel, degree)

    #predicts the amount of liquid, using slope intercept formula y = mx+b
    #store predicted amount
    predictamount = []

    # Iterate over each feature in meanpredict
    for i in meanpredict:
        # linear equation
        amount = coefficients[0] * i + coefficients[1]
        # Append predicted amount to the list
        predictamount.append(amount)

    
    #returns the predicted amount
    return predictamount

# Gets the black area, since this represents the liquid area

def countpixel(image):

    return np.sum(image == 0)


# Main function
def main():
    location = r'C:\Users\Laviele\Desktop\Lab\data'

    # Process images for different liquid volumes
    countpixel, volumelabel = volumeprocess(location)

    # Process guess subfolders
    meanpredict, subfolders = predictvolume(location)

    # Predict volumes for guess images
    predictamount = volumepredict(countpixel, volumelabel, meanpredict)

    # Print predicted amounts

    for i in range(len(predictamount)):
        print(subfolders[i] + ": " + str(predictamount[i]) + " ml")


main()