import cv2
import numpy as np
from picamera2 import Picamera2

# Function to identify and label shapes
def identify_and_label_shapes(contour, img):
    # cv2.approxPloyDP() function to approximate the shape
    approx = cv2.approxPolyDP(
        contour, 0.01 * cv2.arcLength(contour, True), True)

    # finding center point of shape
    M = cv2.moments(contour)
    if M['m00'] != 0.0:
        x = int(M['m10'] / M['m00'])
        y = int(M['m01'] / M['m00'])

        # Check if contour area is greater than 1000 before labeling
        if cv2.contourArea(contour) > 3000:
            # putting shape name at the center of each shape
            if len(approx) == 3:
                cv2.putText(img, 'Triangle', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            elif len(approx) == 4:
                cv2.putText(img, 'Quadrilateral', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            elif len(approx) == 5:
                cv2.putText(img, 'Pentagon', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            elif len(approx) == 6:
                cv2.putText(img, 'Hexagon', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            else:
                cv2.putText(img, 'Circle', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

# Start capturing video input from the Pi Camera
picam2 = Picamera2()
width, height = 800, 600  # set your desired resolution
picam2.preview_configuration.main.size = (width, height)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

try:
    while True:
        # Capture a frame from the Pi Camera
        frame = picam2.capture_array()
        img=frame
        #img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # converting image into grayscale image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # setting threshold of gray image
        _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # using a findContours() function
        contours, _ = cv2.findContours(
            threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # list for storing names of shapes
        for contour in contours:

            # Call the function to identify and label shapes
            identify_and_label_shapes(contour, img)

        # displaying the image after drawing contours
        cv2.imshow('shapes', img)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop the Pi Camera
    picam2.stop()
    cv2.destroyAllWindows()
