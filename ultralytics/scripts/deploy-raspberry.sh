#!/bin/bash
# 🍓 树莓派部署脚本 - Ultralytics YOLOv8
# 适用于 Raspberry Pi 5 (4GB/8GB)

set -e  # 遇到错误立即退出

echo "=========================================="
echo "🍓 树莓派 YOLOv8 部署脚本"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否在树莓派上运行
if ! command -v vcgencmd &> /dev/null; then
    echo -e "${YELLOW}⚠️  警告：这不是树莓派设备，但仍可继续部署${NC}"
fi

# 检查 Python 版本
echo "📋 检查 Python 版本..."
python3 --version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}"
echo ""

# 创建项目目录
PROJECT_DIR="$HOME/ultralytics-project"
echo "📁 创建项目目录：$PROJECT_DIR"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"
echo -e "${GREEN}✓ 项目目录已创建${NC}"
echo ""

# 创建虚拟环境
echo "🐍 创建 Python 虚拟环境..."
python3 -m venv venv
echo -e "${GREEN}✓ 虚拟环境已创建${NC}"
echo ""

# 激活虚拟环境
echo "🔌 激活虚拟环境..."
source venv/bin/activate
echo -e "${GREEN}✓ 虚拟环境已激活${NC}"
echo ""

# 升级 pip
echo "📦 升级 pip..."
pip install --upgrade pip
echo -e "${GREEN}✓ pip 已升级${NC}"
echo ""

# 安装依赖
echo "📚 安装依赖包..."
pip install -r requirements-raspberry.txt
echo -e "${GREEN}✓ 依赖包已安装${NC}"
echo ""

# 验证安装
echo "✅ 验证安装..."
python3 -c "import ultralytics; print(f'Ultralytics v{ultralytics.__version__}')"
python3 -c "import cv2; print(f'OpenCV v{cv2.__version__}')"
python3 -c "import numpy; print(f'NumPy v{numpy.__version__}')"
echo -e "${GREEN}✓ 所有依赖验证通过${NC}"
echo ""

# 下载示例模型
echo "📥 下载示例模型 (YOLOv8n)..."
python3 -c "from ultralytics import YOLO; model = YOLO('yolov8n.pt')"
echo -e "${GREEN}✓ 模型已下载${NC}"
echo ""

# 创建测试脚本
echo "📝 创建测试脚本..."
cat > test_raspberry.py << 'EOF'
#!/usr/bin/env python3
"""
树莓派 YOLOv8 测试脚本
"""
from ultralytics import YOLO
import cv2
import time

def test_image_inference():
    """测试图片推理"""
    print("🖼️  测试图片推理...")
    
    # 加载模型
    model = YOLO('yolov8n.pt')
    
    # 创建测试图片（或替换为实际图片路径）
    img = cv2.imread('test.jpg')
    if img is None:
        print("⚠️  未找到 test.jpg，创建纯色测试图")
        img = cv2.imread('/usr/share/pixmaps/debian-logo.png')
        if img is None:
            img = cv2.cvtColor(cv2.resize(cv2.imread('/usr/share/pixmaps/debian-logo.png'), (640, 640)), cv2.COLOR_BGR2RGB)
    
    # 推理
    start = time.time()
    results = model(img, imgsz=320, verbose=False)
    end = time.time()
    
    # 显示结果
    annotated = results[0].plot()
    cv2.imwrite('result.jpg', annotated)
    
    print(f"✅ 推理完成！耗时：{end-start:.2f}秒")
    print(f"📊 检测结果：{len(results[0].boxes)} 个目标")
    print("💾 结果已保存到 result.jpg")
    print()

def test_camera():
    """测试摄像头（可选）"""
    print("📷 测试摄像头...")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ 无法打开摄像头")
        return
    
    model = YOLO('yolov8n.pt')
    
    print("按 q 键退出")
    frame_count = 0
    start = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 每 5 帧检测一次（提高速度）
        if frame_count % 5 == 0:
            results = model(frame, imgsz=320, verbose=False)
            annotated = results[0].plot()
        else:
            annotated = frame
        
        cv2.imshow('YOLOv8 on Raspberry Pi', annotated)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_count += 1
    
    end = time.time()
    fps = frame_count / (end - start)
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"✅ 摄像头测试完成！FPS: {fps:.2f}")
    print()

