# -*- coding: utf-8 -*-
'''
@Project ：yolov5-v6.1-pytorch 
@File    ：change_labels.py
@Author  ：Jackwxiao
@Date    ：2022/11/21 21:26
改变标签里的内容
'''
import xml.etree.ElementTree as ET
import os


def reLabelName(old_xml_path, new_xml_path, new_labeli, new_labeld):
    # 判断路径是否存在
    if os.path.exists(old_xml_path):
        # 获取该目录下所有文件，存入列表中
        fileList = os.listdir(old_xml_path)
        if len(fileList) > 0:
            if not os.path.exists(new_xml_path):
                os.makedirs(new_xml_path)
        for xml in fileList:
            old_xml_full_path = os.path.join(old_xml_path, xml)
            tree = ET.parse(old_xml_full_path)  # 解析xml文件路径
            nodes = tree.findall('./object')
            for node in nodes:
                node.find('name').text
                print(node.find('name').text)
                if node.find('name').text == 'circular':
                    node.find('name').text = new_labeli
                if node.find('name').text == 'muck_cover':
                    node.find('name').text = new_labeld
            new_xml_full_path = os.path.join(new_xml_path, xml)
            tree.write(new_xml_full_path)

if __name__ == '__main__':
    old_xml_path = r'D:\wx3.29\images_process\duichang\annotations/'
    new_xml_path = r'D:\wx3.29\images_process\duichang\annotations1_stack/'
    new_labeld = 'no_'
    new_labeli = 'stack'
    reLabelName(old_xml_path, new_xml_path, new_labeli, new_labeld)
