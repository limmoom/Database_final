# -*- coding: utf-8 -*-

"""
Module implementing guahaoDialog.
"""

from PyQt5.QtCore import pyqtSlot,Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem,QMessageBox

from Ui_guahao import Ui_Form
from db import dbop


class guahaoDialog(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(guahaoDialog, self).__init__(parent)
        self.setupUi(self)
        self.currentpage = 1  # 当前页数
        self.totalpages = 1  # 总页数
        self.load_doctors()
        self.cnt_pages()
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
    
    @pyqtSlot()
    def on_pushButton_search_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_pushButton_front_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_pushButton_after_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_pushButton_skip_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    def showTable(self, doctorlist):
        """
        显示医生列表
        doctorlist: 数据库查询后返回的数据
        """
        self.tableWidget.clearContents()
        self.tableWidget.model().removeRows(0, self.tableWidget.rowCount())
        for i,doctor in enumerate(doctorlist):
            id = doctor[0]
            name = doctor[1]
            title = doctor[2]
            fee = doctor[3]
            dept = doctor[4]

            self.tableWidget.insertRow(i)

            id_item = QTableWidgetItem(id)
            name_item = QTableWidgetItem(name)
            title_item = QTableWidgetItem(title)
            fee_item = QTableWidgetItem(fee)
            dept_item = QTableWidgetItem(dept)
            id_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            name_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            title_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            fee_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            dept_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            self.tableWidget.setItem(i, 0, id_item)
            self.tableWidget.setItem(i, 1, name_item)
            self.tableWidget.setItem(i, 2, title_item)
            self.tableWidget.setItem(i, 3, fee_item)
            self.tableWidget.setItem(i, 4, dept_item)

            self.tableWidget.resizeColumnsToContents()


    def load_doctors(self):
        """
        加载第一页医生列表
        """
        firstPage = listAllDoctors(0, 20)
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