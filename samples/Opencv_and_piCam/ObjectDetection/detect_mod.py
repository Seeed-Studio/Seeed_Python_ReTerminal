import cv2
from picamera2 import Picamera2
import numpy as np
import time
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils
import argparse
import sys
import time

def run(model: str, width: int, height: int, num_threads: int, enable_edgetpu: bool) -> None:
    # Variables to calculate FPS
    counter, fps = 0, 0
    start_time = time.time()

    # Initialize the PiCamera
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (width, height)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()

    # Visualization parameters
    row_size = 20  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 255)  # red
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

    # Initialize the object detection model
    base_options = core.BaseOptions(file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
    detection_options = processor.DetectionOptions(max_results=8, score_threshold=0.3)
    options = vision.ObjectDetectorOptions(base_options=base_options, detection_options=detection_options)
    detector = vision.ObjectDetector.create_from_options(options)

    # Continuously capture images from the camera and run inference
    while True:
        im = picam2.capture_array()

        counter += 1

        # Convert the image from BGR to RGB as required by the TFLite model.
        rgb_image = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

        # Create a TensorImage object from the RGB image.
        input_tensor = vision.TensorImage.create_from_array(rgb_image)

        # Run object detection estimation using the model.
        detection_result = detector.detect(input_tensor)

        # Draw keypoints and edges on input image
        im = utils.visualize(im, detection_result)

        # Calculate the FPS
        if counter % fps_avg_frame_count == 0:
            end_time = time.time()
            fps = fps_avg_frame_count / (end_time - start_time)
            start_time = time.time()

        # Show the FPS
        fps_text = 'FPS = {:.1f}'.format(fps)
        text_location = (left_margin, row_size)
        cv2.putText(im, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN, font_size, text_color, font_thickness)

        # Stop the program if the ESC key is pressed.
        if cv2.waitKey(1) == 27:
            break
        cv2.imshow('object_detector', im)

    picam2.stop()
    cv2.destroyAllWindows()


def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model',
      help='Path of the object detection model.',
      required=False,
      default='efficientdet_lite0.tflite')
  parser.add_argument(
      '--frameWidth',
      help='Width of frame to capture from camera.',
      required=False,
      type=int,
      default=640)
  parser.add_argument(
      '--frameHeight',
      help='Height of frame to capture from camera.',
      required=False,
      type=int,
      default=480)
  parser.add_argument(
      '--numThreads',
      help='Number of CPU threads to run the model.',
      required=False,
      type=int,
      default=4)
  parser.add_argument(
      '--enableEdgeTPU',
      help='Whether to run the model on EdgeTPU.',
      action='store_true',
      required=False,
      default=False)
  args = parser.parse_args()

  run(args.model,args.frameWidth, args.frameHeight,
      int(args.numThreads), bool(args.enableEdgeTPU))


if __name__ == '__main__':
  main()
