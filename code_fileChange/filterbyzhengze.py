# 使用正则表达式匹配文件名中的时间部分，然后将时间字符串转换为时间对象，并判断时间是否在指定范围内。
# 如果符合条件，就输出文件名并保存该文件到新文件夹。

import os
import re
import datetime
import shutil


# 定义正则表达式
pattern = re.compile('.*(\d{17}).*\.jpg$')

# 定义文件夹路径
folder_path = r'D:\wx3.29\images_process\total_smoke\images/'
save_path = r'D:\wx3.29\images_process\total_smoke\filted_images/'

if not os.path.exists(save_path):
    os.makedirs(save_path)


# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 使用正则表达式匹配文件名中的时间部分
    match = pattern.match(filename)
    if match:
        # 提取时间部分
        time_str = match.group(1)
        # 将时间字符串转换为时间对象
        time_obj = datetime.datetime.strptime(time_str, '%Y%m%d%H%M%S%f')
        # 判断时间是否在指定范围内
        if time_obj.time() >= datetime.time(18, 0, 0):
            # 符合条件的文件名
            print(filename)
            shutil.copy(os.path.join(folder_path, filename), os.path.join(save_path, filename))
