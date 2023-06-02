# -*- coding: utf-8 -*-
'''
@Project ：yolov5-v6.1-pytorch 
@File    ：label_transform.py
@Author  ：Jackwxiao
@Date    ：2022/11/7 16:30 
'''

import os
import glob
from PIL import Image

# 将yolo格式(txt)转换为voc格式(xml)

# img_path = 'JPEGImages'
# yolo_txt = 'labels'
# voc_annotations = 'Annotations'
#
# # 目标类别
# labels = ['Insulator', 'Defect']
# # 图像存储位置
# src_img_dir = img_path  # 添加你的路径
# # 图像的txt文件存放位置
# src_txt_dir = yolo_txt
# src_xml_dir = voc_annotations
#
# img_Lists = glob.glob(src_img_dir + '/*.jpg')
#
# img_basenames = []
# for item in img_Lists:
#     img_basenames.append(os.path.basename(item))
#
# img_names = []
# for item in img_basenames:
#     temp1, temp2 = os.path.splitext(item)
#     img_names.append(temp1)
#
# for img in img_names:
#     im = Image.open((src_img_dir + '/' + img + '.jpg'))
#     width, height = im.size
#
#     # 打开txt文件
#     gt = open(src_txt_dir + '/' + img + '.txt').read().splitlines()
#     print(gt)
#     if gt:
#         # 将主干部分写入xml文件中
#         xml_file = open((src_xml_dir + '/' + img + '.xml'), 'w')
#         xml_file.write('<annotation>\n')
#         xml_file.write('    <folder>VOC2007</folder>\n')
#         xml_file.write('    <filename>' + str(img) + '.jpg' + '</filename>\n')
#         xml_file.write('    <size>\n')
#         xml_file.write('        <width>' + str(width) + '</width>\n')
#         xml_file.write('        <height>' + str(height) + '</height>\n')
#         xml_file.write('        <depth>3</depth>\n')
#         xml_file.write('    </size>\n')
#         xml_file.write('<source>\n')
#         xml_file.write('    <database>Unknown</database>\n')
#         xml_file.write('</source>\n')
#         xml_file.write('<segmented>0</segmented>\n')
#         # write the region of image on xml file
#         for img_each_label in gt:
#             spt = img_each_label.split(' ')  # 这里如果txt里面是以逗号‘，’隔开的，那么就改为spt = img_each_label.split(',')。
#             print(f'spt:{spt}')
#             xml_file.write('    <object>\n')
#             xml_file.write('        <name>' + str(labels[int(spt[0])]) + '</name>\n')
#             xml_file.write('        <pose>Unspecified</pose>\n')
#             xml_file.write('        <truncated>0</truncated>\n')
#             xml_file.write('        <difficult>0</difficult>\n')
#             xml_file.write('        <bndbox>\n')
#
#             center_x = round(float(spt[1].strip()) * width)
#             center_y = round(float(spt[2].strip()) * height)
#             bbox_width = round(float(spt[3].strip()) * width)
#             bbox_height = round(float(spt[4].strip()) * height)
#             xmin = str(int(center_x - bbox_width / 2))
#             ymin = str(int(center_y - bbox_height / 2))
#             xmax = str(int(center_x + bbox_width / 2))
#             ymax = str(int(center_y + bbox_height / 2))
#
#             xml_file.write('            <xmin>' + xmin + '</xmin>\n')
#             xml_file.write('            <ymin>' + ymin + '</ymin>\n')
#             xml_file.write('            <xmax>' + xmax + '</xmax>\n')
#             xml_file.write('            <ymax>' + ymax + '</ymax>\n')
#             xml_file.write('        </bndbox>\n')
#             xml_file.write('    </object>\n')
#
#         xml_file.write('</annotation>')



import xml.etree.ElementTree as ET
import os


# voc格式转换为yolo格式

def convert(size, box):
    x_center = (box[0] + box[1]) / 2.0
    y_center = (box[2] + box[3]) / 2.0
    x = x_center / size[0]
    y = y_center / size[1]

    w = (box[1] - box[0]) / size[0]
    h = (box[3] - box[2]) / size[1]

    # print(x, y, w, h)
    return (x, y, w, h)


def convert_annotation(xml_files_path, save_txt_files_path, classes):
    xml_files = os.listdir(xml_files_path)
    # print(xml_files)
    for xml_name in xml_files:
        # print(xml_name)
        xml_file = os.path.join(xml_files_path, xml_name)
        out_txt_path = os.path.join(save_txt_files_path, xml_name.split('.')[0] + '.txt')
        out_txt_f = open(out_txt_path, 'w')
        tree = ET.parse(xml_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            # b=(xmin, xmax, ymin, ymax)
            # print(w, h, b)
            bb = convert((w, h), b)
            out_txt_f.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


if __name__ == "__main__":
    # 把voc的xml标签文件转化为yolo的txt标签文件
    # 1、需要转化的类别
    # classes = ['pinhole', 'scratch', 'dirty', 'fold']  # 注意：这里根据自己的类别名称及种类自行更改
    classes = ['dust']  # 注意：这里根据自己的类别名称及种类自行更改
    # 2、voc格式的xml标签文件路径
    xml_files1 = r'D:\wx3.29\images_process\dust\dust_429checked\labels/'
    # 3、转化为yolo格式的txt标签文件存储路径
    save_txt_files1 = r'D:\wx3.29\images_process\dust\dust_429checked\txt/'

    convert_annotation(xml_files1, save_txt_files1, classes)