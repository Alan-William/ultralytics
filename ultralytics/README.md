# 🎯 仪表盘指针检测系统

> 基于 YOLOv8 的视觉检测系统 - 精准识别仪表盘指针角度与数字显示

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-8.0+-purple.svg)](https://github.com/ultralytics/ultralytics)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)

---

## 📋 项目简介

本项目是一个**完整的仪表盘视觉检测系统**，使用 YOLOv8 目标检测算法，实现：

- 🔍 **指针角度检测** - 识别指针位置并计算 0-360° 角度
- 🔢 **数字表盘识别** - 检测数码管、LCD 数字显示区域
- 🖥️ **PyQt5 可视化界面** - 实时显示检测结果
- 🛠️ **完整工具链** - 数据标注、增强、训练、推理全流程

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Windows / Linux / macOS
- NVIDIA GPU (推荐，用于加速训练)

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/Alan-William/ultralytics.git
cd ultralytics

# 安装依赖
pip install -r requirements.txt

# 或手动安装
pip install ultralytics PyQt5 opencv-python numpy
```

### 测试推理

```bash
# 运行测试脚本
python demo_test.py

# 运行 GUI 程序
python pyqt_pointer_newmethod2.py
```

---

## 📁 项目结构

```
ultralytics/
├── ultralytics/              # YOLOv8 核心库
│   ├── nn/                   # 神经网络模块
│   ├── models/               # 模型定义
│   ├── utils/                # 工具函数
│   └── solutions/            # 解决方案示例
│
├── datasets/                 # 自定义数据集
│   ├── mydata_pointer/       # 指针检测数据集
│   ├── mydata_pointer360/    # 360 度指针数据集
│   ├── mydata_pointer_newmethod/  # 新方法 v1
│   ├── mydata_pointer_newmethod2/ # 新方法 v2 (推荐)
│   ├── mydata_digital/       # 数字表盘数据集
│   └── mydata_type/          # 类型分类数据集
│
├── tools/                    # 数据处理工具
│   ├── caijian.py            # 图像裁剪
│   ├── qingxiejiaozheng.py   # 倾斜校正
│   ├── shujuzengqiang_*.py   # 数据增强
│   ├── txt2xml.py            # 格式转换
│   └── xml2txt.py            # 格式转换
│
├── runs/                     # 训练结果
│   ├── detect/               # 检测结果
│   └── sets/                 # 训练实验
│
├── pyqt_*.py                 # PyQt5 GUI 程序 (5 个版本)
├── dataset_*.yaml            # 数据集配置 (6 个)
├── train.py                  # 训练脚本
├── demo_test.py              # 测试脚本
└── README.md                 # 本文件
```

---

## 📊 数据集说明

### 1. 指针检测数据集 (推荐新手)

**配置文件**: `dataset_pointer.yaml`

```yaml
path: datasets/mydata_pointer
train: images/train  # 128 张训练图像
val: images/val      # 128 张验证图像

classes:
  0: Start Line    # 起始线
  1: End Line      # 终止线
```

**用途**: 检测仪表盘的起始线和终止线，作为角度计算的参考基准

**适用场景**: 标准圆形表盘，有明确刻度线

---

### 2. 360 度指针数据集

**配置文件**: `dataset_pointer360.yaml`

**特点**: 
- 支持全角度指针检测
- 适用于圆形表盘
- 无参考线，直接检测指针

**适用场景**: 无刻度线的简化表盘

---

### 3. 新方法数据集 (推荐进阶)

**版本对比**:

| 版本 | 配置文件 | 改进点 | 推荐度 |
|------|---------|--------|--------|
| **v1** | `dataset_pointer_newmethod.yaml` | 优化标注方法 | ⭐⭐⭐⭐ |
| **v2** | `dataset_pointer_newmethod2.yaml` | 进一步改进精度 | ⭐⭐⭐⭐⭐ |

**使用方法**:
```bash
# 编辑 train.py，使用新方法数据集
model.train(data='dataset_pointer_newmethod2.yaml', epochs=200, batch=8)
```

---

### 4. 数字表盘数据集

**配置文件**: `dataset_digital.yaml`

**用途**: 识别数字显示区域（数码管、LCD 等）

**适用场景**: 数字式仪表，非指针式

---

## 🛠️ 工具脚本使用

### 数据预处理

#### 1. 图像裁剪

```bash
python tools/caijian.py
```

**功能**: 裁剪 ROI 区域，减少背景干扰

---

#### 2. 倾斜校正

```bash
# 标准版本
python tools/qingxiejiaozheng.py

# 快速版本
python tools/qingxiejiaozheng_shan.py
```

**功能**: 校正拍摄角度导致的表盘倾斜

**原理**: 
1. 检测关键点
2. 计算透视变换矩阵
3. 应用 `cv2.warpPerspective`

---

#### 3. 数据增强

```bash
# 旋转增强
python tools/shujuzengqiang_xuanzhuan.py

# 颜色增强
python tools/shujuzengqiang_yanse.py
```

**功能**: 
- 随机旋转（-30° 到 +30°）
- 亮度、对比度、色相调整
- 扩充数据集，提升模型鲁棒性

---

### 格式转换

#### YOLO TXT ↔ VOC XML

```bash
# YOLO TXT → VOC XML
python tools/txt2xml.py

# VOC XML → YOLO TXT
python tools/xml2txt.py
```

**用途**: 适配不同标注格式需求

---

## 🎯 模型训练

### 基础训练

```bash
python train.py
```

**默认配置**:
```python
model.train(
    data='dataset_pointer_newmethod2.yaml',  # 数据集
    epochs=200,        # 训练轮数
    batch=8,          # 批次大小
    workers=0,        # 数据加载线程数
    imgsz=640,        # 输入图像尺寸
    device=0,         # GPU 设备 (0=GPU, cpu=CPU)
)
```

---

### 自定义训练

**编辑 `train.py`**:

```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')  # 加载预训练模型

# 训练配置
model.train(
    data='dataset_digital.yaml',    # 选择数据集
    epochs=500,                      # 训练轮数
    batch=16,                        # 批次大小
    workers=4,                       # 数据加载线程
    device='0',                      # 使用 GPU 0
    patience=50,                     # 早停耐心值
    lr0=0.01,                        # 初始学习率
)
```

---

### 训练参数说明

| 参数 | 默认值 | 说明 | 建议 |
|------|--------|------|------|
| **epochs** | 200 | 训练轮数 | 200-500 |
| **batch** | 8 | 批次大小 | 8-16 (根据显存) |
| **workers** | 0 | 数据加载线程 | 0-4 (Windows 建议 0) |
| **imgsz** | 640 | 输入尺寸 | 640 或 1280 |
| **patience** | 50 | 早停耐心值 | 30-100 |
| **lr0** | 0.01 | 初始学习率 | 0.001-0.01 |

---

### 监控训练

**查看训练日志**:
```bash
# 实时查看
tail -f runs/sets/3pointer_newmethod2/args.yaml

# 查看训练指标
cat runs/sets/3pointer_newmethod2/results.csv
```

**训练结果位置**:
```
runs/sets/3pointer_newmethod2/
├── weights/
│   ├── best.pt      # 最佳模型权重
│   └── last.pt      # 最后一轮权重
├── results.csv      # 训练指标
└── args.yaml        # 训练参数
```

---

## 🖥️ PyQt5 GUI 使用

### 程序版本对比

| 程序 | 大小 | 功能 | 适用场景 |
|------|------|------|---------|
| **pyqt_pointer.py** | 21.9KB | 基础指针检测 | 学习参考 |
| **pyqt_pointer360.py** | 21.1KB | 360 度检测 | 全角度表盘 |
| **pyqt_pointer_newmethod.py** | 14.5KB | 新方法 v1 | 代码优化 |
| **pyqt_pointer_newmethod2.py** | 13.2KB | 新方法 v2 | **推荐使用** |
| **pyqt_digital.py** | 9.5KB | 数字识别 | 数字表盘 |

---

### 运行 GUI

```bash
# 推荐版本
python pyqt_pointer_newmethod2.py

# 数字表盘
python pyqt_digital.py

# 360 度检测
python pyqt_pointer360.py
```

---

### GUI 功能

1. **📷 图像加载**
   - 支持 JPG、PNG 格式
   - 拖拽加载或按钮选择

2. **🎯 模型推理**
   - 加载训练好的 YOLO 模型
   - 实时检测目标

3. **📐 角度计算**
   - 自动计算指针角度
   - 显示 0-360° 读数

4. **📊 结果可视化**
   - 绘制检测框
   - 显示置信度
   - 标注角度值

5. **💾 结果保存**
   - 保存标注图像
   - 导出检测结果

---

### 核心算法

**角度计算** (来自 `pyqt_pointer.py`):

```python
class Functions:
    @staticmethod
    def GetClockAngle(v1, v2):
        """计算两个向量的夹角 (0-360 度)"""
        TheNorm = np.linalg.norm(v1) * np.linalg.norm(v2)
        
        # 叉乘判断方向
        rho = np.rad2deg(np.arcsin(np.cross(v1, v2) / TheNorm))
        
        # 点乘计算角度
        theta = np.rad2deg(np.arccus(np.dot(v1, v2) / TheNorm))
        
        # 返回 0-360 度
        if rho > 0:
            return theta
        else:
            return 360 - theta
    
    @staticmethod
    def Distances(a, b):
        """计算两点间欧几里得距离"""
        return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
```

---

## 📈 性能优化

### 推理加速

1. **使用 TensorRT**
   ```bash
   yolo export model=best.pt format=engine
   ```

2. **模型量化**
   ```bash
   yolo export model=best.pt format=onnx opset=13
   ```

3. **减小输入尺寸**
   ```python
   model.predict(source='image.jpg', imgsz=320)
   ```

---

### 精度提升

1. **增加训练数据**
   - 使用数据增强工具
   - 收集更多样化的样本

2. **调整超参数**
   ```python
   model.train(
       lr0=0.001,      # 降低学习率
       epochs=500,     # 增加轮数
       augment=True,   # 启用增强
   )
   ```

3. **使用更大模型**
   ```python
   model = YOLO('yolov8m.pt')  # medium 版本
   model = YOLO('yolov8l.pt')  # large 版本
   ```

---

## 🔧 常见问题

### Q1: 训练时显存不足

**解决**:
```python
# 减小 batch size
model.train(batch=4)  # 或 2

# 减小图像尺寸
model.train(imgsz=320)

# 使用更小模型
model = YOLO('yolov8n.pt')  # nano 版本
```

---

### Q2: Windows 多进程错误

**解决**:
```python
# 设置 workers=0
model.train(workers=0)
```

---

### Q3: 检测精度低

**检查**:
1. 数据集标注质量
2. 训练轮数是否足够
3. 学习率是否合适
4. 数据增强是否充分

**改进**:
```bash
# 使用新方法数据集
python train.py  # 编辑为 dataset_pointer_newmethod2.yaml
```

---

### Q4: GUI 程序无法启动

**检查**:
```bash
# 确认 PyQt5 已安装
pip install PyQt5

# 检查模型路径
# 编辑 pyqt_*.py，确认模型文件路径正确
```

---

## 📚 进阶使用

### 自定义数据集

1. **准备图像**
   ```
   datasets/mydata_custom/
   ├── images/
   │   ├── train/
   │   └── val/
   └── labels/
       ├── train/
       └── val/
   ```

2. **创建配置文件**
   ```yaml
   # dataset_custom.yaml
   path: datasets/mydata_custom
   train: images/train
   val: images/val
   
   classes:
     0: YourClass1
     1: YourClass2
   ```

3. **开始训练**
   ```python
   model.train(data='dataset_custom.yaml')
   ```

---

### 部署到生产

1. **导出模型**
   ```bash
   yolo export model=best.pt format=onnx
   ```

2. **创建服务**
   ```python
   from flask import Flask, request
   from ultralytics import YOLO
   
   app = Flask(__name__)
   model = YOLO('best.onnx')
   
   @app.route('/predict', methods=['POST'])
   def predict():
       img = request.files['image']
       results = model(img)
       return results[0].tojson()
   ```

3. **Docker 部署**
   ```dockerfile
   FROM python:3.9
   COPY . /app
   RUN pip install -r /app/requirements.txt
   CMD ["python", "app.py"]
   ```

---

## 📄 许可证

MIT License © 2024-2026 Alan William

---

## 🙏 致谢

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) - 核心检测框架
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - GUI 框架
- [OpenCV](https://opencv.org/) - 图像处理

---

## 📞 联系方式

- **GitHub**: [@Alan-William](https://github.com/Alan-William)
- **项目仓库**: https://github.com/Alan-William/ultralytics

---

**最后更新**: 2026-03-13  
**版本**: v1.0  
**状态**: ✅ 活跃维护
