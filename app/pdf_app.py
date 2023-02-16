from PyQt5 import QtCore, QtWidgets, QtGui
import os, sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QMessageBox

from pdf_toolbox_ui import Ui_MainWindow

from PyPDF2 import PdfReader,PdfWriter, PdfMerger

import urllib.parse


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
        # TextwithHF,TextwithoutHF,Annotation(all),Annotation(text),Annotation(highlights)
        self.extract_flags_list = [False, False, False, False, False]
        self.merge_file_list = []
        self.stamp_flag = True
        self.stamp_file = ''
        # Remove duplication,Lossless compression,Remove images(all)
        self.reduce_flags_list = [True, True, False]
        self.droplist_files = DropList(forbid_external=False)
        self.droplist_merge = DropList(forbid_external=True)

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
        self.droplist_merge.setObjectName("dropList_merge")
        self.horizontalLayout_2.replaceWidget(self.listWidget_merge,self.droplist_merge)
        self.listWidget_merge.deleteLater()
        # Tab
        self.droplist_files.drop_external_over_signal.connect(self.on_droplist_files_drop_external_over_signal)

    def on_droplist_files_drop_external_over_signal(self):
        self.update_merge_items()

    def on_pushButton_files_clicked(self):
        files_dialog = QtWidgets.QFileDialog()
        files_list, file_type = files_dialog.getOpenFileNames(filter="PDF Files (*.pdf)")
        self.droplist_files.clear()
        if files_list.__len__() != 0:
            for file in files_list:
                item = QtWidgets.QListWidgetItem()
                file_name = os.path.basename(file)
                item.setText(file_name)
                item.setWhatsThis(file)
                self.droplist_files.addItem(item)
            self.update_merge_items()

    def on_pushButton_extract_clicked(self):
        print("---------Extract Start---------")
        print("Text(with HF):\t{0}\n"
              "Text(without HF):\t{1}\n"
              "Annotation(all):\t{2}\n"
              "Annotation(text):\t{3}\n"
              "Annotation(highlights):\t{4}\n"
              .format(self.extract_flags_list[0]
                      ,self.extract_flags_list[1]
                      ,self.extract_flags_list[2]
                      ,self.extract_flags_list[3]
                      ,self.extract_flags_list[4]))
        output_dir = self.get_output_dir()
        if self.extract_flags_list[0]:
            for row in range(self.droplist_files.count()):
                file_path = self.droplist_files.item(row).whatsThis()
                file_name_base = os.path.splitext(os.path.basename(file_path))[0]
                reader = PdfReader(file_path,strict=self.strict_flag)
                with open (output_dir+'/'+file_name_base+'_extract_Text(with HF).txt','w',encoding='utf-8') as f:
                    for page_num in range(len(reader.pages)):
                        page = reader.pages[page_num]
                        f.write('Page {0}:\n'.format(page_num+1))
                        f.write(page.extract_text())
                        f.write('\n')
                    f.close()
        if self.extract_flags_list[1]:
            for row in range(self.droplist_files.count()):
                file_path = self.droplist_files.item(row).whatsThis()
                file_name_base = os.path.splitext(os.path.basename(file_path))[0]
                reader = PdfReader(file_path,strict=self.strict_flag)
                with open (output_dir+'/'+file_name_base+'_extract_Text(without HF).txt','w',encoding='utf-8') as f:
                    for page_num in range(len(reader.pages)):
                        page = reader.pages[page_num]
                        parts = []
                        def visitor_body(text, cm, tm, fontDict, fontSize):
                            y = tm[5]
                            if y > 50 and y < 720:
                                parts.append(text)
                        page.extract_text(visitor_text=visitor_body)
                        text_body = "".join(parts)
                        f.write('Page {0}:\n'.format(page_num+1))
                        f.write(text_body)
                        f.write('\n')
                    f.close()
        if self.extract_flags_list[2]:
            for row in range(self.droplist_files.count()):
                file_path = self.droplist_files.item(row).whatsThis()
                file_name_base = os.path.splitext(os.path.basename(file_path))[0]
                reader = PdfReader(file_path,strict=self.strict_flag)
                with open (output_dir+'/'+file_name_base+'_extract_Annotation(all).txt','w',encoding='utf-8') as f:
                    for page_num in range(len(reader.pages)):
                        page = reader.pages[page_num]
                        f.write('Page {0}:\n'.format(page_num+1))
                        if "/Annots" in page:
                            for annot in page["/Annots"]:
                                obj = annot.get_object()
                                subtype = obj["/Subtype"]
                                annotation = 'None'
                                if subtype == "/Text":
                                    annotation = {"subtype": obj["/Subtype"], "location": obj["/Rect"], "Contents": obj["/Contents"]}
                                elif subtype == "/Highlight":
                                    annotation = {"subtype": obj["/Subtype"], "location": obj["/Rect"], "QuadPoints": obj["/QuadPoints"]}
                                else:
                                    pass
                                f.write(str(annotation))
                                f.write('\n')
                    f.close()
        if self.extract_flags_list[3]:
            for row in range(self.droplist_files.count()):
                file_path = self.droplist_files.item(row).whatsThis()
                file_name_base = os.path.splitext(os.path.basename(file_path))[0]
                reader = PdfReader(file_path,strict=self.strict_flag)
                with open (output_dir+'/'+file_name_base+'_extract_Annotation(text).txt','w',encoding='utf-8') as f:
                    for page_num in range(len(reader.pages)):
                        page = reader.pages[page_num]
                        f.write('Page {0}:\n'.format(page_num+1))
                        if "/Annots" in page:
                            for annot in page["/Annots"]:
                                obj = annot.get_object()
                                subtype = obj["/Subtype"]
                                annotation = 'None'
                                if subtype == "/Text":
                                    annotation = {"subtype": obj["/Subtype"], "location": obj["/Rect"], "Contents": obj["/Contents"]}
                                else:
                                    pass
                                f.write(str(annotation))
                                f.write('\n')
                    f.close()
        if self.extract_flags_list[4]:
            for row in range(self.droplist_files.count()):
                file_path = self.droplist_files.item(row).whatsThis()
                file_name_base = os.path.splitext(os.path.basename(file_path))[0]
                reader = PdfReader(file_path,strict=self.strict_flag)
                with open (output_dir+'/'+file_name_base+'_extract_Annotation(highlights).txt','w',encoding='utf-8') as f:
                    for page_num in range(len(reader.pages)):
                        page = reader.pages[page_num]
                        f.write('Page {0}:\n'.format(page_num+1))
                        if "/Annots" in page:
                            for annot in page["/Annots"]:
                                obj = annot.get_object()
                                subtype = obj["/Subtype"]
                                annotation = 'None'
                                if subtype == "/Highlight":
                                    annotation = {"subtype": obj["/Subtype"], "location": obj["/Rect"], "QuadPoints": obj["/QuadPoints"]}
                                else:
                                    pass
                                f.write(str(annotation))
                                f.write('\n')
                    f.close()
        print("---------Extract Over---------")

    def on_pushButton_merge_clicked(self):
        print("---------Merge Start---------")
        file_path_list = []
        if self.droplist_merge.count() == 0:
            QMessageBox(QMessageBox.Warning,'Warning','No merge file!').exec_()
        else:
            for row in range(self.droplist_merge.count()):
                print("Row\t{0}:\t{1}\n".format(row,self.droplist_merge.item(row).text()))
                file_path_list.append(self.droplist_merge.item(row).whatsThis())
            output_dir = self.get_output_dir()
            merger = PdfWriter()
            for file_path in file_path_list:
                merger.append(file_path)
            metadata = self.get_metadata()
            if metadata is not None:
                merger.add_metadata(metadata)
            pw = self.get_encrypt_pw()
            if pw == '':
                merger.write(output_dir+'/merge.pdf')
            elif pw is None:
                pass
            else:
                merger.encrypt(self.get_encrypt_pw())
                merger.write(output_dir+'/merge.pdf')
            merger.close()
        print("---------Merge Over---------")

    def on_pushButton_sandm_clicked(self):
        file_path, file_type = QtWidgets.QFileDialog().getOpenFileName(filter="PDF File (*.pdf)")
        self.stamp_file = file_path
        self.label_sandm.setText("<a href=\"{0}\">{1}</a>".format(file_path,os.path.basename(self.stamp_file)))
        self.label_sandm.setOpenExternalLinks(True)

    def on_pushButton_add_clicked(self):
        print("---------Stamp/Watermark Start---------")
        print("Stamp:\t{0}\nWatermark:\t{1}\n".format(self.stamp_flag, not self.stamp_flag))
        if self.droplist_files.count() == 0:
            QMessageBox(QMessageBox.Warning,'Warning','No input file!').exec_()
        else:
            if self.stamp_file == '':
                QMessageBox(QMessageBox.Warning,'Warning','Select a stamp/watermark file!').exec_()
            else:
                output_dir = self.get_output_dir()
                stamp_reader = PdfReader(self.stamp_file,strict=self.strict_flag)
                stamp_page = stamp_reader.pages[0]
                for row in range(self.droplist_files.count()):
                    writer = PdfWriter()
                    file_path = self.droplist_files.item(row).whatsThis()
                    file_name_base = os.path.splitext(os.path.basename(file_path))[0]
                    reader = PdfReader(file_path,strict=self.strict_flag)
                    file_output_path = ''
                    if self.stamp_flag:
                        for page_num in range(len(reader.pages)):
                            page = reader.pages[page_num]
                            mediabox = page.mediabox
                            page.merge_page(stamp_page)
                            page.mediabox = mediabox
                            writer.add_page(page)
                            file_output_path = output_dir+'/'+file_name_base+'_stamp.pdf'
                    else:
                        for page_num in range(len(reader.pages)):
                            page = reader.pages[page_num]
                            mediabox = page.mediabox
                            stamp_page.merge_page(page)
                            page.mediabox = mediabox
                            writer.add_page(stamp_page)
                            file_output_path = output_dir+'/'+file_name_base+'_watermark.pdf'
                    metadata = self.get_metadata()
                    if metadata is not None:
                        writer.add_metadata(metadata)
                    pw = self.get_encrypt_pw()
                    if pw == '':
                        writer.write(file_output_path)
                    elif pw is None:
                        pass
                    else:
                        writer.encrypt(self.get_encrypt_pw())
                        writer.write(file_output_path)
                    writer.close()
        print("---------Stamp/Watermark Over---------")

    def on_pushButton_reduce_clicked(self):
        print("---------Reduce PDF Size Start---------")
        print("Remove duplication:\t{0}\n"
              "Lossless compression:\t{1}\n"
              "Remove images:\t{2}\n"
              .format(self.reduce_flags_list[0]
                      ,self.reduce_flags_list[1]
                      ,self.reduce_flags_list[2]))
        if self.droplist_files.count() == 0:
            QMessageBox(QMessageBox.Warning,'Warning','No input file!').exec_()
        else:
            output_dir = self.get_output_dir()
            for row in range(self.droplist_files.count()):
                file_path = self.droplist_files.item(row).whatsThis()
                file_name_base = os.path.splitext(os.path.basename(file_path))[0]
                reader = PdfReader(file_path,strict=self.strict_flag)
                writer = PdfWriter()
                file_output_path = output_dir+'/'+file_name_base
                for page in reader.pages:
                    if self.reduce_flags_list[1]:
                        page.compress_content_streams()
                    writer.add_page(page)
                if self.reduce_flags_list[2]:
                    writer.remove_images()
                writer.add_metadata(reader.metadata)
                if self.reduce_flags_list[0]:
                    file_output_path = file_output_path+'_rmduplication'
                if self.reduce_flags_list[1]:
                    file_output_path = file_output_path+'_lossless'
                if self.reduce_flags_list[2]:
                    file_output_path = file_output_path+'_rmimages'
                file_output_path= file_output_path + '.pdf'
                metadata = self.get_metadata()
                if metadata is not None:
                    writer.add_metadata(metadata)
                pw = self.get_encrypt_pw()
                if pw == '':
                    writer.write(file_output_path)
                elif pw is None:
                    pass
                else:
                    writer.encrypt(self.get_encrypt_pw())
                    writer.write(file_output_path)
                writer.close()
        print("---------Reduce PDF Size Over---------")

    def on_radioButton_stamp_clicked(self):
        self.stamp_flag = self.radioButton_stamp.isChecked()

    def on_radioButton_watermark_clicked(self):
        self.stamp_flag = not self.radioButton_watermark.isChecked()

    def on_checkBox_strict_clicked(self):
        self.strict_flag = self.checkBox_strict.isChecked()

    def on_groupBox_metadata_clicked(self):
        self.edit_metadata_flag = self.groupBox_metadata.isChecked()
        if self.edit_metadata_flag == True:
            if self.get_output_dir() != '':
                author,creator,producer,subject,title = self.read_metadata()
                self.lineEdit_author.setText(author)
                self.lineEdit_creator.setText(creator)
                self.lineEdit_producer.setText(producer)
                self.lineEdit_subject.setText(subject)
                self.plainTextEdit_title.setPlainText(title)
            else:
                self.groupBox_metadata.setChecked(False)
                self.edit_metadata_flag = self.groupBox_metadata.isChecked()
        else:
            self.lineEdit_author.setText(None)
            self.lineEdit_creator.setText(None)
            self.lineEdit_producer.setText(None)
            self.lineEdit_subject.setText(None)
            self.plainTextEdit_title.setPlainText(None)

    def on_groupBox_crypt_clicked(self):
        self.crypt_flag = self.groupBox_crypt.isChecked()
        if self.crypt_flag == False:
            self.lineEdit_enterpw.setText('')
            self.lineEdit_confirmpw.setText('')

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

    def update_merge_items(self):
        if self.droplist_files.count() != 0:
            self.droplist_merge.clear()
            for row in range(self.droplist_files.count()):
                self.droplist_merge.addItem(self.droplist_files.item(row).clone())

    def get_output_dir(self)->str:
        if self.droplist_files.count() == 0:
            QMessageBox(QMessageBox.Warning,'Warning','No input file!').exec_()
            return ''
        else:
            return os.path.dirname(self.droplist_files.item(0).whatsThis())

    def read_metadata(self):
        reader = PdfReader(self.droplist_files.item(0).whatsThis(),strict=self.strict_flag)
        if reader.is_encrypted:
            if self.crypt_flag:
                reader.decrypt(self.lineEdit_enterpw.text())
            else:
                QMessageBox(QMessageBox.Warning,'Warning','Encrypted!').exec_()
                return None,None,None,None,None
        metadata = reader.metadata
        return metadata.author,metadata.creator,metadata.producer,metadata.subject,metadata.title

    def get_encrypt_pw(self):
        if self.crypt_flag:
            if self.lineEdit_enterpw.text() == self.lineEdit_confirmpw.text():
                if self.lineEdit_enterpw.text() == '':
                    QMessageBox(QMessageBox.Warning,'Warning','Input your password!').exec_()
                    return None
                else:
                    return self.lineEdit_enterpw.text()
            else:
                QMessageBox(QMessageBox.Warning,'Warning','Confirm the passwords are the same!').exec_()
                return None
        else:
            return ''

    def get_metadata(self):
        if self.edit_metadata_flag:
            return {
                "/Author": self.lineEdit_author.text(),
                "/Creator": self.lineEdit_creator.text(),
                "/Producer": self.lineEdit_producer.text(),
                "/Subject": self.lineEdit_subject.text(),
                "/Title": self.plainTextEdit_title.toPlainText(),
            }
        else:
            return None

