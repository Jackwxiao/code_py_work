# -*- coding: utf-8 -*-
import argparse
import os
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
import numpy as np
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized

hsv_v = 255


classes = ['smoke']


def convert(size, box):  # size:(原图w,原图h) , box:(xmin,xmax,ymin,ymax)
    dw = 1. / size[0]  # 1/w
    dh = 1. / size[1]  # 1/h
    x = (box[0] + box[1]) / 2.0  # 物体在图中的中心点x坐标
    y = (box[2] + box[3]) / 2.0  # 物体在图中的中心点y坐标
    w = box[1] - box[0]  # 物体实际像素宽度
    h = box[3] - box[2]  # 物体实际像素高度
    x = x * dw  # 物体中心点x的坐标比(相当于 x/原图w)
    w = w * dw  # 物体宽度的宽度比(相当于 w/原图w)
    y = y * dh  # 物体中心点y的坐标比(相当于 y/原图h)
    h = h * dh  # 物体宽度的宽度比(相当于 h/原图h)
    return [x, y, w, h]  # 返回 相对于原图的物体中心点的x坐标比,y坐标比,宽度比,高度比,取值范围[0-1]


def hsv_filter(frame, bbox_info):
    """draw bbox on image"""
    crop_smoke_img = frame[bbox_info[1]:bbox_info[3], bbox_info[0]:bbox_info[2], :]
    crop_smoke_hsv = cv2.cvtColor(crop_smoke_img, cv2.COLOR_BGR2HSV)
    crop_smoke_img_hsv_v = crop_smoke_hsv[:, :, 2]
    v = np.mean(crop_smoke_img_hsv_v)
    if v > hsv_v:
        is_filter = True
    else:
        is_filter = False

    return v, is_filter


