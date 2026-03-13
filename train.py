from ultralytics import YOLO

model = YOLO()

# model.train(data='dataset_type.yaml', workers=0, epochs=500, batch=16)
# model.train(data='dataset_digital.yaml', workers=0, epochs=500, batch=16)
# model.train(data='dataset_pointer.yaml', workers=0, epochs=500, batch=16)
# model.train(data='dataset_pointer360.yaml', workers=0, epochs=500, batch=16)
# model.train(data='dataset_shan.yaml', workers=0, epochs=500, batch=16)
# model.train(data='dataset_pointer_newmethod.yaml', workers=0, epochs=500, batch=16)
model.train(data='dataset_yibiao.yaml', workers=0, epochs=200, batch=8)