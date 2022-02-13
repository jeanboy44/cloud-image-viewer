import time
from pathlib import Path
from PyQt5.QtCore import pyqtSlot, QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QDialog, QFileDialog

from views.settings_cloud_account_dialog_ui import Ui_MenuSettingsAccountDialog
from views.file_upload_dialog_ui import Ui_MenuFileUploadDig
from views.file_opencloud_dialog_ui import Ui_MenuFileOpenCloudDig

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

        # set combobox
        self.connection_names = [key for key in self._mdl.settings.accounts.keys()]
        self.ui.comboBox.addItems(self.connection_names)
        self.select_connection_name()

        self.connection_types = ["azure", "aws", "gcp"]
        self.ui.comboBox_2.addItems(self.connection_types)

        # listen for model event signals
        self.ui.comboBox.currentIndexChanged.connect(self.select_connection_name)
        self.ui.comboBox_2.currentIndexChanged.connect(self.select_connection_type)
        self.ui.apply_pushButton_1.clicked.connect(self.click_apply)
        self.ui.connectiontest_pushButton_1.clicked.connect(self.click_connection_test)
        self.ui.edit_pushButton_1.clicked.connect(self.click_edit)
        self.ui.save_pushButton_1.clicked.connect(self.click_save)

    @pyqtSlot()
    def click_save(self):
        # save it to settings
        current_info = self._get_current_info()
        connection_name = self.ui.comboBox.currentText()
        self._mdl.settings.accounts[connection_name] = current_info
        self._mdl.settings.save_config()

        self.ui.comboBox_2.setEnabled(False)
        self.ui.textEdit.setEnabled(False)
        self.ui.textEdit_2.setEnabled(False)
        self.ui.textEdit_3.setEnabled(False)
        self.ui.edit_pushButton_1.setText("Edit")

    @pyqtSlot()
    def click_apply(self):
        # save it to settings
        connected = self.click_connection_test()
        self._mdl.cloud_file_model.connection_name = self.ui.comboBox.currentText()
        if connected is True:
            self._mdl.click_save()
            self._mdl.cloud_file_model.connection_status = True
        else:
            self._mdl.cloud_file_model.connection_status = False

    @pyqtSlot()
    def click_connection_test(self):
        # save it to settings
        current_info = self._get_current_info()
        test_result = self._mctrl.test_connection(current_info)
        if test_result is True:
            self.ui.account1_label1.setText("Account1 [Connected]")
        else:
            self.ui.account1_label1.setText("Account1 [Disconnected]")

    @pyqtSlot()
    def click_edit(self):
        if self.ui.edit_pushButton_1.text() == "Edit":
            self.ui.comboBox_2.setEnabled(True)
            self.ui.textEdit.setEnabled(True)
            self.ui.textEdit_2.setEnabled(True)
            self.ui.textEdit_3.setEnabled(True)
            self.ui.edit_pushButton_1.setText("Cancel")
        else:
            self._load_connection_info()
            self.ui.comboBox_2.setEnabled(False)
            self.ui.textEdit.setEnabled(False)
            self.ui.textEdit_2.setEnabled(False)
            self.ui.textEdit_3.setEnabled(False)
            self.ui.edit_pushButton_1.setText("Edit")

    @pyqtSlot()
    def select_connection_name(self):
        self.ui.account1_label1.setText(self.ui.comboBox.currentText())
        self._load_connection_info()

    @pyqtSlot()
    def select_connection_type(self):
        self._load_connection_info(include_type=False)

    def _get_current_info(self):
        current_info = {
            "type": self.ui.comboBox_2.currentText(),
            "account_name": self.ui.textEdit.toPlainText(),
            "connection_str": self.ui.textEdit_2.toPlainText(),
            "container_name": self.ui.textEdit_3.toPlainText(),
        }

        return current_info

    def _load_connection_info(self, include_type=True):
        con_info = self._mdl.settings.accounts[self.ui.comboBox.currentText()]
        key_list = [key for key in con_info.keys() if key != "type"]  #
        if include_type is True:
            self.ui.label_2.setText("type")
            self.ui.comboBox_2.setCurrentText(con_info["type"])
        self.ui.label_3.setText(key_list[0])
        self.ui.label_4.setText(key_list[1])
        self.ui.label_5.setText(key_list[2])
        self.ui.textEdit.setText(con_info[key_list[0]])
        self.ui.textEdit_2.setText(con_info[key_list[1]])
        self.ui.textEdit_3.setText(con_info[key_list[2]])


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
            connector=self._mctrl.conn,
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
        self.conn = connector
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

        # Read List of Files
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
                self.conn.upload(src=data, dst=file_path)
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


class MenuFileOpenCloudDig(QDialog):
    """Employee dialog."""

    def __init__(self, model, main_controller, parent=None):
        super(MenuFileOpenCloudDig, self).__init__(parent)

        self._cloud_root_dir = ""

        # initialize ui
        self._mdl = model
        self._mctrl = main_controller
        self.cloud_file_model = self._mdl.dialog_cloud_file_model
        self.cloud_file_model.conn = self._mctrl.conn
        self.ui = Ui_MenuFileOpenCloudDig()
        self.ui.setupUi(self)

        # connect widgets to controller
        self.ui.treeView.doubleClicked.connect(self.double_click_cloud_current_path)
        self.cloud_root_dir_selected.connect(self.on_cloud_root_dir_selected)

        self.init_widget()

    cloud_root_dir_selected = pyqtSignal(str)

    @property
    def cloud_root_dir(self):
        return self._cloud_root_dir

    @cloud_root_dir.setter
    def cloud_root_dir(self, value):
        self._cloud_root_dir = value
        self.cloud_root_dir_selected.emit(value)

    def init_widget(self):
        # listen for model event signals
        self.ui.pushButton.clicked.connect(self.click_pushButton)
        self.ui.pushButton_2.clicked.connect(self.click_pushButton_2)
        self.ui.pushButton_3.clicked.connect(self.click_pushButton_3)

    @pyqtSlot()
    def click_pushButton(self):
        """"""
        self._mdl.cloud_root_dir = self.ui.textEdit.toPlainText()
        self.close()

    @pyqtSlot()
    def click_pushButton_2(self):
        """"""
        self.close()

    @pyqtSlot()
    def click_pushButton_3(self):
        """"""
        self.cloud_root_dir = self.ui.textEdit.toPlainText()

    @pyqtSlot("QModelIndex")
    def double_click_cloud_current_path(self, index):
        """select cloud current path
        index 0: name
        index 1: path
        index 2: id directory
        """
        # print(f"index: {index}")
        # for i in range(self.cloud_file_model.rowCount()):
        #     print(i, end="/")
        #     print(self.cloud_file_model.item(i, 0).text())
        # print(f"index row: {index.row()}")

        name = self.cloud_file_model.item(index.row(), 0).text()
        path = self.cloud_file_model.item(index.row(), 1).text()
        isdir = self.cloud_file_model.item(index.row(), 2).text()
        self.ui.textEdit.setText(path)
        if isdir == "True":
            self.cloud_root_dir = path
        else:
            pass

    @pyqtSlot(str)
    def on_cloud_root_dir_selected(self, value):
        print(value)
        self.cloud_file_model.clear()
        self.cloud_file_model.list_dir(value, only_dir=True)
        self.ui.treeView.setModel(self.cloud_file_model)
        self.ui.treeView.show()
        # selmodel = dialog.ui.treeView.selectionModel()
        # selmodel.selectionChanged.connect(
        #     self._mctrl.select_cloud_current_path
        # )
