import yaml
from pathlib import Path

# from easydict import EasyDict as edict
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QFileSystemModel
from PyQt5.QtCore import Qt

CONFIG_PATH = "config.yml"


class Model(QObject):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.file_system_model = QFileSystemModel()
        self.file_system_model.setReadOnly(False)
        self.cloud_file_model = CloudFileModel()
        # self.cloud_file_model.setReadOnly(False)

        self._root_dir = ""
        self._cloud_root_dir = ""
        self._current_path = ""
        self._main_image = None

    root_dir_selected = pyqtSignal(str)
    cloud_root_dir_selected = pyqtSignal(str)
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
    def cloud_root_dir(self):
        return self._cloud_root_dir

    @cloud_root_dir.setter
    def cloud_root_dir(self, value):
        self._cloud_root_dir = value
        self.cloud_root_dir_selected.emit(value)

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


class CloudFileModel(QStandardItemModel):
    """
    사용자 데이터 모델 설정
    [{"type":str, "objects":[str, ...]}, ...]
    위의 데이터 형식을 이용하여 서브 아이템을 가지는 모델을 생성
    """

    def __init__(self):
        super().__init__()
        self._connection_name = None
        self._connection_status = False

    connection_name_changed = pyqtSignal(str)
    connection_status_changed = pyqtSignal(bool)

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

    @pyqtSlot()
    def listdir(self, dir):
        list_files = self._listdir(dir)
        self._append_data(list_files)

    def setRootPath(self, dir):
        self.removeRows(0, self.rowCount())

    # def _listdir(self, dir):
    #     list_files = []
    #     for path in Path(dir).glob("*"):
    #         f_ = {
    #             "path": path.as_posix(),
    #             "name": path.name,
    #             "isfile": str(path.is_file()),
    #         }
    #         list_files.append(f_)

    #     return list_files

    def _listdir(self, dir):
        print(self.connection_status)
        if self.connection_status is True:
            list_files = []
            for path in Path(dir).glob("*"):
                f_ = {
                    "path": path.as_posix(),
                    "name": path.name,
                    "isfile": str(path.is_file()),
                }
                list_files.append(f_)

            return list_files
        else:
            return []

    def _append_data(self, data, root=None):
        root = self.invisibleRootItem()
        for d in data:
            root.appendRow(
                [
                    QStandardItem(d["path"]),
                    QStandardItem(d["name"]),
                    QStandardItem(d["isfile"]),
                ]
            )

        # self.setRowCount(0)
        # if root is None:
        #     root = self.invisibleRootItem()
        # seen = {}
        # values = deque(data)
        # while values:
        #     value = values.popleft()
        #     if value["level"] == 0:
        #         parent = root
        #     else:
        #         pid = value["parent_ID"]
        #         if pid not in seen:
        #             values.append(value)
        #             continue
        #         parent = seen[pid]
        #     dbid = value["dbID"]
        #     parent.appendRow(
        #         [
        #             QStandardItem(value["short_name"]),
        #             QStandardItem(str(dbid)),
        #         ]
        #     )
        #     seen[dbid] = parent.child(parent.rowCount() - 1)
