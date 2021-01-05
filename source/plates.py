import sys
import os

import numpy as np
import cv2

from source.openalpr import Alpr

def generate_mask(width,height):
    mask = np.zeros([height, width, 3], dtype=np.uint8)
    mask[height//2:,:] = [255, 255, 255]
    cv2.imwrite('mask.jpg', mask)

def process_video(video_path, found):
    """
    Function for detecting license plates from video
    :video_path: path to input video
    :found: set which will be filled with unique license plate numbers
    """
    filename = os.path.basename(video_path).split(sep='.')[0]
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        sys.exit('Failed to open video file!')

    generate_mask(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    writer = cv2.VideoWriter(f"output/{filename}.avi",
        cv2.VideoWriter_fourcc(*"MJPG"), cap.get(cv2.CAP_PROP_FPS),
        (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    alpr = Alpr("eu", "source/openalpr.conf",
        "openalpr/runtime_data")
    if not alpr.is_loaded():
        print('Error loading OpenALPR')
        sys.exit(1)

    alpr.set_top_n(1)
    alpr.set_default_region('pl')

    file = open('output/report.txt','w')

    cnt = 0

    while cap.isOpened():
        ret_val, frame = cap.read()
        if not ret_val:
            break

        cnt += 1

        _, enc = cv2.imencode("*.jpg", frame)
        results = alpr.recognize_array(enc.tobytes())

        if results['results']:
            for plate in results['results']:
                file.write('Frame: {:5} | Plate: {:8}\n'.format(cnt, plate['plate']))
                found.add(plate['plate'])
                cv2.rectangle(frame, (plate["coordinates"][0]["x"],plate["coordinates"][0]["y"]),
                    (plate["coordinates"][2]["x"],plate["coordinates"][2]["y"]), (0,255,0), 3)


        writer.write(frame)

    file.close()
    writer.release()
    cap.release()
