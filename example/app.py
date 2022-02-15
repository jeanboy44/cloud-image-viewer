import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from example_ui import Ui_MainWindow


class MainView(QMainWindow):
    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)


class App(QApplication):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.main_view = MainView()
        self.main_view.show()


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec_())
