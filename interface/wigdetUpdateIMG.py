from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import os
from interface.penalShowImg import widgetIMG
from interface.customButton import customButton

class widgetUploadIMG(QWidget):
    def __init__(self):
        super().__init__()
        self.path = None

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        self.widgetIMG = widgetIMG()

        widgetButon = QWidget()
        widgetButonLayout = QHBoxLayout()
        widgetButonLayout.setSpacing(0)
        widgetButonLayout.setContentsMargins(0, 5, 0, 5)
        widgetButon.setLayout(widgetButonLayout)

        self.buttonOpen = customButton()
        self.buttonOpen.clicked.connect(self.openDialog)
        widgetButonLayout.addWidget(self.buttonOpen)

        layout.addWidget(self.widgetIMG,1000)
        layout.addWidget(widgetButon)

        self.setLayout(layout)


    def openDialog(self):
        fname = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "${HOME}",
            "Image Files (*.jpg *.png)",
        )
        self.path = fname[0]
        self.widgetIMG.setPath(self.path)

class widgetUploadIMGLable(QWidget):
    def __init__(self, name):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        widgetLable = QWidget()
        lableLayout = QHBoxLayout()
        lableLayout.setSpacing(0)
        lableLayout.setContentsMargins(0, 0, 0, 0)
        widgetLable.setLayout(lableLayout)
        lable = QLabel(name)
        lableLayout.addStretch(1)
        lableLayout.addWidget(lable)
        lableLayout.addStretch(1)

        self.widgetUploadIMG = widgetUploadIMG()

        layout.addWidget(widgetLable)
        layout.addWidget(self.widgetUploadIMG)

class widgetTransferStyle(widgetUploadIMGLable):
    def __init__(self, name):
        super().__init__(name)
        self.widgetUploadIMG.buttonOpen.setIcon(QIcon(os.path.join('asset/icon', "tranfer.png")))
        self.widgetUploadIMG.buttonOpen.clicked.disconnect(self.widgetUploadIMG.openDialog)





