from PyQt5 import QtCore, QtWidgets
import os, sys
class PDF_Toolbox(Ui_MainWindow):
    pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    pdf_toolbox = PDF_Toolbox()
    pdf_toolbox.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())