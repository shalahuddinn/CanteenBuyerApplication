from PyQt5.QtGui import QPixmap, QKeySequence
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QSpacerItem, QShortcut
from PyQt5.QtCore import Qt

from OrderWidget import OrderWidget
from SettingWindow import SettingWindow
from LogWindow import LogWindow
from HelperMethod import get_logger

class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Shortcut to open Setting Window
        self.shortcut = QShortcut(QKeySequence("Ctrl+I"), self)
        self.shortcut.activated.connect(self.openSettingWindow)

        self.shortcut2 = QShortcut(QKeySequence("CTRL+L"), self)
        self.shortcut2.activated.connect(self.openLogWindow)

        self.setupUi()

    def setupUi(self):
        self.showFullScreen()

        # #Move screen to the center
        # qtRectangle = self.frameGeometry()
        # centerPoint = QDesktopWidget().availableGeometry().center()
        # qtRectangle.moveCenter(centerPoint)
        # self.move(qtRectangle.topLeft())

        logoLabel = QLabel()
        logoPixmap = QPixmap("images/logo.png")
        logoLabel.setPixmap(logoPixmap)
        logoLabel.setFixedSize(logoPixmap.width(), logoPixmap.height())

        logoHBoxLayout = QHBoxLayout()
        logoHBoxLayout.addStretch(1)
        logoHBoxLayout.addWidget(logoLabel)
        logoHBoxLayout.addStretch(1)

        titleLabel = QLabel()
        titleLabel.setText("Name")
        titleLabel.setAlignment(Qt.AlignCenter)

        memberTeamLabel = QLabel()
        memberTeamLabel.setText("Author​")
        memberTeamLabel.setAlignment(Qt.AlignCenter)



        # titleHBoxLayout = QHBoxLayout()
        # titleHBoxLayout.addStretch(1)
        # titleHBoxLayout.addWidget(titleLabel)
        # titleHBoxLayout.addStretch(1)

        self.orderButton = QPushButton("Mulai Pesan")
        self.orderButton.setMinimumSize(200, 50)
        # font = self.orderButton.font()
        # font.setPointSize(16)
        # self.orderButton.setFont(font)
        # self.orderButton.clicked.connect(self.openOrderWindow)

        orderHBoxLayout = QHBoxLayout()
        orderHBoxLayout.addStretch(1)
        orderHBoxLayout.addWidget(self.orderButton)
        orderHBoxLayout.addStretch(1)

        qspacer = QSpacerItem(0, 25)

        vBoxLayout = QVBoxLayout()
        vBoxLayout.addStretch(1)
        vBoxLayout.addLayout(logoHBoxLayout)
        vBoxLayout.addItem(qspacer)
        vBoxLayout.addWidget(titleLabel)
        vBoxLayout.addWidget(memberTeamLabel)
        vBoxLayout.addItem(qspacer)
        vBoxLayout.addLayout(orderHBoxLayout)
        vBoxLayout.addStretch(1)

        self.setLayout(vBoxLayout)

    def openLogWindow(self):
        logWindow = LogWindow()
        logWindow.exec_()

    def openSettingWindow(self):

        preferenceWindow = SettingWindow()
        preferenceWindow.exec_()

    # def openOrderWindow(self):
    #     orderWidget = OrderWidget(self.mainWindow)
    #     self.mainWindow.centralWidget.addWidget(orderWidget)
    #     self.mainWindow.centralWidget.setCurrentWidget(orderWidget)
