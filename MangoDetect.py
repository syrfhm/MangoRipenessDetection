import cv2
import numpy as np

def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

image = cv2.imread('unripe_mango.jpg')

resize_image1 = cv2.resize(image,(480,360))

adjusted = adjust_gamma(resize_image1, gamma=0.6)
#cv2.imshow('Original image', resize_image1)
#cv2.imshow('Adjusted image', adjusted)

hsv1 = cv2.cvtColor(adjusted, cv2.COLOR_BGR2HSV)
#cv2.imshow('original',hsv1)
#gray1 = cv2.cvtColor(resize_image1, cv2.COLOR_BGR2GRAY)

#_, threshold = cv2.threshold(gray1, 240, 255, cv2.THRESH_BINARY)
#cv2.imshow('test',threshold)

#Threshold
low_range = np.array([8,60,30])
high_range = np.array([80,255,255])

mask = cv2.inRange(hsv1, low_range, high_range)
#cv2.imshow('maskl',mask)
image_final = cv2.bitwise_and(adjusted, adjusted, mask=mask)
(b_ripe, g_ripe, r_ripe,x_ripe) = cv2.mean(image_final, mask)
print("R_mean:",r_ripe,"G_mean:", g_ripe,"B_mean:", b_ripe)
d_ripe = abs(b_ripe-60)+abs(g_ripe-176)+abs(r_ripe-224)
(b_unripe, g_unripe, r_unripe,x_unripe) = cv2.mean(image_final, mask)
d_unripe = abs(b_unripe-60)+abs(g_unripe-174)+abs(r_unripe-65)
print('distance to ripe:', d_ripe)
print('distance to unripe:', d_unripe)

if d_ripe<d_unripe:
    mask = cv2.inRange(hsv1, low_range, high_range)
    image_final = cv2.bitwise_and(adjusted, adjusted, mask=mask)
    print("the fruit is ripe")
    cv2.imshow('Final Image', image_final)
    #cv2.imshow('Adjusted image', adjusted)
    #cv2.imshow('HSV image', hsv1)
    #cv2.imshow('Masked image', mask)
else:
    mask = cv2.inRange(hsv1, low_range, high_range)
    image_final = cv2.bitwise_and(adjusted, adjusted, mask=mask)
    print("the fruit is unripe")
    cv2.imshow('Final image', image_final)
    #cv2.imshow('Adjusted image', adjusted)
    #cv2.imshow('HSV image', hsv1)
    #cv2.imshow('Masked image', mask)

cv2.waitKey(0)
cv2.destroyAllWindows()