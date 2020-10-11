import os
import sys
import cv2
import csv
import numpy as np
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets

def calculate_distance(pointA, pointB):
	distance = int(np.sqrt((pointA[0]-pointB[0])**2 + (pointA[1]-pointB[1])**2))
	return distance

def find_longest_contour(contours):
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
    return coin

def get_coin_width(csv_file, coin_name):
    coin_names = []
    coin_names.append(coin_name)
    if coin_name[-1] == "r":
        coin_names.append(coin_name[:-1])
    elif coin_names[-1] != "r":
        coin_names.append(f"{coin_name}r")

    if csv_file != None:
        with open(csv_file, "r", newline="") as file:
            csv_file = csv.DictReader(file)
            
            for row in csv_file:
                for name in coin_names:
                    if row["name"] == name:
                        return row["width"]
    else:
        return None

def px_to_mm(mm):
    # 1mm = 11.8px
    px = mm * 11.8
    return px

class Ui_coinSegmentation(object):
    def setupUi(self, coinSegmentation):
        coinSegmentation.setObjectName("coinSegmentation")
        coinSegmentation.resize(498, 321)
        self.centralwidget = QtWidgets.QWidget(coinSegmentation)
        self.centralwidget.setObjectName("centralwidget")
        self.image_button_folder = QtWidgets.QPushButton(self.centralwidget)
        self.image_button_folder.setGeometry(QtCore.QRect(100, 30, 281, 41))
        self.image_button_folder.clicked.connect(lambda: self.save_folder(self.image_button_folder))
      
        self.black_bg_check = QtWidgets.QCheckBox(self.centralwidget)
        self.black_bg_check.setGeometry(QtCore.QRect(50, 90, 111, 21))
        self.black_bg_check.setChecked(False)
        self.black_bg_check.stateChanged.connect(lambda:self.button_state(self.black_bg_check))
        
        self.alpha_bg_check = QtWidgets.QCheckBox(self.centralwidget)
        self.alpha_bg_check.setGeometry(QtCore.QRect(300, 90, 141, 17))
        self.alpha_bg_check.setChecked(False)
        self.alpha_bg_check.stateChanged.connect(lambda:self.button_state(self.alpha_bg_check))
        
        self.black_bg_folder = QtWidgets.QPushButton(self.centralwidget)
        self.black_bg_folder.setGeometry(QtCore.QRect(20, 120, 181, 41))
        self.black_bg_folder.setEnabled(False)
        self.black_bg_folder.clicked.connect(lambda: self.save_folder(self.black_bg_folder))

        self.alpha_bg_folder = QtWidgets.QPushButton(self.centralwidget)
        self.alpha_bg_folder.setGeometry(QtCore.QRect(270, 120, 191, 41))
        self.alpha_bg_folder.setEnabled(False)
        self.alpha_bg_folder.clicked.connect(lambda: self.save_folder(self.alpha_bg_folder))

        self.csv_file = QtWidgets.QPushButton(self.centralwidget)
        self.csv_file.setGeometry(QtCore.QRect(270, 180, 191, 41))
        self.csv_file.setEnabled(False)
        self.csv_file.clicked.connect(lambda: self.save_folder(self.csv_file, file=True))
        
        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(100, 250, 281, 41))
        self.start.setEnabled(False)
        self.start.clicked.connect(self.image_processing)
        
        coinSegmentation.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(coinSegmentation)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 498, 21))
        
        coinSegmentation.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(coinSegmentation)
        
        coinSegmentation.setStatusBar(self.statusbar)

        self.retranslateUi(coinSegmentation)
        QtCore.QMetaObject.connectSlotsByName(coinSegmentation)

        self.csv_path = None
        self.images = None
        self.black_bg_folder_path = None
        self.alpha_bg_folder_path = None

    def retranslateUi(self, coinSegmentation):
        _translate = QtCore.QCoreApplication.translate
        coinSegmentation.setWindowTitle(_translate("coinSegmentation", "London Coins - coin segmentation"))
        self.image_button_folder.setText(_translate("coinSegmentation", "Select Folder with images to process"))
        self.black_bg_check.setText(_translate("coinSegmentation", "Black Background"))
        self.alpha_bg_check.setText(_translate("coinSegmentation", "Transparent Background"))
        self.black_bg_folder.setText(_translate("coinSegmentation", "Select Folder to save image"))
        self.alpha_bg_folder.setText(_translate("coinSegmentation", "Select Folder to save image"))
        self.csv_file.setText(_translate("coinSegmentation", "Select CSV file"))
        self.start.setText(_translate("coinSegmentation", "Start Image Processing"))

    def save_folder(self, condition, file=False):
        if file == False:
            folder_path = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Folder", None, QtWidgets.QFileDialog.ShowDirsOnly)
            if condition == self.image_button_folder:
                self.images = [folder_path + "/" + image for image in os.listdir(folder_path) if image.endswith(".jpg")]

            elif condition == self.black_bg_folder:
                self.black_bg_folder_path = folder_path

            elif condition == self.alpha_bg_folder:
                self.alpha_bg_folder_path = folder_path
        
        else:
            file_path = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QFileDialog(), "Select CSV file", None, "csv(*.csv)")
            self.csv_path, ext = file_path

    def button_state(self, button):
        
        if button.text() == "Black Background":
            if button.isChecked() == True:
                self.black_bg_folder.setEnabled(True)
            else:
                self.black_bg_folder.setEnabled(False)
                self.black_bg_folder_path = None
                
        elif button.text() == "Transparent Background":
            if button.isChecked() == True:
                self.alpha_bg_folder.setEnabled(True)
                self.csv_file.setEnabled(True)
            else:
                self.alpha_bg_folder.setEnabled(False)
                self.alpha_bg_folder_path = None
                self.csv_file.setEnabled(False)

        self.enable_start_button()

    def enable_start_button(self):
        if self.black_bg_check.isChecked() == True or self.alpha_bg_check.isChecked() == True:
            self.start.setEnabled(True)
        else:
            self.start.setEnabled(False)

    def show_pop_up(self, failed_check_box):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setText(f"Checkbox: {failed_check_box.text()} selected but directory not selected")

        msg.exec_()


    def start_check(self, check_box, path):
        if check_box.isChecked() == True and path != None:
            return True
        elif check_box.isChecked() == False and path == None:
            return True
        else:
            self.show_pop_up(check_box)
            return False

    def image_processing(self):
        black_bg_condition = self.start_check(self.black_bg_check, self.black_bg_folder_path)
        alpha_bg_condition = self.start_check(self.alpha_bg_check, self.alpha_bg_folder_path)

        if self.images == None:
            self.show_pop_up(self.start)
        
        if black_bg_condition == True and alpha_bg_condition == True and self.images != None:
            for img in self.images:
                try:
                    split_string = img.split("/")
                    name = split_string[-1]
                    name, ext = name.split(".")

                    img = cv2.imread(img)
                    rows, cols, ch = img.shape
                    img_center = (int(cols/2), int(rows/2))
                    
                    grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    blur = cv2.GaussianBlur(grey_img, (5, 5), 0)
                    edges = cv2.Canny(blur,100,200)

                    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    valid_points = []
                    for contour in contours:
                        x,y,w,h = cv2.boundingRect(contour)

                        box_center = (x+(w/2), y+(w/2))
                        distance = calculate_distance(box_center, img_center)

                        if distance < 300:
                            valid_points.append(contour)
                        else:
                            cv2.rectangle(edges,(x,y),(x+w,y+h),(0,0,0),-1)

                    contour = np.concatenate(valid_points)

                    x,y,w,h = cv2.boundingRect(contour)
                    rect = (x, y, w, h)

                    mask = np.zeros(img.shape[:2],np.uint8)
                    bgdModel = np.zeros((1,65),np.float64)
                    fgdModel = np.zeros((1,65),np.float64)
                
                    (mask, bgModel, fgdModel) = cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
                    outputMask = np.where((mask == cv2.GC_BGD) | (mask == cv2.GC_PR_BGD), 0, 1)
                    outputMask = (outputMask * 255).astype("uint8") # scale the mask from the range [0, 1] to [0, 255]

                    contours, _ = cv2.findContours(outputMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    longest_contour = find_longest_contour(contours)

                    hull = cv2.convexHull(longest_contour)
                    x,y,w,h = cv2.boundingRect(hull)

                    output = np.zeros(img.shape[:2],np.uint8)
                    cv2.drawContours(output, [hull], -1, (255,255,255), -1)

                    res = cv2.bitwise_and(img, img, mask=output)

                    padding = 5 # 5px each side
                    final = res[y-padding:y+h+padding, x-padding:x+w+padding] 

                    if self.black_bg_check.isChecked() == True:
                        cv2.imwrite(f"{self.black_bg_folder_path}/{name}.jpg", final)

                    if self.alpha_bg_check.isChecked() == True:
                        output = output[y-padding:y+h+padding, x-padding:x+w+padding] 
                        b, g, r = cv2.split(final)
                        rgba = [b,g,r, output]
                        dst = cv2.merge(rgba,4)
                        
                        width = get_coin_width(self.csv_path, name)
                        if width != None:
                            width = px_to_mm(int(width))
                        else:
                            width = px_to_mm(25) # default mm size
                        
                        rows, cols, ch= dst.shape
                        aspect_ratio = cols / rows
                        height = width * aspect_ratio

                        dst = cv2.resize(dst, (int(width), int(height)))
                        RGBimage = cv2.cvtColor(dst, cv2.COLOR_BGRA2RGBA)
                        PILimage = Image.fromarray(RGBimage)
                        PILimage.save(f"{self.alpha_bg_folder_path}/{name}.png", dpi=(300,300))

                except Exception as e:
                    with open("error_logs.txt", "w") as log:
                        log.write(f"{e}")

if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        coinSegmentation = QtWidgets.QMainWindow()
        ui = Ui_coinSegmentation()
        ui.setupUi(coinSegmentation)
        coinSegmentation.show()
        sys.exit(app.exec_())

    except Exception as e:
        with open("error_logs.txt", "w") as log:
            log.write(f"{e}")
