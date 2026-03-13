from ultralytics import YOLO

# yolo = YOLO(model='runs/detect/1type/weights/best.pt', task='detect')    # task非必须
# result = yolo(source='datasets/mydata_type/images/train', save=True, save_txt=True)

# yolo = YOLO(model='runs/detect/2digital/weights/best.pt', task='detect')
# result = yolo(source='datasets/mydata_digital/images/test/', save=True)


# yolo = YOLO(model='runs/detect/3pointer/weights/best.pt', task='detect')
# result = yolo(source='datasets/mydata_pointer/images/val', save=True)

# yolo = YOLO(model='runs/sets/3pointer_newmethod2/weights/best.pt', task='detect')    # task非必须
# result = yolo(source='datasets/mydata_pointer_newmethod2/images/test/test', save=True, save_txt=True, conf=0.7)

# result = yolo(source='./ultralytics/assets/bus.jpg', save=True)  #screen 0(摄像头)

# yolo = YOLO(model='runs/sets/4pointer360/weights/best.pt', task='detect')
# result = yolo(source='datasets/mydata_pointer360/images/train/r(4).jpg', save=True)


yolo = YOLO(model='runs/sets/1type/weights/best.pt', task='detect')
result = yolo(source='datasets/mydata_type/images/train', save=True)
