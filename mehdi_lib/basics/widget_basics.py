# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore

from mehdi_lib.basics import basic_types
from mehdi_lib.generals import general_ui_titles


# ===========================================================================
class SpinBox(QtWidgets.QSpinBox):
    # ===========================================================================
    def __init__(self, min_, max_, action, parent=None):
        super().__init__(parent)
        self.setRange(min_, max_)
        # noinspection PyUnresolvedReferences
        self.valueChanged.connect(action)


# ===========================================================================
class Layout(QtWidgets.QLayout):
    # ===========================================================================
    def __init__(self, parent=None):
        super().__init__(parent)

    # ===========================================================================
    def add_widgets(self, *widgets):

        for widget in widgets:
            if isinstance(widget, QtWidgets.QLayout):
                self.addLayout(widget)
            elif widget == Dialog.stretch:
                self.addStretch()
            elif isinstance(widget, QtWidgets.QWidget):
                self.addWidget(widget)

    # ===========================================================================
    def add_widget(self, widget):

        if isinstance(widget, QtWidgets.QLayout):
            self.addLayout(widget)
        elif isinstance(widget, QtWidgets.QWidget):
            self.addWidget(widget)

    # ===========================================================================
    def insert_widget(self, index, widget):

        if isinstance(widget, QtWidgets.QLayout):
            self.insertLayout(index, widget)
        elif isinstance(widget, QtWidgets.QWidget):
            self.insertWidget(index, widget)

    # ===========================================================================
    def add_widget_with_label(self, label_text, widget):
        layout = HLayout()
        label = QtWidgets.QLabel(label_text)
        layout.add_widgets(widget, label)
        self.addLayout(layout)

        # label should be returned for making future updates possible
        return label

    # ===========================================================================
    def insert_widget_with_label(self, index, label_text, widget):
        layout = HLayout()
        label = QtWidgets.QLabel(label_text)
        layout.add_widgets(label, widget)
        self.insert_widget(index, layout)

        # label should be returned for making future updates possible
        return label

    # ===========================================================================
    def remove_widget(self, widget):
        if isinstance(widget, QtWidgets.QLayout):
            self.removeItem(widget)
        elif isinstance(widget, QtWidgets.QWidget):
            self.removeWidget(widget)


# ===========================================================================
class HLayout(QtWidgets.QHBoxLayout, Layout):
    # ===========================================================================
    def __init__(self, parent=None):
        QtWidgets.QHBoxLayout.__init__(self, parent)
        Layout.__init__(self, parent)


# ===========================================================================
class VLayout(QtWidgets.QVBoxLayout, Layout):
    # ===========================================================================
    def __init__(self, parent=None):
        QtWidgets.QVBoxLayout.__init__(self, parent)
        Layout.__init__(self, parent)

    # ===========================================================================
    def add_row_widgets(self, *widgets):
        h_layout = HLayout()
        h_layout.add_widgets(*widgets)
        self.addLayout(h_layout)


# ===========================================================================
class Dialog(QtWidgets.QDialog):
    stretch = 'stretch'

    # ===========================================================================
    def __init__(self, parent=None):
        # noinspection PyArgumentList
        super().__init__(parent)

        # maximize minimize buttons
        self.setWindowFlags(QtCore.Qt.Window)

        # first the super layout
        self.super_layout = VLayout()
        self.setLayout(self.super_layout)

        # now the header layout
        self.header_layout = HLayout()
        self.super_layout.addLayout(self.header_layout)

        # now the body layout
        self.body_layout = VLayout()
        self.super_layout.addLayout(self.body_layout)

        # now the footer layout
        self.footer_layout = HLayout()
        self.super_layout.addLayout(self.footer_layout)

    # ===========================================================================
    def add_row_widgets(self, *widgets):
        self.body_layout.add_row_widgets(*widgets)

    # ===========================================================================
    def add_widget(self, widget):
        self.body_layout.add_widget(widget)

    # ===========================================================================
    def remove_widget(self, widget):
        self.body_layout.remove_widget(widget)

    # ===========================================================================
    def add_widget_with_label(self, label_text, widget):
        self.body_layout.add_widget_with_label(label_text, widget)


# ===========================================================================
class DialogWithOkCancel(Dialog):

    # ===========================================================================
    def __init__(self, parent=None):

        super().__init__(parent)

        # buttons
        self.accept_button = Button(general_ui_titles.ok, self.accept)
        self.reject_button = Button(general_ui_titles.cancel, self.reject)
        self.footer_layout.add_widgets(Dialog.stretch, self.accept_button, self.reject_button)


# ===========================================================================
class Button(QtWidgets.QPushButton):
    # ===========================================================================
    def __init__(self, multi_lingual_text: basic_types.MultilingualString, action, parent=None):
        text = multi_lingual_text[basic_types.Language.get_active_language()]
        super().__init__(text, parent)
        # noinspection PyUnresolvedReferences
        self.clicked.connect(action)


# ===========================================================================
class ButtonWithActionParameters(QtWidgets.QPushButton):
    # ===========================================================================
    def __init__(self, text, action, action_parameters, parent=None):
        super().__init__(text, parent)
        # noinspection PyUnresolvedReferences
        self.clicked.connect(lambda: action(*action_parameters))


# ===========================================================================
class YesNoMessageBox(QtWidgets.QMessageBox):
    # ===========================================================================
    def __init__(self, message):
        super().__init__()
        self.setText(message)
        # self.setInformativeText(message2)
        self.setStandardButtons(YesNoMessageBox.Yes | YesNoMessageBox.No)
        self.setDefaultButton(YesNoMessageBox.No)

    # ===========================================================================
    def show(self):
        if self.exec_() == YesNoMessageBox.Yes:
            return True
        return False


# ===========================================================================
class YesNoCancelMessageBox(QtWidgets.QMessageBox):
    # ===========================================================================
    def __init__(self, message):
        super().__init__()
        self.setText(message)
        # self.setInformativeText(message2)
        self.setStandardButtons(YesNoCancelMessageBox.Yes | YesNoCancelMessageBox.No | YesNoCancelMessageBox.Cancel)
        self.setDefaultButton(YesNoMessageBox.Cancel)

    # ===========================================================================
    def show(self):
        return self.exec()


# ===========================================================================
class WarningMessageBox(QtWidgets.QMessageBox):
    # ===========================================================================
    def __init__(self, message):
        super().__init__()
        self.setText(message)
        # self.setInformativeText(message2)
        self.setStandardButtons(WarningMessageBox.Ok)

    # ===========================================================================
    def show(self):
        self.exec_()