def detect(save_img=False):
    source, weights, view_img, save_txt, imgsz = opt.source, opt.weights, opt.view_img, opt.save_txt, opt.img_size
    save_img = not opt.nosave and not source.endswith('.txt')  # save inference images
    webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
        ('rtsp://', 'rtmp://', 'http://', 'https://'))

    # Directories
    save_dir = Path(increment_path(Path(opt.project) / opt.name, exist_ok=opt.exist_ok))  # increment run
    print(save_dir)    # runs\detect\exp2
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Initialize
    set_logging()
    device = select_device(opt.device)
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    torch.save(model.state_dict(), "yolov5sv5_bare_cover_20220513_last_unzip.pt", _use_new_zipfile_serialization=False)

    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size
    if half:
        model.half()  # to FP16

    # Second-stage classifier
    classify = False
    if classify:
        modelc = load_classifier(name='resnet101', n=2)  # initialize
        modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()

    # Set Dataloader
    vid_path, vid_writer = None, None
    if webcam:
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    print(names)
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    t0 = time.time()
    image_num = len(os.listdir(opt.source))
    ii = 0

    # 统计所有图像每个阈值得分的占比
    scores_5 = 0
    scores_6 = 0
    scores_7 = 0
    scores_8 = 0
    scores_9 = 0

    for path, img, im0s, vid_cap in dataset:

        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = time_synchronized()
        pred = model(img, augment=opt.augment)[0]

        # Apply NMS
        pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)
        t2 = time_synchronized()

        # Apply Classifier
        if classify:
            pred = apply_classifier(pred, modelc, img, im0s)

        pred_lst = pred[0].cpu().numpy().tolist()
        n = len(pred_lst)
        # detect no person
        if n == 0 and pred_lst == []:
            ii = ii + 1
            p = Path(path)
            if not os.path.exists(os.path.join(save_dir, "leak_img")):
                os.makedirs(os.path.join(save_dir, "leak_img"))
            save_leak_img_path = os.path.join(save_dir, "leak_img", p.name) # img.jpg
            cv2.imwrite(save_leak_img_path, im0s)
            continue

        # Process detections
        for i, det in enumerate(pred):  # detections per image

            if webcam:  # batch_size >= 1
                p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count
            else:
                p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path

            if not os.path.exists(os.path.join(save_dir, "det_img")):
                os.makedirs(os.path.join(save_dir, "det_img"))

            save_path = os.path.join(save_dir, "det_img", p.name) # img.jpg

            if not os.path.exists(os.path.join(save_dir, "img_or")):
                os.makedirs(os.path.join(save_dir, "img_or"))
            save_original_img = os.path.join(save_dir, "img_or", p.name)  # img.jpg

            if not os.path.exists(os.path.join(save_dir, "labels")):
                os.makedirs(os.path.join(save_dir, "labels"))
            label_txt = os.path.join(save_dir, "labels", os.path.splitext(p.name)[0] + '.txt')


            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # img.txt
            s += '%gx%g ' % img.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            img_or = im0.copy()

            # detect object
            if len(det):

                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                scores = []
                bboxes = []

                for *xyxy, conf, cls in reversed(det):

                    label_name = f'{names[int(cls)]}'

                    if label_name == 'light_points':
                        continue

                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh, conf) if opt.save_conf else (cls, *xywh)  # label format
                        with open(txt_path + '.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')


                    if save_img or view_img:  # Add bbox to image

                        label = f'{names[int(cls)]} {conf:.2f}'
                        if conf.item() >= 0.5 and  conf.item() < 0.6:
                            scores_5  = scores_5 + 1

                        if conf.item() >= 0.6 and  conf.item() < 0.7:
                            scores_6  = scores_6 + 1

                        if conf.item() >= 0.7 and  conf.item() < 0.8:
                            scores_7  = scores_7 + 1

                        if conf.item() >= 0.8 and  conf.item() < 9:
                            scores_8  = scores_8 + 1

                        if conf.item() >= 0.9 and conf.item() < 1:
                            scores_9 = scores_9 + 1

                        # scores.append(str(conf.item())[:3])
                        # print(scores)

                        crop_bbox = [int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])]
                        # 亮度值过滤
                        hsv_v, is_filter = hsv_filter(im0, crop_bbox)
                        if is_filter:
                            print("亮度值过高已过滤:", hsv_v)
                            continue
                        plot_one_box(xyxy, im0, label=label, color=(0, 0, 255), line_thickness=2)

                        H, W = im0.shape[:2]
                        C = [int(xyxy[0]), int(xyxy[2]), int(xyxy[1]), int(xyxy[3])] # xmin, xmax, ymin, ymax
                        bb = convert((W, H), C)
                        bb.insert(0, int(cls))
                        bboxes.append(bb)
                        print(xyxy, label, hsv_v)

                if save_img:
                    if dataset.mode == 'image':
                        cv2.imwrite(save_path, im0)
                        cv2.imwrite(save_original_img, img_or)
                        with open(label_txt, "w+") as f:
                            for box in bboxes:
                                f.write(str(box[0]) + " " + " ".join([str(a) for a in box[1:]]) + '\n')

                    else:  # 'video' or 'stream'
                        if vid_path != save_path:  # new video
                            vid_path = save_path
                            if isinstance(vid_writer, cv2.VideoWriter):
                                vid_writer.release()  # release previous video writer
                            if vid_cap:  # video
                                fps = vid_cap.get(cv2.CAP_PROP_FPS)
                                w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                                h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                            else:  # stream
                                fps, w, h = 30, im0.shape[1], im0.shape[0]
                                save_path += '.mp4'
                            vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                        vid_writer.write(im0)

            # Print time (inference + NMS)
            print(f'{s}Done. ({t2 - t1:.3f}s)')

            # Stream results
            # if view_img:
            #     cv2.imshow(str(p), im0)
            #     cv2.waitKey(0)  # 1 millisecond

            # Save results (image with detections)

    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        print(f"Results saved to {save_dir}{s}")

    print(image_num, image_num - ii, (image_num - ii) / image_num)
    print("0.5 -- 0.6: ", scores_5)
    print("0.6 -- 0.7: ", scores_6)
    print("0.7 -- 0.8: ", scores_7)
    print("0.8 -- 0.9: ", scores_8)
    print("0.9 -- 1:  ",  scores_9)
    print(f'Done. ({time.time() - t0:.3f}s)')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str,
                        default="/home/grd/PycharmProjects/traffic_car/yolov5-5.0/weights/dust_11213_last.pt", help='model.pt path(s)')
    parser.add_argument('--source', type=str, default="/home/grd/PycharmProjects/traffic_car/yolov5-5.0/data/water3",help='source')  # file/folder, 0 for webcam
    parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.35, help='object confidence threshold')  # 0.5
    parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')     # 0.45
    parser.add_argument('--device', default='0', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', default=True, help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default='runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp_water_c', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    opt = parser.parse_args()
    print(opt)
    check_requirements(exclude=('pycocotools', 'thop'))

    with torch.no_grad():
        if opt.update:  # update all models (to fix SourceChangeWarning)
            for opt.weights in ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt']:
                detect()
                strip_optimizer(opt.weights)
        else:
            detect()

