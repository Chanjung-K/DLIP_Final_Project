###############################################################################
# @course 	Deep Learning and Image Processing - HGU
# @author	ChanJung Kim / 22000188
#           JongHyeon Kim / 21900179
# @Created	2025-06-7 by CJKIM
# @Modified	2025-06-21 by CJKIM
# @brief	[DLIP] Final Project: Camera-Based System for Automatic Recognition
#           and Node Pin Mapping
###############################################################################

import cv2 
# Insert appropriate module you downloaded
import ModuleYouDownloaded as OCRModule

# Variable Initiation
lastValidClass = [("", 0.0) for _ in range(10)]

# ========================================== Change Eval_Flag as True to Evauluate Project Accuracy ==========================================
evalFlag = False
evalNum = 50
count = 1
totalCount = -5

############## |Mode2| Mode3| Mode4| Mode5| Evaluation | ##############
pinModeFlag  = [False, False, False, False,  evalFlag  ]  
ICName = list(OCRModule.IC_INFO.keys())
ICLength = len(OCRModule.IC_INFO)
number = [0 for _ in range(ICLength)]

# Connect Smartphone as Webcam
cap = cv2.VideoCapture(1) 

if not cap.isOpened(): 
    print("Error: Could not open video stream.") 
    exit() 

# ====================================================================================================================================
while True:
    ret, frame = cap.read()
    if not ret: 
        print("Error: Failed to capture image.") 
        break 
    
    # Find IC Chip Orientation
    contours = OCRModule.FindingContours(frame)
    
    # Identify IC Chip through Contour
    frame, point, length, rate, whMinRect, angle, box, Flag = OCRModule.IdentifyICchip(frame, lastValidClass, contours, pinModeFlag)
    # GUI Print
    OCRModule.GUIPrint(frame, lastValidClass, point, length, whMinRect, rate, box, angle, pinModeFlag)

    # Result Show
    cv2.imshow("Detecting",frame)
    Key = cv2.waitKey(10)
    # Mode Changing
    pinModeFlag  = OCRModule.ModeChanger(Key, frame, cap, pinModeFlag)

    #########################################################################################################
    ########################################## Evaluation Accuracy ##########################################
    #########################################################################################################
    totalCount += 1
    if  Flag and evalFlag:
        count += 1
        idx = ICName.index(lastValidClass[0][0])
        number[idx] += 1
        print(f"Total Iteration: {totalCount}\tDetected Count: {count}\n Class Name: {lastValidClass[0][0]}\tAccuracy: {lastValidClass[0][1]*100:.2f}%")

    if count > evalNum:
        break

# Evaluation Result Print
if evalFlag:
    for ch in ICName:
        print(f"|{ch}|\t", end='')
    print(f'')
    for i in range(8):
        print(f"|\t{number[i]} |\t", end='')
