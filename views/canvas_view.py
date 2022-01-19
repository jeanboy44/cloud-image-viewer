from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from views.main_view_ui import Ui_MainWindow
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap

from views.main_view_ui import Ui_MainWindow


class Canvas(QWidget):
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        self.main_view = QLabel(self)

        self._verticalLayout = QVBoxLayout(self)
        self._verticalLayout.addWidget(self.main_view)

    @pyqtSlot("QImage")
    def on_main_image_loaded(self, value):
        qpix_map = QPixmap.fromImage(value)
        self.main_view.setPixmap(qpix_map)
        self.main_view.setAlignment(Qt.AlignCenter)
        self.main_view.setScaledContents(True)
        # self._ui.main_view.setPixmap(qpix_map)
        # self._ui.main_view.setScaledContents(True)
