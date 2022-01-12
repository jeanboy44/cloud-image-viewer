from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QFileSystemModel
from PyQt5.QtGui import QImageReader

DEFAULT_OPEN_DIR_PATH = ""


class MainController(QObject):
    def __init__(self, model):
        super().__init__()
        self._mdl = model
        self.file_system_model = QFileSystemModel()
        self.file_system_model.setReadOnly(False)

        # listen for model event signals
        self._mdl.current_path_selected.connect(self._on_current_path_selected)

    @pyqtSlot()
    def open_menu_file_dialog(self):
        self._mdl.root_dir = QFileDialog.getExistingDirectory(
            None,
            "Open Directory",
            DEFAULT_OPEN_DIR_PATH,
            # QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )

    @pyqtSlot("QModelIndex")
    def select_current_path(self, index):
        self._mdl.current_path = self.file_system_model.filePath(index)

    @pyqtSlot(str)
    def _on_current_path_selected(self, value):
        extensions = [
            ".%s" % fmt.data().decode("ascii").lower()
            for fmt in QImageReader.supportedImageFormats()
        ]
        if value.lower().endswith(tuple(extensions)):
            reader = QImageReader(value)
            reader.setAutoTransform(True)
            self._mdl.main_image = reader.read()
            # self.canvas.load_pixmap(QPixmap.fromImage(image))
