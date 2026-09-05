# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'home.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QLabel, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(674, 401)
        self.gridLayout_11 = QGridLayout(Form)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.gridLayout_10 = QGridLayout(self.frame)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_2)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.groupBox_4 = QGroupBox(self.frame_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        font = QFont()
        font.setBold(True)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout = QGridLayout(self.groupBox_4)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_total = QLabel(self.groupBox_4)
        self.lbl_total.setObjectName(u"lbl_total")
        self.lbl_total.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lbl_total, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.groupBox_4, 2, 0, 1, 1)

        self.groupBox = QGroupBox(self.frame_2)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font)
        self.groupBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(9, 0, 9, 0)
        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setStyleSheet(u"background-color: rgb(255, 170, 0);")

        self.gridLayout_2.addWidget(self.comboBox, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.frame_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font)
        self.groupBox_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_3 = QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(0)
        self.gridLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 0, 3, 1, 1)

        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 0, 2, 1, 1)

        self.lbl_ng = QLabel(self.groupBox_3)
        self.lbl_ng.setObjectName(u"lbl_ng")

        self.gridLayout_3.addWidget(self.lbl_ng, 1, 1, 1, 1)

        self.lbl_ok = QLabel(self.groupBox_3)
        self.lbl_ok.setObjectName(u"lbl_ok")

        self.gridLayout_3.addWidget(self.lbl_ok, 0, 1, 1, 1)

        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 1, 2, 1, 1)

        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 1, 3, 1, 1)


        self.gridLayout_5.addWidget(self.groupBox_3, 1, 0, 1, 1)

        self.gridLayout_5.setRowStretch(0, 1)
        self.gridLayout_5.setRowStretch(1, 2)
        self.gridLayout_5.setRowStretch(2, 10)

        self.gridLayout_10.addWidget(self.frame_2, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_3)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.groupBox_6 = QGroupBox(self.frame_3)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setFont(font)
        self.groupBox_6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_7 = QGridLayout(self.groupBox_6)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.lbl_step0 = QLabel(self.groupBox_6)
        self.lbl_step0.setObjectName(u"lbl_step0")
        self.lbl_step0.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lbl_step0, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_6, 0, 0, 1, 1)

        self.groupBox_7 = QGroupBox(self.frame_3)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setFont(font)
        self.groupBox_7.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_8 = QGridLayout(self.groupBox_7)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.lbl_step2 = QLabel(self.groupBox_7)
        self.lbl_step2.setObjectName(u"lbl_step2")
        self.lbl_step2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lbl_step2, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_7, 0, 1, 1, 1)

        self.groupBox_8 = QGroupBox(self.frame_3)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setFont(font)
        self.groupBox_8.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_12 = QGridLayout(self.groupBox_8)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.lbl_step1_raw = QLabel(self.groupBox_8)
        self.lbl_step1_raw.setObjectName(u"lbl_step1_raw")
        self.lbl_step1_raw.setFont(font)
        self.lbl_step1_raw.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.lbl_step1_raw, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_8, 1, 0, 1, 1)

        self.groupBox_9 = QGroupBox(self.frame_3)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setFont(font)
        self.groupBox_9.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_13 = QGridLayout(self.groupBox_9)
        self.gridLayout_13.setSpacing(0)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.lbl_step1_bin = QLabel(self.groupBox_9)
        self.lbl_step1_bin.setObjectName(u"lbl_step1_bin")
        self.lbl_step1_bin.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.lbl_step1_bin, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_9, 1, 1, 1, 1)

        self.gridLayout_4.setRowStretch(0, 1)
        self.gridLayout_4.setRowStretch(1, 1)
        self.gridLayout_4.setColumnStretch(0, 1)
        self.gridLayout_4.setColumnStretch(1, 1)

        self.gridLayout_10.addWidget(self.frame_3, 0, 1, 1, 1)

        self.gridLayout_10.setColumnStretch(0, 1)
        self.gridLayout_10.setColumnStretch(1, 10)

        self.gridLayout_11.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"K\u1ebeT QU\u1ea2 KI\u1ec2M TRA", None))
        self.lbl_total.setText(QCoreApplication.translate("Form", u"color", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"M\u00c3 S\u1ea2N PH\u1ea8M", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Form", u"1", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Form", u"2", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Form", u"3", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Form", u"4", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Form", u"5", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("Form", u"6", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("Form", u"7", None))

        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"S\u1ea2N L\u01af\u1ee2NG", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"1", None))
        self.label.setText(QCoreApplication.translate("Form", u"OK:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"NG:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"%OK:", None))
        self.lbl_ng.setText(QCoreApplication.translate("Form", u"1", None))
        self.lbl_ok.setText(QCoreApplication.translate("Form", u"1", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"%NG", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"1", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Form", u"CAMERA 1 - L1", None))
        self.lbl_step0.setText(QCoreApplication.translate("Form", u"P1", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Form", u"CAMERA 2", None))
        self.lbl_step2.setText(QCoreApplication.translate("Form", u"P4", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Form", u"CAMERA 1 - L2 - G\u1ed0C", None))
        self.lbl_step1_raw.setText(QCoreApplication.translate("Form", u"P2", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("Form", u"CAMERA 1 - L2 - NH\u1eca PH\u00c2N", None))
        self.lbl_step1_bin.setText(QCoreApplication.translate("Form", u"P3", None))
    # retranslateUi

