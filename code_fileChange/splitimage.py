from PIL import Image

IMAGE_ROW = 4     #the num of rows to split/compose
IMAGE_COLUMN = 5  #the num of cols to split/compose

def fill_image(image):
    width, height = image.size

    new_image_length = width if width > height else height

    new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')   

    if width > height:
        new_image.paste(image, (0, int((new_image_length - height) / 2)))
    else:
        new_image.paste(image, (int((new_image_length - width) / 2),0))
    return new_image


def split_image(image):
    width, height = image.size
    item_width = int(width / IMAGE_COLUMN)
    item_height = int(height / IMAGE_ROW)
    box_list = []
    # (left, upper, right, lower)
    for i in range(0,IMAGE_ROW):
        for j in range(0,IMAGE_COLUMN):
            #print((i*item_width,j*item_width,(i+1)*item_width,(j+1)*item_width))
            box = (j*item_width,i*item_height,(j+1)*item_width,(i+1)*item_height)
            box_list.append(box)
    image_list = [image.crop(box) for box in box_list]
    return image_list


def save_images(image_list):
    index = 1
    for image in image_list:
        image.save(str(index) + '.jpg', quality=100, subsampling=0)
        index += 1

if __name__ == '__main__':
    file_path = "../extended/images/001.jpg"
    image = Image.open(file_path)
    image_list = split_image(image)
    save_images(image_list)