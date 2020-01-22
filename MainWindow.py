# Main File
# Control the Widget Flow

from PyQt5.Qt import QApplication
from PyQt5.QtCore import QCoreApplication, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QStackedWidget

from HomeWidget import HomeWidget
from LodingWidget import LoadingWidget
from OrderWidget import OrderWidget
from TableNumberWidget import TableNumberWidget
from PaymentWidget import PaymentWidget
from QuestionWidget import QuestionWidget
from InformationWidget import InformationWidget


class MainWindow(QMainWindow):

    Home = 0
    Loading = 1
    Order = 2
    Table = 3
    Payment = 4
    Question = 5
    Information = 6

    def __init__(self):
        super().__init__()

        #Init QSetting
        QCoreApplication.setOrganizationName("YOUR_ORGANIZATION_NAME")
        QCoreApplication.setOrganizationDomain("YOUR_ORGANIZATION_DOMAIN")
        QCoreApplication.setApplicationName("YOUR_APPLICATION_NAME")
        QApplication.setGlobalStrut(QSize(0,50))
        font = QFont("Arial", 25, QFont.Normal)
        QApplication.setFont(font)

        self.showFullScreen()
        # self.resize(900, 700)

        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)

        self.homeWidget = HomeWidget()
        self.loadingWidget = LoadingWidget()
        self.orderWidget = OrderWidget()
        self.tableNumberWidget = TableNumberWidget()
        self.paymentWidget = PaymentWidget()
        self.questionWidget = QuestionWidget()
        self.informationWidget = InformationWidget()

        self.setupNavigation()

    def setupNavigation(self):
        self.centralWidget.addWidget(self.homeWidget)
        self.centralWidget.addWidget(self.loadingWidget)
        self.centralWidget.addWidget(self.orderWidget)
        self.centralWidget.addWidget(self.tableNumberWidget)
        self.centralWidget.addWidget(self.paymentWidget)
        self.centralWidget.addWidget(self.questionWidget)
        self.centralWidget.addWidget(self.informationWidget)

        self.centralWidget.setCurrentIndex(0)

        self.homeWidget.orderButton.clicked.connect(self.goToLoading)

        self.orderWidget.menuLoaded.connect(self.goToOrder)
        self.orderWidget.launchQuestion.connect(self.goToQuestion)
        self.orderWidget.closed.connect(self.goToHome)
        self.orderWidget.ordered.connect(self.goToTableNumber)
        self.orderWidget.launchInformation.connect(self.goToInformation)

        self.tableNumberWidget.closed.connect(self.goToOrder)
        self.tableNumberWidget.tableNumberInserted.connect(self.goToPayment)
        self.tableNumberWidget.launchQuestion.connect(self.goToQuestion)
        self.tableNumberWidget.launchInformation.connect(self.goToInformation)

        self.paymentWidget.menuProblem.connect(self.backToOrder)
        self.paymentWidget.finished.connect(self.goToHome)
        self.paymentWidget.launchInformation.connect(self.goToInformation)
        self.paymentWidget.launchQuestion.connect(self.goToQuestion)

        self.questionWidget.yesClicked.connect(self.responseYesQuestion)
        self.questionWidget.noClicked.connect(self.responseNoQuestion)

        self.informationWidget.okClicked.connect(self.responseOkInformation)

    def goToQuestion(self, sender):
        self.centralWidget.setCurrentIndex(self.Question)
        self.questionWidget.setSender(sender)

    def responseYesQuestion(self, sender):
        if sender == "order":
            self.goToHome()
        elif sender == "table":
            self.tableNumberWidget.sendTableNumber()
        elif sender == "payment":
            self.centralWidget.setCurrentIndex(self.Payment)
            self.paymentWidget.cancelOrder()

    def responseNoQuestion(self, sender):
        if sender == "order":
            self.goToOrder()
        elif sender == "table":
            self.goToTableNumber()
        elif sender == "payment":
            self.centralWidget.setCurrentIndex(self.Payment)

    def goToInformation(self, sender, message):
        self.informationWidget.setSender(sender)
        self.informationWidget.setMessage(message)
        self.centralWidget.setCurrentIndex(self.Information)

    def responseOkInformation(self, sender):
        if sender == "order":
            self.goToHome()
        elif sender == "table":
            self.goToTableNumber()
        elif sender == "payment":
            self.goToHome()
        elif sender == "payment-menuProblem":
            self.backToOrder()
        elif sender == "payment-readCard":
            self.centralWidget.setCurrentIndex(self.Payment)
            self.paymentWidget.readingCard()
        elif sender == "payment-doRefund":
            self.centralWidget.setCurrentIndex(self.Payment)
            self.paymentWidget.refundCard()

    def goToLoading(self):
        self.centralWidget.setCurrentIndex(self.Loading)
        self.orderWidget.doRequestMenu()

    def goToOrder(self):
        self.centralWidget.setCurrentIndex(self.Order)

    def goToTableNumber(self):
        self.centralWidget.setCurrentIndex(self.Table)

    def goToPayment(self, tableNumber):
        self.centralWidget.setCurrentIndex(self.Payment)
        self.paymentWidget.process(tableNumber, self.orderWidget.tabCart.totalPrice, self.orderWidget.orderList)

    def goToHome(self):
        self.clearAllWidget()
        self.centralWidget.setCurrentIndex(self.Home)

    def backToOrder(self):
        self.clearAllWidget()
        self.goToLoading()

    def clearAllWidget(self):
        self.orderWidget.clear()
        self.tableNumberWidget.clear()
        self.paymentWidget.clear()



