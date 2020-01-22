from PyQt5.QtWidgets import QLabel, QVBoxLayout, QProgressBar, QWidget, QHBoxLayout, QSpacerItem


class LoadingWidget(QWidget):
    def __init__(self):
        super().__init__()
        titleLabel = QLabel()
        titleLabel.setText("Loading....")


        titleHBoxLayout = QHBoxLayout()
        titleHBoxLayout.addStretch(1)
        titleHBoxLayout.addWidget(titleLabel)
        titleHBoxLayout.addStretch(1)

        progressBar = QProgressBar()
        progressBar.setMinimum(0)
        progressBar.setMaximum(0)

        orderHBoxLayout = QHBoxLayout()
        orderHBoxLayout.addStretch(1)
        orderHBoxLayout.addWidget(progressBar)
        orderHBoxLayout.addStretch(1)

        qspacer = QSpacerItem(0, 25)

        vBoxLayout = QVBoxLayout()
        vBoxLayout.addStretch(1)
        vBoxLayout.addLayout(titleHBoxLayout)
        vBoxLayout.addItem(qspacer)
        vBoxLayout.addLayout(orderHBoxLayout)
        vBoxLayout.addStretch(1)

        self.setLayout(vBoxLayout)

    # def openOrderWindow(self):
    #     orderWidget = OrderWidget(self.mainWindow)
    #     self.mainWindow.centralWidget.addWidget(orderWidget)
    #     self.mainWindow.centralWidget.setCurrentWidget(orderWidget)
