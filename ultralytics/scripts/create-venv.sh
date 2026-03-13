#!/bin/bash
# 本地测试虚拟环境部署脚本（修复版）

set -e

echo "🚀 创建 Ultralytics 项目虚拟环境..."

# 进入项目目录
cd ~/.openclaw/workspace/ultralytics

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 升级 pip
pip install --upgrade pip

# 安装核心依赖（不包含 PyQt5）
echo "📦 安装核心依赖..."
pip install ultralytics opencv-python-headless numpy Pillow tqdm pyyaml requests

# 检查系统 PyQt5
echo ""
echo "🔍 检查系统 PyQt5..."
if python3 -c "import PyQt5" 2>/dev/null; then
    echo "✅ 系统已安装 PyQt5，虚拟环境可直接使用"
else
    echo "⚠️  系统未安装 PyQt5"
    echo "   安装方法："
    echo "   sudo apt install python3-pyqt5 -y"
fi

# 验证安装
echo ""
echo "✅ 验证安装..."
python -c "import ultralytics; print(f'Ultralytics v{ultralytics.__version__}')"
python -c "import cv2; print(f'OpenCV v{cv2.__version__}')"
python -c "import numpy; print(f'NumPy v{numpy.__version__}')"

echo ""
echo "🎉 虚拟环境创建完成！"
echo ""
echo "📂 位置：~/.openclaw/workspace/ultralytics/venv"
echo ""
echo "🔌 激活虚拟环境:"
echo "   source venv/bin/activate"
echo ""
echo "🚀 运行测试:"
echo "   python demo_test.py"
echo ""
echo "🖥️  运行 GUI (需要 PyQt5):"
echo "   sudo apt install python3-pyqt5 -y"
echo "   python pyqt_pointer_newmethod2.py"
echo ""
