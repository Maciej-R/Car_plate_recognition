import plates_finder
import cv2 as cv

cap = cv.VideoCapture('../video/video2.mp4') # input file

findPlate = plates_finder.PossiblePlatesFinder()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Exiting ...")
        break

    possible_plates, possible_contours = findPlate.find_possible_plates(frame)

    if possible_contours is not None:
        cv.imshow('frame', cv.drawContours(frame, possible_contours, -1, (0, 0, 255), 3))
        if cv.waitKey(1) == ord('q'):
            break

# Release everything if job is finished
cap.release()
cv.destroyAllWindows()
