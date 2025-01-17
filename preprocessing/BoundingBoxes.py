import cv2
from SymbolRecognition.SymbolRecognition import SymbolRecognition
import collections
import os
import shutil

path_temp = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'results/temp/'))

class BoundingBoxes(object):
   """
   BoundingBoxes used to segment binary image into boxes.
   """

   def __init__(self):
      super(BoundingBoxes, self).__init__()
      self.symbolRecognition = SymbolRecognition()
      # save the last box to compare it to current box.
      self.lastBox = {"x": 0, "y": 0, "h": 0, "w": 0, "value": '1'}

   def SegmentImageToBoxes(self, binaryImagePath):
      """
      Segment the given image to separate bounding boxes.
      :param binaryImagePath: path to the binary image we want to segment
      :type binaryImagePath: string
      """
      # Open the binary image.
      image = cv2.imread(binaryImagePath)
      # Convert the white pixels to black and the blck to white.
      image[image == 255] = 1
      image[image == 0] = 255
      image[image == 1] = 0
      im2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

      # resize if the impage too small
      if (im2.shape[0] < 130) and (im2.shape[1] / im2.shape[0]) > 3.5:
         im2 = cv2.resize(im2, (4 * im2.shape[1], 4 * im2.shape[0]), interpolation=cv2.INTER_CUBIC)
         cv2.imwrite(binaryImagePath, im2)
         image = cv2.imread(binaryImagePath)

      ret, thresh = cv2.threshold(im2, 127, 255, 0)
      # Find all the contours using openCV function.
      im3, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      boundingBoxes = {}
      directory = ""
      # for each boundingBoxes - save as image.
      for i in range(1, len(contours)):
         currentBoundingBox = contours[i]
         # The coordinate of the boundingBoxes.
         x, y, w, h = cv2.boundingRect(currentBoundingBox)
         # check if skip
         if self._CheckIfContains(x, y, w, h):
            continue
         # Crop each box in the image and save it.
         letter = image[y:y + h, x:x + w]
         file_path = path_temp + str(i) + '.png'
         directory = os.path.dirname(file_path)
         try:
            os.stat(directory)
         except:
            os.mkdir(directory)
            # all the information about this boundingBox
         cv2.imwrite(file_path, letter)
         value = self.symbolRecognition.Recognize(file_path)
         # fix unusual cases
         if value == '\sum':
            x -= 7.5
         if value == '\cdot':
            if w > h + 10:
               value = '\\frac'
         if value == '\\frac':
            if abs(w - h) < 5:
               value = '\cdot'
         # check if equal sigh.
         if boundingBoxes.__contains__(x):
            if value == boundingBoxes.get(x)["value"]:
               if (value == '\\frac') or (value == "-"):
                  boundingBoxes.get(x)["value"] = "="
                  continue
            x += 0.5
         boundingBoxes.update({x: {"x": x, "y": y, "h": h, "w": w, "value": value}})
         self.lastBox = {"x": x, "y": y, "h": h, "w": w, "value": value}
      # remove help folder
      shutil.rmtree(directory)
      # Return array of boundingBoxes sorted by
      return sorted(boundingBoxes.items())


   def _CheckIfContains(self, x, y, w, h):
      # check if the current box is inside the last box
      if x + w < self.lastBox['x'] + self.lastBox['w'] and y + h < self.lastBox['y'] + self.lastBox['h'] \
              and x < self.lastBox['x'] + self.lastBox['w'] and y < self.lastBox['y'] + self.lastBox['h']\
              and x > self.lastBox['x'] and y > self.lastBox['y'] and self.lastBox['value'] != '\sqrt' or (h < 6 and w < 6):
         return True
      return False


