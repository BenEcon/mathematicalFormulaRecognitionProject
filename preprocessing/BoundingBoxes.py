import cv2


class BoundingBoxes(object):
   """
   BoundingBoxes used to segment binary image into boxes.
   """

   def __init__(self):
      super(BoundingBoxes, self).__init__()

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
      ret, thresh = cv2.threshold(im2, 127, 255, 0)
      # Find all the contours using openCV function.
      im3, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      boundingBoxes = []
      #ToDo - check if the boundongBoxes are atomic.
      # for each boundingBoxes - save as image.
      for i in range(1, len(contours)):
         currentBoundingBox = contours[i]
         # The coordinate of the boundingBoxes.
         x, y, w, h = cv2.boundingRect(currentBoundingBox)
         # Crop each box in the image and save it.
         letter = image[y:y + h, x:x + w]
         cv2.imwrite(str(i) + '.png', letter)
         boundingBoxes.append(str(i) + '.png')
      # Return array of boundingBoxes
      return boundingBoxes
