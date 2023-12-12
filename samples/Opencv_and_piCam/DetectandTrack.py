import cv2
from picamera2 import Picamera2

# Initialize PiCamera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Use a Haar Cascade Classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the CSRT tracker
tracker = cv2.legacy.TrackerCSRT_create()

# Flag to switch between tracking and detection
tracking = False

while True:
    # Read a new frame from the PiCamera
    frame = picam2.capture_array()

    # Convert the frame to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if tracking:
        # Update the tracker
        ok, bbox = tracker.update(frame)

        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:
            # Tracking failure, switch to detection
            tracking = False

    else:
        # Detect faces
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            # Use the first detected face as the initial bounding box
            bbox = tuple(faces[0])

            # Initialize the tracker with the bounding box
            tracker = cv2.legacy.TrackerCSRT_create()
            tracker.init(frame, bbox)

            tracking = True

    # Display result
    cv2.imshow("Tracking and Detection", frame)

    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

# Release the PiCamera and close the OpenCV window
picam2.stop()
cv2.destroyAllWindows()
