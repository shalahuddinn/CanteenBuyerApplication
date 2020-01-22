import json
from datetime import datetime

from PyQt5 import QtNetwork
from PyQt5.QtCore import (QByteArray, QUrl, QSettings, Qt, QCoreApplication, pyqtSignal)
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QProgressBar, QLabel, QHBoxLayout,
                             QPushButton)
from escpos.printer import File

from ReaderThread import PayCardThread, RefundCardThread
from HelperMethod import formatRupiah, get_logger


# UI for displaying the progress
class PaymentWidget(QWidget):

    finished = pyqtSignal()
    menuProblem = pyqtSignal()
    launchQuestion = pyqtSignal(str)
    launchInformation = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self.orderList = []
        self.nam = QtNetwork.QNetworkAccessManager()

        # self.setupUi()
        # self.doRequestOrder()
        self.orderID = 0
        self.orderTime = 0
        self.totalPrice = 0
        self.balance = 0
        self.cardID = 0

        self.attempt = 3
        self.cardPaymentStatus = False
        self.doRefund = False
        self.refundStatus = False
        self.serverPaymentStatus = False

    # def setupUi(self):
        self.pleaseWaitLabel = QLabel()
        self.pleaseWaitLabel.setAlignment(Qt.AlignCenter)
        self.pleaseWaitLabel.setText("Silahkan Tunggu...")
        self.messageLabel = QLabel()
        self.messageLabel.setAlignment(Qt.AlignCenter)
        self.totalPriceLabel = QLabel()
        self.totalPriceLabel.setAlignment(Qt.AlignCenter)
        self.totalPriceLabel.setText("Total Price: {}".format(formatRupiah(self.totalPrice)))
        self.balanceLabel = QLabel()
        self.balanceLabel.setAlignment(Qt.AlignCenter)
        self.balanceLabel.hide()
        self.progreessBar = QProgressBar()
        self.progreessBar.setMinimum(0)
        self.progreessBar.setMaximum(0)

        self.cancelButton = QPushButton()
        self.cancelButton.setText("Cancel")
        self.cancelButton.setMinimumSize(200, 50)
        self.cancelButton.setEnabled(False)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)

        cancelHBox = QHBoxLayout()
        cancelHBox.addStretch(1)
        cancelHBox.addWidget(self.cancelButton)
        cancelHBox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.pleaseWaitLabel)
        vbox.addWidget(self.messageLabel)
        vbox.addWidget(self.totalPriceLabel)
        vbox.addWidget(self.balanceLabel)
        vbox.addWidget(self.progreessBar)
        vbox.addLayout(cancelHBox)
        vbox.addStretch(1)

        self.mylogger = get_logger("Payment")
        self.setLayout(vbox)

    def cancelButtonClicked(self):
        self.launchQuestion.emit("payment")

    def cancelOrder(self):
        self.doRequestCancelOrder()
        self.removedCard()

    def clear(self):
        self.orderList.clear()
        self.orderID = 0
        self.orderTime = 0
        self.totalPrice = 0
        self.balance = 0
        self.cardID = 0

        self.attempt = 3
        self.cardPaymentStatus = False
        self.doRefund = False
        self.refundStatus = False
        self.serverPaymentStatus = False

        self.totalPriceLabel.setText("Total Price: {}".format(formatRupiah(self.totalPrice)))
        self.balanceLabel.hide()

    def process(self, tableNumber, totalPrice, orderList):
        self.totalPrice = totalPrice
        self.orderList = orderList
        for item in orderList:
            item['tableNumber'] = int(tableNumber)
        self.doRequestOrder()

    # Attempt to do HTTP Request for Order Model
    def doRequestOrder(self):
        # Update the Loading Text
        self.totalPriceLabel.setText("Total Price: {}".format(formatRupiah(self.totalPrice)))
        self.messageLabel.setText("Memproses Order (1/2)")
        QCoreApplication.processEvents()

        data = QByteArray()
        data.append("paymentID=0")
        data.append("&")
        data.append("amount=")
        data.append(str(self.totalPrice))
        data.append("&")
        data.append("orderStatus=placed")

        # print("DO REQUEST ORDER:")
        # print(data)
        self.mylogger.debug("Req Order: {}".format(data))

        setting = QSettings()
        url = setting.value("baseURL", "")
        url += "/order/"
        # url = "http://127.0.0.1:8000/api/order/"

        req = QtNetwork.QNetworkRequest(QUrl(url))
        req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader,
                      "application/x-www-form-urlencoded")

        reply = self.nam.post(req, data)
        reply.finished.connect(self.handleResponseOrder)

    def handleResponseOrder(self):
        reply = self.sender()
        er = reply.error()
        if er == QtNetwork.QNetworkReply.NoError:
            bytes_string = reply.readAll()
            data = json.loads(str(bytes_string, 'utf-8'))

            # print("Response Order:")
            # print(data)
            self.mylogger.debug("Resp Order: {}".format(data))

            # Get the orderID and orderTime from reply from the server
            self.orderID = data['id']
            self.orderTime = data['orderTime']
            datetime_object = datetime.strptime(self.orderTime[0:len(self.orderTime) - 6], "%Y-%m-%dT%H:%M:%S.%f")
            self.orderTime = datetime_object.strftime("%b %-d, %Y %H:%M:%S")

            # Update the Loading Text
            self.messageLabel.setText("Order (1/2) Sukses")
            QCoreApplication.processEvents()
            self.doRequestOrderDetail()
        else:
            errorMessage = "Error Order(1/2): " + str(er) + "\n" + str(reply.errorString())
            # QFramelessMessageBox(QMessageBox.Critical, errorMessage)
            self.mylogger.debug(errorMessage)
            self.launchInformation.emit("payment", errorMessage)
            # self.finished.emit()
        reply.deleteLater()

    # Attempt to do HTTP Request for Order Detail Model
    def doRequestOrderDetail(self):
        # print(self.orderList)

        # Update the Loading Text
        self.messageLabel.setText("Memproses Order (2/2)")
        QCoreApplication.processEvents()

        # Add Order ID value to each of item in orderList
        for item in self.orderList:
            item['orderID'] = str(self.orderID)

        data = QByteArray()
        data.append(json.dumps(self.orderList))

        # print("DO REQUEST ORDER DETAIL:")
        # print(data)
        self.mylogger.debug("Req OrderDetail: {}".format(data))

        setting = QSettings()
        url = setting.value("baseURL", "")
        url += "/orderdetail/"

        req = QtNetwork.QNetworkRequest(QUrl(url))
        req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader,
                      "application/json")

        reply = self.nam.post(req, data)
        reply.finished.connect(self.handleResponseOrderDetail)

    def handleResponseOrderDetail(self):
        reply = self.sender()
        er = reply.error()
        bytes_string = reply.readAll()
        data = json.loads(str(bytes_string, 'utf-8'))
        # print("Response OrderDetail:")
        # print(data)
        if er == QtNetwork.QNetworkReply.NoError:

            # print("Response Order Detail:")
            # print(data)
            self.mylogger.debug("Resp OrderDetail: {}".format(data))

            # Update the Loading Text
            self.messageLabel.setText("Order (2/2) Sukses")
            QCoreApplication.processEvents()

            # TODO Change this for real App
            # self.readingCard()
            # self.doRequestPayment()
        else:
            # Stock insufficient
            if str(er) == '302':
                errorMessage = "Maaf, Item Berikut Tidak Dapat Diproses: " + "\n"
                for item in data:
                    if item:
                        # print(item['non_field_errors'])
                        errorMessage += item['non_field_errors'][0] + "\n"
                errorMessage += "Silahkan Pesan Ulang"
                self.mylogger.debug(errorMessage)
                # TODO Change this or not?
                self.doRequestCancelOrder()
                self.launchInformation.emit("payment-menuProblem", errorMessage)
                # QFramelessMessageBox(QMessageBox.Critical, errorMessage)
                # self.menuProblem.emit()
            # Other Error
            else:
                errorMessage = "Error Order(2/2): " + str(er) + "\n" + str(reply.errorString())
                self.mylogger.debug(errorMessage)
                self.launchInformation.emit("payment", errorMessage)
                # QFramelessMessageBox(QMessageBox.Critical, errorMessage)
                # self.finished.emit()
        reply.deleteLater()

    def successReadCard(self, data):
        self.pleaseWaitLabel.hide()
        self.cardPaymentStatus = True
        self.cardID, self.balance = data
        self.mylogger.debug("Success Read Card: CardID:{} Balance:{}".format(self.cardID, self.balance))

        self.messageLabel.setText("Kartu Selesai Diproses. Silahkan Keluarkan Kartunya!")
        self.balanceLabel.setText("Saldo Akhir: {}".format(formatRupiah(self.balance)))
        QCoreApplication.processEvents()
        self.balanceLabel.show()
        # self.doRequestPayment()

    def insertedCard(self):
        self.cancelButton.setEnabled(False)
        self.pleaseWaitLabel.show()
        self.messageLabel.setText("Memproses Kartu. Jangan Keluarkan Kartunya!")
        QCoreApplication.processEvents()

    def failAuth(self):
        self.pleaseWaitLabel.hide()
        self.attempt -= 1
        self.mylogger.debug("Fail Auth: Attempt Remaining:{}".format(self.attempt))
        if self.attempt > 0:
            self.messageLabel.setText("Gagal Autentifikasi. Silahkan Keluarkan Kartunya!\n"
                                      "Kesempatan Tersisa: {}x".format(self.attempt))
            QCoreApplication.processEvents()
        else:
            self.cancelOrder()

    def failBalance(self, data):
        self.pleaseWaitLabel.hide()
        self.attempt -= 1
        balance = data
        self.mylogger.debug("Fail Balance: Attempt Remaining:{} Balance:{}".format(self.attempt, self.balance))
        if self.attempt > 0:
            self.messageLabel.setText("Saldo Tidak Cukup. Silahkan Keluarkan Kartunya!\n"
                                      "Kesempatan Tersisa: {}x".format(self.attempt))
            self.balanceLabel.setText("Sisa Saldo: {}".format(formatRupiah(balance)))
            self.balanceLabel.show()
            QCoreApplication.processEvents()
        else:
            self.cancelOrder()

    def errorCard(self):
        self.pleaseWaitLabel.hide()
        self.attempt -= 1
        self.mylogger.debug("Unexpected Removed Card: Attempt Remaining:{}".format(self.attempt))
        if self.attempt>0:
            message = "Kartu Telah Dikeluarkan Tiba-tiba. \n " \
                      "Kesempatan Tersisa: {}x".format(self.attempt)
            self.launchInformation.emit("payment-readCard", message)
        else:
            self.doRequestCancelOrder()
            self.removedCard()

    def removedCard(self):
        self.pleaseWaitLabel.hide()
        if self.cardPaymentStatus:
            if self.doRefund:
                if self.refundStatus:
                    message = "Refund Berhasil dan Pesanan Anda Telah Dibatalkan."
                    self.launchInformation.emit("payment", message)
                else:
                    message = "Refund Gagal.\n" \
                              "Hubungi Petugas Untuk Refund Dengan Menyebutkan Order ID Anda.\n" \
                              "Order ID Anda: {}".format(self.orderID)
                    self.launchInformation.emit("payment", message)
            else:
                self.doRequestPayment()
        else:
            message = "Pesanan Anda Telah Dibatalkan."
            self.launchInformation.emit("payment", message)

    def readingCard(self):
        # Update the Loading Text
        self.pleaseWaitLabel.hide()
        self.messageLabel.setText("Silahkan Masukkan Kartu Untuk Pembayaran!")
        self.balanceLabel.hide()
        self.cancelButton.setEnabled(True)
        QCoreApplication.processEvents()

        self.payCardThread = PayCardThread(self.totalPrice, self.attempt)
        self.payCardThread.failAuth.connect(self.failAuth)
        self.payCardThread.failBalance.connect(self.failBalance)
        self.payCardThread.inserted.connect(self.insertedCard)
        self.payCardThread.successRead.connect(self.successReadCard)
        self.payCardThread.removed.connect(self.removedCard)
        self.payCardThread.retry.connect(self.readingCard)
        self.payCardThread.error.connect(self.errorCard)
        # self.payCardThread.infoBalance.connect(self.infoInitialBalance)

        self.payCardThread.start()

    def infoInitialBalance(self, balance):
        self.messageLabel.setText("Saldo Awal: {}".format(formatRupiah(balance)))
        self.messageLabel.show()
        QCoreApplication.processEvents()

    def refundCard(self):
        self.mylogger.debug("Refund Card: Begin Refund".format(self.attempt))
        self.pleaseWaitLabel.hide()
        if self.attempt == 3:
            self.messageLabel.setText("Koneksi Server Bermasalah.\n"
                                      "Silahkan Masukkan Kartu Untuk Refund!")
        else:
            self.messageLabel.setText("Silahkan Masukkan Kartu Untuk Refund!")
        self.balanceLabel.hide()
        self.doRefund = True
        self.refundCardThread = RefundCardThread(self.totalPrice, self.cardID, self.attempt)

        self.refundCardThread.failAuth.connect(self.failCardId)
        self.refundCardThread.failCardId.connect(self.failCardId)
        self.refundCardThread.inserted.connect(self.insertedCard)
        self.refundCardThread.success.connect(self.successRefund)
        self.refundCardThread.removed.connect(self.removedCard)
        self.refundCardThread.retry.connect(self.refundCard)
        self.refundCardThread.error.connect(self.errorRefund)

        self.refundCardThread.start()

    def failCardId(self):
        self.pleaseWaitLabel.hide()
        self.attempt -= 1
        self.mylogger.debug("Refund Fail Auth/ID: Attempt Remaining:{}".format(self.attempt))
        if self.attempt > 0:
            self.messageLabel.setText("Kartu Berbeda dengan Kartu saat Pembayaran.\n"
                                      "Silahkan Keluarkan Kartunya!\n"
                                      "Kesempatan Tersisa: {}x".format(self.attempt))
            QCoreApplication.processEvents()
        else:
            self.removedCard()

    def errorRefund(self):
        self.pleaseWaitLabel.hide()
        self.attempt -= 1
        self.mylogger.debug("Refund Unexpected Removed Card: Attempt Remaining:{}".format(self.attempt))
        if self.attempt > 0:
            message = "Kartu Telah Dikeluarkan Tiba-tiba.\n" \
                      "Kesempatan Tersisa: {}x".format(self.attempt)
            self.launchInformation.emit("payment-doRefund", message)
            self.messageLabel.setText("Silahkan Masukkan Kartu untuk Refund!")
            QCoreApplication.processEvents()
        else:
            self.removedCard()

    def successRefund(self, balance):
        self.refundStatus = True
        self.pleaseWaitLabel.hide()
        self.mylogger.debug("Success Refund")
        self.messageLabel.setText("Refund Berhasil. Silahkan Keluarkan Kartunya!")
        self.balanceLabel.setText("Saldo Akhir: {}".format(formatRupiah(balance)))
        self.balanceLabel.show()
        QCoreApplication.processEvents()

    def doRequestPayment(self):
        # Update the Loading Text
        self.messageLabel.setText("Memproses Pembayaran. Jangan Keluarkan Kartu!")
        QCoreApplication.processEvents()

        data = QByteArray()
        data.append("cardID=")
        # TODO Change this for real app
        # data.append(self.cardID[-8:])
        # data.append("1234")
        data.append("&")
        data.append("amount=")
        data.append(str(self.totalPrice))
        data.append("&")
        data.append("orderID=")
        data.append(str(self.orderID))

        # print("DO REQUEST PAYMENT:")
        # print(data)
        self.mylogger.debug("Req Payment: {}".format(data))

        setting = QSettings()
        url = setting.value("baseURL", "")
        url += "/payment/"
        # url = "http://127.0.0.1:8000/api/order/"

        req = QtNetwork.QNetworkRequest(QUrl(url))
        req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader,
                      "application/x-www-form-urlencoded")

        reply = self.nam.post(req, data)
        reply.finished.connect(self.handleResponsePayment)

    def handleResponsePayment(self):
        reply = self.sender()
        er = reply.error()
        if er == QtNetwork.QNetworkReply.NoError:
            self.serverPaymentStatus = True
            bytes_string = reply.readAll()
            data = json.loads(str(bytes_string, 'utf-8'))

            # print("Response Payment:")
            # print(data)
            self.mylogger.debug("Resp Payment: {}".format(data))

            # Get the orderID and orderTime from reply from the server
            # self.paymentID = data['id']
            # self.paymentTime = data['time']
            # datetime_object = datetime.strptime(self.paymentTime[0:len(self.paymentTime)-6], "%Y-%m-%dT%H:%M:%S.%f")
            # self.paymentTime = datetime_object.strftime("%b %-d, %Y %H:%M:%S")

            # TODO Change this for real App
            # self.printReceipt()

            message = "Proses Pembayaran Selesai. \n" \
                      "Silahkan Tunggu Pesanan Anda di Meja Anda!\n" \
                      "Hubungi Petugas Jika Struk Tidak Keluar.\n " \
                      "Order ID Anda: {}".format(self.orderID)
            self.launchInformation.emit("payment", message)
        else:
            errorMessage = "Error Pembayaran: " + str(er) + "\n" + str(reply.errorString())
            self.mylogger.debug(errorMessage)
            self.refundCard()
        reply.deleteLater()

    # Attempt to do HTTP Request for Order Model to Cancel the Order
    def doRequestCancelOrder(self):
        # Update the Loading Text
        self.messageLabel.setText("Update Order")
        QCoreApplication.processEvents()

        temp = {'paymentID': 0, 'amount': self.totalPrice, 'orderStatus': "canceled"}

        data = QByteArray()
        data.append(json.dumps(temp))

        # print("DO REQUEST CANCEL ORDER:")
        # print(data)
        self.mylogger.debug("Req Cancel Order: {}".format(data))

        setting = QSettings()
        url = setting.value("baseURL", "")
        url += "/order/" + str(self.orderID) + "/"
        # print("URL: {}".format(url))
        # url = "http://127.0.0.1:8000/api/order/"

        req = QtNetwork.QNetworkRequest(QUrl(url))
        req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader,
                      "application/json")

        reply = self.nam.put(req, data)
        reply.finished.connect(self.handleResponseCancelOrder)

    def handleResponseCancelOrder(self):
        reply = self.sender()
        er = reply.error()

        self.messageLabel.setText("Silahkan Keluarkan Kartunya!")
        QCoreApplication.processEvents()

        if er == QtNetwork.QNetworkReply.NoError:
            bytes_string = reply.readAll()
            data = json.loads(str(bytes_string, 'utf-8'))

            # print("Response Order2:")
            # print(data)
            self.mylogger.debug("Resp Cancel Order: {}".format(data))
        else:
            errorMessage = "Error Order2: " + str(er) + "\n" + str(reply.errorString())
            self.mylogger.debug(errorMessage)
            # self.removedCard()

    def printReceipt(self):
        p = File("/dev/usb/lp0", auto_flush=False)
        # Header Receipt
        p.set(align='center', text_type='B')
        p.text("Kantin Wisuda Oktober\n")
        p.text("Institut Teknologi Bandung\n")
        p.text(self.orderTime + "\n")
        # p.text("Rabu,13/02/2019,15:30\n")
        # printTableNumber(orderList[0]['tableNumber'])
        p.text("Nomor Meja: " + str(self.orderList[0]['tableNumber']))
        p.text("\n")
        p.text("Order ID: " + str(self.orderID))
        p.text("\n\n\n")

        # Print Receipt List
        p.set(align='left')
        p.text('\x1b\x44\x00')  # reset tabulation
        p.text('\x1b\x44\x10\x19\x00')  # tabulation setting location
        for item in self.orderList:
            subTotal = item['price'] * item['qty']
            p.text(str(item['menuName']) + "\n")
            p.text(str(item['price']) + "\x09" + "x" + str(item['qty']) + "\x09" + str(subTotal) + "\n")
        p.text("--------------------------------\n\n")
        p.text("Total Belanja " + "\t" + "\t" + str(self.totalPrice))
        p.text("\n")
        p.set(align='center')
        p.text("Card ID: {}".format(self.cardID))
        p.text("\n")
        p.text("Saldo Akhir: {}".format(formatRupiah(self.balance)))
        p.text("\n\n")
        p.set(align='center')
        p.text("-TERIMAKASIH-")
        p.cut()
        p.flush()
