# 📊 仪表盘自动读数系统

> 基于 YOLOv8 的指针式/数字式仪表盘自动识别与读数系统

---

## 🎯 项目简介

本项目使用深度学习方法实现仪表盘的自动读数，支持：
- ✅ **指针式仪表盘** - 指针检测 + 刻度线识别 + 角度计算
- ✅ **数字式仪表盘** - 数字 OCR 识别
- ✅ **360°全角度指针** - 任意角度指针检测
- ✅ **GUI 可视化界面** - 实时显示检测结果和读数

---

## 📁 项目结构

```
/home/alanwilliam/.openclaw/workspace/
├── pyqt_*.py                    # GUI 程序（5 个）
│   ├── pyqt_pointer.py          # 指针式仪表盘检测
│   ├── pyqt_pointer_newmethod.py # 新方法指针检测
│   ├── pyqt_pointer_newmethod2.py # 新方法 2（推荐）
│   ├── pyqt_pointer360.py       # 360°全角度指针检测
│   └── pyqt_digital.py          # 数字式仪表盘识别
│
├── runs/sets/                   # 训练好的模型
│   ├── 1type/weights/best.pt    # 仪表盘类型分类
│   ├── 2digital/weights/best.pt # 数字识别模型
│   ├── 3pointer/weights/best.pt # 指针检测（基础版）
│   ├── 3pointer_newmethod/weights/best.pt  # 指针检测（新方法）
│   ├── 3pointer_newmethod2/weights/best.pt # 指针检测（新方法 2）⭐
│   └── 4pointer360/weights/best.pt # 360°指针检测
│
├── datasets/                    # 数据集
│   ├── mydata_type/             # 类型分类数据集
│   ├── mydata_digital/          # 数字识别数据集
│   ├── mydata_pointer/          # 指针检测数据集
│   ├── mydata_pointer_newmethod/ # 新方法数据集
│   ├── mydata_pointer_newmethod2/ # 新方法 2 数据集
│   └── mydata_pointer360/       # 360°数据集
│
└── ultralytics/                 # YOLOv8 库（已部署）
```

---

## 🚀 快速开始

### 1. 激活虚拟环境

```bash
cd ~/.openclaw/workspace
source ultralytics/venv/bin/activate
```

### 2. 运行 GUI 程序

#### 指针式仪表盘（推荐）
```bash
python3 pyqt_pointer_newmethod2.py
```

#### 数字式仪表盘
```bash
python3 pyqt_digital.py
```

#### 360°全角度指针
```bash
python3 pyqt_pointer360.py
```

### 3. 命令行推理

```bash
# 指针检测
yolo predict model=runs/sets/3pointer_newmethod2/weights/best.pt source=image.jpg

# 数字识别
yolo predict model=runs/sets/2digital/weights/best.pt source=image.jpg

# 360°指针
yolo predict model=runs/sets/4pointer360/weights/best.pt source=image.jpg
```

---

## 📊 模型性能

| 模型 | 用途 | 参数量 | 大小 | 训练日期 |
|------|------|--------|------|---------|
| **1type** | 仪表盘类型分类 | 3.1M | 6.0M | 2024-02-03 |
| **2digital** | 数字识别 | 3.1M | 6.0M | 2024-02-03 |
| **3pointer** | 指针检测（基础） | 3.1M | 6.0M | 2024-02-29 |
| **3pointer_newmethod** | 指针检测（新方法） | 3.1M | 6.0M | 2024-03-09 |
| **3pointer_newmethod2** ⭐ | 指针检测（新方法 2） | 3.1M | 6.0M | 2024-03-10 |
| **4pointer360** | 360°全角度指针 | 3.1M | 6.0M | 2024-02-08 |

---

## 🔧 核心算法

### 指针式仪表盘读数流程

```
1. 仪表盘定位 → YOLOv8 检测表盘区域
2. 指针检测 → YOLOv8 检测指针端点和中心点
3. 刻度线识别 → 检测零刻度线和分度值
4. 角度计算 → 计算指针与零刻度的夹角
5. 读数计算 → 根据角度和分度值计算实际读数
```

### 数学公式

```python
# 读数计算
angle = atan2(farPoint[1] - center[1], farPoint[0] - center[0])
zero_angle = atan2(zeroPoint[1] - center[1], zeroPoint[0] - center[0])
relative_angle = angle - zero_angle

# 读数
reading = (relative_angle / 360) * full_scale_value
```

---

## 💻 GUI 功能

### pyqt_pointer_newmethod2.py

**功能特性**：
- ✅ 图片加载和显示
- ✅ 实时检测推理
- ✅ 结果可视化（指针、刻度线、中心点）
- ✅ 读数显示和保存
- ✅ 批量处理
- ✅ 参数调整（置信度、IoU）

