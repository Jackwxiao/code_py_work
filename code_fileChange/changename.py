'''
@Project ：yolov5-v6.1-pytorch
@File    ：changename.py
@Author  ：Jackwxiao
@Date    ：2022/11/21 21:26
批量改变文件命名
'''

# 只改变单一类型文件的命名
# import os
# IMAGES_PATH = r"D:\wx3.29\images_process\paiwukou&water/"
# filename_list = os.listdir(IMAGES_PATH)
# a = 0
# index = 0
#
# for i in filename_list:
#     used_name = IMAGES_PATH + filename_list[a]
#     new_name = IMAGES_PATH + "obspaiwukou_" +str(index) + ".jpg"
#     os.rename(used_name,new_name)
#     print("文件%s重命名成功,新的文件名为%s" %(used_name,new_name))
#     a += 1
#     index += 1



# 改变后缀png -> jpg

#
# import os
#
# folder_path = r"D:\wx3.29\images_process\yancong\test/"
#
# for filename in os.listdir(folder_path):
#     if filename.endswith(".png"):
#         new_filename = os.path.splitext(filename)[0] + ".jpg"
#         os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
#         print(f"Renamed file {filename} to {new_filename}")
#     elif filename.endswith(".jpg"):
#         print(f"File {filename} already has the correct extension")


# 可以同时改变图片和对应的标签文件的命名
import os
import shutil

# 指定图片文件夹和标签文件夹的路径
img_folder = r'D:\wx3.29\images_process\over_dirty_truck\images_all/'
label_folder = r'D:\wx3.29\images_process\over_dirty_truck\xmls_all/'

# 指定新的文件名前缀
new_prefix = 'trucks0601_'

# 新建保存文件的文件夹
new_folder = r'D:\wx3.29\images_process\over_dirty_truck\newNameTrucks/'
os.makedirs(new_folder, exist_ok=True)

new_img_folder = os.path.join(new_folder, 'images')
os.makedirs(new_img_folder, exist_ok=True)

new_label_folder = os.path.join(new_folder, 'xmls')
os.makedirs(new_label_folder, exist_ok=True)

# 遍历图片文件夹
img_files = os.listdir(img_folder)
for i, img_file in enumerate(img_files):
    # 构造新的文件名
    new_name = new_prefix + str(i) + '.jpg'
    # 重命名图片文件
    shutil.copy(os.path.join(img_folder, img_file), os.path.join(new_img_folder, new_name))

    # 构造标签文件的文件名
    label_file = os.path.splitext(img_file)[0] + '.xml'
    # 重命名标签文件
    shutil.copy(os.path.join(label_folder, label_file), os.path.join(new_label_folder, new_name[:-4] + '.xml'))
