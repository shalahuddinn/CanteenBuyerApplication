#Main Program

import sys

from PyQt5.QtWidgets import QApplication

from MainWindow import MainWindow

if __name__ == '__main__':
    qApplication = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    qApplication.exec_()
