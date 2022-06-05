import math
from PyQt5 import QtCore, QtGui, QtWidgets
from controller import Controller


class MainWindow(object):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.menus_height = 0.5  # 菜单区与主页面高度比。
        self.main_window = None
        self.main_layout = None
        self.menus_widget = QtWidgets.QWidget()
        self.menus_layout = None
        self.menu_margin = 10
        self.menu_size = [-1, -1]
        self.menu_1 = Menu()
        self.menu_2 = Menu()
        self.menu_3 = Menu()
        self.menu_4 = Menu()
        self.controller = Controller(self)

    def setup_view(self, main_window):
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # 设置主窗口。
        self.main_window = main_window
        self.main_window.setMinimumSize(1280, 720)
        # self.main_window.resize(1400, 790)
        self.main_window.setWindowTitle('IE Automation Kit')
        self.main_window.setWindowIcon(QtGui.QIcon(r'assets\icons\title.png'))
        self.main_window.setStyleSheet('background-color: #2A2A2A')
        # 上部空白区。
        empty_widget = QtWidgets.QWidget()
        empty_widget.setSizePolicy(size_policy)
        # 中部功能区。
        self.menus_widget.setStyleSheet('background-color: #333333')
        self.menus_widget.setFixedHeight(self.main_window.height() * 0.6)
        # 菜单。
        self.menu_1.setText('图卡支架')
        self.menu_1.setPixmap(r'assets\icons\card_holder.png')
        self.menu_1.folder_button.clicked.connect(lambda: self.controller.select_dir(1))
        self.menu_1.switch_button.clicked.connect(lambda: self.controller.switch_camera(1))
        self.menu_2.setText('实景灯箱')
        self.menu_2.setPixmap(r'assets\icons\light_box.png')
        self.menu_2.folder_button.clicked.connect(lambda: self.controller.select_dir(2))
        self.menu_2.switch_button.clicked.connect(lambda: self.controller.switch_camera(2))
        self.menu_3.setText('机械臂')
        self.menu_3.setPixmap(r'assets\icons\arm.png')
        self.menu_3.folder_button.clicked.connect(lambda: self.controller.select_dir(3))
        self.menu_3.switch_button.clicked.connect(lambda: self.controller.switch_camera(3))
        self.menu_4.setText('系统设置')
        self.menu_4.setPixmap(r'assets\icons\title.png')
        self.menu_4.folder_button.clicked.connect(lambda: self.controller.select_dir(4))
        self.menu_4.switch_button.clicked.connect(lambda: self.controller.switch_camera(4))
        self.menus_layout = QtWidgets.QHBoxLayout(self.menus_widget)
        self.menus_layout.setContentsMargins(self.menu_margin, self.menu_margin, self.menu_margin, self.menu_margin)
        self.menus_layout.setSpacing(self.menu_margin)
        self.menus_layout.addWidget(self.menu_1)
        self.menus_layout.addWidget(self.menu_2)
        self.menus_layout.addWidget(self.menu_3)
        self.menus_layout.addWidget(self.menu_4)
        # 下部版权区。
        copyright_label = QtWidgets.QLabel(self.main_window)
        copyright_label.setText('QtDemo @ 2022 All Rights Reserved.')
        copyright_label.setSizePolicy(size_policy)
        copyright_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignBottom)
        copyright_label.setStyleSheet("color:white")
        # 总布局：上部是菜单区，下部是版权文字区。
        self.main_layout = QtWidgets.QVBoxLayout(self.main_window)
        self.main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(empty_widget)
        self.main_layout.addWidget(self.menus_widget)
        self.main_layout.addWidget(copyright_label)

    def resizeEvent(self, event):
        # 菜单高度动态变化。
        h = event.size().height()
        self.menus_widget.setFixedHeight(h * self.menus_height)
        # 计算单个菜单的宽高。
        menus_num = self.menus_layout.count()
        self.menu_size[0] = int((self.main_window.width() - self.menu_margin * (menus_num + 1)) / menus_num)
        self.menu_size[1] = self.menu_1.img_label.height()
        # 维持各菜单宽度相等。
        self.menu_1.setFixedWidth(self.menu_size[0])
        self.menu_2.setFixedWidth(self.menu_size[0])
        self.menu_3.setFixedWidth(self.menu_size[0])
        self.menu_4.setFixedWidth(self.menu_size[0])


