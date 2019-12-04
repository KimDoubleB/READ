import math
import os
import pickle
import sys
from collections import OrderedDict
import pandas as pd

import cv2
import imutils
import numpy as np
from django.core.files.storage import default_storage
from imutils import face_utils

import dlib

from .models import User_Image

FACIAL_ONLY = OrderedDict([
   ("right_eye", (36, 42)),
   ("left_eye", (42, 48)),
   ("nose", (27, 36)),
   ("jaw", (0, 17))
])
def area_cal(ad, bd, cd):
   s = (ad + bd + cd) / 2.0
   area = (s*(s-ad)*(s-bd)*(s-cd)) ** 0.5
   return area

def dist(p1, p2):
   return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def dist_x(p1, p2):
   return math.hypot(p1[0] - p2[0], 0)
def dist_y(p1, p2):
   return math.hypot(0, p1[1]-p2[1])

def area_eye(eye_points, i):
   dist_list = [
      dist(eye_points[i], eye_points[i+1]),
      dist(eye_points[i+1], eye_points[i+2]),
      dist(eye_points[i], eye_points[i+2]),
      dist(eye_points[i+2], eye_points[i+3]),
      dist(eye_points[i], eye_points[i+3]),
      dist(eye_points[i], eye_points[i+5]),
      dist(eye_points[i+5], eye_points[i+3]),
      dist(eye_points[i+5], eye_points[i+4]),
      dist(eye_points[i+4], eye_points[i+3])
      ]

   return (area_cal(dist_list[0], dist_list[1], dist_list[2]) + 
   area_cal(dist_list[2], dist_list[3], dist_list[4]) + 
   area_cal(dist_list[4], dist_list[5], dist_list[6]) + 
   area_cal(dist_list[6], dist_list[7], dist_list[8])
   )

