# -*- coding: utf-8 -*-

"""
Module implementing guahaoDialog.
"""

from PyQt5.QtCore import pyqtSlot,Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem,QMessageBox

from Ui_guahao import Ui_Form
from db import dbop
import curuser


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
        self.Init()
        self.currentpage = 1  # 当前页数
        self.totalpages = 1  # 总页数
        self.currentrow = 0  # 当前行数
        self.load_doctors()
        self.cnt_pages()
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)

    @pyqtSlot()
    def on_pushButton_search_pressed(self):
        """
        搜索
        """
        self.currentpage = 1
        self.showTablecontent()

    @pyqtSlot()
    def on_pushButton_front_pressed(self):
        """
        上一页
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
    def on_pushButton_after_pressed(self):
        """
        下一页
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
    def on_pushButton_skip_pressed(self):
        """
        跳转到xx页
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

    @pyqtSlot()
    def on_pushButton_guahao_pressed(self):
        """
        挂号
        """
        doctorid = self.tableWidget.item(self.currentrow, 0).text()
        doctorname = self.tableWidget.item(self.currentrow, 1).text()
        patientid = curuser.getuserid()
        res = QMessageBox.question(self, "确认", "确认挂%s医生的号？" % doctorname, QMessageBox.Yes | QMessageBox.No)
        if res == QMessageBox.Yes:
            guahao = dbop.guahao(patientid, doctorid)
            if guahao == "already_reg":
                QMessageBox.information(self, "提示", "挂号成功")
            elif guahao == "date_same":
                QMessageBox.warning(self, "警告", "您今日已挂过%s医生的号" % doctorname)

    @pyqtSlot(int, int)
    def on_tableWidget_cellPressed(self, row, column):
        """
        选中医生
        """
        self.pushButton_guahao.setEnabled(True)
        self.currentrow = row



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
            fee = str(doctor[3])
            dept = doctor[5]

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
            self.tableWidget.setItem(i, 2, dept_item)
            self.tableWidget.setItem(i, 3, title_item)
            self.tableWidget.setItem(i, 4, fee_item)

            self.tableWidget.resizeColumnsToContents()


    def load_doctors(self):
        """
        加载第一页医生列表
        """
        firstPage = dbop.listAllDoctors(0, 10)
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

    def Init(self):
        self.pushButton_guahao.setEnabled(False)
        self.pushButton_skip.setEnabled(False)
        self.pushButton_after.setEnabled(False)
        self.pushButton_front.setEnabled(False)


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
                currentDoctorlist = dbop.listAllDoctors((self.currentpage - 1) * 10, 10, options, searchInfo)
                if currentDoctorlist == "connect_error":
                    QMessageBox.warning(self, "警告", "数据库连接失败")
                elif currentDoctorlist == "excute_error":
                    QMessageBox.warning(self, "警告", "数据库查询失败")
                else:
                    self.showTable(currentDoctorlist)
        elif not (searchInfo):         # 无搜索信息，无搜索选项
            self.cnt_pages()
            self.label_cur.setText(str(self.currentpage))
            self.label_sum.setText(str(self.totalpages))
            currentDoctorlist = dbop.listAllDoctors((self.currentpage - 1) * 10, 10)
            if currentDoctorlist == "connect_error":
                QMessageBox.warning(self, "警告", "数据库连接失败")
            elif currentDoctorlist == "excute_error":
                QMessageBox.warning(self, "警告", "数据库查询失败")
            else:
                self.showTable(currentDoctorlist)



    def cnt_pages(self, options=None, searchInfo=None):
        '''
        计算总页数
        '''
        page = dbop.totalPages(options, searchInfo)
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

