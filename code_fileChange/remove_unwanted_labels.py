
import os
import shutil


### 根据一个文件夹里的文件名称去匹配另一个文件夹中的同名文件（即后缀不同的文件，如根据图片名称去匹配同名标签文件）
def Compare_deduplicate_two_folders(img_dir, label_dir):

    img_files = os.listdir(img_dir)  # 获取图片文件夹下所有文件名列表
    label_files = os.listdir(label_dir)  # 获取标签文件夹下所有文件名列表

    img_names = set([os.path.splitext(file)[0] for file in img_files])  # 获取图片文件名列表（去掉后缀）
    label_names = set([os.path.splitext(file)[0] for file in label_files])  # 获取标签文件名列表（去掉后缀）

    # 遍历标签文件夹，删除未匹配到的标签文件
    for label_file in label_files:
        label_name = os.path.splitext(label_file)[0]  # 获取标签文件名（去掉后缀）
        if label_name not in img_names:
            os.remove(os.path.join(label_dir, label_file))  # 删除标签文件

    print('标签文件匹配完毕！')


img_dir = r'D:\wx3.29\images_process\total_smoke\filted_images/'  # 标准路径
label_dir = r'D:\wx3.29\images_process\total_smoke\labels/'  # 目标路径
Compare_deduplicate_two_folders(img_dir,label_dir)


#
# ##   有点问题
# import os
# import shutil
#
# # 定义两个文件夹的路径和新建文件夹的路径
# folder1_path = 'folder1'
# folder2_path = 'folder2'
# new_folder_path = 'new_folder'
#
# #### 保存两个文件夹下的同名文件到新的文件夹中，方便以后进行比对
# def save_two_same_file(folder1_path, folder2_path, new_folder_path):
#     # 创建新建文件夹
#     if not os.path.exists(new_folder_path):
#         os.mkdir(new_folder_path)
#
#     # 定义文件名分隔符
#     name_separator = '_'
#
#     # 定义文件名分隔符后第一段字符个数
#     name_prefix_len = 7
#
#     # 遍历第一个文件夹中的文件
#     for filename in os.listdir(folder1_path):
#         # 如果文件名在第二个文件夹中也存在
#         if filename in os.listdir(folder2_path):
#             # 判断是否为同一组文件
#             name_prefix = filename.split(name_separator)[0][:name_prefix_len]
#             match1 = name_prefix + name_separator + '0' in filename
#             match2 = name_prefix + name_separator + '1' in filename
#             if match1 or match2:
#                 # 将两个文件复制到新建文件夹下
#                 shutil.copy(os.path.join(folder1_path, filename), os.path.join(new_folder_path, filename))
#                 shutil.copy(os.path.join(folder2_path, filename), os.path.join(new_folder_path, filename))
#
#
# # 定义两个文件夹的路径和新建文件夹的路径
# folder1_path = r'D:\wx3.29\images_process\dust_4_18\crop_img/'  # 文件夹1
# folder2_path = r'D:\wx3.29\images_process\dust_crop_35577\images/'  # 文件夹2
# new_folder_path = r'new_folder'                                    # 新建文件夹，保存同名文件的路径
# save_two_same_file(folder1_path, folder2_path, new_folder_path)
