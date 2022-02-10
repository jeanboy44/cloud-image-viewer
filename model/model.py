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
    """ """

    def __init__(self):
        super().__init__()
        self.conn = None
        self.current_dir = None

    # @pyqtSlot()
    # def list_dir(self, dir):
    #     self.current_dir = dir
    #     list_files = self._listdir(dir)
    #     self._append_data(list_files)

    @pyqtSlot()
    def list_dir(self, dir):
        # dir = obj.item.text()
        self.current_dir = dir
        list_files = self._listdir(dir)
        self._append_data(list_files)

    @pyqtSlot()
    def clear(self):
        self.removeRows(0, self.rowCount())

    def _listdir(self, dir):
        print(f"_listdir: dir: {dir}")
        # if self.conn.check_connection() is True:
        #     yield {
        #             "name": "..",
        #             "path": Path(self.current_dir).parent.as_posix(),
        #             "isdir": str(True),
        #         }

        # paths = self.conn.get_list(dir)
        # for path in paths:
        #     path = Path(path)
        #     f_ = {
        #         "name": path.name,
        #         "path": path.as_posix(),
        #         "isdir": str(path.is_dir()),
        #     }
        #     list_files.append(f_)

        # return list_files

        if self.conn.check_connection() is True:
            parent_dir = Path(self.current_dir).parent.as_posix()
            if parent_dir == ".":
                parent_dir = ""
            list_files = [
                {
                    "name": "..",
                    "path": parent_dir,
                    "isdir": str(True),
                }
            ]
            paths, isdirs = self.conn.get_list(dir)
            for i, path in enumerate(paths):
                path = Path(path)
                f_ = {
                    "name": path.name,
                    "path": path.as_posix(),
                    "isdir": str(isdirs[i]),
                }
                list_files.append(f_)

            return list_files
        else:
            return []

    # def _listdir(self, dir):
    #     if self.conn.check_connection() is True:
    #         list_files = [
    #             {
    #                 "name": "..",
    #                 "path": Path(self.current_dir).parent.as_posix(),
    #                 "isdir": str(True),
    #             }
    #         ]
    #         for path in Path(dir).glob("*"):
    #             f_ = {
    #                 "name": path.name,
    #                 "path": path.as_posix(),
    #                 "isdir": str(path.is_dir()),
    #             }
    #             list_files.append(f_)

    #         return list_files
    #     else:
    #         return []

    def _append_data(self, data, dir=None):
        """
        dir (QStandardItem): directory to open
        """
        if dir is None:
            dir = self.invisibleRootItem()
        for d in data:
            dir.appendRow(
                [
                    QStandardItem(d["name"]),
                    QStandardItem(d["path"]),
                    QStandardItem(d["isdir"]),
                ]
            )

    # def double_clicked(self, index):
    #     item = self.model().item(index.row(), index.column())
    #     strData = item.data(0).toPyObject()
    #     # self.treeMedia.currentIndex()
    #     print("" + str(strData))

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
