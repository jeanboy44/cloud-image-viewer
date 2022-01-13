from PyQt5.QtCore import pyqtSlot
from views.main_view_ui import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap


class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()

        # initialize ui
        self._mdl = model
        self._mctrl = main_controller
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        # set model to side bar
        self._ui.side_bar.setModel(self._mctrl.file_system_model)

        # connect widgets to controller
        self._ui.action_menu_file_open.triggered.connect(
            self._mctrl.open_menu_file_dialog
        )
        side_bar_selmodel = self._ui.side_bar.selectionModel()
        side_bar_selmodel.selectionChanged.connect(self._mctrl.select_current_path)
        # self._ui.side_bar.clicked.connect(self._mctrl.select_current_path)

        # listen for model event signals
        self._mdl.root_dir_selected.connect(self.on_root_dir_selected)
        self._mdl.main_image_loaded.connect(self.on_main_image_loaded)

    @pyqtSlot(str)
    def on_root_dir_selected(self, value):
        if value != "":
            root = self._mctrl.file_system_model.setRootPath(value)
            self._ui.side_bar.setModel(self._mctrl.file_system_model)
            self._ui.side_bar.setRootIndex(root)
            self._ui.side_bar.show()

    @pyqtSlot("QImage")
    def on_main_image_loaded(self, value):
        qpix_map = QPixmap.fromImage(value)
        self._ui.main_viewer.setPixmap(qpix_map)
