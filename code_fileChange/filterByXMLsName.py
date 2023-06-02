import os
import xml.etree.ElementTree as ET
import shutil

def filter_xml_files(xml_path, dst_path):
    """
    根据标签名过滤XML文件
    :param xml_path: XML文件所在的文件夹路径
    :param dst_path: 过滤后的XML文件所在的文件夹路径
    """
    # 如果目标文件夹不存在，则创建目标文件夹
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)

    # 遍历XML文件夹下的所有XML文件
    for xml_file in os.listdir(xml_path):
        if not xml_file.endswith('.xml'):
            continue

        # 解析XML文件
        xml_tree = ET.parse(os.path.join(xml_path, xml_file))
        xml_root = xml_tree.getroot()

        # 获取XML文件中所有标签的名称
        tag_names = [tag.tag for tag in xml_root.iter()]

        # 判断XML文件中是否包含需要过滤的标签
        if 'bare_cover' in tag_names and 'muck_cover' not in tag_names:
            # 如果XML文件中只包含bare_cover标签，则将该XML文件移动到目标文件夹
            shutil.move(os.path.join(xml_path, xml_file), os.path.join(dst_path, xml_file))

xml_path = r'D:\wx3.29\images_process\duichang\test'
dst_path = r'D:\wx3.29\images_process\duichang\test2'
filter_xml_files(xml_path, dst_path)