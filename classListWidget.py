import scene
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QAction, QListWidget, QListWidgetItem, QMenu, QMessageBox


class ListWidget(QListWidget):
    """
       Виджет списка для управления объектами сцены.

       Атрибуты:
           LMB (bool): Состояние левой кнопки мыши.
           RMB (bool): Состояние правой кнопки мыши.
           MMB (bool): Состояние средней кнопки мыши.
           scene (Scene): Экземпляр класса Scene, управляющий объектами.
           child (any): Дочерний элемент или виджет, который необходимо обновлять при изменении состояния.

       Методы:
           getChild(child): Устанавливает ссылку на дочерний виджет, который требуется обновлять.
           mousePressEvent(e): Обрабатывает нажатие кнопок мыши.
           mouseReleaseEvent(e): Обрабатывает отпускание кнопок мыши.
           itemClick(item): Обрабатывает клики по элементам списка.
           showContextMenu(pos): Отображает контекстное меню для элементов списка.
           updateList(): Обновляет список элементов в соответствии с объектами на сцене.
           deleteItem(): Удаляет выбранные элементы из списка и соответствующие объекты из сцены.
    """
    def __init__(self):
        """
            Инициализирует экземпляр ListWidget, создавая начальные значения для кнопок мыши
            и инициализируя сцену и дочерний элемент.
        """
        super().__init__()
        self.LMB = False
        self.RMB = False
        self.MMB = False
        self.scene = scene.Scene()
        self.child = 0

    def getChild(self, child):
        """ Устанавливает дочерний виджет, который будет обновляться при изменениях. """
        self.child = child

    def mousePressEvent(self, e):
        """ Обрабатывает нажатия кнопок мыши, регистрируя состояние кнопок и выбор элемента. """
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
        """ Обрабатывает отпускание кнопок мыши, сбрасывая состояние кнопок. """
        self.LMB = False
        self.RMB = False
        self.MMB = False

    def itemClick(self, item):
        """
            Обрабатывает клики по элементам списка, устанавливая или снимая выбор с объектов.

            Параметры:
                item (QListWidgetItem): Элемент списка, по которому был произведен клик.
        """
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
        """
            Отображает контекстное меню с опциями действий для выбранного элемента.

            Параметры:
                    pos (QPoint): Позиция на экране, где должно быть отображено меню.
        """
        menu = QMenu(self)
        delete_action = QAction("Удалить", self)
        delete_action.triggered.connect(self.deleteItem)
        menu.addAction(delete_action)
        menu.exec_(pos)

    def updateList(self):
        """ Обновляет отображаемый список объектов, синхронизируя его с объектами на сцене. """
        self.clear()
        for obj in self.scene.listOfOBJ:
            item = QListWidgetItem(obj.name)
            self.addItem(item)

    def deleteItem(self):
        """ Удаляет выбранные элементы из списка и сцены, а также обновляет дочерний элемент. """
        selected_items = self.selectedItems()
        for item in selected_items:
            self.takeItem(self.row(item))
            self.scene.removeOBJ(item.text())
            self.child.update()