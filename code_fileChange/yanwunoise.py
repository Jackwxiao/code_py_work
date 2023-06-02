import random
from PIL import Image, ImageDraw
import os

# 设置烟雾噪声的大小上限为图片宽度或高度的一半
def get_smoke_size_limit(img):
    return min(img.size) // 4

# 给图片添加烟雾噪声
def add_smoke_noise(img):
    smoke_size_limit = get_smoke_size_limit(img)
    smoke_opacity = 50  # 烟雾不透明度
    smoke_color = (108, 108, 108)  # 烟雾颜色为灰色
    draw = ImageDraw.Draw(img)
    center_x, center_y = img.size[0] // 2, img.size[1] // 2
    # 在图片的中心范围添加随机烟雾噪声
    for _ in range(50):
        smoke_radius = random.randint(1, smoke_size_limit // 2)
        x = random.randint(center_x - smoke_size_limit // 2, center_x + smoke_size_limit // 2)
        y = random.randint(center_y - smoke_size_limit // 2, center_y + smoke_size_limit // 2)
        draw.ellipse((x - smoke_radius, y - smoke_radius,
                      x + smoke_radius, y + smoke_radius),
                     fill=smoke_color + (smoke_opacity,))
    del draw
    return img

# 循环遍历图片文件夹，并给每张图片添加烟雾噪声，将添加噪声后的图片保存到新文件夹中
def add_smoke_noise_to_folder(folder_path, output_path):
    os.makedirs(output_path, exist_ok=True)
    for filename in os.listdir(folder_path):
        if not filename.endswith('.jpg'):
            continue
        img_path = os.path.join(folder_path, filename)
        with Image.open(img_path) as img:
            img = add_smoke_noise(img)
            output_img_path = os.path.join(output_path, filename)
            img.save(output_img_path)

# 将名为“input”文件夹中的图片添加烟雾噪声，保存到名为“output”文件夹中
add_smoke_noise_to_folder('D:\wx3.29\images_process\yanwu_add_test', 'D:\wx3.29\images_process\output_path')
