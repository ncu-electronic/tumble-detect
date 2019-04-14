from PyQt5 import QtWidgets #Official Library
from toolbar import Example,SecondWindow #Custom Library
import sys                  #Official Library


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    s = SecondWindow()
    ex.ui.actionAbout_us.triggered.connect(s.handle_click)
    sys.exit(app.exec_())