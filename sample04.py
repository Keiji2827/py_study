import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import *

class FormTest(QDialog):
    def __init__(self, parent=None):
        super(FormTest, self).__init__(parent)

        self.initButton()
        self.initUI()

        self.setGeometry(700,300,300,300)
        self.setWindowTitle("QComboBox")

    def initUI(self):
        self.label = QLabel("東京",self)
        combo = QComboBox(self)
        combo.addItem("東京")
        combo.addItem("足立区")
        combo.addItem("台東区")
        combo.addItem("千代田区")
        combo.addItem("品川区")
        combo.addItem("墨田区")
        combo.move(50,50)
        self.label.move(50,150)
        combo.activated[str].connect(self.onActivated)

    def onActivated(self, text):
        self.label.setText(text)
        self.label.adjustSize()

    def initButton(self):
        btn1 = QPushButton("One")
        #btn1.setCheckable(True)
        btn1.setFocusPolicy(Qt.NoFocus)

        rbtn2 = QRadioButton("Two")
        rbtn2.setCheckable(True)
        rbtn2.setFocusPolicy(Qt.NoFocus)

        self.group = QButtonGroup()
        self.group.addButton(btn1,1)
        self.group.addButton(rbtn2,2)

        self.label = QLabel("ラジオボタンをクリックしてください")

        #QHBoxLayout()は、Horizontal（水平方向）にレイアウトします
        layout = QHBoxLayout()

        layout.addWidget(btn1)
        layout.addWidget(rbtn2)

        #QVBoxLayout()は、vertical（垂直方向）にレイアウトします
        Vlayout = QVBoxLayout()

        Vlayout.addLayout(layout)
        Vlayout.addWidget(self.label)
        Vlayout.addWidget(self.label)

        self.setLayout(Vlayout)

        btn1.clicked.connect(self.btnclicked)
        rbtn2.clicked.connect(self.rbtnclicked)

    def btnclicked(self):
        button = self.sender()
        if button is None or not isinstance(button,QPushButton):
            return
        self.label.setText("あなたは'%s'のラジをボタンをクリックしました" % button.text())
        self.label.adjustSize()

    def rbtnclicked(self):
        radiobutton = self.sender()
        if radiobutton is None or not isinstance(radiobutton,QRadioButton):
            return
        self.label.setText("あなたは'%s'のラジオボタンをチェックしました" % radiobutton.text())
        self.label.adjustSize()

class myTableModel(QAbstractTableModel):
    def __init__(self, list, headers = [], parent = None):
        QAbstractTableModel.__init__(self, parent)
        self.list = list
        self.headers = headers

    def rowCount(self, parent):
        return len(self.list)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle("plastique")

    listView = QListView()
    listView.show()

    comboBox = QComboBox()
    comboBox.show()

    tableView = QTableView()
    tableView.show()

    headers = ["000","001","002"]

    tableData0 = [
                ['abc',100,200],
                ['def',130,260],
                ['ghi',190,300],
                ['jkl',700,500],
                ['lmn',800,980]
    ]

    model = myTableModel(tableData0, headers)

    listView.setModel(model)
    comboBox.setModel(model)
    tableView.setModel(model)

#    formtest = FormTest()
#    formtest.show()
    sys.exit(app.exec_())
