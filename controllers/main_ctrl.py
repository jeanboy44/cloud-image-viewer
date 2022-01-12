from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QFileSystemModel
from PyQt5.QtGui import QImageReader, QImage

DEFAULT_OPEN_DIR_PATH = ""


class MainController(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model
        self.file_system_model = QFileSystemModel()
        self.file_system_model.setReadOnly(False)

        # listen for model event signals
        self._mdl.current_path_selected.connect(self._on_current_path_selected)

    @pyqtSlot()
    def open_menu_file_dialog(self):
        self._model.root_dir = QFileDialog.getExistingDirectory(
            None,
            "Open Directory",
            DEFAULT_OPEN_DIR_PATH,
            # QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )

    @pyqtSlot("QModelIndex")
    def select_current_path(self, index):
        self._model.current_path = self.file_system_model.filePath(index)

    @pyqtSlot(str)
    def _on_current_path_selected(self, value):
        extensions = [
            ".%s" % fmt.data().decode("ascii").lower()
            for fmt in QImageReader.supportedImageFormats()
        ]
        if value.lower().endswith(tuple(extensions)):
            reader = QImageReader(value)
            reader.setAutoTransform(True)
            image_data = reader.read()
            image = QImage.fromData(self.image_data)

    # @pyqtSlot()
    # def select_file(self):


# class MainController(QObject):
#     def __init__(self, model):
#         super().__init__()

#         self._model = model

#     @pyqtSlot(int)
#     def change_amount(self, value):
#         self._model.amount = value

#         # calculate even or odd
#         self._model.even_odd = "odd" if value % 2 else "even"

#         # calculate button enabled state
#         self._model.enable_reset = True if value else False
