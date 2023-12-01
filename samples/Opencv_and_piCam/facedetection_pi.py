import cv2
from picamera2 import Picamera2

# Load the pre-trained Haar Cascade classifier for face detection for Bookworm
#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Load the pre-trained Haar Cascade classifier for face detection for Bullseye
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

try:
    while True:
        im = picam2.capture_array()
        cv2.imshow("Camera", im)

        # Convert the image to grayscale for face detection
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        # Perform face detection
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Display the image with face detection
        cv2.imshow("Face Detection", im)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

finally:
    # Release resources
    cv2.destroyAllWindows()
    picam2.stop()
    picam2.close()
