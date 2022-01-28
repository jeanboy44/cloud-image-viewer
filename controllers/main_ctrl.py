from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QFileSystemModel
from PyQt5.QtGui import QImageReader

from azure.storage.blob import BlobServiceClient


class MainController(QObject):
    def __init__(self, model):
        super().__init__()
        self._mdl = model
        self.file_system_model = QFileSystemModel()
        self.file_system_model.setReadOnly(False)
        self._connector = _Connector()

        # listen for model event signals
        self._mdl.current_path_selected.connect(self._on_current_path_selected)
        self._mdl.connection_name_changed.connect(self._connection_name_changed)

    @pyqtSlot("QItemSelection", "QItemSelection")
    def select_current_path(self, selected, deselected):
        indices = selected.indexes()
        # print(len(indices))
        # print(indices)
        # for index in indices:
        self._mdl.current_path = self.file_system_model.filePath(indices[0])

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
    def _connection_name_changed(self, value):
        if self._mdl.connection_status is True:
            info = self._mdl.settings.accounts[value]
            self._connector.connect(info)

    def test_connection(self, connection_info):
        try:
            conn = self._connector.connect(connection_info, return_=True)
            print("Connected Successfully")
            return conn.exists()
        except:
            print("Wrong connection information")
            return False

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

    def on_open_app(self):
        self._mdl.settings


class ConfigController(QObject):
    def __init__(self, model):
        super().__init__()
        self._mdl = model

    @pyqtSlot()
    def click_apply(self):
        # save it to settings
        connected = self.click_connection_test()
        if connected is True:
            self._mdl.settings.config.account_name = (
                self.ui.account_name_textedit_1.toPlainText()
            )
            self._mdl.settings.config.connection_str = (
                self.ui.connection_str_textedit_1.toPlainText()
            )
            self._mdl.settings.config.container_name = (
                self.ui.container_name_textedit_1.toPlainText()
            )
            self._mdl.settings.save()
            self.ui.account_name_textedit_1.setEnabled(False)
            self.ui.container_name_textedit_1.setEnabled(False)
            self.ui.connection_str_textedit_1.setEnabled(False)
            self.ui.edit_pushButton_1.setText("Edit")
            self._mdl.current_connection = self._mctrl.get_container_client(
                self._mdl.settings.config.connection_str,
                self._mdl.settings.config.container_name,
            )
        else:
            self._mdl.current_connection = None


class _Connector:
    def __init__(self, type="azure"):
        self.connector = None
        self.connection_info = None

    def connect(self, connection_info=None, return_=False):
        if connection_info is None:
            connection_info = self.connection_info

        if connection_info["type"] == "azure":
            connector = self.connect_azure_blob(
                connection_str=connection_info["connection_str"],
                container_name=connection_info["container_name"],
            )

        if return_ is True:
            return connector
        else:
            self.connector = connector

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
