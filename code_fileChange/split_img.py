# coding:utf-8
import cv2
import os
import PIL.Image as Image
import codecs
import xml_parse
import xml.dom.minidom as xmldom
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
import numpy as np
from PIL import Image
from tqdm import tqdm
import sys
import natsort  # 解决os.listdir遍历的顺序问题
import shutil

# 分割带标签

# shutil.rmtree('./split_annotation')
# shutil.rmtree('./split_img')
sys.setrecursionlimit(10000)
# 定义步长信息，stride越大，步长越大，生成的图片越少（最好不要超过0.8，会出现有的图片没有标注框的情况）
stride=0.5
output_shape = []

"""imgpath = './JPEGImages'  # 原图路径
annotation = './Annotations'  # 原图对应的标注xml文件路径
cropAnno = './new_annotation'  # 裁剪后存储xml的路径
cropImg = './new_img'  # 裁剪后存储图片的路径"""

def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint16)


def crop_xml_modify(head, objectlist, hmin, wmin, new_height, new_width, origin_xml__path):




    sizeobj = head['size']
    width = sizeobj.getElementsByTagName('width')[0]
    width.childNodes[0].data = str(new_width)
    # print(str(WIDTH))
    height = sizeobj.getElementsByTagName('height')[0]
    height.childNodes[0].data = str(new_height)

    # tree = ET.parse(origin_xml__path)
    # root = tree.getroot()
    obj = objectlist
    i = 0
    while (i < obj.length):
        # for obj in objectlist1:
        bndbox = obj[i].getElementsByTagName('bndbox')[0]
        xmin = bndbox.getElementsByTagName('xmin')[0]
        XMIN = float(xmin.childNodes[0].data)
        ymin = bndbox.getElementsByTagName('ymin')[0]
        YMIN = float(ymin.childNodes[0].data)
        xmax = bndbox.getElementsByTagName('xmax')[0]
        XMAX = float(xmax.childNodes[0].data)
        ymax = bndbox.getElementsByTagName('ymax')[0]
        YMAX = float(ymax.childNodes[0].data)
        if (XMIN >= wmin) and (XMAX <= (wmin + new_width)) and (YMIN >= hmin) and (YMAX <= (hmin + new_height)):
            xmin.childNodes[0].data = str(int(XMIN - wmin))
            xmax.childNodes[0].data = str(int(XMAX - wmin))
            ymin.childNodes[0].data = str(int(YMIN - hmin))
            ymax.childNodes[0].data = str(int(YMAX - hmin))
        else:
            obj.remove(obj[i])
            i = i - 1  # 一定要向前提一个位置 删除的话用for是会出错的 耽搁了好久。。。
            # obj = objectlist1[i-1]
        i = i + 1
    return head, obj

def crop_dataset(imgpath, output_shape, annotation, cropAnno, cropImg, stride,geshi):



    origin_image = cv2.imread(imgpath)

    # image = Image.open(imgpath)
    # image_np = load_image_into_numpy_array(image)
    # origin_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    height, width = origin_image.shape[:2]




    x = 0
    newheight = output_shape[0]
    newwidth = output_shape[1]
    while x < width:
        y = 0
        if x + newwidth <= width:
            while y < height:
                # 裁剪为output_shape*output_shape
                # newheight = output_shape
                # newwidth = output_shape
                head, objectlist = xml_parse.voc_xml_parse(annotation)

                if y + newheight <= height:
                    hmin = y
                    hmax = y + newheight
                    wmin = x
                    wmax = x + newwidth
                else:
                    hmin = height - newheight
                    hmax = height
                    wmin = x
                    wmax = x + newwidth
                    y = height  # JPEGImages
                #cropImg1 = cropImg + '_' + str(wmax) + '_' + str(hmax) + '.' + geshi
                modify_head, modify_objectlist = crop_xml_modify(head, objectlist, hmin, wmin, newheight, newwidth,
                                                                 origin_xml__path)
                cropAnno1 = cropAnno + '_' + str(wmax) + '_' + str(hmax) + '.xml'
                xml_parse.voc_xml_modify(cropAnno1, modify_head, modify_objectlist)

                tree = ET.parse(cropAnno1)
                root = tree.getroot()
                root.find('filename').text= cropAnno.split('\\')[1] + '_' + str(wmax) + '_' + str(hmax) + '.' + geshi
                tree = ET.ElementTree(root)
                tree.write(cropAnno1)


                cropImg1 = cropImg + '_' + str(wmax) + '_' + str(hmax) + '.' + geshi

                cv2.imwrite(cropImg1, origin_image[hmin: hmax, wmin: wmax])
                y = y + stride
                if y + output_shape[0] == height:  # 第一张图就已经涵盖了height*height
                    y = height
                # if y + newheight > height:
                #     break
        else:
            while y < height:
                # 裁剪为output_shape*output_shape
                # newheight = output_shape
                # newwidth = output_shape
                head, objectlist = xml_parse.voc_xml_parse(annotation)
                if y + newheight <= height:
                    hmin = y
                    hmax = y + newheight
                    wmin = width - newwidth
                    wmax = width
                else:
                    hmin = height - newheight
                    hmax = height
                    wmin = width - newwidth
                    wmax = width
                    y = height  # JPEGImages
                modify_head, modify_objectlist = crop_xml_modify(head, objectlist, hmin, wmin, newheight, newwidth,
                                                                 origin_xml__path)
                cropAnno1 = cropAnno + '_' + str(wmax) + '_' + str(hmax) + '.xml'
                xml_parse.voc_xml_modify(cropAnno1, modify_head, modify_objectlist)
                tree = ET.parse(cropAnno1)
                root = tree.getroot()
                root.find('filename').text = cropAnno.split('\\')[1] + '_' + str(wmax) + '_' + str(hmax) + '.' + geshi
                tree = ET.ElementTree(root)
                tree.write(cropAnno1)

                cropImg1 = cropImg + '_' + str(wmax) + '_' + str(hmax) + '.' + geshi

                cv2.imwrite(cropImg1, origin_image[hmin: hmax, wmin: wmax])

                y = y + stride
                # if y + newheight > height:
                #     break
            x = width
        x = x + stride
        if x + output_shape[1] == width:  # 第一张图就已经涵盖了height*height
            x = width
        # if x + newwidth > width:
        #     break


if __name__ == '__main__':

    imgpath = './raw'  # 原图路径
    annotation = './raw_labels'  # 原图对应的标注xml文件路径
    cropAnno = './enannotations'  # 裁剪后存储xml的路径
    cropImg = './enimgs'  # 裁剪后存储图片的路径
    if not os.path.exists(cropImg):
        os.mkdir(cropImg)
    if not os.path.exists(cropAnno):
        os.mkdir(cropAnno)

    mults = tqdm(os.listdir(imgpath))
    mults = natsort.natsorted(mults)
    for each in mults:
        # each = os.listdir(annotation)
        name = each.split('.')[0]
        geshi = each.split('.')[1]
        print(each)
        origin_img_path = os.path.join(imgpath, each)
        windows = cv2.imread(origin_img_path)

        output_shape = [int(windows.shape[0]*0.5), int(windows.shape[1]*0.5)]  # 512 1024
        stride = int(output_shape[1] * 0.7)

        origin_xml__path = os.path.join(annotation, name + '.xml')
        crop_img_path = os.path.join(cropImg, name)
        crop_xml__path = os.path.join(cropAnno, name)
        # tree = ET.parse(origin_xml__path)
        # root = tree.getroot()
        crop_dataset(origin_img_path, output_shape, origin_xml__path, crop_xml__path, crop_img_path, stride,geshi)
