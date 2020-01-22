from PyQt5.QtWidgets import QDialog, QPlainTextEdit, QVBoxLayout
from PyQt5.QtGui import QFont


class LogWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("LOG")
        self.showMaximized()

        text_edit = QPlainTextEdit()
        font = QFont("Arial", 12, QFont.Normal)
        text_edit.setFont(font)
        text = open('SELFO_LOG.log').read()
        text_edit.setPlainText(text)

        vBox = QVBoxLayout()
        vBox.addWidget(text_edit)
        self.setLayout(vBox)

