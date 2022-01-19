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

        # listen for model event signals
        self._mdl.current_path_selected.connect(self._on_current_path_selected)

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

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            x = event.angleDelta().y() / 120
            if x > 0:
                self.scale(1.05, 1.05)
            elif x < 0:
                self.scale(0.95, 0.95)
        else:
            super().wheelEvent(event)

    def get_container_client(self, connection_str, container_name):
        blob_service_client = BlobServiceClient.from_connection_string(connection_str)
        container_client = blob_service_client.get_container_client(container_name)

        return container_client
