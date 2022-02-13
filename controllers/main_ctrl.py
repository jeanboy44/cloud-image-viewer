from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QFileSystemModel
from PyQt5.QtGui import QImageReader

import os
import tempfile
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobPrefix

# from model import CloudFileModel


class MainController(QObject):
    def __init__(self, model):
        super().__init__()
        self._mdl = model
        # self.cloud_file_system_model = CloudFileModel()
        # self.cloud_file_system_model.setReadOnly(False)

        # initialize
        self.conn = Connector()
        self._on_open_app()
        self._mdl.cloud_file_model.conn = self.conn

        # listen for model event signals
        self._mdl.current_path_selected.connect(self._on_current_path_selected)
        self._mdl.cloud_current_path_selected.connect(
            self._on_cloud_current_path_selected
        )
        # self._mdl.cloud_file_model.doubleClicked.connect(self._mdl.d)
        # self._mdl.cloud_file_model.connection_name_changed.connect(
        #     self._connection_name_changed
        # )

    @pyqtSlot("QItemSelection", "QItemSelection")
    def select_current_path(self, selected, deselected):
        indices = selected.indexes()
        # print(len(indices))
        # print(indices)
        # for index in indices:
        self._mdl.current_path = self._mdl.file_system_model.filePath(indices[0])

    @pyqtSlot("QItemSelection", "QItemSelection")
    def select_cloud_current_path(self, selected, deselected):
        """select cloud current path
        index 0: name
        index 1: path
        index 2: id directory
        """
        indices = selected.indexes()
        # print(len(indices))
        # print(indices)
        # for index in indices:
        #     print(index)
        #     item = self._mdl.cloud_file_model.itemFromIndex(index)
        #     print(item.text())
        # print(self._mdl.cloud_file_model.itemFromIndex(indices[0]))
        # item = self._mdl.cloud_file_model.itemFromIndex(indices[0])
        # print(item.data())
        try:
            item = self._mdl.cloud_file_model.itemFromIndex(indices[1])

            self._mdl.cloud_current_path = item.text()
        except:
            pass

    @pyqtSlot("QModelIndex")
    def double_click_cloud_current_path(self, index):
        """select cloud current path
        index 0: name
        index 1: path
        index 2: id directory
        """
        name = self._mdl.cloud_file_model.item(index.row(), 0).text()
        path = self._mdl.cloud_file_model.item(index.row(), 1).text()
        isdir = self._mdl.cloud_file_model.item(index.row(), 2).text()
        if isdir == "True":
            self._mdl.cloud_root_dir = path
        else:
            pass

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

    @pyqtSlot(str)
    def _on_cloud_current_path_selected(self, value):
        extensions = [
            ".%s" % fmt.data().decode("ascii").lower()
            for fmt in QImageReader.supportedImageFormats()
        ]

        # if value.lower().endswith(tuple(extensions)):
        #     blob_client = self._mdl.cloud_file_model.conn.connector.get_blob_client(
        #         value
        #     )
        #     with tempfile.TemporaryFile() as fp:
        #         fp.write(blob_client.download_blob().readall())
        #     reader = QImageReader(fp.name)
        #     reader.setAutoTransform(True)
        #     self._mdl.main_image = reader.read()
        #     # fp.close()
        if value.lower().endswith(tuple(extensions)):
            TMPDIR = tempfile.TemporaryDirectory()
            path = Path(TMPDIR.name).joinpath(value).as_posix()
            print(path)
            os.makedirs(Path(path).parent, exist_ok=True)

            blob_client = self._mdl.cloud_file_model.conn.connector.get_blob_client(
                value
            )
            print(f"path:{path}")
            with open(path, mode="wb") as f:
                f.write(blob_client.download_blob().readall())
            reader = QImageReader(path)
            reader.setAutoTransform(True)
            self._mdl.main_image = reader.read()

            # TMPDIR.cleanup()

    # @pyqtSlot(str)
    # def _connection_name_changed(self, value):
    #     if self._mdl.cloud_file_model.connection_status is True:
    #         info = self._mdl.settings.accounts[value]
    #         self.conn.connect(info)

    # def test_connection(self, connection_info):
    #     try:
    #         conn = self.conn.connect(connection_info, return_=True)
    #         print("Connected Successfully")
    #         return conn.exists()
    #     except:
    #         print("Wrong connection information")
    #         return False

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            x = event.angleDelta().y() / 120
            if x > 0:
                self.scale(1.05, 1.05)
            elif x < 0:
                self.scale(0.95, 0.95)
        else:
            super().wheelEvent(event)

    # def get_container_client(self, connection_str, container_name):
    #     blob_service_client = BlobServiceClient.from_connection_string(connection_str)
    #     container_client = blob_service_client.get_container_client(container_name)

    #     return container_client

    def _on_open_app(self):
        first_account = next(iter(self._mdl.settings.accounts))
        self.conn.connect(self._mdl.settings.accounts[first_account])


# class ConfigController(QObject):
#     def __init__(self, model):
#         super().__init__()
#         self._mdl = model

