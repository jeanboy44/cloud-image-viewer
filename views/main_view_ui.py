# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/main_view.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(904, 905)
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("central_widget")
        self.side_bar = QtWidgets.QTreeView(self.central_widget)
        self.side_bar.setGeometry(QtCore.QRect(-5, 1, 251, 861))
        self.side_bar.setAnimated(True)
        self.side_bar.setObjectName("side_bar")
        self.widget = QtWidgets.QWidget(self.central_widget)
        self.widget.setGeometry(QtCore.QRect(250, 0, 651, 861))
        self.widget.setObjectName("widget")
        MainWindow.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(MainWindow)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 904, 21))
        self.menu_bar.setObjectName("menu_bar")
        self.menu_file = QtWidgets.QMenu(self.menu_bar)
        self.menu_file.setObjectName("menu_file")
        self.menu_view = QtWidgets.QMenu(self.menu_bar)
        self.menu_view.setObjectName("menu_view")
        self.menu_settings = QtWidgets.QMenu(self.menu_bar)
        self.menu_settings.setObjectName("menu_settings")
        MainWindow.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(MainWindow)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)
        self.action_menu_file_open = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("file")
        self.action_menu_file_open.setIcon(icon)
        self.action_menu_file_open.setObjectName("action_menu_file_open")
        self.action_menu_file_save = QtWidgets.QAction(MainWindow)
        self.action_menu_file_save.setObjectName("action_menu_file_save")
        self.action_menu_view_main = QtWidgets.QAction(MainWindow)
        self.action_menu_view_main.setObjectName("action_menu_view_main")
        self.action_menu_view_list = QtWidgets.QAction(MainWindow)
        self.action_menu_view_list.setObjectName("action_menu_view_list")
        self.action_menu_view_grid = QtWidgets.QAction(MainWindow)
        self.action_menu_view_grid.setObjectName("action_menu_view_grid")
        self.action_menu_view_filelist = QtWidgets.QAction(MainWindow)
        self.action_menu_view_filelist.setObjectName("action_menu_view_filelist")
        self.action_menu_settings_account = QtWidgets.QAction(MainWindow)
        self.action_menu_settings_account.setObjectName("action_menu_settings_account")
        self.menu_file.addAction(self.action_menu_file_open)
        self.menu_file.addAction(self.action_menu_file_save)
        self.menu_view.addAction(self.action_menu_view_main)
        self.menu_view.addAction(self.action_menu_view_list)
        self.menu_view.addAction(self.action_menu_view_grid)
        self.menu_view.addAction(self.action_menu_view_filelist)
        self.menu_settings.addAction(self.action_menu_settings_account)
        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_view.menuAction())
        self.menu_bar.addAction(self.menu_settings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu_file.setTitle(_translate("MainWindow", "File"))
        self.menu_view.setTitle(_translate("MainWindow", "View"))
        self.menu_settings.setTitle(_translate("MainWindow", "Settings"))
        self.action_menu_file_open.setText(_translate("MainWindow", "Open"))
        self.action_menu_file_save.setText(_translate("MainWindow", "Save"))
        self.action_menu_view_main.setText(_translate("MainWindow", "main"))
        self.action_menu_view_list.setText(_translate("MainWindow", "list"))
        self.action_menu_view_grid.setText(_translate("MainWindow", "grid"))
        self.action_menu_view_filelist.setText(_translate("MainWindow", "file list"))
        self.action_menu_settings_account.setText(_translate("MainWindow", "account"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
