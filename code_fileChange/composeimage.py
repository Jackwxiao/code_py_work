import PIL.Image as Image

 
IMAGES_PATH = '/数据处理代码/按比例分割图片/'
IMAGE_W = 1840    #single picture width
IMAGE_H = 1228    #single picture height
IMAGE_ROW = 4     #the num of rows to split/compose
IMAGE_COLUMN = 5  #the num of cols to split/compose


def image_compose():
    to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_W, IMAGE_ROW * IMAGE_H))     #new a BG pic
    num = 1
    for y in range(1, IMAGE_ROW + 1):
        for x in range(1, IMAGE_COLUMN + 1):
            from_image = Image.open(IMAGES_PATH + str(num) + '.jpg').resize(
                (IMAGE_W, IMAGE_H),Image.ANTIALIAS)
            to_image.paste(from_image, ((x - 1) * IMAGE_W, (y - 1) * IMAGE_H))
            num += 1
    return to_image.save('final.jpg', quality=100, subsampling=0) 


if __name__ == '__main__':
    image_compose()
    
