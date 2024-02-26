import cv2
import numpy as np
image = cv2.imread('../UI_image/a1.jpg')  
# 將圖片轉換為RGBA，以便添加透明度通道
img_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

# 將圖片從 BGR 轉換到 HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# 設定黑色的 HSV 閾值範圍
lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 30])       

# 將背景變白，物體保持黑色
mask = cv2.inRange(hsv, lower_black, upper_black)
img_rgba[:, :, 3] = np.where(mask == 255, 0, 255)

cv2.imwrite('../UI_image/a1_nb.png', img_rgba)
