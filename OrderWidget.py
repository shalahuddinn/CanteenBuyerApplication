# Implement the row of a QListWidget with a custom Widget

import json
import urllib.request

from PyQt5 import QtNetwork
from PyQt5.QtCore import QUrl, QSettings, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QLabel, QTabWidget)

from HelperClass import QFramelessMessageBox, MenuItemWidget, QFramelessQuestionBox
from TabCart import TabCart
from TabDrink import TabDrink
from TabFood import TabFood
from QuestionWidget import QuestionWidget


class OrderWidget(QWidget):

    closed = pyqtSignal()
    menuLoaded = pyqtSignal()
    ordered = pyqtSignal()
    launchQuestion = pyqtSignal(str)
    launchInformation = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.foodMenuList = []
        self.drinkMenuList = []
        self.orderList = []
        self.networkAccessManager = QtNetwork.QNetworkAccessManager()

        # self.doRequestMenu()
        # self.setupUi()

    # def setupUi(self):
        # self.resize(1280, 800)
        # self.showFullScreen()
        # self.setWindowTitle('Order')

        mainLayout = QVBoxLayout()
        font = QFont('Arial', 30)

        titleLabel = QLabel('Silahkan Pilih Item Menu yang Akan Dibeli!')
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setFont(font)

        instructionLabel = QLabel()
        instructionLabel.setText("Pindah ke Tab Keranjang untuk Merubah Jumlah atau Menghapus Item.")
        instructionLabel.setAlignment(Qt.AlignCenter)


        self.tabWidget = QTabWidget()
        self.tabWidget.setStyleSheet("QTabBar::tab { height: 50px; width: 250px; }")


        mainLayout.addWidget(titleLabel)
        mainLayout.addWidget(instructionLabel)
        mainLayout.addWidget(self.tabWidget)
        cancelButton = QPushButton('Batal')
        cancelButton.clicked.connect(self.closeOrderWidget)
        mainLayout.addWidget(cancelButton)

        myBoxLayout = QHBoxLayout()
        self.tabWidget.setLayout(myBoxLayout)

        self.tabCart = TabCart()
        self.tabCart.orderButton.clicked.connect(self.proceedOrder)

        self.tabFood = TabFood()

        self.tabDrink = TabDrink()

        self.tabWidget.addTab(self.tabFood, 'Makanan')
        self.tabWidget.addTab(self.tabDrink, 'Minuman')
        self.tabWidget.addTab(self.tabCart, 'Keranjang')

        self.setLayout(mainLayout)

    def clear(self):
        self.foodMenuList.clear()
        self.drinkMenuList.clear()
        self.orderList.clear()
        self.tabFood.clearList()
        self.tabDrink.clearList()
        self.tabCart.clearList()

        self.tabWidget.setCurrentIndex(0)

    def closeOrderWidget(self):
        self.launchQuestion.emit("order")
        # reply = QFramelessQuestionBox(QMessageBox.Information, "Are you sure?")
        # reply.show()
        # reply.clicked.connect(self.XXX)
        
    def XXX(self):
        self.clear()
        self.closed.emit()

    def proceedOrder(self):
        tabCardList = self.tabCart.mylist
        for order in range(tabCardList.count()):
            temp = {}
            temp['menuID'] = tabCardList.itemWidget(tabCardList.item(order)).id
            temp['menuName'] = tabCardList.itemWidget(tabCardList.item(order)).name
            temp['price'] = tabCardList.itemWidget(tabCardList.item(order)).price
            temp['qty'] = tabCardList.itemWidget(tabCardList.item(order)).quantityItem.value()
            temp['sellerID'] = tabCardList.itemWidget(tabCardList.item(order)).sellerID
            self.orderList.append(temp)
        self.ordered.emit()


    def doRequestMenu(self):
        setting = QSettings()
        url = setting.value("baseURL", "")
        url += "/menu/"
        # url = "http://127.0.0.1:8000/api/menu/"
        req = QtNetwork.QNetworkRequest(QUrl(url))

        reply = self.networkAccessManager.get(req)
        reply.finished.connect(self.handleResponseMenu)

    def handleResponseMenu(self):
        reply = self.sender()

        er = reply.error()

        if er == QtNetwork.QNetworkReply.NoError:

            bytes_string = reply.readAll()
            data = json.loads(str(bytes_string, 'utf-8'))

            for menu in data:
                id = menu['id']
                data = urllib.request.urlopen(menu['image']).read()
                image = QPixmap()
                image.loadFromData(data)
                name = menu['name']
                price = menu['price']
                category = menu['category']
                availability = menu['availability']
                qtyAvailable = menu['qtyAvailable']
                sellerID = menu['sellerID']
                if category == "food":
                    foodMenuItem = MenuItemWidget(id, image, name, price, availability, qtyAvailable, sellerID)
                    self.foodMenuList.append(foodMenuItem)
                else:
                    drinkMenuItem = MenuItemWidget(id, image, name, price, availability,qtyAvailable, sellerID)
                    self.drinkMenuList.append(drinkMenuItem)
            self.tabFood.populateList(self.foodMenuList, self.tabCart)
            self.tabDrink.populateList(self.drinkMenuList, self.tabCart)
            self.menuLoaded.emit()

        else:
            errorMessage = "Error occured: "+ str(er) + "\n"+ str(reply.errorString())
            # QMessageBox.critical(self, "Error Menu", errorMessage)
            # window = QMessageBox()
            # messageBox = QMessageBox()
            # messageBox.setIcon(QMessageBox.Critical)
            # messageBox.setText(errorMessage)
            # messageBox.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog)
            # messageBox.exec_()
            # QFramelessMessageBox(QMessageBox.Critical, errorMessage)
            self.launchInformation.emit("order", errorMessage)
            # self.closed.emit()
            # window.exec_()
            # print("Error occured: ", er)
            # print(reply.errorString())
        reply.deleteLater()













