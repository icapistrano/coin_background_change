import cv2
import os
import numpy as np

path_file = os.path.abspath(os.getcwd())
folder = "test_images"
image_name = "statue.jpg"

img = cv2.imread(f"{path_file}/{folder}/{image_name}") 
img = cv2.resize(img, (150,150))

grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred_img = cv2.GaussianBlur(grey_img, (7,7), 0)
_, otsu_img = cv2.threshold(blurred_img, 0, 255,  cv2.THRESH_BINARY + cv2.THRESH_OTSU)
contours, _ = cv2.findContours(otsu_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if len(contours) == 1:
    cv2.drawContours(img, contours, -1, (0,255,0), 3)

    # res = cv2.bitwise_and(img, img, mask=otsu_img)
    # contours, _ = cv2.findContours(otsu_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print(len(contours))
    # cv2.imshow('res', res)
    # for i,c in enumerate(contours):
    #     rect = cv2.boundingRect(c)
    #     x,y,w,h = rect
    #     # box = cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2)
    #     cropped = img[y: y+h, x: x+w]
    #     cv2.imshow("Show Boxes", cropped)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
    #     cv2.imwrite("blobby"+str(i)+".png", cropped)

cv2.imshow('original', img)
cv2.imshow('blurred', blurred_img)
cv2.imshow('otsu', otsu_img)

cv2.waitKey(0)