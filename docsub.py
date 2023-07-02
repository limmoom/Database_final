# -*- coding: utf-8 -*-

"""
Module implementing docsubDialog.
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem

import curuser
import dbop
from Ui_docsub import Ui_Form
from phdoc import phdocDialog

class docsubDialog(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(docsubDialog, self).__init__(parent)
        self.setupUi(self)
        self.Init()
        self.currentpage = 1  # 当前页数
        self.totalpages = 1  # 总页数
        self.currentrow = 0  # 当前行数
        self.load_patients()
        self.cnt_pages()
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
    
    @pyqtSlot()
    def on_pushButton_search_clicked(self):
        """
        Slot documentation goes here.
        """
        self.currentpage = 1
        self.showTablecontent()
    
    @pyqtSlot()
    def on_pushButton_ph_clicked(self):
        """
        Slot documentation goes here.
        """
        curuser.uploadpatient(self.tableWidget.item(self.currentrow,0).text())
        self.phdoc = phdocDialog()
        self.phdoc.show()


    
    @pyqtSlot(int,int)
    def on_tableWidget_cellClicked(self, row, column):
        """
        Slot documentation goes here.

        """
        self.currentrow = row
        self.pushButton_ph.setEnabled(True)
    
    @pyqtSlot()
    def on_pushButton_front_clicked(self):
        """
        Slot documentation goes here.
        """
        self.currentpage -= 1
        if self.currentpage >= 1:
            self.label_cur.setText(str(self.currentpage))
            self.showTablecontent()
            if self.currentpage == 1:
                self.pushButton_front.setEnabled(False)
        else:
            self.currentpage = 1
            self.pushButton_front.setEnabled(False)
    
    @pyqtSlot()
    def on_pushButton_after_clicked(self):
        """
        Slot documentation goes here.
        """
        self.currentpage += 1
        if self.currentpage <= self.totalpages:
            self.label_cur.setText(str(self.currentpage))
            self.showTablecontent()
            self.pushButton_front.setEnabled(True)
            if self.currentpage == self.totalpages:
                self.pushButton_after.setEnabled(False)
        else:
            self.currentpage = self.totalpages
            self.pushButton_after.setEnabled(False)
    
    @pyqtSlot()
    def on_pushButton_skip_clicked(self):
        """
        Slot documentation goes here.
        """
        goPage = self.spinBox.value()
        if goPage > self.totalpages:
            QMessageBox.warning(self, "警告", "超出页数范围")
        elif goPage < 1:
            QMessageBox.warning(self, "警告", "页数不能小于1")
        else:
            self.currentpage = goPage
            self.label_cur.setText(str(self.currentpage))
            if goPage == 1 and goPage < self.totalpages:
                self.pushButton_front.setEnabled(False)
                self.pushButton_after.setEnabled(True)
            elif goPage == self.totalpages and goPage > 1:
                self.pushButton_front.setEnabled(True)
                self.pushButton_after.setEnabled(False)
            elif goPage == 1 and goPage == self.totalpages:
                self.pushButton_front.setEnabled(False)
                self.pushButton_after.setEnabled(False)
            elif 1 < goPage < self.totalpages:
                self.pushButton_front.setEnabled(True)
                self.pushButton_after.setEnabled(True)
            self.showTablecontent()

    def Init(self):
        opt = ["患者病历卡号","患者姓名", "患者身份证号"]
        self.comboBox.addItems(opt)
        self.pushButton_front.setEnabled(False)
        self.pushButton_after.setEnabled(False)
        self.pushButton_skip.setEnabled(False)
        self.pushButton_ph.setEnabled(False)

    def cnt_pages(self,options="", searchInfo=""):
        docid = curuser.getuserid()
        page = dbop.totalpatPages_already(docid, options, searchInfo)
        if page == "connect_error":
            QMessageBox.warning(self, "警告", "数据库连接失败")
            self.totalpages = 1
        elif page == "excute_error":
            QMessageBox.warning(self, "警告", "数据库查询失败")
            self.totalpages = 1
        elif page:
            if page[0][0] % 10 == 0:
                self.totalpages = page[0][0] // 10
            else:
                self.totalpages = page[0][0] // 10 + 1
            if self.currentpage == 1:
                self.pushButton_front.setEnabled(False)
            if self.currentpage == self.totalpages:
                self.pushButton_after.setEnabled(False)
            if 1 < self.currentpage < self.totalpages:
                self.pushButton_front.setEnabled(True)
                self.pushButton_after.setEnabled(True)
                self.pushButton_skip.setEnabled(True)
            if self.totalpages > 1:
                self.pushButton_skip.setEnabled(True)
                self.pushButton_after.setEnabled(True)

    def showTable(self, patientlist):
        """
        显示已就诊病人列表
        doctorlist: 数据库查询后返回的数据
        """
        self.tableWidget.clearContents()
        self.tableWidget.model().removeRows(0, self.tableWidget.rowCount())
        for i,patient in enumerate(patientlist):
            id = patient[0]
            name = patient[1]
            datetime = str(patient[2])
            idnumber = patient[3]


            self.tableWidget.insertRow(i)

            id_item = QTableWidgetItem(id)
            name_item = QTableWidgetItem(name)
            datetime_item = QTableWidgetItem(datetime)
            idnumber_item = QTableWidgetItem(idnumber)
            id_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            name_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            datetime_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            idnumber_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            self.tableWidget.setItem(i, 0, id_item)
            self.tableWidget.setItem(i, 1, name_item)
            self.tableWidget.setItem(i, 2, datetime_item)
            self.tableWidget.setItem(i, 3, idnumber_item)

            self.tableWidget.resizeColumnsToContents()

    def showTablecontent(self):
        '''
        显示当前表格内容
        '''
        searchInfo = self.lineEdit.text()
        options = self.comboBox.currentText()
        if searchInfo:
            if options:
                self.cnt_pages(options, searchInfo)
                self.label_cur.setText(str(self.currentpage))
                self.label_sum.setText(str(self.totalpages))
                currentPatientlist = dbop.listAllPatients_already((self.currentpage - 1) * 10, 10, curuser.getuserid(), options, searchInfo)
                if currentPatientlist == "connect_error":
                    QMessageBox.warning(self, "警告", "数据库连接失败")
                elif currentPatientlist == "excute_error":
                    QMessageBox.warning(self, "警告", "数据库查询失败")
                else:
                    self.showTable(currentPatientlist)
        elif not searchInfo:
            self.cnt_pages()
            self.label_cur.setText(str(self.currentpage))
            self.label_sum.setText(str(self.totalpages))
            currentPatientlist = dbop.listAllPatients_already((self.currentpage - 1) * 10, 10, curuser.getuserid())
            if currentPatientlist == "connect_error":
                QMessageBox.warning(self, "警告", "数据库连接失败")
            elif currentPatientlist == "excute_error":
                QMessageBox.warning(self, "警告", "数据库查询失败")
            else:
                self.showTable(currentPatientlist)

    def load_patients(self):
        """
        加载第一页医生列表
        """
        firstPage = dbop.listAllPatients_already(0, 10, curuser.getuserid())
        if firstPage == "connect_error":
            QMessageBox.warning(self, "警告", "数据库连接失败")
        elif firstPage == "excute_error":
            QMessageBox.warning(self, "警告", "数据库查询失败")
        elif firstPage:
            self.showTable(firstPage)
            self.currentpage = 1
            self.cnt_pages()
            self.label_cur.setText(str(self.currentpage))
            self.label_sum.setText(str(self.totalpages))
