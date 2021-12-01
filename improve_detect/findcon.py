import cv2
import numpy as np
from read_num import read_num_path

img = cv2.imread('image_65.png')

x_size = img.shape[0]
y_size = img.shape[1]
edge = cv2.Canny(img, 240, 250, True)

contours, hierarchy = cv2.findContours(edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

app = []
for i in range(len(contours)):
    length = cv2.arcLength(contours[i], True)
    app.append((contours[i], length))

app.sort(key = lambda x: x[1], reverse = True)
'''a
contours = []
for i in range(min(len(app), 5)):
    contours.append(app[i][0])
'''

emp = np.zeros((x_size, y_size))
img = cv2.drawContours(emp, contours, -1, (255, 0, 0), 6)


cv2.imwrite("test.jpg", img)

print(read_num_path('test.jpg'))
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()