import time
from pathlib import Path
from PyQt5.QtCore import pyqtSlot, QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QDialog, QFileDialog

from views.settings_cloud_account_dialog_ui import Ui_MenuSettingsAccountDialog
from views.file_upload_dialog_ui import Ui_MenuFileUploadDig

DEFAULT_OPEN_DIR_PATH = ""

# class ThreadClass(QThread):
#     def __init__(self, parent = None):
#         super(ThreadClass,self).__init__(parent)
#     def run(self):
#         #~~~~~


class MenuSettingsAccountDig(QDialog):
    """Employee dialog."""

    def __init__(self, model, main_controller, parent=None):
        super(MenuSettingsAccountDig, self).__init__(parent)

        # initialize ui
        self._mdl = model
        self._mctrl = main_controller
        self.ui = Ui_MenuSettingsAccountDialog()
        self.ui.setupUi(self)

        self.thread = QThread(self)

        # listen for model event signals
        self.ui.apply_pushButton_1.clicked.connect(self.click_apply)
        self.ui.connectiontest_pushButton_1.clicked.connect(self.click_connection_test)
        self.ui.edit_pushButton_1.clicked.connect(self.click_edit)

        # initialize settigns
        self.initialize()

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

    @pyqtSlot()
    def click_connection_test(self):
        # save it to settings
        account_name = self.ui.account_name_textedit_1.toPlainText()
        connection_str = self.ui.connection_str_textedit_1.toPlainText()
        container_name = self.ui.container_name_textedit_1.toPlainText()
        try:
            container_client = self._mctrl.get_container_client(
                connection_str, container_name
            )
            self.ui.account1_label1.setText("Account1 [Connected]")
            return container_client.exists()
        except:
            self.ui.account1_label1.setText("Account1 [Disconnected]")
            print("Wrong connection information")
            return False

    @pyqtSlot()
    def click_edit(self):
        if self.ui.edit_pushButton_1.text() == "Edit":
            self.ui.account_name_textedit_1.setEnabled(True)
            self.ui.container_name_textedit_1.setEnabled(True)
            self.ui.connection_str_textedit_1.setEnabled(True)
            self.ui.edit_pushButton_1.setText("Cancel")
        else:
            self.ui.account_name_textedit_1.setText(
                self._mdl.settings.config.account_name
            )
            self.ui.container_name_textedit_1.setText(
                self._mdl.settings.config.container_name
            )
            self.ui.connection_str_textedit_1.setText(
                self._mdl.settings.config.connection_str
            )
            self.ui.account_name_textedit_1.setEnabled(False)
            self.ui.container_name_textedit_1.setEnabled(False)
            self.ui.connection_str_textedit_1.setEnabled(False)
            self.ui.edit_pushButton_1.setText("Edit")

    def initialize(self):
        self.ui.account_name_textedit_1.setText(self._mdl.settings.config.account_name)
        self.ui.container_name_textedit_1.setText(
            self._mdl.settings.config.container_name
        )
        self.ui.connection_str_textedit_1.setText(
            self._mdl.settings.config.connection_str
        )
        self.click_apply()


class MenuFileUploadDig(QDialog):
    """Employee dialog."""

    def __init__(self, model, main_controller, parent=None):
        super(MenuFileUploadDig, self).__init__(parent)

        # initialize ui
        self._mdl = model
        self._mctrl = main_controller
        self.ui = Ui_MenuFileUploadDig()
        self.ui.setupUi(self)

        self.uploader = FileUploader(
            local_root_dir=self.ui.textEdit.toPlainText(),
            cloud_root_dir=self.ui.textEdit_2.toPlainText(),
            connector=self._mdl.current_connection,
        )

        self.init_widget()

    def init_widget(self):
        # listen for model event signals
        self.ui.pushButton.clicked.connect(self.click_pushButton)
        self.ui.pushButton_2.clicked.connect(self.click_pushButton_2)
        self.ui.pushButton_3.clicked.connect(self.click_pushButton_3)

        self.ui.progressBar.setValue(0)
        self.uploader.progress_.connect(self.ui.progressBar.setValue)
        self.uploader.progress_max.connect(self.ui.progressBar.setMaximum)

    @pyqtSlot()
    def click_pushButton(self):
        local_dir = QFileDialog.getExistingDirectory(
            None,
            "Open Directory",
            DEFAULT_OPEN_DIR_PATH,
            # QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )
        self.ui.textEdit.setText(local_dir)

    @pyqtSlot()
    def click_pushButton_2(self):
        self.uploader.local_root_dir = self.ui.textEdit.toPlainText()
        self.uploader.cloud_root_dir = self.ui.textEdit_2.toPlainText()

        if self.ui.pushButton_2.text() == "Paused":
            self.ui.pushButton_2.setText("Resume")
            self.uploader.pause()
        else:
            self.ui.pushButton_2.setText("Paused")
            """Upload files in local directory to blob"""
            self.uploader.resume()
            self.uploader.start()

    @pyqtSlot()
    def click_pushButton_3(self):
        self.uploader.cancel()
        self.uploader.stop()


class FileUploader(QThread):
    progress_ = pyqtSignal(int)
    progress_max = pyqtSignal(int)

    def __init__(self, local_root_dir, cloud_root_dir, connector, parent=None):
        super(FileUploader, self).__init__(parent)
        self._local_root_dir = local_root_dir
        self._cloud_root_dir = cloud_root_dir
        self._status = "canceled"  # running, canceled, paused
        self._file_list = None
        self.connector = connector
        self.threadactive = False

    @property
    def local_root_dir(self):
        return self._local_root_dir

    @local_root_dir.setter
    def local_root_dir(self, value):
        self._local_root_dir = value

    @property
    def cloud_root_dir(self):
        return self._cloud_root_dir

    @cloud_root_dir.setter
    def cloud_root_dir(self, value):
        self._cloud_root_dir = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    def run(self):
        """Upload files in local directory to blob"""
        self.threadactive = True

        # Read List of Blobs
        if self._file_list is None:
            self._file_list = []
            for path in Path(self.local_root_dir).rglob("*"):
                if Path(path).is_file():
                    self._file_list.append(path)
            self.progress_max.emit(len(self._file_list))

        # Upload
        for i, path in enumerate(self._file_list):
            file = Path(path).relative_to(self.local_root_dir)
            file_path = Path(self.cloud_root_dir).joinpath(file).as_posix()
            with open(path, "rb") as data:
                self.connector.upload_blob(name=file_path, data=data)
            self.progress_.emit(i + 1)

            while self.status == "paused":
                time.sleep(0)

            if self.status == "canceled":
                self.progress_.emit(0)
                break

    def resume(self):
        self.status = "running"

    def pause(self):
        self.status = "paused"

    def cancel(self):
        self.status = "canceled"

    def stop(self):
        # self.power = False
        # self.quit()
        # self.wait(2000)
        self.threadactive = False
        self.wait(2000)


# class MenuOpenRemoteDialog(QDialog):
