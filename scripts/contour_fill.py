import cv2
import os
import numpy as np

path_file = os.path.abspath(os.getcwd())
folder = "test_images"
image_name = "shilling16.jpg"

img = cv2.imread(f"{path_file}/{folder}/{image_name}") 
img = cv2.resize(img, (150,150))

grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred_img = cv2.GaussianBlur(grey_img, (15,15), 0)
_, otsu_img = cv2.threshold(blurred_img, 0, 255,  cv2.THRESH_BINARY + cv2.THRESH_OTSU)
dilation = cv2.dilate(otsu_img,np.ones((5,5),np.uint8),iterations = 1)

cv2.imshow("dilate", dilation)
contours, _ = cv2.findContours(dilation, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# cv2.drawContours(img, contours, 8, (0,255,0), 3)

if len(contours) == 1:
    print("easy to process, only 1 contour found")

    res = cv2.bitwise_and(img, img, mask=dilation)
    cv2.imshow("res", res)

else:
    print(f"not so easy to process, {len(contours)} found. Looking for max contour")
    max_area = None
    coin = None
    for contour in contours:
        contour_area = cv2.contourArea(contour)

        if max_area == None:
            max_area = contour_area
            coin = contour
        
        else:
            if contour_area > max_area:
                max_area = contour_area
                coin = contour

    cv2.drawContours(grey_img, [coin], -1, (255,255,255), cv2.FILLED)
    _, binary_img = cv2.threshold(grey_img, 250, 255,  cv2.THRESH_BINARY)

    bin_contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(bin_contours) > 1:
        print("Still more contours found, applying morphology op to remove small noises")
        opening = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, np.ones((5,5),np.uint8)) # get rid of small contours
        res = cv2.bitwise_and(img, img, mask=opening)
        cv2.imshow('Desired', res) # coloured ROI in black bg

    else:
        print("No open morph operation needed")
        res = cv2.bitwise_and(img, img, mask=binary_img)
        # cv2.imshow('Desired', res) # coloured ROI in black bg


# cv2.imshow('original', img)
# cv2.imshow('blurred', blurred_img)
cv2.imshow('otsu', otsu_img)

cv2.waitKey(0)