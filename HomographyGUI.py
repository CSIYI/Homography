# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HomographyGUI.ui'
#
# Created: Mon Nov 28 15:15:37 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_homography(object):
    def setupUi(self, homography):
        homography.setObjectName("homography")
        homography.resize(755, 534)
        self.LoadSource = QtGui.QPushButton(homography)
        self.LoadSource.setGeometry(QtCore.QRect(10, 20, 121, 31))
        self.LoadSource.setObjectName("LoadSource")
        self.LoadTarget = QtGui.QPushButton(homography)
        self.LoadTarget.setGeometry(QtCore.QRect(390, 20, 121, 31))
        self.LoadTarget.setObjectName("LoadTarget")
        self.SourceImage = QtGui.QGraphicsView(homography)
        self.SourceImage.setGeometry(QtCore.QRect(10, 60, 351, 321))
        self.SourceImage.setObjectName("SourceImage")
        self.pt2 = QtGui.QLineEdit(homography)
        self.pt2.setGeometry(QtCore.QRect(630, 390, 113, 27))
        self.pt2.setObjectName("pt2")
        self.pt1 = QtGui.QLineEdit(homography)
        self.pt1.setGeometry(QtCore.QRect(510, 390, 113, 27))
        self.pt1.setObjectName("pt1")
        self.pt3 = QtGui.QLineEdit(homography)
        self.pt3.setGeometry(QtCore.QRect(510, 420, 113, 27))
        self.pt3.setObjectName("pt3")
        self.pt4 = QtGui.QLineEdit(homography)
        self.pt4.setGeometry(QtCore.QRect(630, 420, 113, 27))
        self.pt4.setObjectName("pt4")
        self.AcquirePoints = QtGui.QPushButton(homography)
        self.AcquirePoints.setGeometry(QtCore.QRect(390, 390, 111, 31))
        self.AcquirePoints.setObjectName("AcquirePoints")
        self.TargetImage = QtGui.QGraphicsView(homography)
        self.TargetImage.setGeometry(QtCore.QRect(390, 60, 351, 321))
        self.TargetImage.setObjectName("TargetImage")
        self.label = QtGui.QLabel(homography)
        self.label.setGeometry(QtCore.QRect(460, 460, 62, 17))
        self.label.setObjectName("label")
        self.Effect = QtGui.QComboBox(homography)
        self.Effect.setGeometry(QtCore.QRect(510, 450, 231, 31))
        self.Effect.setObjectName("Effect")
        self.Effect.addItem("")
        self.Effect.addItem("")
        self.Effect.addItem("")
        self.Effect.addItem("")
        self.Effect.addItem("")
        self.Effect.addItem("")
        self.Effect.addItem("")
        self.Transform = QtGui.QPushButton(homography)
        self.Transform.setGeometry(QtCore.QRect(370, 490, 121, 31))
        self.Transform.setObjectName("Transform")
        self.Reset = QtGui.QPushButton(homography)
        self.Reset.setGeometry(QtCore.QRect(500, 490, 121, 31))
        self.Reset.setObjectName("Reset")
        self.Save = QtGui.QPushButton(homography)
        self.Save.setGeometry(QtCore.QRect(630, 490, 121, 31))
        self.Save.setObjectName("Save")

        self.retranslateUi(homography)
        QtCore.QMetaObject.connectSlotsByName(homography)

    def retranslateUi(self, homography):
        homography.setWindowTitle(QtGui.QApplication.translate("homography", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.LoadSource.setText(QtGui.QApplication.translate("homography", "Load Source...", None, QtGui.QApplication.UnicodeUTF8))
        self.LoadTarget.setText(QtGui.QApplication.translate("homography", "Load Target...", None, QtGui.QApplication.UnicodeUTF8))
        self.AcquirePoints.setText(QtGui.QApplication.translate("homography", "Acquire Points", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("homography", "Effect", None, QtGui.QApplication.UnicodeUTF8))
        self.Effect.setItemText(0, QtGui.QApplication.translate("homography", "Nothing", None, QtGui.QApplication.UnicodeUTF8))
        self.Effect.setItemText(1, QtGui.QApplication.translate("homography", "Rotate 90° ", None, QtGui.QApplication.UnicodeUTF8))
        self.Effect.setItemText(2, QtGui.QApplication.translate("homography", "Rotate 180° ", None, QtGui.QApplication.UnicodeUTF8))
        self.Effect.setItemText(3, QtGui.QApplication.translate("homography", "Rotate 270° ", None, QtGui.QApplication.UnicodeUTF8))
        self.Effect.setItemText(4, QtGui.QApplication.translate("homography", "Flip Horizontally", None, QtGui.QApplication.UnicodeUTF8))
        self.Effect.setItemText(5, QtGui.QApplication.translate("homography", "Flip Vertically", None, QtGui.QApplication.UnicodeUTF8))
        self.Effect.setItemText(6, QtGui.QApplication.translate("homography", "Transpose", None, QtGui.QApplication.UnicodeUTF8))
        self.Transform.setText(QtGui.QApplication.translate("homography", "Transform", None, QtGui.QApplication.UnicodeUTF8))
        self.Reset.setText(QtGui.QApplication.translate("homography", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.Save.setText(QtGui.QApplication.translate("homography", "Save...", None, QtGui.QApplication.UnicodeUTF8))

