import os

# 定义标签文件夹路径和标签文件后缀
label_folder = r"D:\wx3.29\yolov7-main\datasets\labels"
label_suffix = ".txt"

# 定义一个字典来保存标签序号及其出现次数
label_count = {}

# 遍历标签文件夹下的所有标签文件
for filename in os.listdir(label_folder):
    if filename.endswith(label_suffix):
        # 读取标签文件中的标签序号
        with open(os.path.join(label_folder, filename), "r") as f:
            for line in f:
                label = int(line.strip().split()[0])
                # 统计标签序号的数量
                if label in label_count:
                    label_count[label] += 1
                else:
                    label_count[label] = 1

# 打印每个标签序号及其出现次数
for label, count in label_count.items():
    print(f"Label {label}: {count} instances")
