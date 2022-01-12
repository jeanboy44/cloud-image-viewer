from PyQt5.QtCore import QObject, pyqtSignal


class Model(QObject):
    def __init__(self):
        super().__init__()
        self._root_dir = ""
        self._current_path = ""

    root_dir_selected = pyqtSignal(str)
    current_path_selected = pyqtSignal(str)
    main_image_loaded = pyqtSignal(str)

    @property
    def root_dir(self):
        return self._root_dir

    @root_dir.setter
    def root_dir(self, value):
        self._root_dir = value
        self.root_dir_selected.emit(value)

    @property
    def current_path(self):
        return self._current_path

    @current_path.setter
    def current_path(self, value):
        self._current_path = value
        self.current_path_selected.emit(value)

    @property
    def main_image(self):
        return self._current_path

    @main_image.setter
    def main_image(self, value):
        self._main_image = value
        self.main_image_loaded.emit(value)
