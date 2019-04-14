import sys, time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QTimer

class App(QWidget):
 
    def __init__(self):
        
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        self.init_timer()
        
    def init_timer(self):
        
        self.q_timer = QTimer()
        self.q_timer.timeout.connect(self.refresh_img)
        self.q_timer.start(300)
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        # Create widget
        self.label = QLabel(self)
        pixmap = QPixmap('/home/upsquared/workspace/tensorflow/tf-pose-estimation/previous_ver/src/img_for_push.png')
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height()) 
        self.show()

    def refresh_img(self):
        
        self.label.setPixmap(QPixmap('/home/upsquared/workspace/tensorflow/tf-pose-estimation/previous_ver/src/img_for_push.png'))

        time.sleep(1)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    
    sys.exit(app.exec_())
