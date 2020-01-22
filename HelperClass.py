from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QSpinBox, QAbstractSpinBox, QToolButton, QMainWindow, QMessageBox, QHBoxLayout, \
    QLabel, QPushButton, QVBoxLayout, QSpacerItem
from HelperMethod import formatRupiah


class MenuItemWidget(QWidget):
    def __init__(self, id, image, name, price, availability, qty, sellerID):
        super().__init__()

        self.id = id
        self.image = image
        self.name = name
        self.price = price
        self.availability = availability
        self.qty = qty
        self.sellerID = sellerID

        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(self.image)

        self.nameLabel = QLabel()
        self.nameLabel.setText(self.name)

        self.priceLabel = QLabel()
        self.priceLabel.setText(formatRupiah(price))

        self.availabilityLabel = QLabel()
        self.addToCartButton = QPushButton("Tambah ke Keranjang")

        if self.availability:
            self.availabilityLabel.setText("Tersedia")
        else:
            self.availabilityLabel.setText("Tidak Tersedia")
            self.addToCartButton.setText("Tidak Tersedia")
            self.addToCartButton.setEnabled(False)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.nameLabel)
        self.vbox.addWidget(self.availabilityLabel)
        self.vbox.addWidget(self.priceLabel)

        self.hbox = QHBoxLayout()

        self.hbox.addWidget(self.imageLabel)
        self.hbox.addLayout(self.vbox)
        self.hbox.addWidget(self.addToCartButton)

        self.setLayout(self.hbox)


class ChartItemWidget(QWidget):
    def __init__(self, id, image, name, price, availability, qty, sellerID):
        super().__init__()

        self.id = id
        self.image = image
        self.name = name
        self.price = price
        self.subTotalPrice = price
        self.availability = availability
        self.qty = qty
        self.sellerID = sellerID

        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(self.image)

        self.nameLabel = QLabel()
        self.nameLabel.setText(self.name)

        self.priceLabel = QLabel()
        self.priceLabel.setText(formatRupiah(self.price))

        # self.quantityItem = QSpinBox(minimum=1, maximum=200)
        self.quantityItem = QHSpinBox(1, self.qty)
        self.subPriceItemLabel = QLabel()
        self.subPriceItemLabel.setText(formatRupiah(self.price))
        self.quantityItem.valueChanged.connect(self.calculateSubTotal)

        self.removeButton = QPushButton()
        self.removeButton.setText("Hapus dari Keranjang")

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.nameLabel)
        self.vbox.addWidget(self.priceLabel)

        self.hbox = QHBoxLayout()
        self.hboxQty = QHBoxLayout()
        self.hboxQty.addWidget(self.subPriceItemLabel)
        self.hboxQty.addWidget(self.quantityItem)

        self.vbox2 = QVBoxLayout()
        self.vbox2.addLayout(self.hboxQty)
        self.vbox2.addWidget(self.removeButton)

        self.hbox.addWidget(self.imageLabel)
        self.hbox.addLayout(self.vbox)
        self.hbox.addLayout(self.vbox2)

        self.setLayout(self.hbox)

    def calculateSubTotal(self):
        self.subTotalPrice = self.price * self.quantityItem.value()
        self.subPriceItemLabel.setText(formatRupiah(self.subTotalPrice))


