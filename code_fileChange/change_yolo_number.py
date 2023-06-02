import os

def updateFile(file,file2,num):
    #原地址，复制后地址，要改的数
    with open(file, "r", encoding="utf-8") as f1, open(file2, "w", encoding="utf-8") as f2:
        for line in f1:
            line=list(line)
            line[0]=num
            line=''.join(line)
            f2.write(line)
    f1.close()
    f2.close()

src_path=r'D:\wx3.29\images_process\dust_219\dust_crop_labels'
dst_path=r'D:\wx3.29\images_process\dust_219\dust_crop_labels_changedTo3'
files=os.listdir(src_path)
for file in files:
    updateFile(f'{src_path}/{file}', f'{dst_path}/{file}','3')

