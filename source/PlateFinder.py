import cv2
import imutils
from skimage import measure
from skimage.filters import threshold_local
import numpy as np
import matplotlib

def crop(img, rect):
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    W = rect[1][0]
    H = rect[1][1]

    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)

    rotated = False
    angle = rect[2]

    if angle < -45:
        angle+=90
        rotated = True

    center = (int((x1+x2)/2), int((y1+y2)/2))
    size = (int((x2-x1)),int((y2-y1)))

    M = cv2.getRotationMatrix2D((size[0]/2, size[1]/2), angle, 1.0)

    cropped = cv2.getRectSubPix(img, size, center)    
    cropped = cv2.warpAffine(cropped, M, size)

    croppedW = W if not rotated else H 
    croppedH = H if not rotated else W

    return cv2.getRectSubPix(cropped, (int(croppedW), int(croppedH)), (size[0]/2, size[1]/2))

class PlateFinder:
    def __init__(self):
        # ratio of the plate
        self.ratioMin = 3
        self.ratioMax = 6

        # ratio of the plate
        self.preRatioMin = 2.5
        self.preRatioMax = 7

        # max tilt level
        self.angle = 15
          
        # minimum area of the plate 
        self.min_area = 1000
          
        # maximum area of the plate 
        self.max_area = 10000
  
    def preprocess(self, input_img): 
        # filter input_img
        imgBlurred = cv2.GaussianBlur(input_img, (7, 7), 0)
          
        # convert to gray 
        gray = cv2.cvtColor(imgBlurred, cv2.COLOR_BGR2GRAY)

        # sobelX to get the vertical edges 
        sobelx = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize = 3)
          
        # otsu's thresholding 
        threshold_img = cv2.threshold(sobelx, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        return cv2.morphologyEx(src = threshold_img, op = cv2.MORPH_CLOSE,
            kernel = cv2.getStructuringElement(shape = cv2.MORPH_RECT, ksize =(22, 3)))
  
    def extract_contours(self, after_preprocess):
        return cv2.findContours(after_preprocess,
            mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_NONE)[0]

    def check_plate(self, input_img, contour):           
        min_rect = cv2.minAreaRect(contour)
          
        if self.validateRatio(min_rect):
            """
            box = np.int0(cv2.boxPoints(min_rect))
            cv2.imshow('frame', cv2.drawContours(input_img, [box], -1, (0, 0, 255), 3))
            """

            after_clean_plate_img = crop(input_img, min_rect) 
            
            """
            after_clean_plate_img, plateFound, coordinates = self.clean_plate(after_validation_img) 
              
            if plateFound:
                
                characters_on_plate = self.find_characters_on_plate( 
                                              after_clean_plate_img) 
                  
                if (characters_on_plate is not None and len(characters_on_plate) == 8): 
                    x1, y1, w1, h1 = coordinates 
                    coordinates = x1 + x, y1 + y 
                    after_check_plate_img = after_clean_plate_img 
                      
                    return after_check_plate_img, characters_on_plate, coordinates
                """
            return after_clean_plate_img, None, None
          
        return None, None, None
    
    def find_possible_plates(self, input_img):          
        """ 
        Finding all possible contours that can be plates 
        """
        plates = []
        after_preprocess = self.preprocess(input_img)

        for cnts in self.extract_contours(after_preprocess):
            plate = self.check_plate(input_img, cnts)
            if plate is not None: plates.append(plate)

        return plates if len(plates) > 0 else None
    
    def validateRatio(self, rect): 
        _, (width, height), rect_angle = rect
        angle = -rect_angle if width > height else 90 + rect_angle 
        if angle > self.angle or height == 0 or width == 0: return False
        return self.preRatioCheck(width * height, width, height)

    def ratioCheck(self, area, width, height):
        ratio = max(width, height)/min(width, height)
        return self.min_area < area < self.max_area and self.ratioMin < ratio < self.ratioMax
 
    def preRatioCheck(self, area, width, height): 
        ratio = max(width, height)/min(width, height)
        return self.min_area < area < self.max_area and self.preRatioMin < ratio < self.preRatioMax

    def filter(self, cnr):
        tmp = []
        for c in cnr:
            min_rect = cv2.minAreaRect(c) 
            if self.validateRatio(min_rect):
                box = np.int0(cv2.boxPoints(min_rect))
                tmp.append(box)

        return tmp