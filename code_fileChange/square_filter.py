import os
import shutil
import xml.etree.ElementTree as ET
from PIL import Image

# 创建用于保存筛选后的图片和标签的目录
os.makedirs('images_filter', exist_ok=True)
os.makedirs('labels_filter', exist_ok=True)

# 遍历labels文件夹中的所有XML文件
for xml_file in os.listdir('labels'):
    if not xml_file.endswith('.xml'):
        continue

    # 解析XML文件
    tree = ET.parse(os.path.join('labels', xml_file))
    root = tree.getroot()

    # 获取图片文件名和尺寸
    img_filename = root.find('filename').text
    img_path = os.path.join('images', img_filename)
    img_width = int(root.find('size/width').text)
    img_height = int(root.find('size/height').text)

    # 遍历XML中的每个对象并计算其面积
    for obj in root.findall('object'):
        xmin = int(obj.find('bndbox/xmin').text)
        ymin = int(obj.find('bndbox/ymin').text)
        xmax = int(obj.find('bndbox/xmax').text)
        ymax = int(obj.find('bndbox/ymax').text)

        box_area = (xmax - xmin) * (ymax - ymin)

        # 如果面积大于100，则保存图片和XML
        if box_area > 10000:
            # 复制图片文件到images_filter文件夹
            shutil.copy(img_path, os.path.join('images_filter', img_filename))

            # 复制XML文件到labels_filter文件夹
            shutil.copy(os.path.join('labels', xml_file), os.path.join('labels_filter', xml_file))

            # 修改XML文件中的文件名和标注框坐标
            root.find('filename').text = img_filename
            root.find('size/width').text = str(xmax - xmin)
            root.find('size/height').text = str(ymax - ymin)
            root.find('size/depth').text = '3'
            obj.find('bndbox/xmin').text = '0'
            obj.find('bndbox/ymin').text = '0'
            obj.find('bndbox/xmax').text = str(xmax - xmin)
            obj.find('bndbox/ymax').text = str(ymax - ymin)

            # 保存修改后的XML文件
            tree.write(os.path.join('labels_filter', xml_file))
