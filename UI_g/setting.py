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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QFrame, QGridLayout,
    QGroupBox, QLabel, QSizePolicy, QSpinBox,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(828, 517)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.groupBox_2 = QGroupBox(self.frame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        font = QFont()
        font.setBold(True)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.groupBox_8 = QGroupBox(self.groupBox_2)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_10 = QGridLayout(self.groupBox_8)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.sp_conf_TS2 = QDoubleSpinBox(self.groupBox_8)
        self.sp_conf_TS2.setObjectName(u"sp_conf_TS2")
        self.sp_conf_TS2.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_conf_TS2.setMinimum(0.010000000000000)
        self.sp_conf_TS2.setMaximum(0.990000000000000)
        self.sp_conf_TS2.setSingleStep(0.010000000000000)

        self.gridLayout_10.addWidget(self.sp_conf_TS2, 2, 5, 1, 1)

        self.label_23 = QLabel(self.groupBox_8)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_10.addWidget(self.label_23, 1, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox_8)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_3, 1, 6, 1, 1)

        self.lbl_4 = QLabel(self.groupBox_8)
        self.lbl_4.setObjectName(u"lbl_4")
        self.lbl_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lbl_4, 1, 1, 1, 1)

        self.label = QLabel(self.groupBox_8)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label, 1, 2, 1, 1)

        self.lbl_7 = QLabel(self.groupBox_8)
        self.lbl_7.setObjectName(u"lbl_7")
        self.lbl_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lbl_7, 1, 7, 1, 1)

        self.sp_area_TS2 = QSpinBox(self.groupBox_8)
        self.sp_area_TS2.setObjectName(u"sp_area_TS2")
        self.sp_area_TS2.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_area_TS2.setMinimum(2)
        self.sp_area_TS2.setMaximum(99999)

        self.gridLayout_10.addWidget(self.sp_area_TS2, 1, 5, 1, 1)

        self.sp_conf_TS1 = QDoubleSpinBox(self.groupBox_8)
        self.sp_conf_TS1.setObjectName(u"sp_conf_TS1")
        self.sp_conf_TS1.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_conf_TS1.setMinimum(0.010000000000000)
        self.sp_conf_TS1.setMaximum(0.990000000000000)
        self.sp_conf_TS1.setSingleStep(0.010000000000000)

        self.gridLayout_10.addWidget(self.sp_conf_TS1, 2, 3, 1, 1)

        self.label_24 = QLabel(self.groupBox_8)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_10.addWidget(self.label_24, 2, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox_8)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_2, 1, 4, 1, 1)

        self.sp_area_TS1 = QSpinBox(self.groupBox_8)
        self.sp_area_TS1.setObjectName(u"sp_area_TS1")
        self.sp_area_TS1.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_area_TS1.setMinimum(1)
        self.sp_area_TS1.setMaximum(99999)

        self.gridLayout_10.addWidget(self.sp_area_TS1, 1, 3, 1, 1)

        self.lbl_3 = QLabel(self.groupBox_8)
        self.lbl_3.setObjectName(u"lbl_3")
        self.lbl_3.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.lbl_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lbl_3, 0, 6, 1, 1)

        self.lbl_2 = QLabel(self.groupBox_8)
        self.lbl_2.setObjectName(u"lbl_2")
        self.lbl_2.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.lbl_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lbl_2, 0, 4, 1, 1)

        self.lbl_1 = QLabel(self.groupBox_8)
        self.lbl_1.setObjectName(u"lbl_1")
        self.lbl_1.setMaximumSize(QSize(32, 30))
        self.lbl_1.setStyleSheet(u"background-color: rgb(0, 255, 0);")
        self.lbl_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lbl_1, 0, 2, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_8, 0, 0, 1, 1)

        self.groupBox_9 = QGroupBox(self.groupBox_2)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_11 = QGridLayout(self.groupBox_9)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.label_4 = QLabel(self.groupBox_9)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.label_4, 1, 2, 1, 1)

        self.label_6 = QLabel(self.groupBox_9)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.label_6, 1, 6, 1, 1)

        self.label_27 = QLabel(self.groupBox_9)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout_11.addWidget(self.label_27, 2, 0, 1, 1)

        self.lbl_19 = QLabel(self.groupBox_9)
        self.lbl_19.setObjectName(u"lbl_19")
        self.lbl_19.setMaximumSize(QSize(32, 30))
        self.lbl_19.setStyleSheet(u"background-color: rgb(0, 255, 0);")
        self.lbl_19.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lbl_19, 0, 2, 1, 1)

        self.lbl_23 = QLabel(self.groupBox_9)
        self.lbl_23.setObjectName(u"lbl_23")
        self.lbl_23.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lbl_23, 1, 7, 1, 1)

        self.lbl_26 = QLabel(self.groupBox_9)
        self.lbl_26.setObjectName(u"lbl_26")
        self.lbl_26.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.lbl_26.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lbl_26, 0, 6, 1, 1)

        self.lbl_27 = QLabel(self.groupBox_9)
        self.lbl_27.setObjectName(u"lbl_27")
        self.lbl_27.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lbl_27, 1, 1, 1, 1)

        self.lbl_22 = QLabel(self.groupBox_9)
        self.lbl_22.setObjectName(u"lbl_22")
        self.lbl_22.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.lbl_22.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lbl_22, 0, 4, 1, 1)

        self.label_28 = QLabel(self.groupBox_9)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_11.addWidget(self.label_28, 1, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox_9)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.label_5, 1, 4, 1, 1)

        self.sp_area_LS1 = QSpinBox(self.groupBox_9)
        self.sp_area_LS1.setObjectName(u"sp_area_LS1")
        self.sp_area_LS1.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_area_LS1.setMinimum(1)
        self.sp_area_LS1.setMaximum(99999)

        self.gridLayout_11.addWidget(self.sp_area_LS1, 1, 3, 1, 1)

        self.sp_area_LS2 = QSpinBox(self.groupBox_9)
        self.sp_area_LS2.setObjectName(u"sp_area_LS2")
        self.sp_area_LS2.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_area_LS2.setMinimum(2)
        self.sp_area_LS2.setMaximum(99999)

        self.gridLayout_11.addWidget(self.sp_area_LS2, 1, 5, 1, 1)

        self.sp_conf_LS1 = QDoubleSpinBox(self.groupBox_9)
        self.sp_conf_LS1.setObjectName(u"sp_conf_LS1")
        self.sp_conf_LS1.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_conf_LS1.setMinimum(0.010000000000000)
        self.sp_conf_LS1.setMaximum(0.990000000000000)
        self.sp_conf_LS1.setSingleStep(0.010000000000000)

        self.gridLayout_11.addWidget(self.sp_conf_LS1, 2, 3, 1, 1)

        self.sp_conf_LS2 = QDoubleSpinBox(self.groupBox_9)
        self.sp_conf_LS2.setObjectName(u"sp_conf_LS2")
        self.sp_conf_LS2.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_conf_LS2.setMinimum(0.010000000000000)
        self.sp_conf_LS2.setMaximum(0.990000000000000)
        self.sp_conf_LS2.setSingleStep(0.010000000000000)

        self.gridLayout_11.addWidget(self.sp_conf_LS2, 2, 5, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_9, 1, 0, 1, 1)

        self.groupBox_10 = QGroupBox(self.groupBox_2)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_12 = QGridLayout(self.groupBox_10)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.lbl_35 = QLabel(self.groupBox_10)
        self.lbl_35.setObjectName(u"lbl_35")
        self.lbl_35.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.lbl_35.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.lbl_35, 0, 6, 1, 1)

        self.lbl_31 = QLabel(self.groupBox_10)
        self.lbl_31.setObjectName(u"lbl_31")
        self.lbl_31.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.lbl_31.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.lbl_31, 0, 4, 1, 1)

        self.lbl_36 = QLabel(self.groupBox_10)
        self.lbl_36.setObjectName(u"lbl_36")
        self.lbl_36.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.lbl_36, 1, 1, 1, 1)

        self.label_11 = QLabel(self.groupBox_10)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.label_11, 1, 4, 1, 1)

        self.lbl_28 = QLabel(self.groupBox_10)
        self.lbl_28.setObjectName(u"lbl_28")
        self.lbl_28.setMaximumSize(QSize(32, 30))
        self.lbl_28.setStyleSheet(u"background-color: rgb(0, 255, 0);")
        self.lbl_28.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.lbl_28, 0, 2, 1, 1)

        self.label_12 = QLabel(self.groupBox_10)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.label_12, 1, 6, 1, 1)

        self.label_10 = QLabel(self.groupBox_10)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.label_10, 1, 2, 1, 1)

        self.label_30 = QLabel(self.groupBox_10)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_12.addWidget(self.label_30, 1, 0, 1, 1)

        self.lbl_32 = QLabel(self.groupBox_10)
        self.lbl_32.setObjectName(u"lbl_32")
        self.lbl_32.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.lbl_32, 1, 7, 1, 1)

        self.label_29 = QLabel(self.groupBox_10)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_12.addWidget(self.label_29, 2, 0, 1, 1)

        self.sp_area_HC1 = QSpinBox(self.groupBox_10)
        self.sp_area_HC1.setObjectName(u"sp_area_HC1")
        self.sp_area_HC1.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_area_HC1.setMinimum(1)
        self.sp_area_HC1.setMaximum(99999)

        self.gridLayout_12.addWidget(self.sp_area_HC1, 1, 3, 1, 1)

        self.sp_area_HC2 = QSpinBox(self.groupBox_10)
        self.sp_area_HC2.setObjectName(u"sp_area_HC2")
        self.sp_area_HC2.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_area_HC2.setMinimum(2)
        self.sp_area_HC2.setMaximum(99999)

        self.gridLayout_12.addWidget(self.sp_area_HC2, 1, 5, 1, 1)

        self.sp_conf_HC1 = QDoubleSpinBox(self.groupBox_10)
        self.sp_conf_HC1.setObjectName(u"sp_conf_HC1")
        self.sp_conf_HC1.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_conf_HC1.setMinimum(0.010000000000000)
        self.sp_conf_HC1.setMaximum(0.990000000000000)
        self.sp_conf_HC1.setSingleStep(0.010000000000000)

        self.gridLayout_12.addWidget(self.sp_conf_HC1, 2, 3, 1, 1)

        self.sp_conf_HC2 = QDoubleSpinBox(self.groupBox_10)
        self.sp_conf_HC2.setObjectName(u"sp_conf_HC2")
        self.sp_conf_HC2.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_conf_HC2.setMinimum(0.010000000000000)
        self.sp_conf_HC2.setMaximum(0.990000000000000)
        self.sp_conf_HC2.setSingleStep(0.010000000000000)

        self.gridLayout_12.addWidget(self.sp_conf_HC2, 2, 5, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_10, 2, 0, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_2, 0, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.frame)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font)
        self.groupBox_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_2 = QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox_11 = QGroupBox(self.groupBox_3)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.groupBox_11.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_13 = QGridLayout(self.groupBox_11)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.label_25 = QLabel(self.groupBox_11)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_13.addWidget(self.label_25, 2, 0, 1, 1)

        self.lbl_18 = QLabel(self.groupBox_11)
        self.lbl_18.setObjectName(u"lbl_18")
        self.lbl_18.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.lbl_18, 1, 1, 1, 1)

        self.lbl_12 = QLabel(self.groupBox_11)
        self.lbl_12.setObjectName(u"lbl_12")
        self.lbl_12.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.lbl_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.lbl_12, 0, 6, 1, 1)

        self.lbl_15 = QLabel(self.groupBox_11)
        self.lbl_15.setObjectName(u"lbl_15")
        self.lbl_15.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.lbl_15.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.lbl_15, 0, 4, 1, 1)

        self.lbl_17 = QLabel(self.groupBox_11)
        self.lbl_17.setObjectName(u"lbl_17")
        self.lbl_17.setMaximumSize(QSize(32, 30))
        self.lbl_17.setStyleSheet(u"background-color: rgb(0, 255, 0);")
        self.lbl_17.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.lbl_17, 0, 2, 1, 1)

        self.label_7 = QLabel(self.groupBox_11)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.label_7, 1, 2, 1, 1)

        self.label_26 = QLabel(self.groupBox_11)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout_13.addWidget(self.label_26, 1, 0, 1, 1)

        self.label_9 = QLabel(self.groupBox_11)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.label_9, 1, 6, 1, 1)

        self.lbl_10 = QLabel(self.groupBox_11)
        self.lbl_10.setObjectName(u"lbl_10")
        self.lbl_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.lbl_10, 1, 7, 1, 1)

        self.label_8 = QLabel(self.groupBox_11)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.label_8, 1, 4, 1, 1)

        self.sp_area_CD1 = QSpinBox(self.groupBox_11)
        self.sp_area_CD1.setObjectName(u"sp_area_CD1")
        self.sp_area_CD1.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_area_CD1.setMinimum(1)
        self.sp_area_CD1.setMaximum(99999)

        self.gridLayout_13.addWidget(self.sp_area_CD1, 1, 3, 1, 1)

        self.sp_area_CD2 = QSpinBox(self.groupBox_11)
        self.sp_area_CD2.setObjectName(u"sp_area_CD2")
        self.sp_area_CD2.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_area_CD2.setMinimum(2)
        self.sp_area_CD2.setMaximum(99999)

        self.gridLayout_13.addWidget(self.sp_area_CD2, 1, 5, 1, 1)

        self.sp_conf_CD1 = QDoubleSpinBox(self.groupBox_11)
        self.sp_conf_CD1.setObjectName(u"sp_conf_CD1")
        self.sp_conf_CD1.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_conf_CD1.setMinimum(0.010000000000000)
        self.sp_conf_CD1.setMaximum(0.990000000000000)
        self.sp_conf_CD1.setSingleStep(0.010000000000000)

        self.gridLayout_13.addWidget(self.sp_conf_CD1, 2, 3, 1, 1)

        self.sp_conf_CD2 = QDoubleSpinBox(self.groupBox_11)
        self.sp_conf_CD2.setObjectName(u"sp_conf_CD2")
        self.sp_conf_CD2.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_conf_CD2.setMinimum(0.010000000000000)
        self.sp_conf_CD2.setMaximum(0.990000000000000)
        self.sp_conf_CD2.setSingleStep(0.010000000000000)

        self.gridLayout_13.addWidget(self.sp_conf_CD2, 2, 5, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_11, 0, 0, 1, 1)

        self.groupBox_12 = QGroupBox(self.groupBox_3)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_14 = QGridLayout(self.groupBox_12)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.label_17 = QLabel(self.groupBox_12)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.label_17, 1, 4, 1, 1)

        self.lbl_40 = QLabel(self.groupBox_12)
        self.lbl_40.setObjectName(u"lbl_40")
        self.lbl_40.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.lbl_40.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lbl_40, 0, 4, 1, 1)

        self.label_16 = QLabel(self.groupBox_12)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.label_16, 1, 2, 1, 1)

        self.lbl_37 = QLabel(self.groupBox_12)
        self.lbl_37.setObjectName(u"lbl_37")
        self.lbl_37.setMaximumSize(QSize(32, 30))
        self.lbl_37.setStyleSheet(u"background-color: rgb(0, 255, 0);")
        self.lbl_37.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lbl_37, 0, 2, 1, 1)

        self.label_32 = QLabel(self.groupBox_12)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_14.addWidget(self.label_32, 1, 0, 1, 1)

        self.lbl_45 = QLabel(self.groupBox_12)
        self.lbl_45.setObjectName(u"lbl_45")
        self.lbl_45.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lbl_45, 1, 1, 1, 1)

        self.lbl_44 = QLabel(self.groupBox_12)
        self.lbl_44.setObjectName(u"lbl_44")
        self.lbl_44.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.lbl_44.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lbl_44, 0, 6, 1, 1)

        self.lbl_41 = QLabel(self.groupBox_12)
        self.lbl_41.setObjectName(u"lbl_41")
        self.lbl_41.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lbl_41, 1, 7, 1, 1)

        self.label_31 = QLabel(self.groupBox_12)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_14.addWidget(self.label_31, 2, 0, 1, 1)

        self.label_18 = QLabel(self.groupBox_12)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.label_18, 1, 6, 1, 1)

        self.sp_area_OV1 = QSpinBox(self.groupBox_12)
        self.sp_area_OV1.setObjectName(u"sp_area_OV1")
        self.sp_area_OV1.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_area_OV1.setMinimum(1)
        self.sp_area_OV1.setMaximum(99999)

        self.gridLayout_14.addWidget(self.sp_area_OV1, 1, 3, 1, 1)

        self.sp_area_OV2 = QSpinBox(self.groupBox_12)
        self.sp_area_OV2.setObjectName(u"sp_area_OV2")
        self.sp_area_OV2.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_area_OV2.setMinimum(2)
        self.sp_area_OV2.setMaximum(99999)

        self.gridLayout_14.addWidget(self.sp_area_OV2, 1, 5, 1, 1)

        self.sp_conf_OV1 = QDoubleSpinBox(self.groupBox_12)
        self.sp_conf_OV1.setObjectName(u"sp_conf_OV1")
        self.sp_conf_OV1.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_conf_OV1.setMinimum(0.010000000000000)
        self.sp_conf_OV1.setMaximum(0.990000000000000)
        self.sp_conf_OV1.setSingleStep(0.010000000000000)

        self.gridLayout_14.addWidget(self.sp_conf_OV1, 2, 3, 1, 1)

        self.sp_conf_OV2 = QDoubleSpinBox(self.groupBox_12)
        self.sp_conf_OV2.setObjectName(u"sp_conf_OV2")
        self.sp_conf_OV2.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_conf_OV2.setMinimum(0.010000000000000)
        self.sp_conf_OV2.setMaximum(0.990000000000000)
        self.sp_conf_OV2.setSingleStep(0.010000000000000)

        self.gridLayout_14.addWidget(self.sp_conf_OV2, 2, 5, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_12, 1, 0, 1, 1)

        self.groupBox_13 = QGroupBox(self.groupBox_3)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.groupBox_13.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_15 = QGridLayout(self.groupBox_13)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.lbl_54 = QLabel(self.groupBox_13)
        self.lbl_54.setObjectName(u"lbl_54")
        self.lbl_54.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lbl_54, 1, 1, 1, 1)

        self.lbl_49 = QLabel(self.groupBox_13)
        self.lbl_49.setObjectName(u"lbl_49")
        self.lbl_49.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.lbl_49.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lbl_49, 0, 4, 1, 1)

        self.label_13 = QLabel(self.groupBox_13)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_13, 1, 2, 1, 1)

        self.label_15 = QLabel(self.groupBox_13)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_15, 1, 6, 1, 1)

        self.lbl_46 = QLabel(self.groupBox_13)
        self.lbl_46.setObjectName(u"lbl_46")
        self.lbl_46.setMaximumSize(QSize(32, 30))
        self.lbl_46.setStyleSheet(u"background-color: rgb(0, 255, 0);")
        self.lbl_46.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lbl_46, 0, 2, 1, 1)

        self.label_33 = QLabel(self.groupBox_13)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_15.addWidget(self.label_33, 2, 0, 1, 1)

        self.label_14 = QLabel(self.groupBox_13)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_14, 1, 4, 1, 1)

        self.lbl_53 = QLabel(self.groupBox_13)
        self.lbl_53.setObjectName(u"lbl_53")
        self.lbl_53.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.lbl_53.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lbl_53, 0, 6, 1, 1)

        self.lbl_50 = QLabel(self.groupBox_13)
        self.lbl_50.setObjectName(u"lbl_50")
        self.lbl_50.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lbl_50, 1, 7, 1, 1)

        self.label_34 = QLabel(self.groupBox_13)
        self.label_34.setObjectName(u"label_34")

        self.gridLayout_15.addWidget(self.label_34, 1, 0, 1, 1)

        self.sp_area_C1 = QSpinBox(self.groupBox_13)
        self.sp_area_C1.setObjectName(u"sp_area_C1")
        self.sp_area_C1.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_area_C1.setMinimum(1)
        self.sp_area_C1.setMaximum(99999)

        self.gridLayout_15.addWidget(self.sp_area_C1, 1, 3, 1, 1)

        self.sp_area_C2 = QSpinBox(self.groupBox_13)
        self.sp_area_C2.setObjectName(u"sp_area_C2")
        self.sp_area_C2.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_area_C2.setMinimum(2)
        self.sp_area_C2.setMaximum(99999)

        self.gridLayout_15.addWidget(self.sp_area_C2, 1, 5, 1, 1)

        self.sp_conf_C1 = QDoubleSpinBox(self.groupBox_13)
        self.sp_conf_C1.setObjectName(u"sp_conf_C1")
        self.sp_conf_C1.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_conf_C1.setMinimum(0.010000000000000)
        self.sp_conf_C1.setMaximum(0.990000000000000)
        self.sp_conf_C1.setSingleStep(0.010000000000000)

        self.gridLayout_15.addWidget(self.sp_conf_C1, 2, 3, 1, 1)

        self.sp_conf_C2 = QDoubleSpinBox(self.groupBox_13)
        self.sp_conf_C2.setObjectName(u"sp_conf_C2")
        self.sp_conf_C2.setStyleSheet(u"background-color: rgb(200, 195, 195);")
        self.sp_conf_C2.setMinimum(0.010000000000000)
        self.sp_conf_C2.setMaximum(0.990000000000000)
        self.sp_conf_C2.setSingleStep(0.010000000000000)

        self.gridLayout_15.addWidget(self.sp_conf_C2, 2, 5, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_13, 2, 0, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_3, 0, 1, 1, 1)

        self.gridLayout_4.setColumnStretch(0, 1)
        self.gridLayout_4.setColumnStretch(1, 1)

        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"CAMERA 1", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Form", u"AI1-NG_THI\u1ebeU S\u01a0N", None))
        self.label_23.setText(QCoreApplication.translate("Form", u"Di\u1ec7n t\u00edch:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"->", None))
        self.lbl_4.setText(QCoreApplication.translate("Form", u"0 ", None))
        self.label.setText(QCoreApplication.translate("Form", u"->", None))
        self.lbl_7.setText(QCoreApplication.translate("Form", u"max", None))
        self.label_24.setText(QCoreApplication.translate("Form", u"\u0110\u1ed9 tin c\u1eady:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"->", None))
        self.lbl_3.setText(QCoreApplication.translate("Form", u"NG", None))
        self.lbl_2.setText(QCoreApplication.translate("Form", u"NG", None))
        self.lbl_1.setText(QCoreApplication.translate("Form", u"OK", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("Form", u"AI1-NG_LEM S\u01a0N", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"->", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"->", None))
        self.label_27.setText(QCoreApplication.translate("Form", u"\u0110\u1ed9 tin c\u1eady:", None))
        self.lbl_19.setText(QCoreApplication.translate("Form", u"OK", None))
        self.lbl_23.setText(QCoreApplication.translate("Form", u"max", None))
        self.lbl_26.setText(QCoreApplication.translate("Form", u"NG", None))
        self.lbl_27.setText(QCoreApplication.translate("Form", u"0 ", None))
        self.lbl_22.setText(QCoreApplication.translate("Form", u"NG", None))
        self.label_28.setText(QCoreApplication.translate("Form", u"Di\u1ec7n t\u00edch:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"->", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("Form", u"AI1-NG_HO\u00c1 CH\u1ea4T", None))
        self.lbl_35.setText(QCoreApplication.translate("Form", u"NG", None))
        self.lbl_31.setText(QCoreApplication.translate("Form", u"NG", None))
        self.lbl_36.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"->", None))
        self.lbl_28.setText(QCoreApplication.translate("Form", u"OK", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"->", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"->", None))
        self.label_30.setText(QCoreApplication.translate("Form", u"Di\u1ec7n t\u00edch:", None))
        self.lbl_32.setText(QCoreApplication.translate("Form", u"max", None))
        self.label_29.setText(QCoreApplication.translate("Form", u"\u0110\u1ed9 tin c\u1eady:", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"CAMERA 2", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("Form", u"AI2-NG_CH\u1ea4M \u0110EN", None))
        self.label_25.setText(QCoreApplication.translate("Form", u"\u0110\u1ed9 tin c\u1eady:", None))
        self.lbl_18.setText(QCoreApplication.translate("Form", u"0", None))
        self.lbl_12.setText(QCoreApplication.translate("Form", u"NG", None))
        self.lbl_15.setText(QCoreApplication.translate("Form", u"NG", None))
        self.lbl_17.setText(QCoreApplication.translate("Form", u"OK", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"->", None))
        self.label_26.setText(QCoreApplication.translate("Form", u"Di\u1ec7n t\u00edch:", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"->", None))
        self.lbl_10.setText(QCoreApplication.translate("Form", u"max", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"->", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("Form", u"AI2-NG_\u1ed0 V\u00c0NG", None))
        self.label_17.setText(QCoreApplication.translate("Form", u"->", None))
        self.lbl_40.setText(QCoreApplication.translate("Form", u"NG", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"->", None))
        self.lbl_37.setText(QCoreApplication.translate("Form", u"OK", None))
        self.label_32.setText(QCoreApplication.translate("Form", u"Di\u1ec7n t\u00edch:", None))
        self.lbl_45.setText(QCoreApplication.translate("Form", u"0", None))
        self.lbl_44.setText(QCoreApplication.translate("Form", u"NG", None))
        self.lbl_41.setText(QCoreApplication.translate("Form", u"max", None))
        self.label_31.setText(QCoreApplication.translate("Form", u"\u0110\u1ed9 tin c\u1eady:", None))
        self.label_18.setText(QCoreApplication.translate("Form", u"->", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("Form", u"AI2-NG_C\u1ea4N", None))
        self.lbl_54.setText(QCoreApplication.translate("Form", u"0", None))
        self.lbl_49.setText(QCoreApplication.translate("Form", u"NG", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"->", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"->", None))
        self.lbl_46.setText(QCoreApplication.translate("Form", u"OK", None))
        self.label_33.setText(QCoreApplication.translate("Form", u"\u0110\u1ed9 tin c\u1eady:", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"->", None))
        self.lbl_53.setText(QCoreApplication.translate("Form", u"NG", None))
        self.lbl_50.setText(QCoreApplication.translate("Form", u"max", None))
        self.label_34.setText(QCoreApplication.translate("Form", u"Di\u1ec7n t\u00edch:", None))
    # retranslateUi

