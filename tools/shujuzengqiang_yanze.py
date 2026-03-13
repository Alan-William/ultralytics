import xml.etree.ElementTree as ET
import os
import numpy as np
from PIL import Image
import shutil
import imgaug as ia
from imgaug import augmenters as iaa
from tqdm import tqdm


def read_xml_annotation(root, image_id):
    in_file = open(os.path.join(root, image_id), encoding='UTF-8')
    # print(in_file)
    tree = ET.parse(in_file)
    root = tree.getroot()
    bndboxlist = []

    for object in root.findall('object'):  # 找到root节点下的所有country节点
        bndbox = object.find('bndbox')  # 子节点下节点rank的值

        xmin = int(bndbox.find('xmin').text)
        xmax = int(bndbox.find('xmax').text)
        ymin = int(bndbox.find('ymin').text)
        ymax = int(bndbox.find('ymax').text)
        # print(xmin,ymin,xmax,ymax)
        bndboxlist.append([xmin, ymin, xmax, ymax])
        # print(bndboxlist)

    # ndbox = root.find('object').find('bndbox')
    return bndboxlist



def change_xml_list_annotation(root, image_id, new_target, saveroot, xml_id):
    save_path = os.path.join(saveroot, xml_id)
    in_file = open(os.path.join(root, str(image_id) + '.xml'), encoding='UTF-8')  # 这里root分别由两个意思
    tree = ET.parse(in_file)
    elem = tree.find('filename')
    elem.text = xml_id + img_type
    xmlroot = tree.getroot()
    index = 0

    for object in xmlroot.findall('object'):  # 找到root节点下的所有country节点
        bndbox = object.find('bndbox')  # 子节点下节点rank的值

        new_xmin = new_target[index][0]
        new_ymin = new_target[index][1]
        new_xmax = new_target[index][2]
        new_ymax = new_target[index][3]

        xmin = bndbox.find('xmin')
        xmin.text = str(new_xmin)
        ymin = bndbox.find('ymin')
        ymin.text = str(new_ymin)
        xmax = bndbox.find('xmax')
        xmax.text = str(new_xmax)
        ymax = bndbox.find('ymax')
        ymax.text = str(new_ymax)

        index += 1

    tree.write(save_path + '.xml')


def simple_example(AUGLOOP,IMG_DIR,XML_DIR,AUG_IMG_DIR,AUG_XML_DIR):
    boxes_img_aug_list = []
    new_bndbox_list = []
    new_name = None

    for root, sub_folders, files in os.walk(XML_DIR):
        for name in tqdm(files):
            bndbox = read_xml_annotation(XML_DIR, name)
            shutil.copy(os.path.join(XML_DIR, name), AUG_XML_DIR)
            try:
                shutil.copy(os.path.join(IMG_DIR, name[:-4] + img_type), AUG_IMG_DIR)
            except:
                shutil.copy(os.path.join(IMG_DIR, name[:-4] + '.JPG'), AUG_IMG_DIR)
            # print(os.path.join(IMG_DIR, name[:-4] + img_type))

            for epoch in range(1, AUGLOOP + 1):
                # 增强
                if epoch == 1:
                    seq = iaa.Sequential([
                        ####0.75-1.5随机数值为alpha，对图像进行对比度增强，该alpha应用于每个通道
                        iaa.ContrastNormalization((0.75, 1.5), per_channel=True),
                    ])
                elif epoch == 2:
                    seq = iaa.Sequential([
                        #### loc 噪声均值，scale噪声方差，50%的概率，对图片进行添加白噪声并应用于每个通道
                        iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.1 * 255), per_channel=0.75),
                    ])
                elif epoch == 3:
                    seq = iaa.Sequential([
                        iaa.Fliplr(1),  # 水平镜像翻转
                    ])
                seq_det = seq.to_deterministic()  # 保持坐标和图像同步改变，而不是随机
                # 读取图片
                try:
                    img = Image.open(os.path.join(IMG_DIR, name[:-4] + img_type))
                except:
                    img = Image.open(os.path.join(IMG_DIR, name[:-4] + '.JPG'))

                # JPG不支持alpha透明度，有可能报RGBA错误，将图片丢弃透明度转成RGB
                img = img.convert('RGB')
                # sp = img.size
                img = np.asarray(img)
                # bndbox 坐标增强
                for i in range(len(bndbox)):
                    bbs = ia.BoundingBoxesOnImage([
                        ia.BoundingBox(x1=bndbox[i][0], y1=bndbox[i][1], x2=bndbox[i][2], y2=bndbox[i][3]),
                    ], shape=img.shape)

                    bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]
                    boxes_img_aug_list.append(bbs_aug)

                    # new_bndbox_list:[[x1,y1,x2,y2],...[],[]]
                    n_x1 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x1)))
                    n_y1 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y1)))
                    n_x2 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x2)))
                    n_y2 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y2)))
                    if n_x1 == 1 and n_x1 == n_x2:
                        n_x2 += 1
                    if n_y1 == 1 and n_y2 == n_y1:
                        n_y2 += 1
                    if n_x1 >= n_x2 or n_y1 >= n_y2:
                        print('error', name)
                    new_bndbox_list.append([n_x1, n_y1, n_x2, n_y2])

                    # 存储变化后的图片
                    image_aug = seq_det.augment_images([img])[0]
                    # 新文件名
                    new_name = name[:-4] + '-' + str(epoch)
                    path = os.path.join(AUG_IMG_DIR, new_name + img_type)

                    image_auged = bbs.draw_on_image(image_aug, thickness=0)
                    Image.fromarray(image_auged).save(path)

                # 存储变化后的XML
                change_xml_list_annotation(XML_DIR, name[:-4], new_bndbox_list, AUG_XML_DIR, new_name)
                new_bndbox_list = []


if __name__ == "__main__":

    # 随机种子
    ia.seed(1)
    img_type = '.jpg'
    # img_type = '.png'

    # 原数据路径
    IMG_DIR = "C:/Users/xxa/Desktop/ultralytics/tools_testpic/shujuzengqiang/yanse/images/"
    XML_DIR = "C:/Users/xxa/Desktop/ultralytics/tools_testpic/shujuzengqiang/yanse/xml"


    # 存储增强后的影像文件夹路径
    AUG_IMG_DIR = "C:/Users/xxa/Desktop/ultralytics/tools_result/shujuzengqiang/yanse/new_images/"
    if not os.path.exists(AUG_IMG_DIR):
        os.mkdir(AUG_IMG_DIR)
    # 存储增强后的XML文件夹路径
    AUG_XML_DIR = "C:/Users/xxa/Desktop/ultralytics/tools_result/shujuzengqiang/yanse/new_xml/"
    if not os.path.exists(AUG_XML_DIR):
        os.mkdir(AUG_XML_DIR)

    # 数据增强n倍
    simple_example(3, IMG_DIR, XML_DIR, AUG_IMG_DIR, AUG_XML_DIR)
