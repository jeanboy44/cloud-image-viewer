from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt, QObject
from PyQt5.QtWidgets import QMainWindow, QScrollArea, QFileDialog, QDialog
from PyQt5.QtGui import QPixmap

from views.main_view_ui import Ui_MainWindow
from views.dialog_view import MenuSettingsAccountDig, MenuFileUploadDig
from views.canvas_view import Canvas

DEFAULT_OPEN_DIR_PATH = ""


class MainView(QMainWindow):
    def __init__(self, model, main_controller, parent=None):
        super(MainView, self).__init__(parent)

        # set the title of main window
        self.setWindowTitle("Cloud Image Viewer")

        # set the size of window
        self.Width = 800
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)

        # initialize ui
        self._mdl = model
        self._mctrl = main_controller
        # self._mctrl.menu = MenuController(self)
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        # add custom ui
        self._ui.canvas = Canvas()
        del self._ui.scrollAreaWidgetContents_2
        self._ui.scrollArea.setWidget(self._ui.canvas)

        # connect widgets to controller
        self._ui.side_bar.doubleClicked.connect(
            self._mctrl.double_click_cloud_current_path
        )

        self._ui.action_menu_file_open.triggered.connect(self.click_file_open)
        self._ui.action_menu_file_open_cloud.triggered.connect(
            self.click_file_open_cloud
        )
        self._ui.action_menu_file_upload.triggered.connect(self.click_file_upload)
        self._ui.action_menu_settings_account.triggered.connect(
            self.click_settings_account
        )

        # listen for model event signals
        self._mdl.root_dir_selected.connect(self.on_root_dir_selected)
        self._mdl.cloud_root_dir_selected.connect(self.on_cloud_root_dir_selected)
        self._mdl.main_image_loaded.connect(self._ui.canvas.on_main_image_loaded)

    @pyqtSlot(str)
    def on_root_dir_selected(self, value):
        if value != "":
            root = self._mdl.file_system_model.setRootPath(value)
            self._ui.side_bar.setModel(self._mdl.file_system_model)
            side_bar_selmodel = self._ui.side_bar.selectionModel()
            side_bar_selmodel.selectionChanged.connect(self._mctrl.select_current_path)
            self._ui.side_bar.setRootIndex(root)
            self._ui.side_bar.show()

    @pyqtSlot(str)
    def on_cloud_root_dir_selected(self, value):
        print(value)
        self._mdl.cloud_file_model.clear()
        self._mdl.cloud_file_model.list_dir(value)
        self._ui.side_bar.setModel(self._mdl.cloud_file_model)
        side_bar_selmodel = self._ui.side_bar.selectionModel()
        side_bar_selmodel.selectionChanged.connect(
            self._mctrl.select_cloud_current_path
        )
        self._ui.side_bar.show()

    def wheelEvent(self, event):
        print("wheel")
        print(f"{event.angleDelta().x()}, {event.angleDelta().y()}")

    @pyqtSlot()
    def click_file_open(self):
        self._mdl.root_dir = QFileDialog.getExistingDirectory(
            None,
            "Open Directory",
            DEFAULT_OPEN_DIR_PATH,
            # QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )

    @pyqtSlot()
    def click_file_open_cloud(self):
        self._mdl.cloud_root_dir = QFileDialog.getExistingDirectory(
            None,
            "Open Directory",
            DEFAULT_OPEN_DIR_PATH,
            # QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )

    @pyqtSlot()
    def click_settings_account(self):
        dialog = MenuSettingsAccountDig(self._mdl, self._mctrl)
        dialog.exec()

    @pyqtSlot()
    def click_file_upload(self):
        dialog = MenuFileUploadDig(self._mdl, self._mctrl)
        dialog.exec()
