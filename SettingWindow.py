# file ui_dialog.py

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import (QLabel, QPushButton, QLineEdit, QGridLayout, QDialog)


class SettingWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('Setting')

        self.baseURL = QLabel()
        self.baseURL.setText("Base API URL")
        self.baseURLLineEdit = QLineEdit()

        self.printerPort = QLabel()
        self.printerPort.setText("Printer Port")
        self.printerPortLineEdit = QLineEdit()

        self.readerPort = QLabel()
        self.readerPort.setText("Reader Port")
        self.readerPortLineEdit = QLineEdit()

        # self.portLabel = QLabel()
        # self.portLabel.setText("Port")
        # self.portLineEdit = QLineEdit()
        # self.portLineEdit.setValidator(QRegExpValidator(QRegExp("[0-9_]+")))
        #
        # self.databaseNameLabel = QLabel()
        # self.databaseNameLabel.setText("Database Name")
        # self.databaseNameLineEdit = QLineEdit()
        #
        # self.usernameLabel = QLabel()
        # self.usernameLabel.setText("Username")
        # self.usernameLineEdit = QLineEdit()
        #
        # self.passwordLabel = QLabel()
        # self.passwordLabel.setText("Password")
        # self.passwordLineEdit = QLineEdit()
        # self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        #Read settings
        setting = QSettings()
        self.baseURLLineEdit.setText(setting.value("baseURL", ""))
        self.printerPortLineEdit.setText(setting.value("printerPort"))
        self.readerPortLineEdit.setText(setting.value("readerPort"))
        # self.portLineEdit.setText(setting.value("databasePort", ""))
        # self.databaseNameLineEdit.setText(setting.value("databaseName", ""))
        # self.usernameLineEdit.setText(setting.value("databaseUsername", ""))
        # self.passwordLineEdit.setText(setting.value("databasePassword", ""))


        self.okButton = QPushButton()
        self.okButton.setText("Ok")
        self.okButton.clicked.connect(self.ok)

        layout = QGridLayout()
        layout.addWidget(self.baseURL, 0, 0)
        layout.addWidget(self.baseURLLineEdit, 0, 1)
        # layout.addWidget(self.printerPort, 1, 0)
        # layout.addWidget(self.printerPortLineEdit, 1, 1)
        # layout.addWidget(self.readerPort, 2, 0)
        # layout.addWidget(self.readerPortLineEdit, 2, 1)
        layout.addWidget(self.okButton, 3,1)
        # layout.addWidget(self.portLabel, 1, 0)
        # layout.addWidget(self.portLineEdit, 1, 1)
        # layout.addWidget(self.databaseNameLabel, 2, 0)
        # layout.addWidget(self.databaseNameLineEdit, 2, 1)
        # layout.addWidget(self.usernameLabel, 3, 0)
        # layout.addWidget(self.usernameLineEdit, 3, 1)
        # layout.addWidget(self.passwordLabel, 4, 0)
        # layout.addWidget(self.passwordLineEdit, 4, 1)
        # layout.addWidget(self.testConnectionButton, 5, 1)
        self.setLayout(layout)



    def ok(self):
        setting = QSettings()
        setting.setValue("baseURL", self.baseURLLineEdit.text())
        setting.setValue("printerPort", self.printerPortLineEdit.text())
        setting.setValue("readerPort", self.readerPortLineEdit.text())
        # setting.setValue("databasePort", self.portLineEdit.text())
        # setting.setValue("databaseName", self.databaseNameLineEdit.text())
        # setting.setValue("databaseUsername", self.usernameLineEdit.text())
        # setting.setValue("databasePassword", self.passwordLineEdit.text())
        self.close()
        # try:
        #     connection = mysql.connector.connect(host=self.hostLineEdit.text(),
        #                                          database=self.databaseNameLineEdit.text(),
        #                                          user=self.usernameLineEdit.text(),
        #                                          password=self.passwordLineEdit.text())
        #     if self.connection.is_connected():
        #         db_Info = self.connection.get_server_info()
        #         QMessageBox.Information(self, 'Connection', db_Info)
        #         print("Connected to MySQL database... MySQL Server version on ", db_Info)
        #         # self.cursor = self.connection.cursor()
        #         # self.connection.autocommit = True
        # except Error as e:
        #     QMessageBox.Warning(self, 'Connection', 'Not Connected to DB')

        # self.buttonBox.accepted.connect(self.accept)
        # self.buttonBox.rejected.connect(self.reject)
