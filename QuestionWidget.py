from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, \
    QLabel, QPushButton, QVBoxLayout, QSpacerItem


class QuestionWidget(QWidget):
    yesClicked = pyqtSignal(str)
    noClicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.sender = ""

        self.messageLabel = QLabel()
        self.messageLabel.setText("Apakah Anda Yakin?")
        self.messageLabel.setAlignment(Qt.AlignCenter)

        self.yesButton = QPushButton()
        self.yesButton.setText("Ya")
        self.yesButton.clicked.connect(self.YesResponse)

        self.noButton = QPushButton()
        self.noButton.setText("Tidak")
        self.noButton.clicked.connect(self.NoResponse)

        qspacer = QSpacerItem(0, 25)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        hbox.addStretch()
        hbox.addWidget(self.yesButton)
        hbox.addWidget(self.noButton)
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

    def YesResponse(self):
        self.yesClicked.emit(self.sender)

    def NoResponse(self):
        self.noClicked.emit(self.sender)