class QHSpinBox(QWidget):
    valueChanged = pyqtSignal()

    def __init__(self, minimum, maximum, parent=None):
        super(QHSpinBox, self).__init__(parent)

        # valueChanged = QtCore.pyqtSignal(int)

        # lay = QVBoxLayout(self)
        # for i in range(4):
        #     lay.addWidget(QPushButton("{}".format(i)))

        self.price_spinbox = QSpinBox(minimum=minimum, maximum=maximum)
        self.price_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.price_spinbox.setMaximumWidth(50)
        self.price_spinbox.setAlignment(Qt.AlignCenter)
        self.minButton = QToolButton()
        self.minButton.setMinimumWidth(50)
        self.minButton.setText("-")
        self.minButton.clicked.connect(self.subsValue)
        self.plusButton = QToolButton()
        self.plusButton.setMinimumWidth(50)
        self.plusButton.setText("+")
        self.plusButton.clicked.connect(self.addValue)

        # self.valueChanged = self.price_spinbox.valueChanged()

        # QtCore.pyqtSignal

        # print(self.price_spinbox.value())

        hbox = QHBoxLayout(self)
        hbox.setAlignment(Qt.AlignCenter)
        hbox.addWidget(self.minButton)
        hbox.addWidget(self.price_spinbox)
        hbox.addWidget(self.plusButton)
        # self.setLayout(hbox)

    # def valueChanged(self):
    #     return self.price_spinbox.valueChanged()
    def value(self):
        return self.price_spinbox.value()

    def addValue(self):
        self.price_spinbox.setValue(self.price_spinbox.value() + 1)
        self.valueChanged.emit()

    def subsValue(self):
        self.price_spinbox.setValue(self.price_spinbox.value() - 1)
        self.valueChanged.emit()


class QMessageDialog(QWidget):
    def __init__(self, parent=None):
        super(QMessageDialog, self).__init__(parent)

        # Source:
        # https://stackoverflow.com/questions/37918012/pyqt-give-parent-when-creating-a-widget
        # Accessed on 14 July 2019 11:58 AM
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.resize(400, 400)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.text = QLabel("HAHA")


class QFramelessMessageBox(QMainWindow):
    def __init__(self, icon, message, parent=None):
        super(QFramelessMessageBox, self).__init__(parent)

        # Source:
        # https://stackoverflow.com/questions/37918012/pyqt-give-parent-when-creating-a-widget
        # Accessed on 14 July 2019 11:58 AM
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(.5)
        self.setStyleSheet("QMainWindow { background: 'black'}")
        self.showFullScreen()

        self.dialog = QMessageBox()
        self.dialog.setIcon(icon)
        self.dialog.setText(message)
        self.dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog)
        if self.dialog.exec_():
            self.close()


# class QFramelessQuestionBox(QMainWindow):
#     def __init__(self, icon, message, parent=None):
#         super(QFramelessQuestionBox, self).__init__(parent)
#
#         # Source:
#         # https://stackoverflow.com/questions/37918012/pyqt-give-parent-when-creating-a-widget
#         # Accessed on 14 July 2019 11:58 AM
#         self.setAttribute(Qt.WA_DeleteOnClose)
#
#         self.setWindowFlags(Qt.FramelessWindowHint)
#         self.setWindowOpacity(.5)
#         self.setStyleSheet("QMainWindow { background: 'black'}")
#         self.showFullScreen()
#
#         self.dialog = QMessageBox()
#         self.dialog.setIcon(icon)
#         self.dialog.setText(message)
#         self.dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
#         self.dialog.setDefaultButton(QMessageBox.No)
#
#         self.dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog)
#         if self.dialog.exec_() == QMessageBox.Yes:
#             self.clicked = True
#             self.close()
#         else:
#             self.clicked = False
#             self.close()

class QFramelessQuestionBox(QWidget):
    clicked = pyqtSignal()

    def __init__(self, icon, message, parent=None):
        super(QFramelessQuestionBox, self).__init__(parent)

        # Source:
        # https://stackoverflow.com/questions/37918012/pyqt-give-parent-when-creating-a-widget
        # Accessed on 14 July 2019 11:58 AM
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setWindowOpacity(.5)
        # self.setStyleSheet("QMainWindow { background: 'black'}")
        self.showFullScreen()

        self.messageLabel = QLabel()
        self.messageLabel.setText(message)

        self.yesButton = QPushButton()
        self.yesButton.setText("Ya")
        self.yesButton.clicked.connect(self.YesResponse)

        self.noButton = QPushButton()
        self.noButton.setText("No")
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
        # self.exec_()

    def YesResponse(self):
        print("A")
        self.clicked.emit()
        self.close()

    def NoResponse(self):
        self.clicked = False
        self.close()


class CardRemovedUnexpectedly(Exception):
    """Raised when the card is unexpectedly discarded"""
    pass
