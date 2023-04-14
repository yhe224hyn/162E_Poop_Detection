import cv2
import numpy as np

# Read image
image = cv2.imread("src/Detect_Poop/learning_node/learning_node/sample.jpg")

# Extract pixel color
color = image[444, 488]

# Convert BGR to HSV
bgr_color = np.uint8([[[color[2], color[1], color[0]]]])
hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)

# Print HSV values
print(hsv_color)