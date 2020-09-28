import cv2
import os
import numpy as np

path_file = os.path.abspath(os.getcwd())
folder = "test_images"
image_name = "statue.jpg"

img = cv2.imread(f"{path_file}/{folder}/{image_name}") 
img_shape = (img.shape[0], img.shape[1])
# img = cv2.resize(img, (150,150))

grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred_img = cv2.GaussianBlur(grey_img, (15,15), 0)
_, otsu_img = cv2.threshold(blurred_img, 0, 255,  cv2.THRESH_BINARY + cv2.THRESH_OTSU)
contours, _ = cv2.findContours(otsu_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# find max contour
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



ellipse = cv2.fitEllipse(coin)
cv2.ellipse(grey_img,ellipse,255,-1)
cv2.imshow("el", grey_img)

_, binary_img = cv2.threshold(grey_img, 254, 255,  cv2.THRESH_BINARY)

cv2.imshow('bin', binary_img) # coloured ROI in black bg

res = cv2.bitwise_and(img, img, mask=binary_img)
cv2.imshow('Desired', res) # coloured ROI in black bg

# cv2.imshow("orig", test)
cv2.waitKey(0)