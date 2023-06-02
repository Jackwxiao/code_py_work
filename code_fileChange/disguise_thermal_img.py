import cv2
import os

def convert_to_heatmap(input_folder, output_folder):
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取输入文件夹中的所有图片文件名
    img_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png')]

    for img_file in img_files:
        # 读取彩色图像
        img = cv2.imread(os.path.join(input_folder, img_file))

        # 将彩色图像转换为灰度图像
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 将灰度图像转换为伪彩色图像（热成像图）
        heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_HOT)
        heatmap = cv2.addWeighted(img, 0.5, heatmap, 0.5, 0.5)
        # 保存热成像图
        cv2.imwrite(os.path.join(output_folder, img_file), heatmap)

if __name__ == '__main__':
    input_folder = 'D:\wx3.29\images_process\industrial pollution chimney'
    output_folder = 'D:\wx3.29\images_process\output_disguise'
    convert_to_heatmap(input_folder, output_folder)

