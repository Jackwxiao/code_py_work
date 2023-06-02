import os
import cv2

# 指定彩色热成像图像所在的文件夹和灰度热成像图像要保存的文件夹
color_dir = r'D:\wx3.29\images_process\yancong\re_smoke_video\videoToimgs\record_0200000001_20230426111957_0/'
gray_dir = r'D:\wx3.29\images_process\yancong\re_smoke_video\videoToimgs\record_0200000001_gray/'

# 如果灰度热成像图像保存的文件夹不存在，则新建该文件夹
if not os.path.exists(gray_dir):
    os.makedirs(gray_dir)

# 遍历彩色热成像图像所在的文件夹中的所有图像文件，并逐一进行处理
for file_name in os.listdir(color_dir):
    if file_name.endswith('.png') or file_name.endswith('.jpg'):
        # 读取彩色热成像图像
        color_img = cv2.imread(os.path.join(color_dir, file_name))

        # 将彩色热成像图像转换为灰度图像
        gray_img = cv2.cvtColor(color_img, cv2.COLOR_RGB2GRAY)

        # 保存灰度热成像图像
        gray_file_name = os.path.join(gray_dir, file_name)
        cv2.imwrite(gray_file_name, gray_img)

