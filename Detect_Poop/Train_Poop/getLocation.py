import cv2

image = cv2.imread('src/Detect_Poop/poop/with_Poop/poop001.jpg')

cv2.imshow('Image', image)
cv2.waitKet(0)
cv2.destroyAllWindows()