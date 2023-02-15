from PyQt5 import QtCore, QtWidgets, QtGui
import os, sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from pdf_toolbox_ui import Ui_MainWindow


class PDF_Toolbox(Ui_MainWindow):
    def __init__(self):
        super(PDF_Toolbox, self).__init__()
        # init all flags and containers
        self.strict_flag = False
        self.files_list = []
        self.edit_metadata_flag = False
        self.metadata_dict = {'Author': '',
                              'Creator': '',
                              'Producer': '',
                              'Subject': '',
                              'Title': ''}
        self.crypt_flag = False
        self.enter_pw = ''
        self.confirm_pw = ''
        # TextwithHF,TextwithoutHF,Annotation(all),Annotation(text),Annotation(highlights)
        self.extract_flags_list = [False, False, False, False, False]
        self.merge_file_list = []
        self.stamp_flag = True
        self.stamp_file = ''
        # Remove duplication,Lossless compression,Remove images(all)
        self.reduce_flags_list = [True, True, False]
        self.droplist_files = DropList()

    def setupUi(self, MainWindow):
        # Father's UI
        Ui_MainWindow.setupUi(self, MainWindow)
        # Menu
        self.actionQuit.triggered.connect(on_Action_quit)
        # Push Buttons
        self.pushButton_files.clicked.connect(self.on_pushButton_files_clicked)
        self.pushButton_extract.clicked.connect(self.on_pushButton_extract_clicked)
        self.pushButton_merge.clicked.connect(self.on_pushButton_merge_clicked)
        self.pushButton_sandm.clicked.connect(self.on_pushButton_sandm_clicked)
        self.pushButton_add.clicked.connect(self.on_pushButton_add_clicked)
        self.pushButton_reduce.clicked.connect(self.on_pushButton_reduce_clicked)
        # Radio Buttons
        self.radioButton_stamp.clicked.connect(self.on_radioButton_stamp_clicked)
        self.radioButton_watermark.clicked.connect(self.on_radioButton_watermark_clicked)
        # Checkbox
        self.checkBox_strict.clicked.connect(self.on_checkBox_strict_clicked)
        self.groupBox_metadata.clicked.connect(self.on_groupBox_metadata_clicked)
        self.groupBox_crypt.clicked.connect(self.on_groupBox_crypt_clicked)
        self.checkBox_textwith.clicked.connect(self.on_checkBox_textwith_clicked)
        self.checkBox_textwithout.clicked.connect(self.on_checkBox_textwithout_clicked)
        self.checkBox_annall.clicked.connect(self.on_checkBox_annall_clicked)
        self.checkBox_anntext.clicked.connect(self.on_checkBox_anntext_clicked)
        self.checkBox_annhighlights.clicked.connect(self.on_checkBox_annhighlights_clicked)
        self.checkBox_rmduplication.clicked.connect(self.on_checkBox_checkBox_rmduplication_clicked)
        self.checkBox_lossless.clicked.connect(self.on_checkBox_lossless_clicked)
        self.checkBox_rmimages.clicked.connect(self.on_checkBox_rmimages_clicked)
        # List Widgets
        # Attention: After replace with a new widget, be sure the old one deleted
        self.droplist_files.setObjectName("dropList_files")
        self.horizontalLayout_4.replaceWidget(self.listWidget_files, self.droplist_files)
        self.listWidget_files.deleteLater()

    def on_pushButton_files_clicked(self):
        file_name, file_type = QtWidgets.QFileDialog.getOpenFileNames()
        print('AAAAAA')


    def on_pushButton_extract_clicked(self):
        print('on_pushButton_extract_clicked')

    def on_pushButton_merge_clicked(self):
        print('on_pushButton_merge_clicked')

    def on_pushButton_sandm_clicked(self):
        print('on_pushButton_sandm_clicked')

    def on_pushButton_add_clicked(self):
        print('on_pushButton_add_clicked')

    def on_pushButton_reduce_clicked(self):
        print('on_pushButton_reduce_clicked')

    def on_radioButton_stamp_clicked(self):
        self.stamp_flag = self.radioButton_stamp.isChecked()
        print(self.stamp_flag)

    def on_radioButton_watermark_clicked(self):
        self.stamp_flag = not self.radioButton_watermark.isChecked()
        print(self.stamp_flag)

    def on_checkBox_strict_clicked(self):
        self.strict_flag = self.checkBox_strict.isChecked()

    def on_groupBox_metadata_clicked(self):
        self.edit_metadata_flag = self.groupBox_metadata.isChecked()

    def on_groupBox_crypt_clicked(self):
        self.crypt_flag = self.groupBox_crypt.isChecked()

    def on_checkBox_textwith_clicked(self):
        self.extract_flags_list[0] = self.checkBox_textwith.isChecked()

    def on_checkBox_textwithout_clicked(self):
        self.extract_flags_list[1] = self.checkBox_textwithout.isChecked()

    def on_checkBox_annall_clicked(self):
        self.extract_flags_list[2] = self.checkBox_annall.isChecked()

    def on_checkBox_anntext_clicked(self):
        self.extract_flags_list[3] = self.checkBox_anntext.isChecked()

    def on_checkBox_annhighlights_clicked(self):
        self.extract_flags_list[4] = self.checkBox_annhighlights.isChecked()

    def on_checkBox_checkBox_rmduplication_clicked(self):
        self.reduce_flags_list[0] = self.checkBox_rmduplication.isChecked()

    def on_checkBox_lossless_clicked(self):
        self.reduce_flags_list[1] = self.checkBox_lossless.isChecked()

    def on_checkBox_rmimages_clicked(self):
        self.reduce_flags_list[2] = self.checkBox_rmimages.isChecked()


