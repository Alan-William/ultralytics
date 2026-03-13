import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, \
    QTextEdit, QInputDialog
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from ultralytics import YOLO
import numpy as np
import datetime
import os


class ImageDetection(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.before_imagepath = None
        self.later_imagepath = None
        self.result_string = None
        self.flie_path = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.getenv('YOLO_MODEL_PATH', os.path.join(self.flie_path, 'runs', 'sets', '2digital', 'weights', 'best.pt'))
        self.txt_path = os.path.join(self.flie_path, 'Result_Digital.txt')  # 读数保存路径

    def initUI(self):
        # 设置窗口的标题和大小
        self.setWindowTitle('Digital Detection')
        self.setGeometry(0, 0, 1900, 1050)
        # 获取屏幕的尺寸
        screen = app.primaryScreen()
        screen_rect = screen.availableGeometry()
        # 计算窗口在屏幕中央的位置
        x = (screen_rect.width() - self.width()) // 2
        y = (screen_rect.height() - self.height()) // 2
        self.move(x, y)  # 设置窗口的位置为屏幕中央

        # 创建水平布局和垂直布局
        mainLayout = QVBoxLayout()
        topLayout = QHBoxLayout()

        # 在最上方添加一行文字
        topLayout.addStretch(1)  # 在标签前添加弹性空间
        self.topLabel = QLabel('数字式仪表读数检测识别系统')
        font4 = QFont('times', 26)
        self.topLabel.setFont(font4)
        topLayout.addWidget(self.topLabel)  # 将标签添加到布局中
        # topLayout.addStretch(1)  # 在标签前添加弹性空间
        mainLayout.addLayout(topLayout)
        mainLayout.setAlignment(topLayout, Qt.AlignCenter)

        leftLayout = QVBoxLayout()
        middleLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()
        contentLayout = QHBoxLayout()

        contentLayout.addLayout(leftLayout, 1)
        contentLayout.addLayout(middleLayout, 2)
        contentLayout.addLayout(rightLayout, 3)

        # 创建并设置标签来显示图片
        self.imageLabel1 = QLabel('未检测图片')
        self.imageLabel1.setAlignment(Qt.AlignCenter)
        self.imageLabel2 = QLabel('检测后图片')
        self.imageLabel2.setAlignment(Qt.AlignCenter)

        # 按钮导入图片
        self.loadImageButton = QPushButton('导入图片')
        self.loadImageButton.clicked.connect(self.loadImage)
        # 按钮开始检测
        self.detectButton = QPushButton('开始检测')
        self.detectButton.clicked.connect(self.detect)
        # 按钮提交取消
        self.defineButton = QPushButton('确认')
        self.defineButton.clicked.connect(self.define)
        self.modifyButton = QPushButton('修改')
        self.modifyButton.clicked.connect(self.modify)
        # 按钮清除txt内容
        self.clearButton = QPushButton('清除')
        self.clearButton.clicked.connect(self.clear)
        # 创建文本编辑器来显示文本文件内容
        self.textEdit = QTextEdit()
        # 设置定时器，定期读取文件内容
        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # 设置时间间隔为1000毫秒
        self.timer.timeout.connect(self.readFile)
        self.timer.start()

        # 创建一个QLabel来显示计算后的字符串
        self.txt_label1 = QLabel(f'', self)
        self.txt_label2 = QLabel(f'', self)
        self.txt_label3 = QLabel(f'检测结果', self)
        # 设置QLabel的字体和大小
        font = QFont('times', 16)
        font2 = QFont('times', 18)
        font3 = QFont('times', 12)
        self.txt_label1.setFont(font)
        self.txt_label2.setFont(font)
        self.imageLabel1.setFont(font)
        self.imageLabel2.setFont(font)
        self.txt_label3.setFont(font2)
        self.textEdit.setFont(font3)
        self.textEdit.setStyleSheet("background-color: white; color: black;")

        self.imageLabel1.setMinimumWidth(600)
        self.imageLabel1.setMaximumWidth(600)
        self.imageLabel2.setMinimumWidth(600)
        self.imageLabel2.setMaximumWidth(600)
        self.loadImageButton.setMinimumWidth(600)
        self.loadImageButton.setMaximumWidth(600)
        self.detectButton.setMinimumWidth(600)
        self.detectButton.setMaximumWidth(600)
        self.defineButton.setMinimumWidth(600)
        self.defineButton.setMaximumWidth(600)
        self.modifyButton.setMinimumWidth(600)
        self.modifyButton.setMaximumWidth(600)
        self.textEdit.setMinimumWidth(700)
        self.textEdit.setMaximumWidth(700)

        # 将组件添加到布局中
        topLayout.addWidget(self.topLabel)

        leftLayout.addWidget(self.imageLabel1)
        leftLayout.addWidget(self.loadImageButton)
        leftLayout.addWidget(self.detectButton)

        middleLayout.addWidget(self.imageLabel2)
        middleLayout.addWidget(self.defineButton)
        middleLayout.addWidget(self.modifyButton)

        rightLayout.addWidget(self.txt_label3)
        rightLayout.addWidget(self.txt_label1)
        rightLayout.addWidget(self.txt_label2)
        rightLayout.addWidget(self.textEdit)
        rightLayout.addWidget(self.clearButton)

        # 将水平布局添加到主布局中
        mainLayout.addLayout(contentLayout)
        # 设置主布局
        self.setLayout(mainLayout)

    def define(self):
        with open(self.txt_path, 'a') as file:
            file.write("The reading is correct.\n")

    def clear(self):
        with open(self.txt_path, 'w') as file:
            file.write("")

    def modify(self):
        # 创建输入对话框
        inputDialog = QInputDialog(self)
        inputDialog.setWindowTitle('Modify')
        inputDialog.setLabelText('Enter your value:')
        inputDialog.setTextValue(self.result_string)
        inputDialog.resize(260, 150)  # 设置输入对话框的大小
        # 显示对话框并等待用户响应
        ok = inputDialog.exec_()
        text = inputDialog.textValue()
        if ok:
            # 用户点击了OK，处理输入的文本
            with open(self.txt_path, 'a') as file:
                file.write("The corrected reading is:" + text + '\n')

    def loadImage(self):
        # 打开文件对话框加载图片
        imagePath, _ = QFileDialog.getOpenFileName()
        self.before_imagepath = imagePath
        if imagePath:
            pixmap = QPixmap(imagePath)
            # self.imageLabel1.setPixmap(pixmap.scaled(self.imageLabel1.size(), Qt.KeepAspectRatio))
            scaled_pixmap = pixmap.scaled(600, 420)
            self.imageLabel1.setPixmap(scaled_pixmap)

    def readFile(self):
        # 从文件中读取内容并显示在 QTextEdit 控件中
        try:
            with open(self.txt_path, 'r') as file:
                self.textEdit.setText(file.read())
        except FileNotFoundError:
            self.textEdit.setText("File not found.")

    def detect(self):
        self.yolo = YOLO(model=self.model_path, task='detect')
        self.result = self.yolo(source=self.before_imagepath, save=True, conf=0.3, device='cpu')

        data = self.result[0].boxes.data.cpu().numpy()
        xywh = self.result[0].boxes.xywh.cpu().numpy()

        # 从数组b中提取最后一列，并将其变形为列向量
        data_last_column = data[:, -1].reshape(-1, 1)
        # 使用np.hstack将b的最后一列添加到a的右侧
        xywh_extended = np.hstack((xywh, data_last_column))

        # 使用argsort()方法对第一列进行排序，并获取排序后的索引
        sorted_indices = np.argsort(xywh_extended[:, 0])
        # 使用排序后的索引对整个数组进行排序
        xywh_extended_sorted = xywh_extended[sorted_indices]

        # 从数组中获取最后一列
        last_column = xywh_extended_sorted[:, -1]
        # 将最后一列转换为Python列表
        last_column_list = last_column.tolist()

        # 使用列表推导和字典的get方法获取对应的键值
        keys = [self.result[0].names.get(int(value)) for value in last_column_list]
        # 转为字符串
        self.result_string = ''.join(keys)

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.txt_label1.setText(current_time)
        self.txt_label2.setText('The reading of the instrument is: ' + self.result_string)
        with open(self.txt_path, 'a') as file:
            file.write(current_time)
            file.write("\nThe reading of the instrument is: " + self.result_string + '\n')

        img_name = os.path.basename(self.result[0].path)
        img_path = os.path.join(str(self.result[0].save_dir), img_name)
        pixmap = QPixmap(img_path)
        # self.imageLabel1.setPixmap(pixmap.scaled(self.imageLabel1.size(), Qt.KeepAspectRatio))
        scaled_pixmap = pixmap.scaled(600, 420)  # 将图像缩放
        self.imageLabel2.setPixmap(scaled_pixmap)


# 创建应用程序和窗口实例，并运行应用程序
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageDetection()
    ex.show()
    sys.exit(app.exec_())
