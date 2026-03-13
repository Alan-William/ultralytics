# 树莓派运行说明（YOLO + PyQt）

本文档用于指导你在树莓派上运行本项目中的 5 个仪表识别界面脚本。

## 1. 适配内容

已完成以下跨平台改造：

- 移除 Windows 硬编码路径（如 `C:/Users/...`）。
- 改为自动使用脚本所在目录作为项目根目录。
- 结果图路径改为 Linux/Windows 通用拼接方式。
- 推理改为 `device='cpu'`，避免树莓派上默认走 CUDA 导致报错。

已改造脚本：

- `pyqt_digital.py`
- `pyqt_pointer.py`
- `pyqt_pointer360.py`
- `pyqt_pointer_newmethod.py`
- `pyqt_pointer_newmethod2.py`

## 2. 树莓派环境准备

建议：Raspberry Pi 4/5，64 位系统（Bookworm）。

### 2.1 系统依赖

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv python3-pyqt5 libatlas-base-dev libopenblas-dev
```

### 2.2 创建虚拟环境

```bash
cd ~/ultralytics
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

### 2.3 安装 Python 依赖

如果你是直接使用这个仓库，推荐先安装项目依赖：

```bash
pip install -e .
```

若出现缺少包，可补装：

```bash
pip install pyqt5 opencv-python ultralytics numpy
```

说明：树莓派上如果 `opencv-python` 安装慢或失败，可改为系统 OpenCV（`python3-opencv`）方案。

## 3. 权重文件检查

运行前确认以下权重文件存在：

- `runs/sets/2digital/weights/best.pt`
- `runs/sets/3pointer/weights/best.pt`
- `runs/sets/4pointer360/weights/best.pt`
- `runs/sets/3pointer_newmethod/weights/best.pt`
- `runs/sets/3pointer_newmethod2/weights/best.pt`

如果缺失，请将训练得到的 `best.pt` 放到对应目录。

## 4. 启动方式

在仓库根目录执行（先激活虚拟环境）：

```bash
source .venv/bin/activate
python pyqt_digital.py
```

或：

```bash
python pyqt_pointer.py
python pyqt_pointer360.py
python pyqt_pointer_newmethod.py
python pyqt_pointer_newmethod2.py
```

程序启动后点击“导入图片” -> “开始检测”。

## 5. 常见问题

### 5.1 Could not load the Qt platform plugin "xcb"

安装缺失库：

```bash
sudo apt install -y libxcb-xinerama0 libxkbcommon-x11-0
```

### 5.2 没有图形桌面（纯命令行）

PyQt 程序需要图形环境。你可以：

- 使用树莓派桌面/VNC/HDMI 显示。
- 或改为无界面推理脚本（`demo_test.py` 风格）。

### 5.3 推理慢

树莓派 CPU 推理本身较慢，可尝试：

- 使用更小模型（例如 `yolov8n`）。
- 在推理时加入较小 `imgsz`（如 320 或 416）。
- 使用 ONNX + onnxruntime（CPU）进一步优化。

## 6. 结果文件位置

检测结果文本默认写入仓库根目录：

- `Result_Digital.txt`
- `Result_pointer.txt`
- `Result_pointer360.txt`
- `Result_pointer_newmethod.txt`
- `Result_pointer_newmethod2.txt`

YOLO 输出图在 `runs/detect/...` 或对应 `save_dir` 下。

## 7. 方案2：转换为 ONNX（推荐用于树莓派提速）

你选择的是方案2。下面是最小可用流程。

### 7.1 从 .pt 导出 ONNX

在仓库根目录执行：

```bash
source .venv/bin/activate

python -m ultralytics export model=runs/sets/2digital/weights/best.pt format=onnx imgsz=640
python -m ultralytics export model=runs/sets/3pointer/weights/best.pt format=onnx imgsz=640
python -m ultralytics export model=runs/sets/4pointer360/weights/best.pt format=onnx imgsz=640
python -m ultralytics export model=runs/sets/3pointer_newmethod/weights/best.pt format=onnx imgsz=640
python -m ultralytics export model=runs/sets/3pointer_newmethod2/weights/best.pt format=onnx imgsz=640
```

导出后通常会在对应目录得到 `best.onnx`。

### 7.2 安装 ONNX Runtime

```bash
source .venv/bin/activate
pip install onnxruntime
```

### 7.3 运行 PyQt（不改代码，直接切换模型）

现在脚本支持环境变量 `YOLO_MODEL_PATH`。你可以按需指定 ONNX 模型：

```bash
source .venv/bin/activate
export YOLO_MODEL_PATH=runs/sets/2digital/weights/best.onnx
python pyqt_digital.py
```

其他脚本示例：

```bash
export YOLO_MODEL_PATH=runs/sets/3pointer/weights/best.onnx
python pyqt_pointer.py

export YOLO_MODEL_PATH=runs/sets/4pointer360/weights/best.onnx
python pyqt_pointer360.py

export YOLO_MODEL_PATH=runs/sets/3pointer_newmethod/weights/best.onnx
python pyqt_pointer_newmethod.py

export YOLO_MODEL_PATH=runs/sets/3pointer_newmethod2/weights/best.onnx
python pyqt_pointer_newmethod2.py
```

### 7.4 速度优化建议

- 可尝试导出更小输入尺寸（如 `imgsz=416` 或 `imgsz=320`）。
- 如果精度允许，优先使用轻量模型。
- 树莓派纯 CPU 下，ONNX 一般比直接 PyTorch 更省资源。

### 7.5 排查

- 若报 `onnxruntime` 缺失：重新执行 `pip install onnxruntime`。
- 若报模型路径错误：检查 `YOLO_MODEL_PATH` 是否指向实际存在的 `best.onnx`。
- 若要恢复默认 `.pt`：关闭终端重开，或执行 `unset YOLO_MODEL_PATH`。
