import sys, time
from PyQt5 import QtWidgets, QtGui, QtCore
from view import MainWindow


class MyWindow(QtWidgets.QWidget, MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setup_view(self)

    def closeEvent(self, event):
        msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question, 'IE Automation Kit', "是否关闭程序？",
                                       buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                       parent=self)
        msgBox.setStyleSheet("font-size:14px;font-color:white")
        msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
        msgBox.setStyleSheet("QLabel{ color: white}")
        msgBox.exec_()
        reply = msgBox.standardButton(msgBox.clickedButton())
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap(r'assets\icons\splash.png'))
    splash.showMessage("正在启动 IE Automation Kit...", QtCore.Qt.AlignmentFlag.AlignCenter, QtGui.QColor(0, 0, 0))
    splash.show()
    time.sleep(3)
    QtWidgets.qApp.processEvents()
    win = MyWindow()
    win.show()
    splash.finish(win)
    sys.exit(app.exec_())
