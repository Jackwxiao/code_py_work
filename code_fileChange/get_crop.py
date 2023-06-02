# -*- coding: utf-8 -*-
# xml解析包
# 新的yolo5数据集创建
import xml.etree.ElementTree as ET
import os
from os import getcwd
import shutil
import cv2
import numpy as np
classes = ['dust']

# 进行归一化操作
def convert(size, box):  # size:(原图w,原图h) , box:(xmin,xmax,ymin,ymax)
    dw = 1. / size[0]  # 1/w
    dh = 1. / size[1]  # 1/h
    x = (box[0] + box[1]) / 2.0  # 物体在图中的中心点x坐标
    y = (box[2] + box[3]) / 2.0  # 物体在图中的中心点y坐标
    w = box[1] - box[0]  # 物体实际像素宽度
    h = box[3] - box[2]  # 物体实际像素高度
    x = x * dw  # 物体中心点x的坐标比(相当于 x/原图w)
    w = w * dw  # 物体宽度的宽度比(相当于 w/原图w)
    y = y * dh  # 物体中心点y的坐标比(相当于 y/原图h)
    h = h * dh  # 物体宽度的宽度比(相当于 h/原图h)
    return (x, y, w, h)  # 返回 相对于原图的物体中心点的x坐标比,y坐标比,宽度比,高度比,取值范围[0-1]


# year ='2012', 对应图片的id（文件名）
def convert_annotation(image_id,xml_dir,images_dir,crop_dir,labels):
    '''
    将对应文件名的xml文件转化为label文件，xml文件包含了对应的bunding框以及图片长款大小等信息，
    通过对其解析，然后进行归一化最终读到label文件中去，也就是说
    一张图片文件对应一个xml文件，然后通过解析和归一化，能够将对应的信息保存到唯一一个label文件中去
    labal文件中的格式：calss x y w h　　同时，一张图片对应的类别有多个，所以对应的ｂｕｎｄｉｎｇ的信息也有多个
    '''
    print(image_id)
    # 对应的通过year 找到相应的文件夹，并且打开相应image_id的xml文件，其对应bund文件
    in_file = open(xml_dir+'/%s.xml' % (image_id), 'r',  encoding='UTF-8')   # 训练集中的数据进行转换
    #out_file = open(labels + '/%s.txt' % (image_id), 'w', encoding='UTF-8')  # 写入转换结果

    # 解析xml文件
    tree = ET.parse(in_file)
    # 获得对应的键值对
    root = tree.getroot()
    # 获得图片的尺寸大小
    size = root.find('size')
    # 如果xml内的标记为空，增加判断条件

    if size != None:
        # 获得宽
        w = int(size.find('width').text)
        # 获得高
        h = int(size.find('height').text)
        img_path = images_dir + '/' + image_id + '.jpg'
        if not os.path.exists(img_path):
            img_path = images_dir + '/' + image_id + '.png'
        origin_img = cv2.imread(img_path)

        #中文路径
        #origin_img = cv2.imdecode(np.fromfile(aa, dtype=np.uint8), -1)

        i = 0
        # 遍历目标obj
        for obj in root.iter('object'):
            # 获得difficult ？？
            #difficult = obj.find('difficult').text
            # 获得类别 =string 类型
            cls = obj.find('name').text
            # if cls in ['bare_cover', 'over_truck', 'dirty_truck', 'road_hard', 'muck_cover', 'groud_dust', 'hoarding']:
            #     continue
            # 找到bndbox 对象
            xmlbox = obj.find('bndbox')

            # #截取切片图
            # # 获取对应的bndbox的数组 = ['xmin','xmax','ymin','ymax']
            xmin = int(float(xmlbox.find('xmin').text))
            xmax = int(float(xmlbox.find('xmax').text))
            ymin = int(float(xmlbox.find('ymin').text))
            ymax = int(float(xmlbox.find('ymax').text))

            # 过滤小目标  (应用在扬尘类别上 0.2)
            # if (ymax-ymin) < 20 or (xmax-xmin) < 20:
            #     continue
            # # 过滤大目标  (应用在扬尘类别上 0.5)
            # if (ymax - ymin)/h > 0.5 or (xmax - xmin)/w > 0.5:
            #     continue

            #截取大框图
            c_width = xmax - xmin
            c_height = ymax - ymin
            c_center = (xmin + c_width // 2, ymin + c_height // 2)
            crop_radis = c_height // 2 if c_height > c_width else c_width // 2
            crop_x1 = (c_center[0] - 4 * crop_radis) if (c_center[0] - 4 * crop_radis) > 0 else 0
            crop_x2 = (c_center[0] + 4 * crop_radis) if (c_center[0] + 4 * crop_radis) < w else w
            crop_y1 = (c_center[1] - 4 * crop_radis) if (c_center[1] - 4 * crop_radis) > 0 else 0
            crop_y2 = (c_center[1] + 4 * crop_radis) if (c_center[1] + 4 * crop_radis) < h else h

            #目标在大框图的相对坐标
            relat_x1 = xmin - crop_x1
            relat_x2 = xmax - crop_x1
            relat_y1 = ymin - crop_y1
            relat_y2 = ymax - crop_y1
            relat_b=(relat_x1,relat_x2,relat_y1,relat_y2)
            big_crop_w = crop_x2 - crop_x1
            big_crop_h = crop_y2 - crop_y1
            bb = convert((big_crop_w, big_crop_h), relat_b)
            cls_id = classes.index(cls)
            out_file = open(labels + '/' +image_id + '_' + str(i) + '.txt', 'w', encoding='UTF-8')  # 写入转换结果
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

            #crop_img = origin_img[ymin:ymax, xmin:xmax]
            crop_img = origin_img[crop_y1:crop_y2, crop_x1:crop_x2,:]

            # 截图
            cv2.imencode('.jpg', crop_img)[1].tofile(crop_dir +'/'+image_id + '_' + str(i) + '.jpg')
            #cv2.imwrite(waste_crop + '/' + image_id + '_' + str(i) + '.jpg', crop_img)
            i += 1
    # except:
    #     print(image_id)


# 先找labels文件夹如果不存在则创建
# root = r'D:\E_data\dust\dust_test\negative'
images_dir = r'/dust_all/dust_test\or'
crop_dir = r'/dust_all/dust_test\crop_img/'
#crop_dir = r'D:\E_data\dust\dust_train\neg\second_judge\guangdian\img2'
# 生成总的labels
labels = r'D:\wx3.29\images_process\dust_test\txt/'
#labels = r'D:\E_data\dust\dust_train\neg\second_judge\guangdian\labels2'
xml_dir = r'/dust_all/dust_test\xml'
xml_num = os.listdir(xml_dir)
xml_name_lst = []
for xml in xml_num:
    xml_name = xml[:-4]
    xml_name_lst.append(xml_name)
# print(xml_name_lst)

# 将对应的文件_id以及全路径写进去并换行
for image_id in xml_name_lst:
    convert_annotation(image_id,xml_dir,images_dir,crop_dir,labels)

print("done")



