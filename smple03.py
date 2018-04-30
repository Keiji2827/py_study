#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from PyQt5.QtGui import *
from PyQt5.Qt import *

class Button01(QMainWindow):
    def __init__(self):
        # 親クラスの初期化
        super().__init__()
        # このクラスの初期化
#        self.initUI()
        # ColerDialog
        thisColor = QColor(0,0,0)
        self.ColorButton = QPushButton('select color', self)
        self.ColorButton.move(27, 15)

        # Qpainterを使う方法もあるが、ここではbackground-colorを設定することで色を変える
        self.myFrame = QFrame(self)
        self.myFrame.setStyleSheet("QtWidgets { background-color: %s }" % thisColor.name())
        self.myFrame.setGeometry(75,50,25,25)

        self.ColorButton.clicked.connect(self.showDialog)

        self.setGeometry(200,100,25,25)

        self.show()

    def showDialog(self):
        # ダイアログを表示する
        getcolor = QColorDialog.getColor()

        if getcolor.isValid():
            self.myFrame.setStyleSheet("QtWidgets { background-color: %s }" % getcolor.name())

    # 初期化
    def initUI(self):
        # ボタンの追加
        btn1 = QPushButton("Button01", self)
        # クリックされたときの登録
        btn1.clicked.connect(self.button01clicked)

        # 以下はなんだろう
#        self.statusBar()

        # Windowの名前
        self.setWindowTitle('Button Window')
#        self.show()

    # クリックされたときの動作の定義
    def button01clicked(self):
        sender = self.sender()
        # Windowの下部に文字列を表示
        self.statusBar().showMessage(sender.text() + 'Push Button01')



# メイン関数
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Button01()
    sys.exit(app.exec_())
