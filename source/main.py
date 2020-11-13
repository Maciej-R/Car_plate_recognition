import imutils
from PlateFinder import PlateFinder
import numpy as np
import cv2 as cv
import matplotlib

cap = cv.VideoCapture('../video/video3.mp4') # input file

findPlate = PlateFinder() 

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'DIVX')
out = cv.VideoWriter('../video/output.mp4', fourcc, 30.0, (1280,  720), False) # video jest niezgodne z DIW

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Exiting ...")
        break

    
    """
    pre = findPlate.preprocess(frame)
    cnr = findPlate.extract_contours(pre)
    cnr = findPlate.filter(cnr)
    frame = cv.drawContours(frame, cnr, -1, (0, 0, 255), 3)

    
    # out.write(frame) # write to file
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
    """

    possible_plates = findPlate.find_possible_plates(frame)
    
    for c in possible_plates:
        if c[0] is not None:
            if c[0].any():
                cv.imwrite('../images/'+str(id(c[0]))+'.png', c[0])
    


# Release everything if job is finished
cap.release()
out.release()
cv.destroyAllWindows()