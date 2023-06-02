# -*- coding: utf-8 -*-

import os
import random

print(os.path.abspath("./train/annotations"))

def _main():
    trainval_percent = 1 # 训练加验证集占总数据集的比例
    train_percent = 1  # 训练集占总数据集的比例
    xmlfilepath = r'D:\tools\voc_to_yolov5\data\Annotations'
    total_xml = os.listdir(xmlfilepath)

    num = len(total_xml) # 总的标签数量
    list = range(num)    # 生成列表
    print(list)
    tv = int(num * trainval_percent) # tv 训练+验证样本数量
    tr = int(tv * train_percent)     # tr 训练的样本数量
    trainval = random.sample(list, tv) # 训练+验证：总数据集中随机选择tv个样本，trainval为列表  数字列表
    train = random.sample(trainval, tr) # 训练集： 从trainval列表中随机选择tr个训练样本，train为数字列表
    # trainval 包含 train 样本
    ftrainval = open(r'D:\tools\voc_to_yolov5\data\ImageSets\Main\trainval.txt', 'w')
    ftest = open(r'D:\tools\voc_to_yolov5\data\ImageSets\Main\test.txt', 'w')
    ftrain = open(r'D:\tools\voc_to_yolov5\data\ImageSets\Main\train.txt', 'w')
    fval = open(r'D:\tools\voc_to_yolov5\data\ImageSets\Main\val.txt', 'w')

    for i in list:  # 遍历列表

        name = total_xml[i][:-4] + '\n' # 一次取不含扩展名的文件名
        if i in trainval:
            ftrainval.write(name)
            if i in train:
                ftrain.write(name)
            else:
                fval.write(name)
        else:
            ftest.write(name)

    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest.close()


if __name__ == '__main__':
    _main()

# 首先运行次文件，划分 训练+验证集、训练集、测试集、验证集
