import sys

from PyQt5.QtWidgets import QApplication

from gui.main_controller import Application


def main():
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    app.exec_()
    # some comments


if __name__ == '__main__':
    main()
