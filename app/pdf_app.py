from PyQt5 import QtCore, QtWidgets
import os, sys

from pdf_toolbox_ui import Ui_MainWindow


class PDF_Toolbox(Ui_MainWindow):
    def __init__(self,parent=None):
        super(PDF_Toolbox, self).__init__()
        # init


    def setupUi(self, MainWindow):
        # Father's UI
        Ui_MainWindow.setupUi(self, MainWindow)
        # Menu
        self.actionQuit.triggered.connect(on_Action_quit)
        #

def on_Action_quit():
    sys.exit(0)
    pass
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    pdf_toolbox = PDF_Toolbox()
    pdf_toolbox.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())