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
