import os
from shutil import move
import cv2
from tqdm import tqdm

class_name='Industrial_pocket'
xmls_path=f'data/{class_name}/labels_ad'
images_path=f'data/{class_name}/images_ad'
images_no_an_path=f'data/{class_name}/trash'
xmls_no_image_path=f'data/{class_name}/trash'


xmlnames=os.listdir(xmls_path)
imagenames=os.listdir(images_path)

# 将jpg格式改为png
for image in tqdm(imagenames):
    if image[-4:]=='.png':
        try:
            img=cv2.imread(f'{images_path}/{image}')
            cv2.imwrite(f'{images_path}/{image[:-4]}.jpg', img)
            os.remove(f'{images_path}/{image}')
        except:
            print(image)

xmlnames = os.listdir(xmls_path)
imagenames = os.listdir(images_path)
names1=[name[:-4] for name in xmlnames]
for image in imagenames:
    if image[:-4] not in names1:
        print(image)
        move(f'{images_path}/{image}',f'{images_no_an_path}/{image}')

#文件夹改变后需要重新读取文件名
xmlnames=os.listdir(xmls_path)
imagenames=os.listdir(images_path)
names2=[name[:-4] for name in imagenames]
for xml in xmlnames:
    if xml=='classes':
        continue
    if xml[:-4] not in names2:
        print(xml)
        move(f'{xmls_path}/{xml}',f'{xmls_no_image_path}/{xml}')