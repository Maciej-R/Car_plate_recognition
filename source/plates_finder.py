import cv2
import numpy as np

class PossiblePlatesFinder:
    def __init__(self, ratio_min = 2.5, ratio_max = 7,
        angle = 15, min_area = 1000, max_area = 10000):
        # ratio of the plate
        self.ratio_min = ratio_min
        self.ratio_max = ratio_max

        # max tilt level
        self.angle = angle

        # minimum area of the plate
        self.min_area = min_area

        # maximum area of the plate
        self.max_area = max_area

    def find_possible_plates(self, input_img):
        """
        Finding all possible contours that can be plates
        """
        plates, cfinal = [], []
        after_preprocess = self._preprocess(input_img)
        contours = self._extract_contours(after_preprocess)

        for cnts in contours:
            plate = self._check_plate(input_img, cnts)
            if plate is not None:
                plates.append(plate)
                cfinal.append(np.int0(cv2.boxPoints(cv2.minAreaRect(cnts))))

        return (plates, cfinal) if len(plates) > 0 else (None, None)

    def _check_plate(self, input_img, contour):
        min_rect = cv2.minAreaRect(contour)
        return self._crop(input_img, min_rect) if self._validate_ratio(min_rect) else None

    def _validate_ratio(self, rect):
        _, (width, height), rect_angle = rect
        angle = -rect_angle if width > height else 90 + rect_angle

        if angle > self.angle or height == 0 or width == 0:
            return False

        return self._ratio_check(width * height, width, height)

    def _ratio_check(self, area, width, height):
        ratio = max(width, height)/min(width, height)
        return self.min_area < area < self.max_area and self.ratio_min < ratio < self.ratio_max

    @staticmethod
    def _crop(img, rect):
        box = np.int0(cv2.boxPoints(rect))

        w, h = rect[1][0], rect[1][1]

        Xs = [i[0] for i in box]
        Ys = [i[1] for i in box]
        x_1, x_2 = min(Xs), max(Xs)
        y_1, y_2 = min(Ys), max(Ys)

        rotated = False
        angle = rect[2]

        if angle < -45:
            angle+=90
            rotated = True

        center = (int((x_1+x_2)/2), int((y_1+y_2)/2))
        size = (int(x_2-x_1), int(y_2-y_1))

        M = cv2.getRotationMatrix2D((size[0]/2, size[1]/2), angle, 1.0)

        cropped = cv2.getRectSubPix(img, size, center)
        cropped = cv2.warpAffine(cropped, M, size)

        cropped_w = w if not rotated else h
        cropped_h = h if not rotated else w

        return cv2.getRectSubPix(cropped, (int(cropped_w), int(cropped_h)), (size[0]/2, size[1]/2))

    @staticmethod
    def _preprocess(input_img):
        # filter input_img
        img_blurred = cv2.GaussianBlur(input_img, (7, 7), 0)

        # convert to gray
        gray = cv2.cvtColor(img_blurred, cv2.COLOR_BGR2GRAY)

        # sobelX to get the vertical edges
        sobelx = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize = 3)

        # otsu's thresholding
        threshold_img = cv2.threshold(sobelx, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        return cv2.morphologyEx(src = threshold_img, op = cv2.MORPH_CLOSE,
            kernel = cv2.getStructuringElement(shape = cv2.MORPH_RECT, ksize =(22, 3)))

    @staticmethod
    def _extract_contours(after_preprocess):
        return cv2.findContours(after_preprocess,
            mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_NONE)[0]
