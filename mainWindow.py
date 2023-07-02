# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import time

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from Ui_mainWindow import Ui_MainWindow
from jiaohao import jiaohaoDialog
from guahao import guahaoDialog
from docsub import docsubDialog
from phpat import phpatDialog
import curuser


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.InitUi()
    
    @pyqtSlot()
    def on_actionguahao_2_triggered(self):
        """
        患者挂号
        """
        guahao = guahaoDialog(self)
        self.setCentralWidget(guahao)
    
    @pyqtSlot()
    def on_actionquyao_triggered(self):
        """
        Slot documentation goes here.
        """
        self.phpat = phpatDialog()
        self.phpat.show()

    
    @pyqtSlot()
    def on_actionjiaohao_triggered(self):
        """
        医生叫号
        """
        jiaohao = jiaohaoDialog(self)
        self.setCentralWidget(jiaohao)

    
    @pyqtSlot()
    def on_actionkaiyao_triggered(self):
        """
        医生开药
        """
        docsub = docsubDialog(self)
        self.setCentralWidget(docsub)


    def InitUi(self):
        loginTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        currentuser = curuser.getcuruser()
        self.statusbar.showMessage("当前用户："+currentuser+"  |  登录时间："+loginTime)
        currentopt = curuser.getcurrentopt()
        if currentopt == "patient":
            self.menu_2.menuAction().setVisible(False)
        elif currentopt == "doctor":
            self.menu.menuAction().setVisible(False)