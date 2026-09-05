# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QLabel, QSizePolicy, QSlider, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(674, 404)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.groupBox_2 = QGroupBox(self.frame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        font = QFont()
        font.setBold(True)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_4 = QGridLayout(self.groupBox_2)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(9, 0, 9, 0)
        self.groupBox_8 = QGroupBox(self.groupBox_2)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_5 = QGridLayout(self.groupBox_8)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(-1, 0, -1, 20)
        self.label_24 = QLabel(self.groupBox_8)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_24, 0, 1, 1, 1)

        self.label_22 = QLabel(self.groupBox_8)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_5.addWidget(self.label_22, 1, 0, 1, 1)

        self.label_21 = QLabel(self.groupBox_8)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_5.addWidget(self.label_21, 1, 2, 1, 1)

        self.horizontalSlider_6 = QSlider(self.groupBox_8)
        self.horizontalSlider_6.setObjectName(u"horizontalSlider_6")
        self.horizontalSlider_6.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_5.addWidget(self.horizontalSlider_6, 1, 1, 1, 1)

        self.label_23 = QLabel(self.groupBox_8)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_5.addWidget(self.label_23, 0, 0, 1, 1)

        self.gridLayout_5.setRowStretch(0, 1)

        self.gridLayout_4.addWidget(self.groupBox_8, 0, 0, 1, 1)

        self.groupBox_7 = QGroupBox(self.groupBox_2)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_6 = QGridLayout(self.groupBox_7)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(-1, 0, -1, 20)
        self.label_15 = QLabel(self.groupBox_7)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_6.addWidget(self.label_15, 0, 0, 1, 1)

        self.label_16 = QLabel(self.groupBox_7)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_16, 0, 1, 1, 1)

        self.label_14 = QLabel(self.groupBox_7)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_6.addWidget(self.label_14, 1, 0, 1, 1)

        self.horizontalSlider_4 = QSlider(self.groupBox_7)
        self.horizontalSlider_4.setObjectName(u"horizontalSlider_4")
        self.horizontalSlider_4.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_6.addWidget(self.horizontalSlider_4, 1, 1, 1, 1)

        self.label_13 = QLabel(self.groupBox_7)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_6.addWidget(self.label_13, 1, 2, 1, 1)

        self.gridLayout_6.setRowStretch(0, 1)
        self.gridLayout_6.setRowStretch(1, 1)

        self.gridLayout_4.addWidget(self.groupBox_7, 1, 0, 1, 1)

        self.groupBox_5 = QGroupBox(self.groupBox_2)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.groupBox_5, 2, 0, 1, 1)

        self.gridLayout_4.setRowStretch(0, 1)
        self.gridLayout_4.setRowStretch(1, 1)
        self.gridLayout_4.setRowStretch(2, 1)

        self.gridLayout_2.addWidget(self.groupBox_2, 0, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.frame)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font)
        self.groupBox_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_3 = QGridLayout(self.groupBox_3)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(9, 0, -1, 0)
        self.groupBox_6 = QGroupBox(self.groupBox_3)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_7 = QGridLayout(self.groupBox_6)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(-1, -1, -1, 20)
        self.label_3 = QLabel(self.groupBox_6)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_7.addWidget(self.label_3, 0, 0, 1, 1)

        self.label_4 = QLabel(self.groupBox_6)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.label_4, 0, 1, 1, 1)

        self.label = QLabel(self.groupBox_6)
        self.label.setObjectName(u"label")

        self.gridLayout_7.addWidget(self.label, 1, 0, 1, 1)

        self.horizontalSlider = QSlider(self.groupBox_6)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_7.addWidget(self.horizontalSlider, 1, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox_6)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_7.addWidget(self.label_2, 1, 2, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_6, 0, 0, 1, 1)

        self.groupBox = QGroupBox(self.groupBox_3)
        self.groupBox.setObjectName(u"groupBox")
        font1 = QFont()
        font1.setBold(False)
        self.groupBox.setFont(font1)
        self.groupBox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.groupBox, 1, 0, 1, 1)

        self.gridLayout_3.setRowStretch(0, 1)
        self.gridLayout_3.setRowStretch(1, 2)

        self.gridLayout_2.addWidget(self.groupBox_3, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"CAEMRA 1", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Form", u"NG\u01af\u1ee0NG AI", None))
        self.label_24.setText(QCoreApplication.translate("Form", u"1", None))
        self.label_22.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_21.setText(QCoreApplication.translate("Form", u"100", None))
        self.label_23.setText(QCoreApplication.translate("Form", u"NG\u01af\u1ee0NG:", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Form", u"NG\u01af\u1ee0NG AI", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"NG\u01af\u1ee0NG:", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"1", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"100", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Form", u"V\u1eca TR\u00cd LOGO", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"CAMERA 2", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Form", u"NG\u01af\u1ee0NG AI", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"NG\u01af\u1ee0NG:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"1", None))
        self.label.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"100", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"EMPTY", None))
    # retranslateUi

