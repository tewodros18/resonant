import cv2
import numpy as np

image = cv2.imread('woman-playing-a-guitar-simon-vouet.jpg')

x_min, y_min, x_max, y_max = 913,778,1457,1512
cropped_image = image[y_min:y_max, x_min:x_max]
color = (0, 255, 0)
thickness = 2

mask = np.zeros(image.shape[:2], dtype=np.uint8)
cv2.rectangle(mask, (1764,692), (2458,2343), 255, -1)
#cv2.imshow("Rectangular Mask", mask)
#cv2.waitKey(0)
# apply our mask -- notice how only the person in the image is
# cropped out
masked = cv2.bitwise_and(image, image, mask=mask)
#cv2.imshow("Mask Applied to Image", masked)
#cv2.waitKey(0)

cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, thickness)
imS = cv2.resize(image, (960, 960)) 
cv2.imshow('Image with Bounding Box', imS)
cv2.waitKey(0)
cv2.destroyAllWindows()
#cv2.imwrite('image_with_bounding_box.jpg', image)