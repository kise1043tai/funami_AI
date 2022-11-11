import cv2
import torch
from numpy import random

from models.experimental import attempt_load
from utils.general import check_img_size, non_max_suppression, set_logging

from PIL import Image
import torchvision

WEIGHTS = 'weights/weight.pt'
IMAGE_SIZE = 640

#PIL型でInput
def detect(source):
    # Initialize
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(WEIGHTS, map_location=device)  # load FP32 model
    imgsz = check_img_size(IMAGE_SIZE, s=model.stride.max())  # check img_size
    if half:
        model.half()  # to FP16

    # Get names
    #names = model.module.names if hasattr(model, 'module') else model.names

    # Run inference
    img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
    _ = model(img.half() if half else img) if device.type != 'cpu' else None  # run once

    img = torchvision.transforms.functional.to_tensor(source)

    img = img.unsqueeze(0)
    # Inference
    pred = model(img)[0]

    # Apply NMS
    pred = non_max_suppression(pred, 0.25, 0.45)
    class_num = -1
    # Process detections
    for i, det in enumerate(pred):  # detections per image
        if det is not None and len(det):
            class_num = int(det[:1, -1].unique())
    return class_num


if __name__ == '__main__':
    pass