import os
import xml.dom.minidom as xmldom
import natsort

xml_path = './enannotations/'
img_path = './enimgs/'


dir_list = natsort.natsorted(os.listdir(xml_path))
img_list = natsort.natsorted(os.listdir(img_path))
for filename in dir_list:
    path = os.path.join(xml_path,filename)
    dom = xmldom.parse(path)
    data = dom.documentElement
    objs = data.getElementsByTagName("object")
    if objs==[]:
        for imgname in img_list:
            if filename.split('.')[0] == imgname.split('.')[0]:
                path_img = os.path.join(img_path,imgname)
                print(path_img + '已被移除！')
                os.remove(path_img)
        print(path+'已被移除！')
        os.remove(path)
    else:
        pass

