from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QFileSystemModel
from PyQt5.QtGui import QImageReader

from azure.storage.blob import BlobServiceClient

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
        item = self._mdl.cloud_file_model.itemFromIndex(indices[1])
        self._mdl.current_path = item.text()

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
        self.connection_info = None

    def connect(self, connection_info=None, return_=False):
        if connection_info is None:
            connection_info = self.connection_info
        else:
            self.connection_info = connection_info

        if connection_info["type"] == "azure":
            connector = self.connect_azure_blob(
                connection_str=connection_info["connection_str"],
                container_name=connection_info["container_name"],
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
            connection_type = self.connection_info["type"]

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

    def upload(self):
        """"""

    def download(self):
        """"""

    def get_list(self):
        """"""
