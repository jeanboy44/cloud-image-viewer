import yaml
from easydict import EasyDict as edict
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QImage


class Model(QObject):
    def __init__(self):
        super().__init__()
        self.settings = Settings()

        self._root_dir = ""
        self._current_path = ""
        self._main_image = None

    root_dir_selected = pyqtSignal(str)
    current_path_selected = pyqtSignal(str)
    main_image_loaded = pyqtSignal(QImage)

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
        return self._main_image

    @main_image.setter
    def main_image(self, value):
        self._main_image = value
        self.main_image_loaded.emit(value)


class Settings(QObject):
    def __init__(self):
        super().__init__()
        try:
            with open("config.yml") as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)
        except:
            self.initialize()
            with open("config.yml") as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)

        self.config = edict(self.config)

        print(self.config)

    def initialize(self):
        config = edict({})
        config.name = "cloud-image_viewer"
        config.account_name = ""
        config.connection_str = ""
        config.container_name = ""
        with open("config.yml", mode="w", encoding="utf8") as f:
            yaml.dump(self.edict2dict(config), f, sort_keys=True)

    def edict2dict(self, edict_obj):
        dict_obj = {}

        for key, vals in edict_obj.items():
            if isinstance(vals, edict):
                dict_obj[key] = self.edict2dict(vals)
            else:
                dict_obj[key] = vals

        return dict_obj

    def save(self):
        with open("config.yml", mode="w", encoding="utf8") as f:
            yaml.dump(self.edict2dict(self.config), f, sort_keys=True)
