import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from example_ui import Ui_MainWindow


class MainView(QMainWindow):
    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._ui.label_2.setText("")
        self._ui.pushButton.clicked.connect(self.on_click_enter)
        self._ui.pushButton_2.clicked.connect(self.on_click_delete)

    def on_click_enter(self):
        current_contents = self._ui.label_2.text()
        new_contents = self._ui.textEdit.toPlainText()
        self._ui.label_2.setText(f"{current_contents}\n{new_contents}")
        self._ui.textEdit.setText("")

    def on_click_delete(self):
        self._ui.label_2.setText("")


class App(QApplication):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.main_view = MainView()
        self.main_view.show()


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec_())
