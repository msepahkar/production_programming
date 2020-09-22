# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from things import part_things
from classes import base_widgets, editors_
from modules import processing


# ===========================================================================
class PartRect(QtWidgets.QGraphicsRectItem):
    # ===========================================================================
    width = 80
    height = 30

    # ===========================================================================
    def __init__(self, part, x, y, parent=None):
        super().__init__(parent)
        self.part = part
        self.part.modified_signal.connect(self.update)
        self.setRect(x, y, PartRect.width, PartRect.height)
        self.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        self.setBrush(QtGui.QBrush(QtCore.Qt.green))

        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsRectItem.ItemIsSelectable)
        # self.setFlag(QtWidgets.QGraphicsRectItem.ItemIsMovable)

    # ===========================================================================
    def update(self):
        super().update()

    # ===========================================================================
    def anchor_point_1(self):
        x = self.rect().left()
        y = self.rect().top() + self.rect().height() / 2
        return QtCore.QPointF(x, y)

    # ===========================================================================
    def anchor_point_2(self):
        x = self.rect().right()
        y = self.rect().top() + self.rect().height() / 2
        return QtCore.QPointF(x, y)

    # ===========================================================================
    def hoverEnterEvent(self, event):
        self.setBrush(QtGui.QBrush(QtCore.Qt.yellow))

    # ===========================================================================
    def hoverLeaveEvent(self, event):
        self.setBrush(QtGui.QBrush(QtCore.Qt.green))

    # ===========================================================================
    def mouseDoubleClickEvent(self, event):
        editors_.EditorDialog(editors_.ThingEditor(self.part)).exec()

    # ===========================================================================
    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu()
        edit_part_action = menu.addAction('edit part')
        action = menu.exec_(event.screenPos())

        # open part
        if action == edit_part_action:
            editors_.EditorDialog(editors_.ThingEditor(self.part)).exec()

    # ===========================================================================
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)
        painter.setPen(QtCore.Qt.black)
        painter.drawText(self.rect().left() + 3, self.rect().bottom() - 3, self.part.name)


# ===========================================================================
class GraphicsScene(QtWidgets.QGraphicsScene):
    # ===========================================================================
    def __init__(self, parent=None):
        super().__init__(parent)


# ===========================================================================
class GraphicsView(QtWidgets.QGraphicsView):
    # ===========================================================================
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setMouseTracking(True)
        self.parent = parent
        self.scene = GraphicsScene(self)
        self.scene.setBackgroundBrush(QtCore.Qt.white)
        self.setScene(self.scene)
        # self.setSceneRect(0, 0, w, h)
        self.update_pan_status()

    # ===========================================================================
    def wheelEvent(self, event):
        if self.scene is not None:
            if event.angleDelta().y() > 0:
                factor = 1.25
            else:
                factor = 0.8
            self.scale(factor, factor)
            self.update_pan_status()
        return QtWidgets.QGraphicsView.wheelEvent(self, event)

    # ===========================================================================
    def resizeEvent(self, event):
        pass
        self.update_pan_status()

        return QtWidgets.QGraphicsView.resizeEvent(self, event)

    # ===========================================================================
    def update_pan_status(self):
        rect = QtCore.QRectF(self.sceneRect())
        view_rect = self.viewport().rect()
        scene_rect = self.transform().mapRect(rect)
        if scene_rect.bottom() > view_rect.bottom() or \
                        scene_rect.right() > view_rect.right():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        else:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

    # ===========================================================================
    def fit(self):
        if self.scene is not None:
            rect = QtCore.QRectF(self.sceneRect())
            if not rect.isNull():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                view_rect = self.viewport().rect()
                scene_rect = self.transform().mapRect(rect)
                factor = min(view_rect.width() / scene_rect.width(),
                             view_rect.height() / scene_rect.height())
                self.scale(factor, factor)
                self.centerOn(rect.center())


# ===========================================================================
class AssemblyGraphicsView(GraphicsView):
    # ===========================================================================
    def __init__(self, parent=None):
        super().__init__(parent)


