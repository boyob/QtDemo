import sys, math
from PyQt5 import QtWidgets, QtCore, QtGui


class ImgButton(QtWidgets.QWidget):
    def __init__(self):
        super(ImgButton, self).__init__()
        self.circle1_width = 0.04  # 白色圆环 1 的线条宽度占 button 边长的比例。
        self.space2_width = 0.08  # 白色圆环 1 与白色圆形 2 的间隙宽度占 button 边长的比例。
        self.circle3_radius = 0.2  # 白色圆形3 的半径占 button 边长的比例。
        self.resize(400, 400)
        self.setToolTip('点击拍照')
        self.paint_flag = 0
        self.setStyleSheet('background-color:rgba(0,0,0,60)')

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        distance_x = abs(a0.x() - self.width() // 2)
        distance_y = abs(a0.y() - self.height() // 2)
        if distance_x > self.width() // 2 or distance_y > self.height() // 2:
            return
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


class VideoButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.circle1_width = 0.04  # 白色圆环 1 的线条宽度占 button 边长的比例。
        self.space2_width = 0.08  # 白色圆环 1 与白色圆形 2 的间隙宽度占 button 边长的比例。
        self.circle3_radius = 0.2  # 白色圆形3 的半径占 button 边长的比例。
        self.square4_len = self.circle3_radius
        self.resize(400, 400)
        self.setCheckable(True)
        self.setStyleSheet('background-color:rgba(0,255,0,25)')

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.paint_circle()
        if self.isChecked():
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # window = ImgButton()
    window = VideoButton()
    window.show()
    sys.exit(app.exec())
