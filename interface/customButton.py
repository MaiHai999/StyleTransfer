
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import os



class customButton(QToolButton):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(40)
        self.setFixedHeight(20)

        self.setStyleSheet('''
                    QToolButton {
                        border: 2px solid #ccc; 
                        border-radius: 10px;
                    }
                    
                    QToolButton:hover {
                        background-color: rgb(255,182,182); /* Màu nền sẫm hơn khi rê chuột qua */
                    }
                    
                ''')


        self.setIcon(QIcon(os.path.join('asset/icon', "352278_cloud_upload_icon.png")))

