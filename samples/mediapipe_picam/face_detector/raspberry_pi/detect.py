import argparse
import time
from picamera2 import Picamera2
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from utils import visualize

# Global variables to calculate FPS
COUNTER, FPS = 0, 0
START_TIME = time.time()
DETECTION_RESULT = None


def run(model: str, min_detection_confidence: float,
        min_suppression_threshold: float, width: int,
        height: int) -> None:
    """Continuously run inference on images acquired from the camera.

    Args:
      model: Name of the TFLite face detection model.
      min_detection_confidence: The minimum confidence score for the face
        detection to be considered successful.
      min_suppression_threshold: The minimum non-maximum-suppression threshold for
        face detection to be considered overlapped.
      width: The width of the frame captured from the camera.
      height: The height of the frame captured from the camera.
    """

    # Start capturing video input from the camera
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (width, height)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()

    # Visualization parameters
    row_size = 50  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 0)  # black
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

    def save_result(result: vision.FaceDetectorResult, unused_output_image: mp.Image,
                    timestamp_ms: int):
        global FPS, COUNTER, START_TIME, DETECTION_RESULT

        # Calculate the FPS
        if COUNTER % fps_avg_frame_count == 0:
            FPS = fps_avg_frame_count / (time.time() - START_TIME)
            START_TIME = time.time()

        DETECTION_RESULT = result
        COUNTER += 1

    # Initialize the face detection model
    base_options = python.BaseOptions(model_asset_path=model)
    options = vision.FaceDetectorOptions(base_options=base_options,
                                         running_mode=vision.RunningMode.LIVE_STREAM,
                                         min_detection_confidence=min_detection_confidence,
                                         min_suppression_threshold=min_suppression_threshold,
                                         result_callback=save_result)
    detector = vision.FaceDetector.create_from_options(options)

    # Continuously capture images from the camera and run inference
    while True:
        # Capture a frame from the camera
        frame = picam2.capture_array()
        frame = cv2.flip(frame, 1)

        # Convert the frame from BGR to RGB as required by the TFLite model.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # Run face detection using the model.
        detector.detect_async(mp_image, time.time_ns() // 1_000_000)

        # Show the FPS
        fps_text = 'FPS = {:.1f}'.format(FPS)
        text_location = (left_margin, row_size)
        current_frame = frame
        cv2.putText(current_frame, fps_text, text_location, cv2.FONT_HERSHEY_DUPLEX,
                    font_size, text_color, font_thickness, cv2.LINE_AA)

        if DETECTION_RESULT:
            current_frame = visualize(current_frame, DETECTION_RESULT)

        cv2.imshow('face_detection', current_frame)

        # Stop the program if the ESC key is pressed.
        if cv2.waitKey(1) == 27:
            break

    detector.close()
    picam2.stop()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--model',
        help='Path of the face detection model.',
        required=False,
        default='detector.tflite')
    parser.add_argument(
        '--minDetectionConfidence',
        help='The minimum confidence score for the face detection to be '
             'considered successful.',
        required=False,
        type=float,
        default=0.5)
    parser.add_argument(
        '--minSuppressionThreshold',
        help='The minimum non-maximum-suppression threshold for face detection '
             'to be considered overlapped.',
        required=False,
        type=float,
        default=0.5)
    parser.add_argument(
        '--frameWidth',
        help='Width of frame to capture from camera.',
        required=False,
        type=int,
        default=1280)
    parser.add_argument(
        '--frameHeight',
        help='Height of frame to capture from camera.',
        required=False,
        type=int,
        default=720)
    args = parser.parse_args()

    run(args.model, args.minDetectionConfidence, args.minSuppressionThreshold,
        args.frameWidth, args.frameHeight)


if __name__ == '__main__':
    main()
