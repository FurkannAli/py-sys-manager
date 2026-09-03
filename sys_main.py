# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sys_main.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy,
    QSpinBox, QSplitter, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(482, 846)
        font = QFont()
        font.setPointSize(18)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabShape(QTabWidget.TabShape.Triangular)
        self.tabWidget.setTabBarAutoHide(False)
        self.tab_1 = QWidget()
        self.tab_1.setObjectName(u"tab_1")
        self.layoutWidget = QWidget(self.tab_1)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 670, 440, 38))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_Refresh = QPushButton(self.layoutWidget)
        self.pushButton_Refresh.setObjectName(u"pushButton_Refresh")

        self.horizontalLayout.addWidget(self.pushButton_Refresh)

        self.pushButton_Kill = QPushButton(self.layoutWidget)
        self.pushButton_Kill.setObjectName(u"pushButton_Kill")

        self.horizontalLayout.addWidget(self.pushButton_Kill)

        self.pushButton_3 = QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.layoutWidget1 = QWidget(self.tab_1)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(11, 2, 441, 661))
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_cpu = QLabel(self.layoutWidget1)
        self.label_cpu.setObjectName(u"label_cpu")

        self.verticalLayout.addWidget(self.label_cpu)

        self.progressBar_1 = QProgressBar(self.layoutWidget1)
        self.progressBar_1.setObjectName(u"progressBar_1")
        self.progressBar_1.setValue(0)
        self.progressBar_1.setInvertedAppearance(False)

        self.verticalLayout.addWidget(self.progressBar_1)

        self.label_mem = QLabel(self.layoutWidget1)
        self.label_mem.setObjectName(u"label_mem")

        self.verticalLayout.addWidget(self.label_mem)

        self.progressBar_2 = QProgressBar(self.layoutWidget1)
        self.progressBar_2.setObjectName(u"progressBar_2")
        self.progressBar_2.setValue(100)

        self.verticalLayout.addWidget(self.progressBar_2)


        self.verticalLayout_4.addLayout(self.verticalLayout)

        self.lineEdit_Search = QLineEdit(self.layoutWidget1)
        self.lineEdit_Search.setObjectName(u"lineEdit_Search")

        self.verticalLayout_4.addWidget(self.lineEdit_Search)

        self.listWidget = QListWidget(self.layoutWidget1)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout_4.addWidget(self.listWidget)

        self.tabWidget.addTab(self.tab_1, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayoutWidget = QWidget(self.tab)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 441, 461))
        self.gridLayout_Core = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_Core.setObjectName(u"gridLayout_Core")
        self.gridLayout_Core.setContentsMargins(0, 0, 0, 0)
        self.layoutWidget2 = QWidget(self.tab)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 480, 441, 80))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_Swap = QLabel(self.layoutWidget2)
        self.label_Swap.setObjectName(u"label_Swap")

        self.verticalLayout_2.addWidget(self.label_Swap)

        self.progressBar_Swap = QProgressBar(self.layoutWidget2)
        self.progressBar_Swap.setObjectName(u"progressBar_Swap")
        self.progressBar_Swap.setValue(24)

        self.verticalLayout_2.addWidget(self.progressBar_Swap)

        self.tabWidget.addTab(self.tab, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.gridLayoutWidget_2 = QWidget(self.tab_5)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 10, 441, 601))
        self.gridLayout_Temps = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_Temps.setObjectName(u"gridLayout_Temps")
        self.gridLayout_Temps.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayoutWidget_2 = QWidget(self.tab_4)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 10, 441, 241))
        self.verticalLayout_Disks = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_Disks.setObjectName(u"verticalLayout_Disks")
        self.verticalLayout_Disks.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutWidget_3 = QWidget(self.tab_4)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 260, 441, 451))
        self.verticalLayout_NetStuff = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_NetStuff.setObjectName(u"verticalLayout_NetStuff")
        self.verticalLayout_NetStuff.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayoutWidget = QWidget(self.tab_3)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 441, 701))
        self.verticalLayout_ChartThing = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_ChartThing.setObjectName(u"verticalLayout_ChartThing")
        self.verticalLayout_ChartThing.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.pushButton_Export = QPushButton(self.tab_6)
        self.pushButton_Export.setObjectName(u"pushButton_Export")
        self.pushButton_Export.setGeometry(QRect(1, 669, 461, 41))
        self.splitter = QSplitter(self.tab_6)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setGeometry(QRect(0, 1, 461, 631))
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.label_OS = QLabel(self.splitter)
        self.label_OS.setObjectName(u"label_OS")
        self.label_OS.setWordWrap(True)
        self.splitter.addWidget(self.label_OS)
        self.label_Kernel = QLabel(self.splitter)
        self.label_Kernel.setObjectName(u"label_Kernel")
        self.label_Kernel.setWordWrap(True)
        self.splitter.addWidget(self.label_Kernel)
        self.label_CPUModel = QLabel(self.splitter)
        self.label_CPUModel.setObjectName(u"label_CPUModel")
        self.label_CPUModel.setWordWrap(True)
        self.splitter.addWidget(self.label_CPUModel)
        self.label_Uptime = QLabel(self.splitter)
        self.label_Uptime.setObjectName(u"label_Uptime")
        self.label_Uptime.setWordWrap(True)
        self.splitter.addWidget(self.label_Uptime)
        self.tabWidget.addTab(self.tab_6, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.spinBox_Interval = QSpinBox(self.tab_2)
        self.spinBox_Interval.setObjectName(u"spinBox_Interval")
        self.spinBox_Interval.setGeometry(QRect(180, 10, 91, 51))
        self.spinBox_Interval.setMinimum(1)
        self.spinBox_Interval.setMaximum(60)
        self.pushButton_SaveSettings = QPushButton(self.tab_2)
        self.pushButton_SaveSettings.setObjectName(u"pushButton_SaveSettings")
        self.pushButton_SaveSettings.setGeometry(QRect(10, 590, 441, 51))
        self.label = QLabel(self.tab_2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 181, 51))
        self.tabWidget.addTab(self.tab_2, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 482, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(5)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_Refresh.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.pushButton_Kill.setText(QCoreApplication.translate("MainWindow", u"Kill Process", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Clear Caches", None))
        self.label_cpu.setText(QCoreApplication.translate("MainWindow", u"Cpu Percentage", None))
        self.label_mem.setText(QCoreApplication.translate("MainWindow", u"Memory Percentage", None))
        self.lineEdit_Search.setText("")
        self.lineEdit_Search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.label_Swap.setText(QCoreApplication.translate("MainWindow", u"Swap Memory", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Misc.", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Temps", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Disks, Net", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Graphs", None))
        self.pushButton_Export.setText(QCoreApplication.translate("MainWindow", u"Export Data", None))
        self.label_OS.setText(QCoreApplication.translate("MainWindow", u"os", None))
        self.label_Kernel.setText(QCoreApplication.translate("MainWindow", u"kernel", None))
        self.label_CPUModel.setText(QCoreApplication.translate("MainWindow", u"cpumodel", None))
        self.label_Uptime.setText(QCoreApplication.translate("MainWindow", u"uptime", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"Overview", None))
        self.pushButton_SaveSettings.setText(QCoreApplication.translate("MainWindow", u"Save Settings", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Interval Time:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