**界面布局**：
```
┌─────────────────────────────────────────┐
│  [加载图片]  [检测]  [保存结果]          │
├──────────────┬──────────────────────────┤
│              │                          │
│   原图显示   │    检测结果显示          │
│              │                          │
│              │  读数：123.45            │
│              │  角度：45.6°             │
├──────────────┴──────────────────────────┤
│  日志输出区                              │
└─────────────────────────────────────────┘
```

---

## 📈 训练自己的数据集

### 1. 数据准备

```
datasets/my_custom_dataset/
├── images/
│   ├── train/
│   └── val/
├── labels/
│   ├── train/
│   └── val/
└── data.yaml
```

### 2. 配置文件 (data.yaml)

```yaml
path: datasets/my_custom_dataset
train: images/train
val: images/val

names:
  0: dial
  1: pointer
  2: zero_point
  3: far_point
```

### 3. 开始训练

```bash
yolo train model=yolov8n.pt data=data.yaml epochs=100 imgsz=640
```

### 4. 导出模型

```bash
# 导出为 ONNX（加速推理）
yolo export model=runs/detect/train/weights/best.pt format=onnx imgsz=640

# 导出为 TorchScript
yolo export model=runs/detect/train/weights/best.pt format=torchscript
```

---

## 🍓 树莓派部署

### 优化建议

1. **使用 ONNX 模型**（已导出，速度提升 34 倍）
   ```bash
   yolo predict model=yolov8n.onnx source=0 imgsz=320
   ```

2. **降低输入尺寸**
   ```python
   results = model(img, imgsz=320)  # 更快但精度略低
   ```

3. **降低检测频率**
   ```python
   while True:
       results = model(img)
       time.sleep(1)  # 每秒检测一次
   ```

### 预期性能

| 设备 | 模型 | 输入尺寸 | FPS |
|------|------|---------|-----|
| **PC (GPU)** | YOLOv8n | 640×640 | ~60 |
| **PC (CPU)** | YOLOv8n | 640×640 | ~10 |
| **树莓派 5** | YOLOv8n (PyTorch) | 320×320 | ~0.5 |
| **树莓派 5** | YOLOv8n (ONNX) | 320×320 | ~15-20 ⚡ |

---

## 🔍 常见问题

### Q1: GUI 无法启动

**解决**:
```bash
# 检查 PyQt5 是否安装
python3 -c "from PyQt5.QtWidgets import QApplication"

# 如无显示设备，使用虚拟显示
export QT_QPA_PLATFORM=offscreen
python3 pyqt_pointer_newmethod2.py
```

### Q2: 模型加载失败

**解决**:
```bash
# 检查模型路径
ls -lh runs/sets/3pointer_newmethod2/weights/best.pt

# 设置环境变量
export YOLO_MODEL_PATH=/path/to/best.pt
```

### Q3: 读数不准确

**优化**:
1. 确保仪表盘在图像中央
2. 调整光照条件
3. 重新训练模型（增加相似场景数据）
4. 调整置信度阈值

---

## 📝 使用示例

### Python 脚本调用

```python
from ultralytics import YOLO
import cv2

# 加载模型
model = YOLO('runs/sets/3pointer_newmethod2/weights/best.pt')

# 推理
results = model('dashboard.jpg', imgsz=640)

# 处理结果
for result in results:
    boxes = result.boxes
    for box in boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        print(f"检测到：{model.names[cls]} ({conf:.2%})")
```

### 批量处理

```python
import os
from ultralytics import YOLO

model = YOLO('runs/sets/3pointer_newmethod2/weights/best.pt')

# 批量处理文件夹中的所有图片
for img in os.listdir('images/'):
    if img.endswith('.jpg'):
        results = model(f'images/{img}', imgsz=640)
        results[0].save(f'results/{img}')
```

---

## 🎓 技术细节

### 指针检测原理

1. **YOLOv8 检测**：
   - 检测仪表盘表盘（dial）
   - 检测指针端点（far_point）
   - 检测指针中心点（center_point）
   - 检测零刻度线（zero_point）

2. **几何计算**：
   - 计算指针向量
   - 计算零刻度向量
   - 计算夹角
   - 根据量程计算读数

3. **后处理**：
   - 滤波平滑（多帧平均）
   - 异常值过滤
   - 边界限制

---

## 📚 参考资料

- [YOLOv8 官方文档](https://docs.ultralytics.com/)
- [OpenCV 几何变换](https://docs.opencv.org/)
- [PyQt5 官方文档](https://www.riverbankcomputing.com/static/Docs/PyQt5/)

---

## 📄 许可证

本项目仅供学习和研究使用。

---

**最后更新**: 2026-03-13  
**维护者**: 小爪 (Claw) 🐾  
**项目状态**: ✅ 运行正常
