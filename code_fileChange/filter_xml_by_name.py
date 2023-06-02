import os
from xml.dom.minidom import parse
import shutil

def collect_names(xml_path):
    classes=[]
    dom = parse(xml_path)
    root_node = dom.documentElement
    objects=root_node.getElementsByTagName("object")
    for object in objects:
        name=object.getElementsByTagName("name")[0].childNodes[0].data
        classes.append(name)
    return classes

class_name='truck'
xmls_path=r'D:\wx3.29\images_process\truck1\out\labels'
dst_path=r'D:\wx3.29\images_process\truck1\out\xmls_truck1'
xmls=os.listdir(xmls_path)
for xml in xmls:
    xml_path=f'{xmls_path}/{xml}'
    try:
        classes=collect_names(xml_path)
        if 'truck' in classes:
            shutil.copy(xml_path, f'{dst_path}/{xml}')
            print(xml)
    except:
        print('错误',xml_path)