def get_gaze_ratio(eye_points, facial_landmarks, image, gray):
   left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                              (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                              (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                              (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                              (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                              (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)
   # cv2.polylines(frame, [left_eye_region], True, (0, 0, 255), 2)

   height, width, _ = image.shape
   mask = np.zeros((height, width), np.uint8)
   cv2.polylines(mask, [left_eye_region], True, 255, 2)
   cv2.fillPoly(mask, [left_eye_region], 255)
   eye = cv2.bitwise_and(gray, gray, mask=mask)

   min_x = np.min(left_eye_region[:, 0])
   max_x = np.max(left_eye_region[:, 0])
   min_y = np.min(left_eye_region[:, 1])
   max_y = np.max(left_eye_region[:, 1])
   
   gray_eye = eye[min_y: max_y, min_x: max_x]
   _, threshold_eye = cv2.threshold(gray_eye, 55, 255, cv2.THRESH_BINARY)
   height, width = threshold_eye.shape
   left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
   left_side_white = cv2.countNonZero(left_side_threshold)

   right_side_threshold = threshold_eye[0: height, int(width / 2): width]
   right_side_white = cv2.countNonZero(right_side_threshold)
   # print('left_side_white', left_side_white)
   # print('right_side_white', right_side_white)
   

   if right_side_white < 2:
      gaze_ratio = left_side_white
   else:
      gaze_ratio = left_side_white / right_side_white
   
   #print('gaze_ratio', gaze_ratio)
   return gaze_ratio

def analyze_image(user, video, currentTime, path, image):
  image_file = default_storage.save('images/' + image.name, image)


  # load the COCO class labels our YOLO model was trained on
  labelsPath = os.path.sep.join(['./analyzer/yolo-coco/', "coco.names"])
  LABELS = open(labelsPath).read().strip().split("\n")

  # derive the paths to the YOLO weights and model configuration
  weightsPath = os.path.sep.join(['./analyzer/yolo-coco/', "yolov3.weights"])
  configPath = os.path.sep.join(['./analyzer/yolo-coco/', "yolov3.cfg"])

  net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

  # initialize dlib's face detector (HOG-based) and then create
  # the facial landmark predictor
  detector = dlib.get_frontal_face_detector()
  predictor = dlib.shape_predictor('./analyzer/data/shape_predictor_68_face_landmarks.dat')

  FINAL_result = []

  # load the input image, resize it, and convert it to grayscale
  image_t = cv2.imread('./media/' + path)
  image_t = imutils.resize(image_t, width=500)


  (H, W) = image_t.shape[:2]

  # determine only the *output* layer names that we need from YOLO
  ln = net.getLayerNames()
  ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

  # construct a blob from the input image and then perform a forward
  # pass of the YOLO object detector, giving us our bounding boxes and
  # associated probabilities
  blob = cv2.dnn.blobFromImage(image_t, 1 / 255.0, (416, 416),
    swapRB=True, crop=False)
  net.setInput(blob)
  layerOutputs = net.forward(ln)

  # initialize our lists of detected bounding boxes, confidences, and
  # class IDs, respectively
  boxes = []
  confidences = []
  classIDs = []

    # loop over each of the layer outputs
  for output in layerOutputs:
    # loop over each of the detections
    for detection in output:
      # extract the class ID and confidence (i.e., probability) of
      # the current object detection
      scores = detection[5:]
      classID = np.argmax(scores)
      confidence = scores[classID]

      # filter out weak predictions by ensuring the detected
      # probability is greater than the minimum probability
      if confidence > 0.5:
        # scale the bounding box coordinates back relative to the
        # size of the image, keeping in mind that YOLO actually
        # returns the center (x, y)-coordinates of the bounding
        # box followed by the boxes' width and height
        box = detection[0:4] * np.array([W, H, W, H])
        (centerX, centerY, width, height) = box.astype("int")

        # use the center (x, y)-coordinates to derive the top and
        # and left corner of the bounding box
        x = int(centerX - (width / 2))
        y = int(centerY - (height / 2))

        # update our list of bounding box coordinates, confidences,
        # and class IDs
        boxes.append([x, y, int(width), int(height)])
        confidences.append(float(confidence))
        classIDs.append(classID)

  error = 0

  # apply non-maxima suppression to suppress weak, overlapping bounding boxes
  idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)
  # if detect nothing using deep learning (coco dataset)
  if len(idxs) == 0:
    error = -1 # means "Detect nothing" error
  else:
    items = list(set([classIDs[t] for t in idxs.flatten()]))
    detected_items = [LABELS[item] for item in items]
    # if don't detect person using deep learning (coco dataset)
    if not 'person' in detected_items:
      error = -2 # means "There isn't person" error
    else:
      gray = cv2.cvtColor(image_t, cv2.COLOR_BGR2GRAY)
      rects = detector(gray, 1)
      # Not detect human face using opencv
      if len(rects) == 0: 
        error = -3 # means "Get closer to your webcam" error

  if error < 0:
    FINAL_result = error
  else:
    max_index = max([[dist([rect.left(), rect.top()], [rect.right(), rect.bottom()]), i] for (i, rect) in enumerate(rects)])[1]
    rect = rects[max_index]
    shape = predictor(gray, rect)
    gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], shape, image_t, gray)
    gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], shape, image_t, gray)

    if gaze_ratio_left_eye < 0.6 or gaze_ratio_right_eye < 0.6:
      if gaze_ratio_left_eye > gaze_ratio_right_eye:
          FINAL_result.append(gaze_ratio_right_eye)
      else:
          FINAL_result.append(gaze_ratio_left_eye)
    elif gaze_ratio_left_eye > 1.4 or gaze_ratio_right_eye > 1.4:
      if gaze_ratio_left_eye > gaze_ratio_right_eye:
          FINAL_result.append(gaze_ratio_left_eye)
      else:
          FINAL_result.append(gaze_ratio_right_eye)
    else:
      FINAL_result.append(0)

    shape = face_utils.shape_to_np(shape)

    for (name, (i, j)) in FACIAL_ONLY.items():
      if name == 'left_eye' or name == 'right_eye':
          eye_height = dist_y(shape[i+1], shape[i+5])
          FINAL_result.append(math.log10(eye_height))
                
      if name == 'jaw':
          right = shape[3]
          left = shape[13]
          medium = shape[8]
          
          left_dist = dist_x(left, medium) / dist_x(left, right)
          right_dist = dist_x(right, medium) / dist_x(left, right)
          FINAL_result.append(left_dist)
          FINAL_result.append(right_dist)

      if name == 'nose':
          right = shape[31]
          left = shape[35]
          medium = shape[33]

          left_dist = dist_x(left, medium) / dist_x(left, right)
          right_dist = dist_x(right, medium) / dist_x(left, right)
          FINAL_result.append(left_dist)
          FINAL_result.append(right_dist)
    
    xgb_model = pickle.load(open('./analyzer/data/xgb_reg.pkl', 'rb'))
    columns = ['gaze', 'left_eye', 'right_eye', 'nose_left_ratio', 'nose_right_ratio', 'jaw_left_ratio', 'jaw_right_ratio']
    present = pd.DataFrame([FINAL_result], columns = columns)
    FINAL_result = xgb_model.predict(present)

  os.remove('./media/' + path)

  # save model
  user_img = User_Image(
      user = user,
      video = video,
      currentTime = currentTime,
      path = path,
      reaction = str(FINAL_result) # Temporary data (TODO: deep learning)
  )
  user_img.save()
