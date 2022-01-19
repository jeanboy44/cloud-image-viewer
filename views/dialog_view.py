from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from views.settings_cloud_account_dialog_ui import Ui_MenuSettingsAccountDialog


class MenuSettingsAccountDig(QDialog):
    """Employee dialog."""

    def __init__(self, model, main_controller, parent=None):
        super(MenuSettingsAccountDig, self).__init__(parent)

        # initialize ui
        self._mdl = model
        self._mctrl = main_controller
        self.ui = Ui_MenuSettingsAccountDialog()
        self.ui.setupUi(self)

        # listen for model event signals
        self.ui.apply_pushButton_1.clicked.connect(self.click_apply)
        self.ui.connectiontest_pushButton_1.clicked.connect(self.click_connection_test)

    @pyqtSlot()
    def click_apply(self):
        # save it to settings
        self._mdl.settings.config.account_name = (
            self.ui.account_name_textedit_1.toPlainText()
        )
        self._mdl.settings.config.access_key = (
            self.ui.connection_str_textedit_1.toPlainText()
        )
        self._mdl.settings.config.container_name = (
            self.ui.container_name_textedit_1.toPlainText()
        )
        self._mdl.settings.save()

    @pyqtSlot()
    def click_connection_test(self):
        # save it to settings
        account_name = self.ui.account_name_textedit_1.toPlainText()
        connection_str = self.ui.connection_str_textedit_1.toPlainText()
        container_name = self.ui.container_name_textedit_1.toPlainText()

        print(account_name)
        print(connection_str)
        print(container_name)
        try:
            container_clinet = self._mctrl.get_container_client(
                connection_str, container_name
            )
            print(container_clinet.exists())
        except:
            print("Wrong connection information")
