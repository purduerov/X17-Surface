#!/usr/bin/env python3

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

from interface import Ui_MainWindow
from ssh import controller
from streams import streams

# TODO: Refine error handling across all files


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("ROX X16")
        screen_geometry = QDesktopWidget().screenGeometry()
        screen_height = screen_geometry.height()
        screen_width = screen_geometry.width()
        self.setGeometry(0, screen_height // 2, screen_width, screen_height // 2)
        self.setMaximumSize(screen_width, screen_height // 2)
        self.setMinimumSize(screen_width, screen_height // 2)

    def closeEvent(self, event):
        confirmation = QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirmation == QMessageBox.Yes:
            streams.stop()
            controller.close()
            print("Closing application")
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    print("Starting SSH processes...")
    controller = controller()
    connection = controller.connect()

    print("Starting camera stream processes...")
    streams = streams(connection)
    streams.start()

    app = QApplication(sys.argv)
    window = MainWindow()
    print("Starting application...")
    window.show()
    app.exec()
