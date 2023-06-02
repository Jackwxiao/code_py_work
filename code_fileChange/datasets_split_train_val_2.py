import random
import os
import json
import shutil

root_path = 'D:\wx3.29\images_process\dust_crop_all'
# label_dir = "/home/grd/PycharmProjects/traffic_car/yolov5-5.0/data/dust_9260/images"
# label_dir = "/home/grd/PycharmProjects/traffic_car/yolov5-5.0/data/dust_9904/images"
label_dir = root_path + '/images'

label_path_lst = [os.path.join(label_dir, label) for label in os.listdir(label_dir)]
total_num = len(label_path_lst)
print(total_num)
train_ritia = 0.9
val = 1 - train_ritia
train_num = int(total_num * train_ritia)
val_num = total_num - train_num
print(train_num, val_num)
random.shuffle(label_path_lst)
train_lst = random.sample(label_path_lst, train_num)
print("train_lst num : ", len(train_lst))
for train_img in train_lst:
    with open(root_path + '/train.txt',"a+") as f:
        f.write(train_img + "\n")

val_lst = [anno for anno in label_path_lst if anno not in train_lst]
print("val_lst num : ", len(val_lst))

for val_img in val_lst:
    with open(root_path + '/val.txt',"a+") as f1:
        f1.write(val_img + "\n")

'''is sample images_name'''
# coco_fire_image = "/home/grd/PycharmProjects/traffic_car/yolov5/coco_grand/coco_fire/images"
# coco_smoke_image = "/home/grd/PycharmProjects/traffic_car/yolov5/coco_grand/coco_smoke/images"
#
# fire_img_lst = os.listdir(coco_fire_image)
# i = 0
# for img in fire_img_lst:
#     if img in os.listdir(coco_smoke_image):
#         print("have sample images")
#         i = i + 1
#
# print(i)


# annotations = "/home/grd/PycharmProjects/traffic_car/yolov5/coco_grand/yolo_total_multi_class/annotations.json"
# with open(annotations, 'r') as f:
#     json_text = f.read()
# info_dict = json.loads(json_text)
#
# # images of labels
# print(len(info_dict["images"]))  # 2088  coco_total: 28196
#
# img_name_lst = []
#
# for item in info_dict["images"]:
#     file_name = item["file_name"]
#     img_name_lst.append(os.path.basename(file_name)) # ds_swz12.7_65.png
# print(len(img_name_lst))
#
# # JPEGImages/192.168.1.64_01_20210724092046474_TIMING.jpg
# root_images_dir = "/home/grd/PycharmProjects/traffic_car/yolov5/coco_grand/yolo_total_multi_class/JPEGImages"
# root_img_lst = os.listdir(root_images_dir)
# print(len(root_img_lst)) # 30956
#
# i = 0
# images_dir = "/home/grd/PycharmProjects/traffic_car/yolov5/coco_grand/yolo_total_multi_class/images"
# for label_img in img_name_lst:
#     if label_img in root_img_lst:
#         i = i + 1
#         shutil.copy(os.path.join(root_images_dir, label_img), os.path.join(images_dir, label_img))
#     else:
#         print(label_img)
#
# print(i) # 28196

#  txt_name = os.path.splitext(os.path.basename(file_name))[0] + '.txt'