def on_Action_quit():
    sys.exit()


# Define DropList from QtWidgets.QListWidget
class DropList(QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setAlternatingRowColors(True)
        self.is_internal = False
        self.is_dragging = False
        self.drag_item = None
        self.itemPressed.connect(self.on_itemPressed)

    def on_itemPressed(self,item:QtWidgets.QListWidgetItem):
        # 注意：使用这个原因是pos和posF方法会有偏移
        print('on_itemPressed')
        self.drag_item = item

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        print('dragEnterEvent-1')
        if self.is_dragging:
            # 当前如果是正在拖拽状态那么之久不作任何处理
            event.accept()
            return
        # 当前未进入拖拽状态（第一次触发）
        # 判断抓的是外部文件还是内部的item
        if event.mimeData().hasUrls():
            # 有链接 那么是外部文件
            self.is_internal = False
        else:
            # 没有连接 那么是内部文件
            self.is_internal = True
            # 需要修正pos的偏移
            row = self.indexAt(event.pos()).row()
            self.removeItemWidget(self.drag_item)
            print('Drop up, Row:', row)
            print('Drag item:',QtWidgets.QListWidgetItem(self.drag_item).text())
        event.accept()
        self.is_dragging = True
        print('dragEnterEvent-2')

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent) -> None:
        event.accept()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        print('dropEvent-1')
        if not self.is_internal:
            added_files_list = event.mimeData().text().split('\n')
            if added_files_list[-1] == '':
                added_files_list.pop()
            for file in added_files_list:
                if is_PDF(file):
                    item = QtWidgets.QListWidgetItem()
                    file_name = os.path.basename(file)
                    item.setText(file_name)
                    item.setWhatsThis(file)
                    self.addItem(item)
                    print(item.text())
                    print(item.whatsThis())
        else:
            row = self.indexAt(event.pos()).row()
            print('Drop down, Row:', row)
            print('Drag item:',QtWidgets.QListWidgetItem(self.drag_item).text())
            self.insertItem(row,QtWidgets.QListWidgetItem(self.drag_item))
        # 重置所有参数
        self.drag_item = None
        self.is_internal = False
        self.is_dragging = False
        event.accept()
        print('dropEvent-2')


def is_PDF(file):
    return os.path.splitext(file)[-1][1:].lower() == 'pdf'

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    pdf_toolbox = PDF_Toolbox()
    pdf_toolbox.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
