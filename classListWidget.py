import scene
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QAction, QListWidget, QListWidgetItem, QMenu, QMessageBox


class ListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.LMB = False
        self.RMB = False
        self.MMB = False
        self.scene = scene.Scene()
        self.child = 0

    def getChild(self, child):
        self.child = child

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.LMB = True
            item = self.itemAt(e.pos())
            if item is not None:
                self.itemClick(item)

        elif e.button() == Qt.RightButton:
            self.RMB = True
            item = self.itemAt(e.pos())
            if item is not None:
                self.itemClick(item)
                self.showContextMenu(e.globalPos())

        elif e.button() == Qt.MiddleButton:
            self.MMB = True

    def mouseReleaseEvent(self, e):
        self.LMB = False
        self.RMB = False
        self.MMB = False

    def itemClick(self, item):
        if self.LMB:
            if item.isSelected():
                item.setSelected(False)
            else:
                for selitem in self.selectedItems():
                    self.scene.unselectOBJ(selitem.text())
                    selitem.setSelected(False)
                item.setSelected(True)
                self.scene.setCurrentOBJ(item.text())
                self.child.update()
        elif self.RMB:
                item.setSelected(True)

    def showContextMenu(self, pos):
        menu = QMenu(self)
        delete_action = QAction("Удалить", self)
        delete_action.triggered.connect(self.deleteItem)
        menu.addAction(delete_action)
        menu.exec_(pos)

    def updateList(self):
        self.clear()
        for obj in self.scene.listOfOBJ:
            item = QListWidgetItem(obj.name)
            self.addItem(item)

    def deleteItem(self):
        selected_items = self.selectedItems()
        for item in selected_items:
            self.takeItem(self.row(item))
            self.scene.removeOBJ(item.text())
            self.child.update()