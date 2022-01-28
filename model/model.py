import yaml

# from easydict import EasyDict as edict
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QImage, QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt

CONFIG_PATH = "config.yml"


class Model(QObject):
    def __init__(self):
        super().__init__()
        self.settings = Settings()

        self._root_dir = ""
        self._current_path = ""
        self._main_image = None
        self._connection_name = None
        self._connection_status = False

    root_dir_selected = pyqtSignal(str)
    current_path_selected = pyqtSignal(str)
    main_image_loaded = pyqtSignal(QImage)
    connection_name_changed = pyqtSignal(str)
    connection_status_changed = pyqtSignal(bool)

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

    @property
    def connection_name(self):
        return self._connection_name

    @connection_name.setter
    def connection_name(self, value):
        self._connection_name = value
        self.connection_name_changed.emit(value)

    @property
    def connection_status(self):
        return self._connection_status

    @connection_status.setter
    def connection_status(self, value):
        self._connection_status = value
        self.connection_status_changed.emit(value)


class Settings(QObject):
    def __init__(self):
        super().__init__()
        self.name = "cloud-image_viewer"
        self.accounts = {
            "azure_connection1": {
                "type": "azure",
                "account_name": "",
                "connection_str": "",
                "container_name": "",
            },
            "aws_connection1": {
                "type": "aws",
                "access_key": "",
                "secret_access_key": "",
                "bucket_name": "",
            },
        }
        self.load_config()

    def load_config(self):
        """"""
        try:
            with open(CONFIG_PATH) as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
            self.name = config["name"]
            self.accounts = config["accounts"]

        except:
            self.save_config()

    def save_config(self):
        """"""
        config = {
            "name": self.name,
            "accounts": self.accounts,
        }
        with open(CONFIG_PATH, mode="w", encoding="utf8") as f:
            yaml.dump(config, f, sort_keys=False)


# class CloudFileModel(QStandardItemModel):
#     """
#     사용자 데이터 모델 설정
#     [{"type":str, "objects":[str, ...]}, ...]
#     위의 데이터 형식을 이용하여 서브 아이템을 가지는 모델을 생성
#     """

#     def __init__(self, data):
#         QStandardItemModel.__init__(self)

#         d = data[0]  # Fruit
#         item = QStandardItem(d["type"])
#         child = QStandardItem(d["objects"][0])  # Apple
#         item.appendRow(child)
#         child = QStandardItem(d["objects"][1])  # Banana
#         item.appendRow(child)
#         self.setItem(0, 0, item)

#         d = data[1]  # Vegetable
#         item = QStandardItem(d["type"])
#         child = QStandardItem(d["objects"][0])  # Carrot
#         item.appendRow(child)
#         child = QStandardItem(d["objects"][1])  # Tomato
#         item.appendRow(child)
#         self.setItem(1, 0, item)

#         # for 문을 이용해서 작성했을 경우
#         for j, _type in enumerate(data):
#             item = QStandardItem(_type["type"])
#             for obj in _type["objects"]:
#                 child = QStandardItem(obj)
#                 item.appendRow(child)
#             self.setItem(j, 0, item)

#     def select_folder(self):


#     # def query
