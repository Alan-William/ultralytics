import numpy as np
import cv2


def random_perspective(img, degrees, translate, scale, shear, perspective):
    # 获取图像的垂直尺寸（高度）和水平尺寸（宽度）
    height = img.shape[0]
    width = img.shape[1]

    # 平移矩阵，将图像的中心点平移到原点位置，便于后续处理
    C = np.eye(3)
    C[0, 2] = -img.shape[1] / 2
    C[1, 2] = -img.shape[0] / 2

    # 透视变换矩阵，随机采样透视变换程度，构造透视变换矩阵
    P = np.eye(3)
    P[2, 0] = np.random.uniform(-perspective, perspective)  # x perspective (about y)随机采样
    P[2, 1] = np.random.uniform(-perspective, perspective)  # y perspective (about x)随机采样

    # 旋转和缩放矩阵，随机采样旋转角度和缩放程度，构造旋转缩放矩阵
    R = np.eye(3)
    a = np.random.uniform(-degrees, degrees)
    # a += random.choice([-180, -90, 0, 90])  # add 90deg rotations to small rotations
    s = np.random.uniform(1 - scale, 1 + scale)
    # s = 2 ** random.uniform(-scale, scale)
    R[:2] = cv2.getRotationMatrix2D(angle=a, center=(0, 0), scale=s)  # 旋转角度 旋转中心 缩放比例

    # 剪切变换矩阵，随机采样剪切程度，构造剪切变换矩阵
    S = np.eye(3)
    S[0, 1] = np.tan(np.random.uniform(-shear, shear) * np.pi / 180)
    S[1, 0] = np.tan(np.random.uniform(-shear, shear) * np.pi / 180)

    # 平移变换矩阵，随机采样平移程度，构造平移变换矩阵
    T = np.eye(3)
    T[0, 2] = np.random.uniform(0.5 - translate, 0.5 + translate) * width
    T[1, 2] = np.random.uniform(0.5 - translate, 0.5 + translate) * height

    # 组合变换矩阵，先对图像进行剪切、缩放、旋转、透视变换，再平移回原位
    M = T @ S @ R @ P @ C
    # 判断图像是否有变化，如果有变化，则进行仿射变换或透视变换
    if (M != np.eye(3)).any():
        if perspective:
            img = cv2.warpPerspective(img, M, dsize=(width, height), borderValue=(114, 114, 114))
        else:  # affine
            img = cv2.warpAffine(img, M[:2], dsize=(width, height), borderValue=(114, 114, 114))

    return img


if __name__ == '__main__':
    path = "C:/Users/xxa/Desktop/ultralytics/tools_testpic/shujuzengqiang/xuanzhuan/d(5).jpg"
    original_img = cv2.imread(path)
    img = random_perspective(original_img, degrees=50, translate=0, scale=0, shear=0, perspective=0)
    cv2.imshow("random_perspective_degrees:", img)
    cv2.imwrite(r"C:/Users/xxa/Desktop/ultralytics/tools_result/shujuzengqiang/xuanzhuan/temp1.png", img)
    cv2.waitKey(0)

    img = random_perspective(original_img, degrees=0, translate=0.5, scale=0, shear=0, perspective=0)
    cv2.imshow("random_perspective_translate:", img)
    cv2.imwrite(r"C:/Users/xxa/Desktop/ultralytics/tools_result/shujuzengqiang/xuanzhuan/temp2.png", img)
    cv2.waitKey(0)

    img = random_perspective(original_img, degrees=0, translate=0, scale=0.9, shear=0, perspective=0)
    cv2.imshow("random_perspective_scale:", img)
    cv2.imwrite(r"C:/Users/xxa/Desktop/ultralytics/tools_result/shujuzengqiang/xuanzhuan/temp3.png", img)
    cv2.waitKey(0)

    img = random_perspective(original_img, degrees=0, translate=0.0, scale=0, shear=20, perspective=0)
    cv2.imshow("random_perspective_shear:", img)
    cv2.imwrite(r"C:/Users/xxa/Desktop/ultralytics/tools_result/shujuzengqiang/xuanzhuan/temp4.png", img)
    cv2.waitKey(0)

    img = random_perspective(original_img, degrees=0, translate=0.0, scale=0, shear=0, perspective=0.001)
    cv2.imshow("random_perspective_perspective:", img)
    cv2.imwrite(r"C:/Users/xxa/Desktop/ultralytics/tools_result/shujuzengqiang/xuanzhuan/temp5.png", img)
    cv2.waitKey(0)


