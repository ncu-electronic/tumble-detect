from PyQt5 import QtWidgets		#Official Library
from toolbar import Example		#Custom Library
import sys		#Official Library





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    ex = Example()
    
    sys.exit(app.exec_())