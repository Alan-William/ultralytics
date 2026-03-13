import cv2
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'SimHei'  # matplotlib 绘图库正常使用中文黑体

# 读取图像信息
img0 = cv2.imread('C:/Users/xxa/Desktop/ultralytics/tools_testpic/zhifangtu/1.jpg')
img1 = cv2.resize(img0, dsize=None, fx=1, fy=1)
h, w = img1.shape[:2]
print(h, w)
img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
cv2.namedWindow("ago")
cv2.imshow("ago", img1)
cv2.waitKey(delay=0)

# 绘制直方图
hist0 = cv2.calcHist([img2], [0], None, [256], [0, 255])
plt.plot(hist0, label="灰度图直方图", linestyle="-", color='g')
plt.legend()  # 增加图例
plt.savefig("C:/Users/xxa/Desktop/ultralytics/tools_result/zhifangtu/cveight2.jpg")  # 保存直方图
plt.show()

img3 = cv2.equalizeHist(img2)  # 直方图均衡化
cv2.namedWindow("now")
cv2.imshow("now", img3)

cv2.waitKey(delay=0)
cv2.imwrite('C:/Users/xxa/Desktop/ultralytics/tools_result/zhifangtu/' + 'junhenghua.jpg', img3)
# 绘制均衡化后的直方图
# 绘制直方图
hist0 = cv2.calcHist([img2], [0], None, [256], [0, 255])
hist1 = cv2.calcHist([img3], [0], None, [256], [0, 255])
# plt.subplot(2,1,1)
# plt.plot(hist0, label = "灰度图直方图", linestyle = "-", color = 'g')
# plt.legend()
# plt.subplot(2,1,2)
plt.plot(hist1, label="均衡化直方图", linestyle="-", color='r')
plt.legend()
plt.savefig("C:/Users/xxa/Desktop/ultralytics/tools_result/zhifangtu/cveight3.jpg")
plt.show()
