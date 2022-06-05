from PyQt5 import QtWidgets


class Controller:
    def __init__(self, view):
        super(Controller, self).__init__()
        self.view = view

    @staticmethod
    def select_dir(caller):
        print('-- caller:', caller)
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选择文件保存路径", ".")
        if not directory:
            return

    @staticmethod
    def open_dir():
        import os
        os.system(r'explorer .')

    def switch_camera(self, caller):
        menus = [self.view.menu_1, self.view.menu_2, self.view.menu_3, self.view.menu_4]
        img_button = menus[caller - 1].img_label.findChild(QtWidgets.QLabel, '拍照')
        vid_button = menus[caller - 1].img_label.findChild(QtWidgets.QLabel, '录像')
        if img_button.isHidden():
            img_button.show()
            vid_button.hide()
        else:
            img_button.hide()
            vid_button.show()
