# 🍓 树莓派部署指南

> 在 Raspberry Pi 5 上部署 Ultralytics YOLOv8 仪表盘检测系统

---

## 📋 部署方式

### 方式 1：本地虚拟环境（推荐用于测试）

**适用场景**: 在 PC 上测试、开发

**已完成**: ✅ 虚拟环境已创建

**位置**: `~/.openclaw/workspace/ultralytics/venv`

**使用方法**:
```bash
# 1. 激活虚拟环境
cd ~/.openclaw/workspace/ultralytics
source venv/bin/activate

# 2. 运行测试
python demo_test.py

# 3. 运行 GUI
python pyqt_pointer_newmethod2.py
```

---

### 方式 2：树莓派部署（生产环境）

**适用场景**: 在树莓派上实际运行

**步骤**:

#### 1. 传输项目到树莓派

```bash
# 在 PC 上执行
cd ~/.openclaw/workspace
tar -czf ultralytics-project.tar.gz ultralytics/
scp ultralytics-project.tar.gz pi@raspberrypi.local:~/
```

#### 2. 在树莓派上部署

```bash
# SSH 登录树莓派
ssh pi@raspberrypi.local

# 解压项目
tar -xzf ultralytics-project.tar.gz
cd ultralytics

# 运行部署脚本
chmod +x scripts/deploy-raspberry.sh
bash scripts/deploy-raspberry.sh
```

#### 3. 验证安装

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行测试
python test_raspberry.py
```

---

## 📦 依赖说明

### 核心依赖（已安装）

| 包名 | 版本 | 用途 |
|------|------|------|
| **ultralytics** | 8.4.21 | YOLOv8 框架 |
| **opencv-python** | 4.13.0 | 图像处理 |
| **numpy** | 2.4.3 | 数值计算 |
| **Pillow** | 12.1.1 | 图像加载 |
| **torch** | 2.10.0 | PyTorch 后端 |
| **torchvision** | 0.25.0 | 视觉模型 |
| **matplotlib** | 3.10.8 | 结果可视化 |

### 可选依赖

| 包名 | 用途 | 安装命令 |
|------|------|---------|
| **PyQt5** | GUI 界面 | `sudo apt install python3-pyqt5` |
| **onnxruntime** | ONNX 加速 | `pip install onnxruntime` |
| **tflite-runtime** | TFLite 加速 | 需手动编译 |

---

## 🚀 性能优化

### 1. 模型导出（在 PC 上执行）

```bash
# 导出为 ONNX（推荐）
yolo export model=best.pt format=onnx imgsz=320

# 导出为 TFLite（更快）
yolo export model=best.pt format=tflite imgsz=320

# 导出为 OpenVINO（Intel 设备）
yolo export model=best.pt format=openvino
```

### 2. 复制到树莓派

```bash
scp best.onnx pi@raspberrypi.local:~/ultralytics/
```

### 3. 树莓派推理

```bash
# 使用 ONNX 模型
python inference.py --model best.onnx --source 0
```

---

## 📊 性能对比

| 配置 | 模型 | 输入尺寸 | FPS | 备注 |
|------|------|---------|-----|------|
| **PC (GPU)** | YOLOv8n | 640×640 | ~60 | RTX 3060 |
| **PC (CPU)** | YOLOv8n | 640×640 | ~10 | i7-12700K |
| **树莓派 5** | YOLOv8n | 320×320 | ~2-3 | CPU 推理 |
| **树莓派 5** | YOLOv8n (ONNX) | 320×320 | ~3-4 | ONNX 加速 |
| **树莓派 5** | YOLOv8n (TFLite) | 320×320 | ~5-6 | TFLite+EdgeTPU |

---

## 🔧 常见问题

### Q1: 内存不足

**解决**:
```bash
# 增加交换空间（已在 2026-03-13 完成）
sudo swapon --show

# 使用更小模型
python inference.py --model yolov8n.pt --imgsz 320
```

### Q2: PyQt5 安装失败

**解决**:
```bash
# 使用系统包管理器安装
sudo apt update
sudo apt install python3-pyqt5 -y

# 或在虚拟环境外运行 GUI
system-python3 pyqt_pointer_newmethod2.py
```

### Q3: 推理速度慢

**优化**:
```bash
# 1. 减小输入尺寸
python inference.py --imgsz 320

# 2. 降低检测频率
# 编辑 inference.py，添加 time.sleep(0.5)

# 3. 使用 ONNX 模型
python inference.py --model best.onnx
```

### Q4: 摄像头无法打开

**解决**:
```bash
# 检查摄像头权限
ls -la /dev/video0

# 添加用户到 video 组
sudo usermod -a -G video $USER

# 重启
sudo reboot
```

---

## 📝 使用示例

### 图片检测

```bash
source venv/bin/activate
python inference.py --source image.jpg --save
```

### 摄像头实时检测

```bash
source venv/bin/activate
python inference.py --source 0 --imgsz 320
```

### 视频文件检测

```bash
source venv/bin/activate
python inference.py --source video.mp4 --save
```

### 批量检测

```bash
source venv/bin/activate
python inference.py --source path/to/images/ --save
```

---

## 🎯 最佳实践

### 1. 训练与推理分离

```
PC/服务器：训练模型 → 导出 ONNX → 上传到树莓派
树莓派：加载 ONNX → 推理 → 输出结果
```

### 2. 降低检测频率

```python
# 不需要实时检测时
import time
while True:
    results = model(img)
    time.sleep(1)  # 每秒检测一次
```

### 3. 使用看门狗脚本

```bash
# 创建监控脚本
cat > watchdog.sh << 'EOF'
#!/bin/bash
while true; do
    if ! pgrep -f "inference.py" > /dev/null; then
        echo "$(date): 重启推理服务..." >> watchdog.log
        source venv/bin/activate
        python inference.py --source 0 &
    fi
    sleep 10
done
EOF

chmod +x watchdog.sh
./watchdog.sh &
```

---

## 📚 相关文件

| 文件 | 用途 | 位置 |
|------|------|------|
| **deploy-raspberry.sh** | 树莓派部署脚本 | `scripts/` |
| **create-venv.sh** | 虚拟环境创建 | `scripts/` |
| **inference.py** | 推理脚本 | 项目根目录 |
| **test_raspberry.py** | 测试脚本 | 项目根目录 |
| **ultralytics.service** | Systemd 服务 | 项目根目录 |
| **requirements-raspberry.txt** | 依赖列表 | 项目根目录 |

---

## 🔗 参考资源

- [Ultralytics 官方文档](https://docs.ultralytics.com/)
- [树莓派 YOLOv8 部署教程](https://www.raspberrypi.com/)
- [ONNX 运行时优化](https://onnxruntime.ai/)

---

**最后更新**: 2026-03-13  
**状态**: ✅ 虚拟环境已创建  
**维护者**: 小爪 (Claw) 🐾
