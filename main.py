import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from interface.wigdetUpdateIMG import *
from model.mainModel import TransferStyle
class TransferStyleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.Transfer = TransferStyle()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Image Uploader App")
        self.setGeometry(100, 100, 400, 700)

        layout = QVBoxLayout()

        self.ContentImg = widgetUploadIMGLable("Content Image")
        self.StyleImg = widgetUploadIMGLable("Style Image")
        self.TransferStyle = widgetTransferStyle("Transfer Style Image")

        uploadWidget = QWidget()
        uploadWidgetlayout = QHBoxLayout()
        uploadWidget.setLayout(uploadWidgetlayout)
        uploadWidgetlayout.addWidget(self.ContentImg)
        uploadWidgetlayout.addWidget(self.StyleImg)

        layout.addWidget(uploadWidget)
        layout.addWidget(self.TransferStyle,2)

        self.TransferStyle.widgetUploadIMG.buttonOpen.clicked.connect(self.transfer)

        self.setLayout(layout)

    def transfer(self):
        pathContentIMG = self.ContentImg.widgetUploadIMG.path
        pathStyleIMG = self.StyleImg.widgetUploadIMG.path
        self.Transfer.run(pathContentIMG , pathStyleIMG , 2)
        self.TransferStyle.widgetUploadIMG.widgetIMG.setPath(self.Transfer.path)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TransferStyleApp()
    ex.show()
    sys.exit(app.exec())
