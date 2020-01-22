from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, \
    QLabel, QPushButton, QVBoxLayout, QSpacerItem


class InformationWidget(QWidget):
    okClicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.sender = ""

        self.messageLabel = QLabel()
        # self.messageLabel.setText("Apakah Anda Yakin?")
        self.messageLabel.setAlignment(Qt.AlignCenter)

        self.okButton = QPushButton()
        self.okButton.setText("Ok")
        self.okButton.clicked.connect(self.okResponse)

        qspacer = QSpacerItem(0, 25)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        hbox.addStretch()
        hbox.addWidget(self.okButton)
        hbox.addStretch()

        vbox.addStretch()
        vbox.addWidget(self.messageLabel)
        vbox.addItem(qspacer)
        vbox.addLayout(hbox)
        vbox.addStretch()
        self.setLayout(vbox)

    def setSender(self, sender):
        self.sender = sender

    def setMessage(self, message):
        self.messageLabel.setText(message)

    def okResponse(self):
        self.okClicked.emit(self.sender)
