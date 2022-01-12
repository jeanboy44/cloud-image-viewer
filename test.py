import sys
from PyQt5 import QtCore, QtWidgets


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        layout = QtWidgets.QGridLayout(self)
        menubar = QtWidgets.QMenuBar()
        filemenu = menubar.addMenu("MENU")
        filemenu.triggered.connect(self.actionClicked)
        filemenu.addAction("Option #1")
        filemenu.addAction("Option #2")
        layout.addWidget(menubar)

    @QtCore.pyqtSlot(QtWidgets.QAction)
    def actionClicked(self, action):
        print("Action: ", action.text())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(600, 100, 300, 100)
    window.show()
    sys.exit(app.exec_())
