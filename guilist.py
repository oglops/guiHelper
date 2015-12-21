import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os
import sip
 
import maya.cmds as cmds
import maya.OpenMayaUI as mui
 
from PyQt4 import QtGui, QtCore, uic
 
def getMayaWindow():
    'Get the maya main window as a QMainWindow instance'
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)


data = {'level1': ['1', '2', '3'],
        'level2': ['4', '5', '6'],
        'level3': ['7', '8', '9']}


class GuiListWindow(QMainWindow):

    'This time I try to put the table populating code in main ui'

    def __init__(self, parent=getMayaWindow()):
        super(GuiListWindow, self).__init__(parent)

        self.model = QStandardItemModel()
        # self.model.setRootPath(QDir.currentPath())
        tree = QTreeView()
        tree.setModel(self.model)

        for n, key in enumerate(sorted(data.keys())):
            parent = QStandardItem(key)
            for m, item in enumerate(data[key]):
                child = QStandardItem(item)
                parent.appendRow([child])
            self.model.appendRow(parent)

        # expand third container
        index = self.model.indexFromItem(parent)
        tree.expand(index)

        # select last row
        selmod = tree.selectionModel()
        index2 = self.model.indexFromItem(child)
        selmod.select(
            index2, QItemSelectionModel.Select | QItemSelectionModel.Rows)

        self.model.setHeaderData(0, Qt.Horizontal, "Tree View")

        self.setCentralWidget(tree)
        self.resize(350, 220)
        self.move(200, 400)

def main(*args):
    # app = QApplication(args)
    win = GuiListWindow()
    win.show()
    # sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)
