import os
import shutil

# 源文件夹路径
src_folder = r'D:\wx3.29\images_process\d_smoke\smoke_fog1028\in/'

# 目标文件夹路径
dst_folder = r'D:\wx3.29\images_process\d_smoke\filtered_images\images/'

# 遍历源文件夹中的所有文件
for filename in os.listdir(src_folder):
    # 构造文件的完整路径
    src_file = os.path.join(src_folder, filename)
    dst_file = os.path.join(dst_folder, filename)
    # 移动文件到目标文件夹中
    shutil.move(src_file, dst_file)

