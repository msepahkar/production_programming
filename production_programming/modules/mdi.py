# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from mehdi_lib.basics import widget_basics
from mehdi_lib.generals import general_editors
from things import specialty_things, part_things


# ===========================================================================
class SubWindow(QtWidgets.QMdiSubWindow):
    # ===========================================================================
    def __init__(self, editor, parent=None):
        super().__init__(parent, flags=QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.editor = editor
        self.setWidget(self.editor.widget)

    # ===========================================================================
    def save(self):
        self.editor.accept()
        return self.editor.representing_object.update_in_database()

    # ===========================================================================
    def closeEvent(self, QCloseEvent):
        if self.editor.is_modified():
            save = widget_basics.YesNoCancelMessageBox('save changes?').show()
            if save == widget_basics.YesNoCancelMessageBox.Yes:
                self.save()
            elif save == widget_basics.YesNoCancelMessageBox.No:
                self.editor.reject()

        self.editor.unregister()


# ===========================================================================
class MainWindow(QtWidgets.QMainWindow):
    # ===========================================================================
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent, flags=QtCore.Qt.Window)

        self.mdi = QtWidgets.QMdiArea(self)
        self.setCentralWidget(self.mdi)
        self.sub_window = SubWindow(
            general_editors.TreeOfThingsEditor(part_things.Part.all(), None, responsible=False, parent_editor=None))
        self.mdi.addSubWindow(self.sub_window, flags=QtCore.Qt.Window)

        self.create_actions()
        self.create_menus()
        self.create_tool_bars()
        self.create_status_bar()

    # ===========================================================================
    def open_new_window(self, list_):
        tree_editor = general_editors.TreeOfThingsEditor(list_, None, responsible=False, parent_editor=None)
        sub_window = SubWindow(tree_editor, parent=self.mdi)
        self.mdi.addSubWindow(sub_window, flags=QtCore.Qt.Window)
        sub_window.show()
        self.mdi.setActiveSubWindow(sub_window)

    # ===========================================================================
    def open_selected_item_in_new_window(self):
        node_editor = self.mdi.activeSubWindow().editor.selected_item_editor()
        tree_editor = general_editors.TreeOfThingsEditor.new_tree_editor_from_node(node_editor)
        if tree_editor:
            sub_window = SubWindow(tree_editor, parent=self.mdi)
            self.mdi.addSubWindow(sub_window, flags=QtCore.Qt.Window)
            sub_window.show()
            self.mdi.setActiveSubWindow(sub_window)

    # ===========================================================================
    def new_item(self):
        editor = self.mdi.activeSubWindow().editor.selected_item_editor()
        if editor:
            editor.append_new_item(is_top_editor=(editor == self.mdi.activeSubWindow().editor))

    # ===========================================================================
    def remove_item(self):
        editor = self.mdi.activeSubWindow().editor
        if editor:
            editor.mark_selected_sub_editor_for_removal(is_top_editor=True)

    # ===========================================================================
    def revive_item(self):
        editor = self.mdi.activeSubWindow().editor
        if editor:
            editor.revive_the_latest_sub_editor_marked_for_removal()

    # ===========================================================================
    def create_actions(self):
        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList,PyArgumentList
        self.new_act = QtWidgets.QAction(QtGui.QIcon('../resources/new.png'), "&new", self,
                                         shortcut=QtGui.QKeySequence.New, statusTip="Create a new part",
                                         triggered=self.new_item)

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList,PyArgumentList
        self.open_all_parts_act = QtWidgets.QAction(QtGui.QIcon('../resources/parts.png'), "open all parts",
                                                    self,
                                                    # shortcut=QtGui.QKeySequence.Open,
                                                    statusTip="Opens all parts",
                                                    triggered=lambda: self.open_new_window(part_things.Part.all()))

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList,PyArgumentList
        self.open_all_providers_act = QtWidgets.QAction(QtGui.QIcon('../resources/providers.png'), "open all providers",
                                                        self,
                                                        # shortcut=QtGui.QKeySequence.Open,
                                                        statusTip="Opens all providers",
                                                        triggered=lambda: self.open_new_window(
                                                            part_things.Provider.all()))

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList,PyArgumentList
        self.open_all_specialties_act = QtWidgets.QAction(QtGui.QIcon('../resources/specialties.png'), "open all specialties",
                                                          self,
                                                          # shortcut=QtGui.QKeySequence.Open,
                                                          statusTip="Opens all specialties",
                                                          triggered=lambda: self.open_new_window(
                                                              specialty_things.Specialty.all()))

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList,PyArgumentList
        self.open_selected_act = QtWidgets.QAction(QtGui.QIcon('../resources/open.png'), "&open...",
                                                   self,
                                                   shortcut=QtGui.QKeySequence.Open,
                                                   statusTip="Open an existing item",
                                                   triggered=self.open_selected_item_in_new_window)

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList,PyArgumentList
        self.save_act = QtWidgets.QAction(QtGui.QIcon('../resources/save.png'), "&save", self,
                                          shortcut=QtGui.QKeySequence.Save, statusTip="Saves current window to disk",
                                          triggered=self.save)

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList,PyArgumentList
        self.save_all_act = QtWidgets.QAction(QtGui.QIcon('../resources/save_all.jpg'), "s&ave all", self,
                                          shortcut=QtGui.QKeySequence.Save, statusTip="Saves all windows to disk",
                                          triggered=self.save_all)

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList,PyArgumentList
        self.remove_act = QtWidgets.QAction(QtGui.QIcon('../resources/remove.png'), "&remove", self,
                                            shortcut=QtGui.QKeySequence.Delete, statusTip="remove the selected item",
                                            triggered=self.remove_item)

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList,PyArgumentList
        self.revive_act = QtWidgets.QAction(QtGui.QIcon('../resources/revive.jpg'), "re&vive", self,
                                            shortcut=QtGui.QKeySequence.Delete, statusTip="revive the removed item",
                                            triggered=self.revive_item)

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList,PyArgumentList,PyArgumentList
        self.exit_act = QtWidgets.QAction("E&xit", self, shortcut=QtGui.QKeySequence.Quit,
                                          statusTip="Exit the application",
                                          triggered=QtWidgets.QApplication.instance().closeAllWindows)

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList,PyArgumentList
        self.cut_act = QtWidgets.QAction(QtGui.QIcon('../resources/cut.png'), "cu&t", self,
                                         shortcut=QtGui.QKeySequence.Cut,
                                         statusTip="Cut the current selection's contents to the clipboard",
                                         triggered=self.cut)

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList,PyArgumentList
        self.copy_act = QtWidgets.QAction(QtGui.QIcon('../resources/copy.png'), "&Copy", self,
                                          shortcut=QtGui.QKeySequence.Copy,
                                          statusTip="Copy the current selection's contents to the clipboard",
                                          triggered=self.copy)

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList,PyArgumentList
        self.paste_act = QtWidgets.QAction(QtGui.QIcon('../resources/paste.png'), "&Paste", self,
                                           shortcut=QtGui.QKeySequence.Paste,
                                           statusTip="Paste the clipboard's contents into the current selection",
                                           triggered=self.paste)

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList
        self.close_act = QtWidgets.QAction("Cl&ose", self,
                                           statusTip="Close the active window",
                                           triggered=self.mdi.closeActiveSubWindow)

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList
        self.close_all_act = QtWidgets.QAction("Close &All", self,
                                               statusTip="Close all the windows",
                                               triggered=self.mdi.closeAllSubWindows)

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList
        self.tile_act = QtWidgets.QAction("&Tile", self, statusTip="Tile the windows",
                                          triggered=self.mdi.tileSubWindows)

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList
        self.cascade_act = QtWidgets.QAction("&Cascade", self,
                                             statusTip="Cascade the windows",
                                             triggered=self.mdi.cascadeSubWindows)

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList,PyArgumentList
        self.next_act = QtWidgets.QAction("Ne&xt", self, shortcut=QtGui.QKeySequence.NextChild,
                                          statusTip="Move the focus to the next window",
                                          triggered=self.mdi.activateNextSubWindow)

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList,PyArgumentList
        self.previous_act = QtWidgets.QAction("Pre&vious", self,
                                              shortcut=QtGui.QKeySequence.PreviousChild,
                                              statusTip="Move the focus to the previous window",
                                              triggered=self.mdi.activatePreviousSubWindow)

        # noinspection PyAttributeOutsideInit
        self.separator_act = QtWidgets.QAction(self)
        self.separator_act.setSeparator(True)

        # noinspection PyAttributeOutsideInit,PyArgumentList,PyArgumentList
        self.about_act = QtWidgets.QAction("&About", self,
                                           statusTip="Show the application's About box",
                                           triggered=self.about)

    # ===========================================================================
    def create_menus(self):
        # noinspection PyAttributeOutsideInit
        self.file_menu = self.menuBar().addMenu("&File")
        self.file_menu.addAction(self.new_act)
        self.file_menu.addAction(self.open_all_parts_act)
        self.file_menu.addAction(self.open_all_providers_act)
        self.file_menu.addAction(self.open_all_specialties_act)
        self.file_menu.addAction(self.open_selected_act)
        self.file_menu.addAction(self.save_act)
        self.file_menu.addAction(self.save_all_act)
        self.file_menu.addAction(self.remove_act)
        self.file_menu.addAction(self.revive_act)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_act)

        # noinspection PyAttributeOutsideInit
        self.edit_menu = self.menuBar().addMenu("&Edit")
        self.edit_menu.addAction(self.cut_act)
        self.edit_menu.addAction(self.copy_act)
        self.edit_menu.addAction(self.paste_act)

        # noinspection PyAttributeOutsideInit
        self.window_menu = self.menuBar().addMenu("&Window")
        self.update_window_menu()
        self.window_menu.aboutToShow.connect(self.update_window_menu)

        self.menuBar().addSeparator()

        # noinspection PyAttributeOutsideInit
        self.help_menu = self.menuBar().addMenu("&Help")
        self.help_menu.addAction(self.about_act)

    # ===========================================================================
    def create_tool_bars(self):
        # noinspection PyAttributeOutsideInit
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.new_act)
        self.fileToolBar.addAction(self.open_all_parts_act)
        self.fileToolBar.addAction(self.open_all_providers_act)
        self.fileToolBar.addAction(self.open_all_specialties_act)
        self.fileToolBar.addAction(self.open_selected_act)
        self.fileToolBar.addAction(self.save_act)
        self.fileToolBar.addAction(self.save_all_act)
        self.fileToolBar.addAction(self.remove_act)
        self.fileToolBar.addAction(self.revive_act)

        # noinspection PyAttributeOutsideInit
        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.cut_act)
        self.editToolBar.addAction(self.copy_act)
        self.editToolBar.addAction(self.paste_act)

    # ===========================================================================
    def create_status_bar(self):
        self.statusBar().showMessage("Ready")

    # ===========================================================================
    def save(self):
        if self.mdi.activeSubWindow():
            if self.mdi.activeSubWindow().save():
                self.statusBar().showMessage("File saved", 2000)
            else:
                self.statusBar().showMessage("not saved", 2000)

    # ===========================================================================
    def save_all(self):
        for sub_window in self.mdi.subWindowList():
            sub_window.save()

    # ===========================================================================
    def cut(self):
        pass

    # ===========================================================================
    def copy(self):
        pass

    # ===========================================================================
    def paste(self):
        pass

    # ===========================================================================
    def about(self):
        pass

    # ===========================================================================
    def update_window_menu(self):
        self.window_menu.clear()
        self.window_menu.addAction(self.close_act)
        self.window_menu.addAction(self.close_all_act)
        self.window_menu.addSeparator()
        self.window_menu.addAction(self.tile_act)
        self.window_menu.addAction(self.cascade_act)
        self.window_menu.addSeparator()
        self.window_menu.addAction(self.next_act)
        self.window_menu.addAction(self.previous_act)
        self.window_menu.addAction(self.separator_act)

        windows = self.mdi.subWindowList()
        self.separator_act.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = 'hi'  # '"%d %s" % (i + 1, child.userFriendlyCurrentFile())
            if i < 9:
                text = '&' + text

            action = self.window_menu.addAction(text)
            action.setCheckable(True)
            # action.setChecked(child is self.active_assembly())
            # action.triggered.connect(self.windowMapper.map)
            # self.windowMapper.setMapping(action, window)

    # ===========================================================================
    def closeEvent(self, event):
        self.mdi.closeAllSubWindows()
        # modified = False
        # for part in things_.Part.all():
        #     if part.is_modified():
        #         modified = True
        #         break
        # for specialty in things_.Specialty.all():
        #     if specialty.is_modified():
        #         modified = True
        #         break
        # if modified:
        #     result = base_widgets.YesNoCancelMessageBox('save changes to the tree?').show()
        #     if result == base_widgets.YesNoCancelMessageBox.Yes:
        #         self.save_all()
        #     elif result == base_widgets.YesNoCancelMessageBox.Cancel:
        #         event.ignore()



