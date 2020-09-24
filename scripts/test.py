import cv2
import os
import numpy as np

path_file = os.path.abspath(os.getcwd())
folder = "test_images"
image_name = "old_pound.jpg"

img = cv2.imread(f"{path_file}/{folder}/{image_name}") 
img = cv2.resize(img, (150,150))

grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred_img = cv2.GaussianBlur(grey_img, (3,3), 0)
_, otsu_img = cv2.threshold(blurred_img, 0, 255,  cv2.THRESH_BINARY + cv2.THRESH_OTSU)
contours, hier = cv2.findContours(otsu_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# cv2.drawContours(img, contours, 8, (0,255,0), 3)

if len(contours) == 1:
    # print(if)
    # cv2.drawContours(img, contours, -1, (0,255,0), 3)

    res = cv2.bitwise_and(img, img, mask=otsu_img)
    cv2.imshow("res", res)

else:
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
                # print("here", max_area)
                coin = contour

    print("here")
    cv2.drawContours(grey_img, [coin], -1, (255,255,255), cv2.FILLED)
    _, test_img = cv2.threshold(grey_img, 0, 255,  cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    res = cv2.bitwise_and(img, img, mask=test_img)

    cv2.imshow('res else', res)
    cv2.imshow("new", grey_img)

    # contour_area = cv2.contourArea(contours[8])
    # print(contour_area, max_area)
    # count = 0
    # closing = None
    # while True:
    #     # print(count)
    #     count += 1
    #     closing = cv2.morphologyEx(otsu_img, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8), iterations=count)
    #     contours, hier = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #     if len(contours) == 1:
    #         break

    # print(f"total iteration: {count}")
    # cv2.imshow("closing", closing)

    # res = cv2.bitwise_and(img, img, mask=closing)
    # cv2.imshow("res", res)
# print(len(contours))


cv2.imshow('original', img)
# cv2.imshow('blurred', blurred_img)
# cv2.imshow('otsu', otsu_img)

cv2.waitKey(0)