class Menu(QtWidgets.QWidget):
    def __init__(self):
        super(Menu, self).__init__()
        self.margin = 1  # 下部组件的左右边距，用于实现点击阴影。
        self.height1 = 40  # 中部高度。
        self.height2 = 30  # 下部高度。
        self.paint_flag = 0  # 鼠标按下或松开。

        # 上部组件。
        self.title_label = QtWidgets.QLabel()

        # 中上部组件。
        self.pixpath = r'assets\icons\title.png'
        self.pixmap = QtGui.QPixmap(self.pixpath)
        self.img_label = QtWidgets.QLabel()

        # 中部拍照、录像控制。
        self.mid_layout = None
        self.img_button = ImgButton()
        self.time_label = QtWidgets.QLabel()
        self.video_button = VideoButton()

        # 中下部分割线。
        # separate_line

        # 下部组件。
        self.llight_lable = QtWidgets.QLabel()
        self.play_button = PlayButton()
        self.msg_lable = QtWidgets.QLabel()
        self.folder_button = QtWidgets.QPushButton()
        self.switch_button = SwitchButton('拍照', '录像')
        self.analyze_button = SwitchButton('采集', '分析')
        self.rlight_lable = QtWidgets.QLabel()

        # 创建菜单。
        self.create_parts()
        self.setToolTip('功能区')
        # 设置属性。
        self.setStyleSheet('background-color:#5a5a5a')

    def create_parts(self):
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(self.margin, self.margin, self.margin, self.margin)

        # 上部标题区。
        self.title_label.setFixedHeight(int(self.height2 * 0.8))
        self.title_label.setContentsMargins(5, 0, 0, 0)
        self.title_label.setStyleSheet('background-color:#2A2A2A;color:white;font:bold 12px;')

        # 中上部图像区。
        self.img_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # self.img_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignBottom)
        self.img_label.setScaledContents(False)
        self.img_label.setPixmap(self.pixmap)

        # 中部拍照、录像控制。
        background_color = 'background-color:rgba(0,0,0,60);'
        lempty = QtWidgets.QWidget()
        lempty.setStyleSheet(background_color)
        lempty.setSizePolicy(size_policy)
        self.img_button.setObjectName('拍照')
        self.img_button.setFixedSize(self.height1, self.height1)
        self.img_button.setStyleSheet(background_color)
        self.video_button.setObjectName('录像')
        self.video_button.setFixedSize(self.height1, self.height1)
        self.video_button.setStyleSheet(background_color)
        rempty = QtWidgets.QWidget()
        rempty.setStyleSheet(background_color)
        rempty.setSizePolicy(size_policy)

        # 中下部分割线。
        separate_line = QtWidgets.QWidget()
        separate_line.setFixedHeight(2)
        separate_line.setStyleSheet('background-color:#2A2A2A')

        # 下部状态区。
        light_size = QtCore.QSize(int(self.height2 * 0.8), int(self.height2 * 0.8))
        # 硬件连接状态指示灯。
        llight_lable_pixmap = QtGui.QPixmap(r'assets\icons\gray.png')
        llight_lable_pixmap = llight_lable_pixmap.scaled(light_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.llight_lable.setPixmap(llight_lable_pixmap)
        self.llight_lable.setToolTip('硬件连接状态')
        # 播放停止按键。
        self.play_button.setFixedSize(int(self.height2 * 0.85), int(self.height2 * 0.85))
        # 信息框。
        self.msg_lable.setStyleSheet('QLabel{font:14px;color:black;border:1px solid black};')
        # self.msg_lable.setStyleSheet('QToolTip{background-color:red;color:white;border:1px solid blue}')
        self.msg_lable.setSizePolicy(size_policy)
        self.msg_lable.setText('就绪。')
        self.msg_lable.setToolTip('日志摘要')
        # 文件保持路径选择按键。
        self.folder_button.setStyleSheet("QPushButton{border-image:url('assets/icons/folder.png')};")
        self.folder_button.setFixedSize(int(self.height2 * 0.65 * 1.5), int(self.height2 * 0.65))
        self.folder_button.setToolTip('选择文件保存路径')
        # 拍照录像开关。
        self.switch_button.setToolTip('切换拍照与录像')
        # 采集分析开关。
        self.analyze_button.setToolTip('只采集或采集后分析')
        # 工作状态指示灯。
        rlight_lable_pixmap = QtGui.QPixmap(r'assets\icons\red.png')
        rlight_lable_pixmap = rlight_lable_pixmap.scaled(light_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.rlight_lable.setPixmap(rlight_lable_pixmap)
        self.rlight_lable.setToolTip('任务执行状态')

        # 中部布局。
        self.mid_layout = QtWidgets.QHBoxLayout(self.img_label)  # 完全和 self.img_label 重叠。
        self.mid_layout.setSpacing(0)
        self.mid_layout.addWidget(lempty)
        self.mid_layout.addWidget(self.img_button)
        self.mid_layout.addWidget(self.video_button)
        self.mid_layout.addWidget(rempty)
        self.video_button.hide()

        # 下部布局。
        bottom_widget = QtWidgets.QWidget()
        bottom_widget.setFixedHeight(self.height2)
        bottom_layout = QtWidgets.QHBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(1, 1, 1, 1)  # 左上右下。
        bottom_layout.addWidget(self.llight_lable)
        bottom_layout.addWidget(self.play_button)
        bottom_layout.addWidget(self.msg_lable)
        bottom_layout.addWidget(self.folder_button)
        bottom_layout.addWidget(self.switch_button)
        bottom_layout.addWidget(self.analyze_button)
        bottom_layout.addWidget(self.rlight_lable)

        # 整体布局。
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.title_label)
        layout.addWidget(self.img_label)
        # 中部拍照、录像控制区无需添加。
        layout.addWidget(separate_line)
        layout.addWidget(bottom_widget)
        self.setLayout(layout)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        # 使图像不超出 QLabel。
        w_ratio = self.pixmap.size().width() / self.img_label.size().width()
        h_ratio = self.pixmap.size().height() / self.img_label.size().height()
        # 每次都要用原图缩放。对一个图多次缩放（插值）会严重失真。
        self.pixmap = QtGui.QPixmap(self.pixpath)
        if w_ratio > h_ratio:
            self.pixmap = self.pixmap.scaledToWidth(self.img_label.width())
        else:
            self.pixmap = self.pixmap.scaledToHeight(self.img_label.height())
        self.img_label.setPixmap(self.pixmap)
        # 始终保持在 self.img_label 底部。
        self.mid_layout.setContentsMargins(0, self.img_label.height() - self.height1, 0, 0)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if a0.y() > self.height() - self.height2 * 1.5:
            return
        self.paint_flag = 1
        self.repaint()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        if a0.y() > self.height() - self.height2 * 1.5:
            return
        self.paint_flag = 0
        self.repaint()

    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter()
        painter.begin(self)
        pen_1 = QtGui.QPen(QtGui.QColor(0, 0, 0), self.margin)
        pen_2 = QtGui.QPen(QtGui.QColor(110, 110, 110), self.margin)
        if self.paint_flag == 0:
            painter.setPen(pen_2)
            painter.drawLine(0, 0, self.width(), 0)  # 上
            painter.drawLine(0, self.height(), 0, 0)  # 左
            painter.setPen(pen_1)
            painter.drawLine(self.width() - 1, 0, self.width() - 1, self.height())  # 右
            painter.drawLine(self.width(), self.height() - 1, 0, self.height() - 1)  # 下
        elif self.paint_flag == 1:
            painter.setPen(pen_1)
            painter.drawLine(0, 0, self.width(), 0)  # 上
            painter.drawLine(0, self.height(), 0, 0)  # 左
            painter.setPen(pen_2)
            painter.drawLine(self.width() - 1, 0, self.width() - 1, self.height())  # 右
            painter.drawLine(self.width(), self.height() - 1, 0, self.height() - 1)  # 下
        painter.end()

    def setText(self, text):
        self.title_label.setText(text)

    def setPixmap(self, img_path):
        # todo:应该能接收 OpenCV Mat 等类型的参数。
        self.pixpath = img_path


class SwitchButton(QtWidgets.QPushButton):
    def __init__(self, left, right, parent=None):
        super().__init__(parent)
        self.left = left
        self.right = right
        self.setCheckable(True)
        self.setMinimumWidth(51)
        self.setMinimumHeight(18)

    def paintEvent(self, event):
        label = self.right if self.isChecked() else self.left
        bg_color = QtCore.Qt.GlobalColor.green if self.isChecked() else QtCore.Qt.GlobalColor.cyan

        radius = 9
        width = 24
        center = self.rect().center()

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QtGui.QColor(0, 0, 0))

        pen = QtGui.QPen(QtCore.Qt.GlobalColor.black)
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawRoundedRect(QtCore.QRect(-width, -radius, 2 * width, 2 * radius), radius, radius)
        painter.setBrush(QtGui.QBrush(bg_color))
        sw_rect = QtCore.QRect(-radius, -radius, width + radius, 2 * radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, QtCore.Qt.AlignmentFlag.AlignCenter, label)


class PlayButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.circle_pen_width = 2  # 椭圆线的宽度，配合椭圆的半径，保证椭圆边界不出界。
        self.ratio = 0.65  # 椭圆内切圆中的三角形或正方形的外接圆半径与该内切圆半径的比值。
        self.setCheckable(True)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.paint_circle()
        if self.isChecked():
            self.paint_stop()
            self.setToolTip('点击停止')
        else:
            self.paint_play()
            self.setToolTip('点击开始')

    def paint_circle(self):
        # 按键的内切椭圆。
        # 椭圆的中心坐标和两个半轴长度。
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius_x = (self.width() - self.circle_pen_width) // 2
        radius_y = (self.height() - self.circle_pen_width) // 2
        circle = [QtCore.QPoint(center_x, center_y), radius_x, radius_y]
        # 椭圆的填充颜色。
        color = QtGui.QColor('#333333')
        pen = QtGui.QPen(color, self.circle_pen_width)
        # 画椭圆
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(pen)
        painter.drawEllipse(circle[0], circle[1], circle[2])
        painter.end()

    def paint_play(self):
        # 椭圆的两个半轴长度。
        radius_x = (self.width() - self.circle_pen_width) // 2
        radius_y = (self.height() - self.circle_pen_width) // 2
        # 椭圆内切圆的中心坐标和半径。
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = min(radius_x, radius_y) - self.circle_pen_width // 2
        radius = int(radius * self.ratio)  # 让三角形和椭圆保持一定距离。
        # 三角形的坐标。
        point1_x = int(center_x - radius // 2)
        point1_y = int(center_y - math.sqrt(3) * radius / 2.0)
        point2_x = center_x + radius
        point2_y = center_y
        point3_x = point1_x
        point3_y = int(center_y + math.sqrt(3) * radius / 2.0)
        triangle = QtGui.QPolygon([
            QtCore.QPoint(point1_x, point1_y), QtCore.QPoint(point2_x, point2_y), QtCore.QPoint(point3_x, point3_y)])
        # 三角形的填充颜色。
        color = QtGui.QColor(0, 255, 0)
        pen = QtGui.QPen(color, 1)
        brush = QtGui.QBrush(QtCore.Qt.BrushStyle.SolidPattern)
        brush.setColor(color)
        # 画三角形。
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawPolygon(triangle)
        painter.end()

    def paint_stop(self):
        # 椭圆的两个半轴长度。
        radius_x = (self.width() - self.circle_pen_width) // 2
        radius_y = (self.height() - self.circle_pen_width) // 2
        # 椭圆内切圆的中心坐标和半径。
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = min(radius_x, radius_y) - self.circle_pen_width // 2
        radius = int(radius * self.ratio)  # 让正方形和椭圆保持一定距离。
        # 正方形的半边长和坐标。
        semi_side_length = int(radius / math.sqrt(2))
        point1_x = center_x - semi_side_length
        point1_y = center_y - semi_side_length
        point2_x = center_x + semi_side_length
        point2_y = point1_y
        point3_x = point2_x
        point3_y = center_y + semi_side_length
        point4_x = point1_x
        point4_y = point3_y
        square = QtGui.QPolygon([
            QtCore.QPoint(point1_x, point1_y), QtCore.QPoint(point2_x, point2_y),
            QtCore.QPoint(point3_x, point3_y), QtCore.QPoint(point4_x, point4_y)])
        # 填充颜色。
        color = QtGui.QColor(255, 0, 0)
        pen = QtGui.QPen(color, 1)
        brush = QtGui.QBrush(QtCore.Qt.BrushStyle.SolidPattern)
        brush.setColor(color)
        # 画正方形。
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawPolygon(square)
        painter.end()


class ImgButton(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(ImgButton, self).__init__(parent)
        self.circle1_width = 0.04  # 白色圆环 1 的线条宽度占 button 边长的比例。
        self.space2_width = 0.08  # 白色圆环 1 与白色圆形 2 的间隙宽度占 button 边长的比例。
        self.circle3_radius = 0.2  # 白色圆形3 的半径占 button 边长的比例。
        self.setToolTip('点击拍照')
        self.paint_flag = 0

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.paint_flag = 1
        self.repaint()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        distance_x = abs(a0.x() - self.width() // 2)
        distance_y = abs(a0.y() - self.height() // 2)
        if distance_x > self.width() // 2 or distance_y > self.height() // 2:
            return
        self.paint_flag = 0
        self.repaint()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.paint_circle()
        inner_radius_x = 0
        inner_radius_y = 0
        if self.paint_flag == 0:
            inner_radius_x = self.width() * (0.5 - self.circle1_width - self.space2_width)
            inner_radius_y = self.height() * (0.5 - self.circle1_width - self.space2_width)
        else:
            inner_radius_x = self.width() * self.circle3_radius
            inner_radius_y = self.height() * self.circle3_radius
        self.paint_inter_circle(inner_radius_x, inner_radius_y)

    def paint_circle(self):
        center_x = self.width() // 2
        center_y = self.height() // 2
        # 1.1 白色圆环1。
        radius1_x = center_x * (1 - self.circle1_width)
        radius1_y = center_y * (1 - self.circle1_width)
        circle1 = [QtCore.QPoint(center_x, center_y), radius1_x, radius1_y]
        # 1.2 颜色。
        color1 = QtGui.QColor('#ffffff')
        pen = QtGui.QPen(color1, self.width() * self.circle1_width)
        # 1.3 画白色圆环1。
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(pen)
        painter.drawEllipse(circle1[0], circle1[1], circle1[2])
        painter.end()

    def paint_inter_circle(self, radius_x, radius_y):
        center_x = self.width() // 2
        center_y = self.height() // 2
        # 2.1 白色圆形2。
        circle2 = [QtCore.QPoint(center_x, center_y), radius_x, radius_y]
        # 2.2 颜色。
        color2 = QtGui.QColor('#ffffff')
        pen = QtGui.QPen(color2, 1)
        brush = QtGui.QBrush(QtCore.Qt.BrushStyle.SolidPattern)
        brush.setColor(color2)
        # 2.3 画白色圆形2。
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(circle2[0], circle2[1], circle2[2])
        painter.end()


class VideoButton(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(VideoButton, self).__init__(parent)
        self.circle1_width = 0.04  # 白色圆环 1 的线条宽度占 button 边长的比例。
        self.space2_width = 0.08  # 白色圆环 1 与白色圆形 2 的间隙宽度占 button 边长的比例。
        self.circle3_radius = 0.2  # 白色圆形3 的半径占 button 边长的比例。
        self.square4_len = self.circle3_radius
        self.paint_flag = 0

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.paint_flag = False if self.paint_flag else True

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.paint_circle()
        if self.paint_flag:
            self.paint_stop()
            self.setToolTip('点击停止录像')
        else:
            self.paint_play()
            self.setToolTip('点击开始录像')

    def paint_circle(self):
        center_x = self.width() // 2
        center_y = self.height() // 2
        # 1.1 白色圆环1。
        radius1_x = center_x * (1 - self.circle1_width)
        radius1_y = center_y * (1 - self.circle1_width)
        circle1 = [QtCore.QPoint(center_x, center_y), radius1_x, radius1_y]
        # 1.2 颜色。
        color1 = QtGui.QColor('#ffffff')
        pen = QtGui.QPen(color1, self.width() * self.circle1_width)
        # 1.3 画白色圆环1。
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(pen)
        painter.drawEllipse(circle1[0], circle1[1], circle1[2])
        painter.end()

    def paint_play(self):
        center_x = self.width() // 2
        center_y = self.height() // 2
        # 2.1 白色圆形2。
        radius2_x = self.width() * (0.5 - self.circle1_width - self.space2_width)
        radius2_y = self.width() * (0.5 - self.circle1_width - self.space2_width)
        circle2 = [QtCore.QPoint(center_x, center_y), radius2_x, radius2_y]
        # 2.2 颜色。
        color2 = QtGui.QColor('#ffffff')
        pen = QtGui.QPen(color2, 1)
        brush = QtGui.QBrush(QtCore.Qt.BrushStyle.SolidPattern)
        brush.setColor(color2)
        # 2.3 画白色圆形2。
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(circle2[0], circle2[1], circle2[2])
        painter.end()
        # 3.1 红色圆形3。
        radius3_x = self.width() * self.circle3_radius
        radius3_y = self.width() * self.circle3_radius
        circle3 = [QtCore.QPoint(center_x, center_y), radius3_x, radius3_y]
        # 3.2 颜色。
        color3 = QtGui.QColor('#ff0000')
        pen = QtGui.QPen(color3, 1)
        brush = QtGui.QBrush(QtCore.Qt.BrushStyle.SolidPattern)
        brush.setColor(color3)
        # 3.3 画红色圆形3。
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(circle3[0], circle3[1], circle3[2])
        painter.end()

    def paint_stop(self):
        center_x = self.width() // 2
        center_y = self.height() // 2
        # 4.1 红色正方形4。
        point1_x = center_x - int(self.width() * self.square4_len)
        point1_y = center_y - int(self.height() * self.square4_len)
        point2_x = center_x + int(self.width() * self.square4_len)
        point2_y = point1_y
        point3_x = point2_x
        point3_y = center_y + int(self.height() * self.square4_len)
        point4_x = point1_x
        point4_y = point3_y
        square = QtGui.QPolygon([
            QtCore.QPoint(point1_x, point1_y), QtCore.QPoint(point2_x, point2_y),
            QtCore.QPoint(point3_x, point3_y), QtCore.QPoint(point4_x, point4_y)])
        # 4.2 颜色。
        color4 = QtGui.QColor(255, 0, 0)
        pen = QtGui.QPen(color4, 1)
        brush = QtGui.QBrush(QtCore.Qt.BrushStyle.SolidPattern)
        brush.setColor(color4)
        # 4.3 画正方形4。
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawPolygon(square)
        painter.end()
