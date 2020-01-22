from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLineEdit, QPushButton, QSizePolicy, QLabel, QMessageBox)

from PaymentWidget import PaymentWidget
from HelperClass import QFramelessMessageBox, QFramelessQuestionBox


class TableNumberWidget(QWidget):
    tableNumberInserted = pyqtSignal(int)
    launchQuestion = pyqtSignal(str)
    launchInformation = pyqtSignal(str, str)
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        font = QFont('Arial', 35)
        self.lineEdit = QLineEdit()
        self.lineEdit.setAlignment(Qt.AlignCenter)
        self.lineEdit.setFont(font)
        self.lineEdit.setFocusPolicy(Qt.NoFocus)
        self.lineEdit.setReadOnly(True)

        _1Button = QPushButton('1')
        _1Button.setFont(font)
        _1Button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        _2Button = QPushButton('2')
        _2Button.setFont(font)
        _2Button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        _3Button = QPushButton('3')
        _3Button.setFont(font)
        _3Button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        _4Button = QPushButton('4')
        _4Button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        _4Button.setFont(font)
        _5Button = QPushButton('5')
        _5Button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        _5Button.setFont(font)
        _6Button = QPushButton('6')
        _6Button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        _6Button.setFont(font)
        _7Button = QPushButton('7')
        _7Button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        _7Button.setFont(font)
        _8Button = QPushButton('8')
        _8Button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        _8Button.setFont(font)
        _9Button = QPushButton('9')
        _9Button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        _9Button.setFont(font)
        _0Button = QPushButton('0')
        _0Button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        _0Button.setFont(font)
        clearButton = QPushButton('CLR')
        clearButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        clearButton.setFont(font)

        self.cancelButton = QPushButton('Batal')
        self.orderButton = QPushButton('Lanjut ke Pembayaran')



        titleLabel = QLabel('Silahkan Masukkan Nomor Meja Anda!')
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setFont(font)

        instructionLabel = QLabel()
        instructionLabel.setText("Ambil Nomor Meja Anda di Samping Mesin Ini!")
        instructionLabel.setAlignment(Qt.AlignCenter)

        layout = QGridLayout()
        layout.addWidget(titleLabel, 0, 0, 1, 4)
        layout.addWidget(instructionLabel, 1,0, 1, 4)
        layout.addWidget(self.lineEdit, 2, 0, 1, 4)
        layout.addWidget(_1Button, 3, 0)
        layout.addWidget(_2Button, 3, 1)
        layout.addWidget(_3Button, 3, 2)
        layout.addWidget(clearButton, 3, 3)
        layout.addWidget(_4Button, 4, 0)
        layout.addWidget(_5Button, 4, 1)
        layout.addWidget(_6Button, 4, 2)
        layout.addWidget(_0Button, 4, 3, 2, 1)
        layout.addWidget(_7Button, 5, 0)
        layout.addWidget(_8Button, 5, 1)
        layout.addWidget(_9Button, 5, 2)
        layout.addWidget(self.cancelButton, 6, 0)
        layout.addWidget(self.orderButton, 6, 3)

        # hbox = QHBoxLayout()
        # hbox.addStretch(1)
        # hbox.addLayout(layout)
        # hbox.addStretch(1)
        #
        # vbox = QVBoxLayout()
        # vbox.addStretch(1)
        # vbox.addLayout(hbox)
        # vbox.addStretch(1)

        self.setLayout(layout)

        _0Button.clicked.connect(lambda: self.writeDigit(0))
        _1Button.clicked.connect(lambda: self.writeDigit(1))
        _2Button.clicked.connect(lambda: self.writeDigit(2))
        _3Button.clicked.connect(lambda: self.writeDigit(3))
        _4Button.clicked.connect(lambda: self.writeDigit(4))
        _5Button.clicked.connect(lambda: self.writeDigit(5))
        _6Button.clicked.connect(lambda: self.writeDigit(6))
        _7Button.clicked.connect(lambda: self.writeDigit(7))
        _8Button.clicked.connect(lambda: self.writeDigit(8))
        _9Button.clicked.connect(lambda: self.writeDigit(9))
        clearButton.clicked.connect(self.lineEdit.clear)

        self.cancelButton.clicked.connect(self.closeTableNumberWidget)
        self.orderButton.clicked.connect(self.proceedOrder)

    def clear(self):
        self.lineEdit.clear()

    # Processing the table number input from user
    def proceedOrder(self):
        # Check whether the table number empty or not
        tableNumber = self.lineEdit.text()
        if tableNumber == "":
            # QMessageBox.critical(self, "Error Table Number", "Table Number is Empty")
            self.launchInformation.emit("table", "Nomor Meja Masih Kosong")
            # QFramelessMessageBox(QMessageBox.Critical, "Table Number is Empty")
            return
        elif int(tableNumber) > 99:
            self.launchInformation.emit("table", "Nomor Meja Salah! Maksimum: 99")
            # QFramelessMessageBox(QMessageBox.Critical, "Maximum Value: 99")
            return
        else:
            self.launchQuestion.emit("table")
            # reply = QFramelessQuestionBox(QMessageBox.Information, "Are you sure?")
            # if reply.clicked:
            #     self.tableNumberInserted.emit(int(tableNumber))
                # Add table number value to each of item in orderList
                # for item in self.orderList:
                #     item['tableNumber'] = int(tableNumber)
                    # print(self.orderList)

                # loadingWidget = PaymentWidget(self.totalPrice, self.orderList, self.mainWindow)

                # self.mainWindow.centralWidget.addWidget(loadingWidget)
                # self.mainWindow.centralWidget.setCurrentWidget(loadingWidget)

            # paymentWidget = PaymentWidget(self.totalPrice, self.orderList, self.mainWindow)
            #
            # self.mainWindow.centralWidget.addWidget(paymentWidget)
            # self.mainWindow.centralWidget.setCurrentWidget(paymentWidget)
    def sendTableNumber(self):
        tableNumber = int(self.lineEdit.text())
        self.tableNumberInserted.emit(tableNumber)

    def closeTableNumberWidget(self):
        self.clear()
        self.closed.emit()

    def writeDigit(self, digit):
        if digit in range(0, 10):
            self.lineEdit.setText(
                self.lineEdit.text() + str(digit)
            )