# ===========================================================================
class AssemblyWindow(QtWidgets.QMdiSubWindow):
    # ===========================================================================
    margin = 10

    # ===========================================================================
    def __init__(self, assembly, parent=None):
        super().__init__(parent)
        # layout = QtWidgets.QVBoxLayout()
        self.view = AssemblyGraphicsView(self)
        self.layout().addWidget(self.view)
        # self.setLayout(layout)
        self.assembly = assembly
        self.part_rects = []
        self.draw_assembly()

    # ===========================================================================
    def draw_assembly(self):

        # clear the scene
        self.view.scene.clear()

        # disconnect signals
        for part_rect in self.part_rects:
            part_rect.part[part.Part.sub_parts].list_modified_signal.disconnect(self.draw_assembly)
            # part_rect.part.modified_signal.disconnect(part_rect.part.update_in_database)

        # clear part rects
        self.part_rects.clear()

        # create the levels array
        levels = processing.Processing.put_into_levels(self.assembly)

        # draw parts
        assembly_level_part_rects = []
        current_level_part_rects = []
        for i, level in enumerate(levels):
            x = i * (PartRect.width + AssemblyWindow.margin) + AssemblyWindow.margin
            for j, part in enumerate(level):
                y = j * (PartRect.height + AssemblyWindow.margin) + AssemblyWindow.margin
                # create and add part rect
                self.part_rects.append(PartRect(part, x, y))
                self.view.scene.addItem(self.part_rects[-1])
                current_level_part_rects.append(self.part_rects[-1])

            # draw lines
            for assembly_part_rect in assembly_level_part_rects:
                for part_rect in current_level_part_rects:
                    for sub_part in assembly_part_rect.part.sub_parts_as_parts:
                        if sub_part == part_rect.part:
                            point_1 = assembly_part_rect.anchor_point_2()
                            point_2 = part_rect.anchor_point_1()
                            line = QtCore.QLineF(point_1, point_2)
                            self.view.scene.addItem(QtWidgets.QGraphicsLineItem(line))

            assembly_level_part_rects = current_level_part_rects
            current_level_part_rects = []

        # connect signals
        for part_rect in self.part_rects:
            part_rect.part[part.Part.sub_parts].list_modified_signal.connect(self.draw_assembly)


# ===========================================================================
class AssemblyTree(editors_.TreeOfThingsEditor):
    # ===========================================================================
    open_assembly_signal = QtCore.pyqtSignal('PyQt_PyObject')

    # ===========================================================================
    def __init__(self):
        super().__init__(part_things.Part)
        self.removed_parts = []

    # ===========================================================================
    def new_part(self):
        part = part.Part()
        if self.currentItem():
            assembly = self.currentItem().get_item()
            assembly[part.Part.sub_parts].append(part.SubPart(assembly, part))
            self.find_entry(assembly).setExpanded(True)
            self.find_entry(assembly).setSelected(False)
        self.find_entry(part).setSelected(True)

    # ===========================================================================
    def remove_current(self):
        if self.currentItem():
            if self.currentItem().parent() is None:
                part = self.currentItem().get_item()  # type: part.Part
                if base_widgets.YesNoMessageBox('remove {}?\nbe careful!\nit will be removed from the database'.format(
                        part.name)).exec() == base_widgets.YesNoMessageBox.Yes:
                    part.mark_for_removal()
                    self.removed_parts.append(part)
            else:
                assembly = self.currentItem().parent().get_item()
                part = self.currentItem().get_item()
                if base_widgets.YesNoMessageBox('remove {} from {}'.format(part.name, assembly.name)).exec() == base_widgets.YesNoMessageBox.Yes:
                    assembly.remove_sub_part(part)

    # ===========================================================================
    def contextMenuEvent(self, event):

        # create the menu
        menu = QtWidgets.QMenu(self)

        # create actions
        open_assembly_action = menu.addAction('open assembly')
        new_part_action = menu.addAction('new part ...')
        edit_part_action = menu.addAction('edit part ...')
        remove_part_action = menu.addAction('remove part')

        # execute the menu
        action = menu.exec(self.mapToGlobal(event.pos()))

        # open assembly
        if action == open_assembly_action:
            if self.currentItem():
                self.open_assembly_signal.emit(self.currentItem())

        # new part
        if action == new_part_action:
            self.new_part()

        # edit part
        if action == edit_part_action:
            if self.currentItem():
                editors_.EditorDialog(editors_.ThingEditor(self.currentItem().get_item())).exec()

        # remove part
        if action == remove_part_action:
            self.remove_current()

    # ===========================================================================
    def mouseDoubleClickEvent(self, event):
        if self.currentItem() and isinstance(self.currentItem().get_item(), part_things.Part):
            self.open_assembly_signal.emit(self.currentItem())
