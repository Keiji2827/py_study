# Atomからの実行はCirl + Shift + B

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
import sys, csv


"""
class Window (QWidget):
    def __init__ (self):
        QWidget.__init__(self, None)
        self.setWindowTitle('Table')

"""

class View (QWidget):
    def __init__ (self, parent=None):
        super(View, self).__init__()

        #サイズ固定
        self.setFixedSize(850, 500)

        #Viewを作成
        #tableViewをここで定義
        self.tableView = QTableView()
        #table上をクリックしたときのイベント
        self.tableView.clicked.connect(self.viewClicked)

        #Viewの罫をブラックにする
        self.tableView.setStyleSheet("QTableView{gridline-color: black}")

        self.headers = ["▽", "AAAAAA", "BBBBBB", "CCCCCCC", "DDDDD", "EEEEE", "FFFFF", "GGGGG"]
        tableData0 = [
                     [QCheckBox(''), "ああああああ", "てすと", "ﾃｽﾄ", "評価", "000000", "000000", 1],
                     ]

        #モデルを作成
        #MyTableModelは下部で定義
        self.model = MyTableModel(tableData0, self.headers)
        self.tableView.setModel(self.model)

        #Insert、remove用の選択行に行の最大値をセット
        self.selectRow = self.model.rowCount(QModelIndex())

        #csv用のファイルフィルタをセット
        self.filters = "CSV files (*.csv)"

        #ファイル名を初期化
        self.fileName = None

        #ボタン作成
        self.buttonNew = QPushButton('NEW', self)
        self.buttonOpen = QPushButton('Open', self)
        self.buttonSave = QPushButton('Save', self)
        self.buttonAdd = QPushButton('add', self)
        self.buttonDell = QPushButton('Dell', self)

        #ボタングループをセット
        #ボタングループの意味は何？
        self.group = QButtonGroup()
        self.group.addButton(self.buttonNew)
        self.group.addButton(self.buttonOpen)
        self.group.addButton(self.buttonSave)
        self.group.addButton(self.buttonAdd)
        self.group.addButton(self.buttonDell)

        #Signal、Slotを設定
        self.buttonNew.clicked.connect(self.handleNew)
        self.buttonOpen.clicked.connect(self.handleOpen)
        self.buttonSave.clicked.connect(self.handleSave)
        self.buttonAdd.clicked.connect(self.insertRows)
        self.buttonDell.clicked.connect(self.removeRows)

        #水平レイアウトを設定
        buttonlayout = QHBoxLayout()

        buttonlayout.addWidget(self.buttonNew)
        buttonlayout.addWidget(self.buttonOpen)
        buttonlayout.addWidget(self.buttonSave)
        buttonlayout.addWidget(self.buttonAdd)
        buttonlayout.addWidget(self.buttonDell)

        #垂直レイアウトを設定
        Vlayout = QVBoxLayout()
        Vlayout.addWidget(self.tableView)
        Vlayout.addLayout(buttonlayout)

        #全体のレイアウトをセット
        self.setLayout(Vlayout)

    #保存処理→CSVで保存
    def handleSave(self):
        print("handleSave")
        if self.fileName == None or self.fileName == '':
            self.fileName, self.filters = QFileDialog.getSaveFileName(self, \
            filter=self.filters)
        if(self.fileName != ''):
            with open(self.fileName, 'wt') as stream:
                csvout = csv.writer(stream, lineterminator='\n')
                csvout.writerow(self.headers)
                for row in range(self.model.rowCount(QModelIndex())):
                    print(self.model.rowCount(QModelIndex()))
                    rowdata = []
                    for column in range(self.model.columnCount(QModelIndex())):
                        item = self.model.index( row, column, QModelIndex() ).data( Qt.DisplayRole )
                        if column == 0:
                            rowdata.append('')
                            continue

                        if item is not None:
                            rowdata.append(item)
                        else:
                            rowdata.append('')
                    csvout.writerow(rowdata)
                    print(rowdata)

    #ファイルオープン処理
    def handleOpen(self):
        print("handleOpen")
        self.fileName, self.filterName = QFileDialog.getOpenFileName(self)

        if self.fileName != '':
            with open(self.fileName, 'r') as f:
                reader = csv.reader(f)
                header = next(reader)
                buf = []
                for row in reader:
                    row[0] = QCheckBox("-")
                    buf.append(row)

                self.model = None
                self.model = MyTableModel(buf, self.headers)
                self.tableView.setModel(self.model)
                self.fileName = ''

    #新規作成
    def handleNew(self):
        print ("handleNew")
        self.fileName = ''

        defaultValue =[
        [QCheckBox(''), "ああああああ", "てすと", "ﾃｽﾄ", "評価", "000000", "000000", 1]
        ]