if __name__ == '__main__':
    print("=" * 40)
    print("🍓 树莓派 YOLOv8 测试")
    print("=" * 40)
    print()
    
    test_image_inference()
    
    # 取消注释以测试摄像头
    # test_camera()
    
    print("🎉 所有测试完成！")
EOF

chmod +x test_raspberry.py
echo -e "${GREEN}✓ 测试脚本已创建${NC}"
echo ""

# 创建推理脚本
echo "📝 创建推理脚本..."
cat > inference.py << 'EOF'
#!/usr/bin/env python3
"""
树莓派 YOLOv8 推理脚本
支持图片、视频、摄像头
"""
import argparse
from ultralytics import YOLO
import cv2
import time

def main():
    parser = argparse.ArgumentParser(description='树莓派 YOLOv8 推理')
    parser.add_argument('--source', type=str, default='0', help='输入源 (0=摄像头，图片路径，视频路径)')
    parser.add_argument('--model', type=str, default='yolov8n.pt', help='模型路径')
    parser.add_argument('--imgsz', type=int, default=320, help='输入图像尺寸')
    parser.add_argument('--conf', type=float, default=0.25, help='置信度阈值')
    parser.add_argument('--save', action='store_true', help='保存结果')
    args = parser.parse_args()
    
    # 加载模型
    print(f"📥 加载模型：{args.model}")
    model = YOLO(args.model)
    
    # 推理
    print(f"🚀 开始推理...")
    print(f"   输入源：{args.source}")
    print(f"   图像尺寸：{args.imgsz}")
    print(f"   置信度：{args.conf}")
    print()
    
    start = time.time()
    results = model(
        source=args.source,
        imgsz=args.imgsz,
        conf=args.conf,
        save=args.save,
        verbose=True
    )
    end = time.time()
    
    print()
    print(f"✅ 推理完成！总耗时：{end-start:.2f}秒")

if __name__ == '__main__':
    main()
EOF

chmod +x inference.py
echo -e "${GREEN}✓ 推理脚本已创建${NC}"
echo ""

# 创建 Systemd 服务（可选）
echo "📝 创建 Systemd 服务配置（可选）..."
cat > ultralytics.service << 'EOF'
[Unit]
Description=Ultralytics YOLOv8 Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/ultralytics-project
Environment="PATH=/home/pi/ultralytics-project/venv/bin"
ExecStart=/home/pi/ultralytics-project/venv/bin/python3 /home/pi/ultralytics-project/inference.py --source 0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
echo -e "${GREEN}✓ Systemd 服务配置已创建${NC}"
echo ""

# 显示使用说明
echo ""
echo "=========================================="
echo -e "${GREEN}✅ 部署完成！${NC}"
echo "=========================================="
echo ""
echo "📂 项目目录：$PROJECT_DIR"
echo ""
echo "🚀 快速开始："
echo "   1. 激活虚拟环境:"
echo "      source $PROJECT_DIR/venv/bin/activate"
echo ""
echo "   2. 运行测试:"
echo "      python3 test_raspberry.py"
echo ""
echo "   3. 运行推理:"
echo "      python3 inference.py --source 0  # 摄像头"
echo "      python3 inference.py --source image.jpg  # 图片"
echo ""
echo "📚 文件说明:"
echo "   - test_raspberry.py  : 测试脚本"
echo "   - inference.py       : 推理脚本"
echo "   - ultralytics.service: Systemd 服务配置"
echo ""
echo "⚡ 性能优化建议:"
echo "   - 使用 YOLOv8n 模型（最小）"
echo "   - 减小 imgsz (320 比 640 快 4 倍)"
echo "   - 导出为 ONNX 格式加速推理"
echo ""
echo "🔧 导出 ONNX 模型（在 PC 上执行）:"
echo "   yolo export model=best.pt format=onnx imgsz=320"
echo ""
echo "=========================================="
echo ""
