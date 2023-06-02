# import cv2
# import os
#
# image_base_path = "/videoToimgs";
# root=os.getcwd()
#
# def get_images(video_path,interval):
#     frame_times = -1
#     fileName = video_path.split("/")[-1:][0].split('.')[0]
#     image_out_path = root+'/'+image_base_path+'/'+fileName
#     if not os.path.exists(image_out_path):
#         os.makedirs(image_out_path)
#
#     cap = cv2.VideoCapture(video_path)
#     while cap.isOpened():
#         frame_times = frame_times + 1
#         success, frame = cap.read()
#         if not success:
#             break
#         if frame_times%interval==0:
#             cv2.imwrite(image_out_path+'/'+fileName+'_'+str(frame_times)+'.jpg',frame)
# if __name__ == '__main__':
#     for i in range(0,3):
#         get_images(f'images_process/re_smoke/{i}.mp4',interval=25)


import os
import cv2

def save_img2():  # 提取视频中图片 按照每秒提取   间隔是视频帧率
    video_path = r'D:\wx3.29\images_process\videoToimgs\0531/'  # 视频所在的路径
    f_save_path = r'D:\wx3.29\images_process\videoToimgs\frames/'  # 保存图片的上级目录
    videos = os.listdir(video_path)  # 返回指定路径下的文件和文件夹列表。
    for video_name in videos:  # 依次读取视频文件
        file_name = video_name.split('.')[0]  # 拆分视频文件名称 ，剔除后缀
        folder_name = f_save_path + file_name  # 保存图片的上级目录+对应每条视频名称 构成新的目录存放每个视频的
        os.makedirs(folder_name, exist_ok=True)  # 创建存放视频的对应目录
        vc = cv2.VideoCapture(video_path + video_name)  # 读入视频文件
        fps = vc.get(cv2.CAP_PROP_FPS)  # 获取帧率
        print(fps)  # 帧率可能不是整数  需要取整
        rval = vc.isOpened()  # 判断视频是否打开  返回True或False
        c = 1
        while rval:  # 循环读取视频帧
            rval, frame = vc.read()  # videoCapture.read() 函数，第一个返回值为是否成功获取视频帧，第二个返回值为返回的视频帧：
            pic_path = folder_name + '/'
            if rval:

                if (c % int(fps) == 0):  # 每隔fps帧进行存储操作   ,可自行指定间隔
                    cv2.imwrite(pic_path +f'{file_name}_sewageRecognize_' + str(round(c/fps)) + '.jpg', frame) #存储为图像的命名 video_数字（第几个文件）.png
                    # print('video_' + str(round(c/fps)) + '.jpg')
                cv2.waitKey(1)  # waitKey()--这个函数是在一个给定的时间内(单位ms)等待用户按键触发;如果用户没有按下键,则接续等待(循环)
                c = c + 1

            else:
                break
        vc.release()
        print('save_success' + folder_name)


save_img2()
