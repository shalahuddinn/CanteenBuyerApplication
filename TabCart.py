from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QListWidget, QListWidgetItem, QScrollerProperties, QScroller, QAbstractItemView

from HelperMethod import formatRupiah
from HelperClass import ChartItemWidget
from TableNumberWidget import TableNumberWidget


class TabCart(QWidget):
    def __init__(self):
        super().__init__()
        self.totalPrice = 0

        self.vbox = QVBoxLayout()

        self.mylist = QListWidget()
        self.mylist.setStyleSheet("QListWidget::item { border-bottom: 1px solid gray; }")
        self.mylist.setFocusPolicy(Qt.NoFocus)
        self.mylist.setSelectionMode(QAbstractItemView.NoSelection)
        self.mylist.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.mylist.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.sp = QScrollerProperties()
        self.sp.setScrollMetric(QScrollerProperties.DragVelocitySmoothingFactor, 0.6)
        self.sp.setScrollMetric(QScrollerProperties.MinimumVelocity, 0.0)
        self.sp.setScrollMetric(QScrollerProperties.MaximumVelocity, 0.2)
        self.sp.setScrollMetric(QScrollerProperties.AcceleratingFlickMaximumTime, 0.1)
        self.sp.setScrollMetric(QScrollerProperties.AcceleratingFlickSpeedupFactor, 1.2)
        self.sp.setScrollMetric(QScrollerProperties.SnapPositionRatio, 0.2)
        self.sp.setScrollMetric(QScrollerProperties.MaximumClickThroughVelocity, 1)
        self.sp.setScrollMetric(QScrollerProperties.DragStartDistance, 0.001)
        self.sp.setScrollMetric(QScrollerProperties.MousePressEventDelay, 0.5)

        self.scroller = QScroller.scroller(self.mylist.viewport())
        self.scroller.setScrollerProperties(self.sp)
        self.scroller.grabGesture(self.mylist.viewport(), QScroller.LeftMouseButtonGesture)

        self.hbox = QHBoxLayout()
        self.totalLabel = QLabel("Total:")
        self.totalValueLabel = QLabel()
        self.totalValueLabel.setText(formatRupiah(0))
        self.orderButton = QPushButton('Pesan')

        self.hbox.addStretch()
        self.hbox.addWidget(self.totalLabel)
        self.hbox.addWidget(self.totalValueLabel)
        self.hbox.addStretch()

        self.vbox.addWidget(self.mylist)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.orderButton)

        self.mylist.show()
        self.setLayout(self.vbox)
        self.toggleOrderButton()

    def toggleOrderButton(self):
        if self.mylist.count() == 0:
            self.orderButton.setEnabled(False)
        else:
            self.orderButton.setEnabled(True)

    # def proceedOrder(self):
    #     self.orderList = []
    #     for order in range(self.mylist.count()):
    #         temp = {}
    #         temp['menuID'] = self.mylist.itemWidget(self.mylist.item(order)).id
    #         temp['menuName'] = self.mylist.itemWidget(self.mylist.item(order)).name
    #         temp['price'] = self.mylist.itemWidget(self.mylist.item(order)).price
    #         temp['qty'] = self.mylist.itemWidget(self.mylist.item(order)).quantityItem.value()
    #         temp['sellerID'] = self.mylist.itemWidget(self.mylist.item(order)).sellerID
    #         self.orderList.append(temp)
    #         # print(orderList)
    #     # self.loadingWindow = ProcessingWindow(self.orderList, self.totalPrice,)
    #     tableNumberWidget = TableNumberWidget(self.totalPrice, self.orderList, self.mainWindow)
    #     self.mainWindow.centralWidget.addWidget(tableNumberWidget)
    #     self.mainWindow.centralWidget.setCurrentWidget(tableNumberWidget)

    def calculateTotal(self):
        temp = 0
        for order in range(self.mylist.count()):
            # print (self.mylist.itemWidget(qlistwidgetitem).price)
            temp += self.mylist.itemWidget(self.mylist.item(order)).subTotalPrice
        self.totalValueLabel.setText(formatRupiah(temp))
        self.totalPrice = temp

    def addItem(self, item):
        buttonSender = self.sender()
        buttonSender.setEnabled(False)

        # Add to list a new item (item is simply an entry in your list)
        qListWidgetItem = QListWidgetItem(self.mylist)
        self.mylist.addItem(qListWidgetItem)

        itemNew = ChartItemWidget(item.id, item.image, item.name, item.price, item.availability, item.qty,
                                  item.sellerID)
        itemNew.removeButton.clicked.connect(lambda: self.removeFromCart(buttonSender, qListWidgetItem))

        # # Instanciate a custom widget
        # row = MenuWidget("images/logoITB128x128.png", "Ice Cream", x, True)
        qListWidgetItem.setSizeHint(itemNew.minimumSizeHint())

        # # Associate the custom widget to the list entry
        self.mylist.setItemWidget(qListWidgetItem, itemNew)
        self.mylist.itemWidget(qListWidgetItem).quantityItem.valueChanged.connect(self.calculateTotal)

        self.calculateTotal()
        self.toggleOrderButton()

    def removeFromCart(self, buttonSender, item):
        buttonSender.setEnabled(True)
        # print(row)
        self.mylist.takeItem(self.mylist.row(item))
        self.calculateTotal()
        self.toggleOrderButton()

    def clearList(self):
        self.mylist.clear()