#     @pyqtSlot()
#     def click_apply(self):
#         # save it to settings
#         connected = self.click_connection_test()
#         if connected is True:
#             self._mdl.settings.config.account_name = (
#                 self.ui.account_name_textedit_1.toPlainText()
#             )
#             self._mdl.settings.config.connection_str = (
#                 self.ui.connection_str_textedit_1.toPlainText()
#             )
#             self._mdl.settings.config.container_name = (
#                 self.ui.container_name_textedit_1.toPlainText()
#             )
#             self._mdl.settings.save()
#             self.ui.account_name_textedit_1.setEnabled(False)
#             self.ui.container_name_textedit_1.setEnabled(False)
#             self.ui.connection_str_textedit_1.setEnabled(False)
#             self.ui.edit_pushButton_1.setText("Edit")
#             self._mdl.current_connection = self._mctrl.get_container_client(
#                 self._mdl.settings.config.connection_str,
#                 self._mdl.settings.config.container_name,
#             )
#         else:
#             self._mdl.current_connection = None


class Connector:
    def __init__(self, type="azure"):
        self.connector = None
        self.connection_type = None
        self._connection_info = None

    @property
    def connection_info(self):
        return self._connection_info

    @connection_info.setter
    def connection_info(self, value):
        self._connection_info = value
        if value is not None:
            self.connection_type = value["type"]

    def connect(self, connection_info=None, return_=False):
        if connection_info is None:
            connection_info = self.connection_info
        else:
            self.connection_info = connection_info

        if self.connection_type == "azure":
            connector = self.connect_azure_blob(
                connection_str=self.connection_info["connection_str"],
                container_name=self.connection_info["container_name"],
            )
        else:
            connector = None

        if return_ is True:
            return connector
        else:
            self.connector = connector

    def test(self, connection_info=None):
        if connection_info is None:
            connection_info = self.connection_info
        try:
            conn = self.conn.connect(connection_info, return_=True)
            print("Connected Successfully")
            return self.check_connection(connection_info["type"])
        except:
            print("Wrong connection information")
            return False

    def check_connection(self, connection_type=None):
        if connection_type is None:
            connection_type = self.connection_type

        if connection_type == "azure":
            return self.connector.exists()
        elif connection_type == "aws":
            return False

    def test_azure_blob(self, connector):
        return connector.exists()

    def connect_azure_blob(self, connection_str, container_name):
        blob_service_client = BlobServiceClient.from_connection_string(connection_str)
        container_client = blob_service_client.get_container_client(container_name)

        return container_client

    def upload(self, src, dst):
        """"""
        if self.connection_type == "azure":
            self.connector.upload_blob(name=dst, data=src)
        elif self.connection_type == "aws":
            return False

    def download(self):
        """"""

    # def _walk_blob_hierarchy(self, prefix=""):
    #     for item in self.connector.walk_blobs(name_starts_with=prefix):
    #         if isinstance(item, BlobPrefix):
    #             self._walk_blob_hierarchy(prefix=item.name)
    #         else:
    #             yield item.name

    # def walk_blob_hierarchy(self, prefix=""):
    #     depth = 1
    #     separator = "   "
    #     for item in self.connector.walk_blobs(name_starts_with=prefix):
    #         short_name = item.name[len(prefix) :]
    #         if isinstance(item, BlobPrefix):
    #             print("F: " + separator * depth + short_name)
    #             depth += 1
    #             self.walk_blob_hierarchy(prefix=item.name)
    #             depth -= 1
    #         else:
    #             message = "B: " + separator * depth + short_name
    #             results = list(self.connector.list_blobs(name_starts_with=item.name))

    def get_list(self, path):
        """"""
        # print(f"get_list-path: {path}")
        # for item in self.connector.walk_blobs(name_starts_with=path):
        #     if isinstance(item, BlobPrefix):
        #         for item in self.connector.walk_blobs(name_starts_with=item.name):
        #             print("1")
        #             print(isinstance(item, BlobPrefix))
        #             print(type(item))
        #             print(item)
        #     else:
        #         print("2")
        #         print(isinstance(item, BlobPrefix))
        #         print(type(item))
        #         print(item)
        #     # if isinstance(item, BlobPrefix):
        #     #     print(item.name)
        #     #     self._walk_blob_hierarchy(prefix=item.name)
        #     # else:
        #     #     print(item.name)
        if self.connection_type == "azure":
            path_list = []
            isdir_list = []
            if path == "":
                for blob in self.connector.walk_blobs(name_starts_with=path):
                    path_list.append(blob.name)
                    isdir_list.append(isinstance(blob, BlobPrefix))
            else:
                for blob in self.connector.walk_blobs(name_starts_with=path):
                    for blob in self.connector.walk_blobs(name_starts_with=blob.name):
                        path_list.append(blob.name)
                        isdir_list.append(isinstance(blob, BlobPrefix))

            # path_list = [
            #     blob.name for blob in self.connector.walk_blobs(name_starts_with=path)
            # ]
            return path_list, isdir_list
        elif self.connection_type == "aws":
            return False