#        self.model = None #意味なし？
        self.model = MyTableModel(defaultValue, self.headers)
        print(defaultValue)
        self.tableView.setModel(self.model)

    #Viewとモデルに行追加→選択されている行の上に1行挿入します
    def insertRows(self, position, rows=1, index=QModelIndex()):
        print("position: %d"%position)
        print("rows: %d" % rows)
        print("rowCount: %d" % self.model.rowCount(QModelIndex()))

        position = self.selectRow
        self.model.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.model.list.insert(position, [QCheckBox(''), "ああああああ", "てすと", "ﾃｽﾄ", "評価", "000000", "000000", 1])

        self.model.endInsertRows()
        return True

    #Viewとモデルから行削除→選択位置の行を削除します
    def removeRows(self, position, rows=1, index=QModelIndex()):
        print("Removing at position: %s"%position)
        position = self.selectRow
        self.model.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.model.list = self.model.list[:position] + self.model.list[position + rows:]
        self.model.endRemoveRows()
        return True

    #Viewをクリックしたときの行の位置を取得
    def viewClicked(self, indexClicked):
        print('indexClicked() row: %s  column: %s'%(indexClicked.row(), indexClicked.column() ))
        self.selectRow = indexClicked.row()


class MyTableModel(QAbstractTableModel):

    def __init__(self, list, headers = [], parent = None):
        QAbstractTableModel.__init__(self, parent)
        self.list = list
        self.headers = headers

    def rowCount(self, parent):
        return len(self.list)

    def columnCount(self, parent):
        return len(self.list[0])

    def flags(self, index):
        row = index.row()
        column = index.column()
        if column == 0:
            return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled
        else:
            return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):

        row = index.row()
        column = index.column()

        if role == Qt.EditRole:
            return self.list[row][column]

        if role == Qt.CheckStateRole and column == 0:

            if self.list[row][column].isChecked():
                return QVariant(Qt.Checked)
            else:
                return QVariant(Qt.Unchecked)

        """  CheckBoxのテキストを表示させたい場合
        #if role == Qt.DisplayRole and column == 0:
            #return self.list[row][column].text()
        """

        if role == Qt.DisplayRole:

            row = index.row()
            column = index.column()
            value = self.list[row][column]

            return value

    def setData(self, index, value, role = Qt.EditRole):
        row = index.row()
        column = index.column()

        if role == Qt.EditRole:
            self.list[row][column] = value
            self.dataChanged.emit(index, index)
            return True

        if role == Qt.CheckStateRole and column == 0:
            self.list[row][column] = QCheckBox('')
            if value == Qt.Checked:
                self.list[row][column].setChecked(True)
            else:
                self.list[row][column].setChecked(False)
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role):

        if role == Qt.DisplayRole:

            if orientation == Qt.Horizontal:

                if section < len(self.headers):
                    return self.headers[section]
                else:
                    return "not implemented"
            else:
                return "%d" % (section + 1)

class packageWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.setCentralWidget(self.table)
        data1 = [['A','B'],['1','2']]
        colcnt = len(data1[0])
        rowcnt = len(data1)

        self.table.setRowCount(4)

        for n in range(rowcnt):
            for m in range(colcnt):
                item1 = QTableWidgetItem(str(data1[n][m]))
                if n == 1:
                    item1.setBackground(QColor(Qt.yellow))
                self.table.setItem(n, m, item1)
        self.table.item(1, 0).setBackground(QColor(100, 10, 125))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    #リストの表示
    table = View()
    table.show()
    #パッケージの表示
    window = packageWindow()
    window.show()

    app.exec_()