def on_Action_quit():
    sys.exit()


# Define DropList from QtWidgets.QListWidget
class DropList(QtWidgets.QListWidget):
    # 重要。因为PyQt本身itemEnter信号的缺陷，这里使用自定义的信号
    drop_external_over_signal = pyqtSignal()
    def __init__(self,forbid_external=False):
        super().__init__()
        self.forbid_external = forbid_external
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

    def on_itemPressed(self, item: QtWidgets.QListWidgetItem):
        # 注意：使用这个原因是pos和posF方法会有偏移
        self.drag_item = item

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        if self.is_dragging:
            # 当前如果是正在拖拽状态那么之久不作任何处理
            event.accept()
            return
        # 当前未进入拖拽状态（第一次触发）
        # 判断抓的是外部文件还是内部的item
        if event.mimeData().hasUrls():
            # 有链接 那么是外部文件
            self.is_internal = False
            if self.forbid_external:
                # 不准拖入
                event.ignore()
                return
        else:
            # 没有连接 那么是内部文件
            self.is_internal = True
            # 需要修正pos的偏移
            row = self.indexAt(event.pos()).row()
            self.removeItemWidget(self.drag_item)
            print('Drop up, Row:', row)
            print('Drag item:', QtWidgets.QListWidgetItem(self.drag_item).text())
        event.accept()
        self.is_dragging = True

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent) -> None:
        event.accept()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        if not self.is_internal:
            added_files_list = event.mimeData().text().split('\n')
            if added_files_list[-1] == '':
                added_files_list.pop()
            for file in added_files_list:
                if is_PDF(file):
                    item = QtWidgets.QListWidgetItem()
                    file = file.replace('file:///','')
                    file = urllib.parse.unquote(file)
                    file_name = os.path.basename(file)
                    item.setText(file_name)
                    item.setWhatsThis(file)
                    self.addItem(item)
            self.drop_external_over_signal.emit()
        else:
            row = self.indexAt(event.pos()).row()
            print('Drop down, Row:', row)
            print('Drag item:', QtWidgets.QListWidgetItem(self.drag_item).text())
            self.insertItem(row, QtWidgets.QListWidgetItem(self.drag_item))
        # 重置所有参数
        self.drag_item = None
        self.is_internal = False
        self.is_dragging = False
        event.accept()

def is_PDF(file):
    return os.path.splitext(file)[-1][1:].lower() == 'pdf'


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    pdf_toolbox = PDF_Toolbox()
    pdf_toolbox.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
