# -*- coding: utf-8 -*-

"""
Module implementing phpatDialog.
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox

from Ui_phpat import Ui_Form
from db import dbop
import curuser


class phpatDialog(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(phpatDialog, self).__init__(parent)
        self.setupUi(self)
        self.showTablecontent()

    def showTable(self, medicinelist):
        """
        显示医生列表
        doctorlist: 数据库查询后返回的数据
        """
        self.tableWidget.clearContents()
        self.tableWidget.model().removeRows(0, self.tableWidget.rowCount())
        for i,medicine in enumerate(medicinelist):
            docname = medicine[0]
            docid = medicine[1]
            medname = medicine[2]
            medid = medicine[3]
            medprice = str(medicine[4])
            phname = medicine[5]
            text = medicine[6]
            time = str(medicine[7])

            self.tableWidget.insertRow(i)

            docname_item = QTableWidgetItem(docname)
            docid_item = QTableWidgetItem(docid)
            medname_item = QTableWidgetItem(medname)
            medid_item = QTableWidgetItem(medid)
            medprice_item = QTableWidgetItem(medprice)
            phname_item = QTableWidgetItem(phname)
            text_item = QTableWidgetItem(text)
            time_item = QTableWidgetItem(time)

            self.tableWidget.setItem(i, 0, docname_item)
            self.tableWidget.setItem(i, 1, docid_item)
            self.tableWidget.setItem(i, 2, medname_item)
            self.tableWidget.setItem(i, 3, medid_item)
            self.tableWidget.setItem(i, 4, medprice_item)
            self.tableWidget.setItem(i, 5, phname_item)
            self.tableWidget.setItem(i, 6, text_item)
            self.tableWidget.setItem(i, 7, time_item)

            self.tableWidget.resizeColumnsToContents()

    def showTablecontent(self):
        patid = curuser.getuserid()
        currentPatMedicine = dbop.listAllPatMedicine(patid)
        if currentPatMedicine == "connect_error":
            QMessageBox.warning(self, "警告", "数据库连接失败")
        elif currentPatMedicine == "excute_error":
            QMessageBox.warning(self, "警告", "数据库查询失败")
        else:
            self.showTable(currentPatMedicine)