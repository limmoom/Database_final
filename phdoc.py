# -*- coding: utf-8 -*-

"""
Module implementing phdocDialog.
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMessageBox

import curuser
from Ui_phdoc import Ui_Dialog
from db import dbop


class phdocDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(phdocDialog, self).__init__(parent)
        self.setupUi(self)
        self.Init()
        self.currentpage = 1  # 当前页数
        self.totalpages = 1  # 总页数
        self.currentrow = 0  # 当前行数
        self.load_medicines()
        self.cnt_pages()
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)

    @pyqtSlot()
    def on_pushButton_confirm_clicked(self):
        self.info = self.textEdit.toPlainText()
        medid = self.tableWidget.item(self.currentrow,0).text()
        res = dbop.phconfirm(medid, self.info, curuser.getuserid())
        if res == "stock_error":
            QMessageBox.warning(self,"警告","库存不足！")
        elif res == "execute_error":
            QMessageBox.warning(self,"警告","执行失败！")
        elif res == "connect_error":
            QMessageBox.warning(self,"警告","连接失败！")
        self.showTablecontent()

    @pyqtSlot()
    def on_pushButton_search_clicked(self):
        """
        Slot documentation goes here.
        """
        self.currentpage = 1
        self.showTablecontent()
    
    @pyqtSlot(int,int)
    def on_tableWidget_cellClicked(self, row, column):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type QModelIndex
        """
        self.pushButton_confirm.setEnabled(True)
        self.currentrow = row
    
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
        opt = ["药品名","药品编号"]
        self.comboBox.addItems(opt)
        self.pushButton_front.setEnabled(False)
        self.pushButton_after.setEnabled(False)
        self.pushButton_skip.setEnabled(False)
        self.pushButton_confirm.setEnabled(False)

    def showTable(self, medicinelist):
        """
        显示药品列表
        doctorlist: 数据库查询后返回的数据
        """
        self.tableWidget.clearContents()
        self.tableWidget.model().removeRows(0, self.tableWidget.rowCount())
        for i,medicine in enumerate(medicinelist):
            id = medicine[1]
            name = medicine[2]
            price = str(medicine[3])
            stock = str(medicine[4])

            self.tableWidget.insertRow(i)

            id_item = QTableWidgetItem(id)
            name_item = QTableWidgetItem(name)
            price_item = QTableWidgetItem(price)
            stock_item = QTableWidgetItem(stock)
            id_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            name_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            price_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            stock_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            self.tableWidget.setItem(i, 0, id_item)
            self.tableWidget.setItem(i, 1, name_item)
            self.tableWidget.setItem(i, 2, price_item)
            self.tableWidget.setItem(i, 3, stock_item)

            self.tableWidget.resizeColumnsToContents()

    def load_medicines(self):
        """
        加载第一页药品列表
        """
        firstPage = dbop.listAllmedicines(0, 3)
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

    def cnt_pages(self, options=None, searchInfo=None):
        '''
        计算总页数
        '''
        page = dbop.totalmedicinePages(options, searchInfo)
        if page == "connect_error":
            QMessageBox.warning(self, "警告", "数据库连接失败")
            self.totalpages = 1
        elif page == "excute_error":
            QMessageBox.warning(self, "警告", "数据库查询失败")
            self.totalpages = 1
        elif page:
            if page[0][0] % 3 == 0:
                self.totalpages = page[0][0] // 3
            else:
                self.totalpages = page[0][0] // 3 + 1
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
                currentMedicinelist = dbop.listAllmedicines((self.currentpage - 1) * 3, 3, options, searchInfo)
                if currentMedicinelist == "connect_error":
                    QMessageBox.warning(self, "警告", "数据库连接失败")
                elif currentMedicinelist == "excute_error":
                    QMessageBox.warning(self, "警告", "数据库查询失败")
                else:
                    self.showTable(currentMedicinelist)
        elif not (searchInfo):         # 无搜索信息，无搜索选项
            self.cnt_pages()
            self.label_cur.setText(str(self.currentpage))
            self.label_sum.setText(str(self.totalpages))
            currentMedicinelist = dbop.listAllmedicines((self.currentpage - 1) * 3, 3)
            if currentMedicinelist == "connect_error":
                QMessageBox.warning(self, "警告", "数据库连接失败")
            elif currentMedicinelist == "excute_error":
                QMessageBox.warning(self, "警告", "数据库查询失败")
            else:
                self.showTable(currentMedicinelist)

