# -*- coding: utf-8 -*-

import datetime
import weakref

from PyQt5 import QtWidgets, QtCore, QtGui

from mehdi_lib.basics import widget_basics, basic_types, thing_
from mehdi_lib.tools import date, tools
from mehdi_lib.generals import general_ui_titles


# ===========================================================================
class Widget_for_Editor:
    # ===========================================================================
    def __init__(self):
        self.set_layout_direction()

    # ===========================================================================
    def get_value(self):
        pass

    # ===========================================================================
    def set_layout_direction(self):
        if basic_types.Language.get_active_language().is_right_to_left():
            self.setLayoutDirection(QtCore.Qt.RightToLeft)
        else:
            self.setLayoutDirection(QtCore.Qt.LeftToRight)

    # ===========================================================================
    def set_value(self, value):
        pass

    # ===========================================================================
    def is_selected(self):
        return False

    # ===========================================================================
    def set_selected(self, select):
        pass

    # ===========================================================================
    def update_items(self, items):
        pass


# ===========================================================================
class CheckBox_for_BoolEditor(QtWidgets.QCheckBox, Widget_for_Editor):
    # ===========================================================================
    def __init__(self, name, parent=None):
        super().__init__(name, parent)

    # ===========================================================================
    def get_value(self):
        return self.isChecked()

    # ===========================================================================
    def set_value(self, value):
        self.setChecked(value)


# ===========================================================================
class CheckBox_for_SelectorEditor(QtWidgets.QCheckBox, Widget_for_Editor):

    # ===========================================================================
    def __init__(self, owner, parent=None):

        super().__init__(owner.name, parent)
        self.owner = owner

    # ===========================================================================
    def get_value(self):
        if self.is_Checked():
            return self.owner
        return None

    # ===========================================================================
    def set_value(self, value):
        if value == self.owner:
            self.setChecked(True)
        else:
            self.setChecked(False)


# ===========================================================================
class LineEdit_for_LineEditor(QtWidgets.QLineEdit, Widget_for_Editor):
    error_color = QtCore.Qt.red
    normal_color = QtCore.Qt.white
    select_color = QtCore.Qt.yellow
    value_changed_signal = QtCore.pyqtSignal()

    # ===========================================================================
    def __init__(self, validator=None, parent=None):
        super().__init__(parent)
        self.has_error = False
        self.last_valid_value = None
        self.current_color = LineEdit_for_LineEditor.normal_color
        self.previous_color = LineEdit_for_LineEditor.normal_color
        self.installEventFilter(self)
        # noinspection PyUnresolvedReferences
        self.textChanged.connect(lambda x: self.update_validity_status())
        if validator:
            self.setValidator(validator)

    # ===========================================================================
    def eventFilter(self, object_, event):
        if super().eventFilter(object_, event):
            return True
        # filter Esc key if the value is not correct
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Escape and not self.is_valid():
                if self.last_valid_value is not None:
                    self.set_value(self.last_valid_value)
                    return True

        return QtCore.QObject.eventFilter(self, object_, event)

    # ===========================================================================
    def set_color(self, color: QtGui.QColor):
        self.previous_color = self.current_color
        pal = self.palette()
        pal.setColor(QtGui.QPalette.Window, color)
        pal.setColor(QtGui.QPalette.Base, color)
        self.setPalette(pal)
        self.current_color = color

    # ===========================================================================
    def set_selected(self, select):

        if select and not self.has_error:
            self.set_color(LineEdit_for_LineEditor.select_color)

        if not select and not self.has_error:
            self.set_color(LineEdit_for_LineEditor.normal_color)

    # ===========================================================================
    def update_validity_status(self):
        # error finished
        if self.is_valid() and self.has_error:
            self.set_color(self.previous_color)
            self.has_error = False
        # error just occurred
        elif not self.is_valid() and not self.has_error:
            self.set_color(LineEdit_for_LineEditor.error_color)
            self.has_error = True

        if not self.has_error:
            self.last_valid_value = self.get_value()
            self.value_changed_signal.emit()

    # ===========================================================================
    def is_valid(self):
        raise NotImplementedError

    # ===========================================================================
    def get_value(self):
        raise NotImplementedError

    # ===========================================================================
    def set_value(self, value):
        if value != self.get_value():
            self.setText(str(value))
            self.update_validity_status()


# ===========================================================================
class LineEdit_for_AttachmentEditor(LineEdit_for_LineEditor):

    # ===========================================================================
    def is_valid(self):
        return True

    # ===========================================================================
    def get_value(self):
        return self.text()


# ===========================================================================
class LineEdit_for_FileNameEditor(LineEdit_for_LineEditor):

    # ===========================================================================
    def is_valid(self):
        return True

    # ===========================================================================
    def get_value(self):
        return self.text()


# ===========================================================================
class LineEdit_for_FilePathEditor(LineEdit_for_LineEditor):

    # ===========================================================================
    def is_valid(self):
        return True

    # ===========================================================================
    def get_value(self):
        return self.text()


# ===========================================================================
class LineEdit_for_FloatEditor(LineEdit_for_LineEditor):

    # ===========================================================================
    def __init__(self, bottom: float, top: float, decimals: int, parent=None):
        super().__init__(validator=QtGui.QDoubleValidator(bottom, top, decimals), parent=parent)

    # ===========================================================================
    def is_valid(self) -> bool:
        try:
            float(self.text())
        except ValueError:
            return False

        return True

    # ===========================================================================
    def get_value(self):
        if self.is_valid():
            return float(self.text())
        else:
            return self.last_valid_value


# ===========================================================================
class LineEdit_for_IntEditor(LineEdit_for_LineEditor):

    # ===========================================================================
    def __init__(self, bottom: int, top: int, parent=None):
        super().__init__(validator=QtGui.QIntValidator(bottom, top), parent=parent)

    # ===========================================================================
    def is_valid(self, prompt: bool = False) -> bool:
        try:
            int(self.text())
        except ValueError:
            return False

        return True

    # ===========================================================================
    def get_value(self):
        try:
            return int(self.text())
        except ValueError:
            return self.last_valid_value


# ===========================================================================
class LineEdit_for_NameEditor(LineEdit_for_LineEditor):

    # ===========================================================================
    def is_valid(self):
        return True

    # ===========================================================================
    def get_value(self):
        return self.text()


# ===========================================================================
class LineEdit_for_CommentEditor(LineEdit_for_LineEditor):

    # ===========================================================================
    def is_valid(self):
        return True

    # ===========================================================================
    def get_value(self):
        return self.text()


# ===========================================================================
class LineEdit_for_DurationEditor(LineEdit_for_LineEditor):

    # ===========================================================================
    def __init__(self, parent=None):
        time_format = '^\d{1,4}:([0-5][0-9]|[0-9]):([0-5][0-9]|[0-9])$'
        super().__init__(validator=QtGui.QRegExpValidator(QtCore.QRegExp(time_format)), parent=parent)

    # ===========================================================================
    def is_valid(self) -> bool:
        try:
            hours, minutes, seconds, *extra = self.text().split(':')
            hours = int(hours)
            minutes = int(minutes)
            seconds = int(seconds)
            datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        except ValueError:
            return False

        return True

    # ===========================================================================
    def get_value(self):
        try:
            hours, minutes, seconds, *extra = self.text().split(':')
            hours = int(hours)
            minutes = int(minutes)
            seconds = int(seconds)
            return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        except ValueError:
            return self.last_valid_value

    # ===========================================================================
    def set_value(self, value):
        if isinstance(value, datetime.timedelta):
            hours = value.seconds // 3600 + value.days * 24
            minutes = (value.seconds // 60) % 60
            seconds = value.seconds % 60
            self.setText('{}:{}:{}'.format(hours, minutes, seconds))
            self.update_validity_status()


# ===========================================================================
class LineEdit_for_DateEditor(LineEdit_for_LineEditor):
    date_modified_signal = QtCore.pyqtSignal('PyQt_PyObject')

    # ===========================================================================
    class DateSelector(widget_basics.Dialog):
        date_selected_signal = QtCore.pyqtSignal('PyQt_PyObject')

        # ===========================================================================
        def __init__(self, parent=None):
            super().__init__(parent)

            previous_month = basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'previous month',
                basic_types.Language.AvailableLanguage.fa: 'ماه قبل',
            })

            next_month = basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'next month',
                basic_types.Language.AvailableLanguage.fa: 'ماه بعد',
            })

            today = basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'today',
                basic_types.Language.AvailableLanguage.fa: 'امروز',
            })

            select_date = basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'select date',
                basic_types.Language.AvailableLanguage.fa: 'انتخاب تاریخ',
            })

            self.setWindowTitle('انتخاب تاریخ')
            button_previous = widget_basics.Button(previous_month, self.previous_month)
            button_next = widget_basics.Button(next_month, self.next_month)
            button_go = widget_basics.Button(general_ui_titles.select, self.date_selected)
            button_today = widget_basics.Button(today, self.set_today)
            self.spin_year = widget_basics.SpinBox(1, 9999, self.update_year)
            self.month_combo = ComboBox_for_Editor(date.Shamsi.month_names, self.update_month)

            self.table = LineEdit_for_DateEditor.CalendarTable(date.Shamsi.weekday_names, reverse=True, parent=self)
            # noinspection PyUnresolvedReferences
            self.table.itemClicked.connect(self.update_day)

            self.current_date = date.Shamsi.from_gregorian(datetime.datetime.today())
            self.update_date(self.current_date)
            self.add_row_widgets(button_next, self.spin_year, self.month_combo, button_today, button_go,
                                 button_previous)
            self.add_widget(self.table)
            self.setMinimumWidth(400)
            self.setMinimumHeight(300)

        # ===========================================================================
        def update_date(self, date_: date.ShamsiDate):
            items = date_.month_days_separated_by_weekdays(reverse=True)
            self.table.update_items(items)
            for c in items:
                # noinspection PyTypeChecker
                for r, day in enumerate(items[c]):
                    if day == date_.day:
                        self.table.setCurrentCell(r, c)
            self.spin_year.setValue(date_.year)
            self.month_combo.setCurrentIndex(date_.month - 1)

        # ===========================================================================
        def set_today(self):
            self.current_date = date.Shamsi.from_gregorian(datetime.datetime.today())
            self.update_date(self.current_date)

        # ===========================================================================
        def next_month(self):
            self.current_date = self.current_date.next_month()
            self.update_date(self.current_date)

        # ===========================================================================
        def previous_month(self):
            self.current_date = self.current_date.previous_month()
            self.update_date(self.current_date)

        # ===========================================================================
        def update_year(self, new_year: int):
            if new_year == self.current_date.year:
                return
            self.current_date = date.Shamsi.force_a_date(new_year, self.current_date.month, self.current_date.day)
            self.update_date(self.current_date)

        # ===========================================================================
        def update_month(self, month_index: int):
            new_month = month_index + 1
            if new_month == self.current_date.month:
                return
            self.current_date = date.Shamsi.force_a_date(self.current_date.year, new_month, self.current_date.day)
            self.update_date(self.current_date)

        # ===========================================================================
        def update_day(self, item):
            try:
                new_day = int(item.text())
            except TypeError:
                tools.Tools.warning('invalid day')
                return
            self.current_date.day = new_day

        # ===========================================================================
        def date_selected(self):
            self.date_selected_signal.emit(self.current_date.to_gregorian())
            self.close()

    # ===========================================================================
    class CalendarTable(QtWidgets.QTableWidget):
        # ===========================================================================
        def __init__(self, headers, reverse=False, parent=None):
            QtWidgets.QTableWidget.__init__(self, parent)
            self.headers = headers
            if reverse:
                self.headers.reverse()
            self.setColumnCount(len(self.headers))
            self.setHorizontalHeaderLabels(headers)
            self.verticalHeader().hide()
            self.item_values = None
            self.resizeColumnsToContents()
            self.resizeRowsToContents()
            self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        # ===========================================================================
        def update_items(self, item_values: [[]]):
            while self.rowCount() < len(item_values[0]):
                self.insertRow(self.rowCount())
            while self.rowCount() > len(item_values[0]):
                self.removeRow(self.rowCount() - 1)
            for column_index in range(len(self.headers)):
                for row_index, item_value in enumerate(item_values[column_index]):
                    item = self.item(row_index, column_index)
                    if item is None:
                        item = QtWidgets.QTableWidgetItem(str(item_value))
                        self.setItem(row_index, column_index, item)
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    if item_value is None:
                        item.setText('')
                        item.setFlags(QtCore.Qt.NoItemFlags)
                    else:
                        item.setText(str(item_value))

    # ===========================================================================
    def __init__(self, parent=None):

        date_format = QtCore.QRegExp('^\d{1,4}/(1[0-2]|[0-9])/(3[01]|[12][0-9]|[0-9])$')
        super().__init__(validator=QtGui.QRegExpValidator(date_format), parent=parent)
        self.installEventFilter(self)
        self.date_selector = LineEdit_for_DateEditor.DateSelector(self)
        self.date_selector.date_selected_signal.connect(self.set_value)

    # ===========================================================================
    def eventFilter(self, object_, event):
        if super().eventFilter(object_, event):
            return True
        if event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton and \
                not self.hasSelectedText():
            date_ = self.get_value()
            if date_ is None:
                date_ = datetime.datetime.today()
            self.date_selector.update_date(date.Shamsi.from_gregorian(date_))
            self.date_selector.exec()
            return True
        return False

    # ===========================================================================
    def is_valid(self) -> bool:
        try:
            # extract date items
            year, month, day, *extra = self.text().split('/')
            int(year)
            int(month)
            int(day)
        except ValueError:
            return False

        return True

    # ===========================================================================
    def get_value(self):
        # extract date info
        try:
            year, month, day, *extra = self.text().split('/')
            year = int(year)
            month = int(month)
            day = int(day)
        except ValueError:
            return None

        # check for validity
        if not date.Shamsi.is_valid(year, month, day):
            return None

        # create and return date
        return date.ShamsiDate(int(year), int(month), int(day)).to_gregorian().date()

    # ===========================================================================
    def set_value(self, date_):
        if date_ is None:
            if self.text():
                self.setText('')
                self.date_modified_signal.emit(None)
        else:
            shamsi_date = date.Shamsi.from_gregorian(date_)
            text = '{}/{}/{}'.format(shamsi_date.year, shamsi_date.month, shamsi_date.day)
            if text != self.text():
                self.setText(text)
                self.date_modified_signal.emit(date_)
        self.update_validity_status()


# ===========================================================================
class LineEdit_for_DateTimeEditor(LineEdit_for_DateEditor):

    # ===========================================================================
    def get_value(self):
        # extract date info
        try:
            year, month, day, *extra = self.text().split('/')
            year = int(year)
            month = int(month)
            day = int(day)
        except ValueError:
            return None

        # check for validity
        if not date.Shamsi.is_valid(year, month, day):
            return None

        # create and return date
        return date.ShamsiDate(int(year), int(month), int(day)).to_gregorian()


# ===========================================================================
class ComboBox_for_Editor(QtWidgets.QComboBox, Widget_for_Editor):
    # ===========================================================================
    def __init__(self, items, action, parent=None):
        super().__init__(parent)
        for item in items:
            self.addItem(item)
        # noinspection PyUnresolvedReferences
        self.currentIndexChanged.connect(action)


# ===========================================================================
class ComboBox_for_EnumItemSelectorEditor(QtWidgets.QComboBox, Widget_for_Editor):
    # ===========================================================================
    def __init__(self, enum_):
        super().__init__()
        self.enum = enum_
        if self.enum is not None:
            for item in self.enum:
                self.addItem(item.get_ui_title()[basic_types.Language.get_active_language()], item)

    # ===========================================================================
    def get_value(self):
        return self.currentData()

    # ===========================================================================
    def set_value(self, value):
        if value is None:
            self.setCurrentIndex(-1)
        else:
            index = self.findData(value)
            self.setCurrentIndex(index)

    # ===========================================================================
    def set_enum(self, new_enum):
        self.blockSignals(True)
        self.clear()
        self.enum = new_enum
        for item in new_enum:
            self.addItem(item.get_ui_title()[basic_types.Language.get_active_language()], item)
        self.blockSignals(False)
        self.setCurrentIndex(-1)


# ===========================================================================
class ComboBox_for_SingleItemSelectorEditor(QtWidgets.QComboBox, Widget_for_Editor):
    create_new_item_signal = QtCore.pyqtSignal()
    edit_item_signal = QtCore.pyqtSignal()
    current_selection_changed = QtCore.pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')

    # ===========================================================================
    def __init__(self, parent=None):

        super().__init__(parent)
        self.currentIndexChanged.connect(self.selection_changed)
        self.previous_selected_index = -1

    # ===========================================================================
    def selection_changed(self):
        if self.previous_selected_index > -1:
            previous_data = self.itemData(self.previous_selected_index)
        else:
            previous_data = None
        if self.currentIndex() > -1:
            new_data = self.currentData()
        else:
            new_data = None

        self.current_selection_changed.emit(previous_data, new_data)

    # ===========================================================================
    def update_items(self, items):
        if self.currentIndex() > -1:
            current_item = self.currentData()
        else:
            current_item = None

        self.clear()
        self.setCurrentIndex(-1)
        index = 0

        for item in items:
            self.addItem(str(item), item)
            if item == current_item:
                self.setCurrentIndex(index)
            index += 1

    # ===========================================================================
    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        new_item_action = menu.addAction('new item ...')
        edit_item_action = menu.addAction('edit item ...')
        action = menu.exec(self.mapToGlobal(event.pos()))
        if action == new_item_action:
            self.create_new_item_signal.emit()
        if action == edit_item_action:
            self.edit_item_signal.emit()

    # ===========================================================================
    def get_value(self):
        if self.currentIndex() > -1:
            return self.currentData()
        return None

    # ===========================================================================
    def set_value(self, value):
        index = self.findData(value, flags=QtCore.Qt.MatchExactly)
        self.previous_selected_index = self.currentIndex()
        self.setCurrentIndex(index)


# ===========================================================================
class CheckBoxGroup_for_MultipleItemSelectorEditor(QtWidgets.QWidget, Widget_for_Editor):
    value_changed_signal = QtCore.pyqtSignal()

    # ===========================================================================
    def __init__(self, field_for_retrieving_dependent_on_list_item, parent=None):

        super().__init__(parent, flags=QtCore.Qt.Widget)

        # self.dependent_list_item_type = dependent_list_item_type
        self.field_for_retrieving_dependent_on_list_item = field_for_retrieving_dependent_on_list_item
        self.setLayout(QtWidgets.QVBoxLayout())
        self.items = tools.IndexEnabledDict()

    # ===========================================================================
    def update_items(self, items):

        # remove check-boxes of items not present in the list
        for check_box in self.items.keys():
            if self.items[check_box] not in items:
                check_box.stateChanged.disconnect(self.value_changed_signal)
                check_box.deleteLater()
                del self.items[check_box]

        for i, item in enumerate(items):

            # check for correct index if item already exists
            if item in self.items.values():
                index = self.items.values().index(item)
                self.items.keys()[index].setText(item.name)
                if index != i:
                    check_box = self.items.values()[index]
                    del self.items[check_box]
                    self.items.insert(i, check_box, item)

            # insert the item if it does not exist
            else:
                check_box = QtWidgets.QCheckBox(item.name)
                check_box.stateChanged.connect(self.value_changed_signal)
                self.items.insert(i, check_box, item)
                self.layout().insertWidget(i, check_box)

    # ===========================================================================
    def get_value(self):
        value = []
        for check_box in self.items.keys():
            if check_box.isChecked():
                value.append(self.items[check_box])
        return value

    # ===========================================================================
    def set_value(self, value):

        if self.items and not isinstance(value.type, type(self.items.values()[0])):
            new_value = []
            for item in value:
                new_value.append(item[self.field_for_retrieving_dependent_on_list_item])
            value = new_value

        for check_box in self.items.keys():
            check_box.setChecked(self.items[check_box] in value)


# ===========================================================================
class Widget_for_ThingEditor(QtWidgets.QWidget, Widget_for_Editor):
    # ===========================================================================
    def __init__(self, parent=None):
        super().__init__(parent, flags=QtCore.Qt.Widget)
        self.setLayout(widget_basics.VLayout())

        # labels should be saved based on their assigned field (for later updating)
        self.labels = dict()
        self.widgets = dict()

    # ===========================================================================
    def insert_widget_with_label(self, index, field, sub_editor):
        # added labels should be saved for future updates
        self.labels[field] = self.layout().insert_widget_with_label(index, field.get_ui_title()[basic_types.Language.get_active_language()], sub_editor.widget)
        self.widgets[field] = sub_editor.widget
        if field.is_hidden():
            self.labels[field].hide()
            self.widgets[field].hide()

    # ===========================================================================
    def change_hiding_status(self, field):
        if field.is_hidden():
            self.widgets[field].hide()
            self.labels[field].hide()
        else:
            self.widgets[field].show()
            self.labels[field].show()

    # ===========================================================================
    def change_label_text(self, field):
        self.labels[field].setText(field.get_ui_title()[basic_types.Language.get_active_language()])


# ===========================================================================
class Widget_for_TableRowThingEditor(QtWidgets.QWidget, Widget_for_Editor):
    # ===========================================================================
    def __init__(self, parent=None):
        super().__init__(parent, flags=QtCore.Qt.Widget)


# ===========================================================================
class TableWidget_for_TableOfThingsEditor(QtWidgets.QTableWidget, Widget_for_Editor):
    # ===========================================================================
    def __init__(self, headers, parent=None):
        super().__init__(parent)

        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)


# ===========================================================================
class TreeWidgetItem_for_TreeNodeThingEditor(QtWidgets.QWidget, Widget_for_Editor):
    # ===========================================================================
    item_column = 0
    expand_column = 1

    # ===========================================================================
    def __init__(self, parent_entry, field):
        QtWidgets.QWidget.__init__(self, flags=QtCore.Qt.Widget)
        Widget_for_Editor.__init__(self)
        if isinstance(parent_entry, TreeWidgetItem_for_TreeNodeThingEditor):
            parent_entry = parent_entry.tree_item
        self.tree_item = QtWidgets.QTreeWidgetItem(parent_entry)
        self.field = field
        self.save_expand()

    # ===========================================================================
    def get_name(self):
        return self.tree_item.text(0)

    # ===========================================================================
    def set_name(self, name):
        self.tree_item.setText(0, name)

    # ===========================================================================
    def save_expand(self):
        # TODO: work on this
        expand = self.tree_item.isExpanded()
        self.tree_item.setData(TreeWidgetItem_for_TreeNodeThingEditor.expand_column, QtCore.Qt.UserRole, expand)

    # ===========================================================================
    def restore_expand(self):
        # TODO: work on this
        expand = self.tree_item.data(TreeWidgetItem_for_TreeNodeThingEditor.expand_column, QtCore.Qt.UserRole)
        self.tree_item.setExpanded(expand)

    # ===========================================================================
    def remove_child(self, child):
        self.tree_item.removeChild(child.tree_item)

    # ===========================================================================
    def set_hidden(self, hide):
        self.tree_item.setHidden(hide)

    # ===========================================================================
    def is_selected(self):
        return self.tree_item.isSelected()

    # ===========================================================================
    def get_value(self):
        return self.tree_item.data(TreeWidgetItem_for_TreeNodeThingEditor.item_column, QtCore.Qt.UserRole)

    # ===========================================================================
    def set_value(self, value):
        self.tree_item.setData(TreeWidgetItem_for_TreeNodeThingEditor.item_column, QtCore.Qt.UserRole, value)

        # convert the value to text for the node
        if isinstance(value, thing_.ListOfThings):
            if self.field:
                self.set_name(self.field.get_ui_title()[basic_types.Language.get_active_language()])
            else:
                self.set_name('{}s'.format(value.type))
        elif isinstance(value, thing_.Thing):
            # field of thing but the value is also thing
            if self.field:
                self.set_name('{}: {}'.format(self.field.get_ui_title()[basic_types.Language.get_active_language()], value.name))
            # thing editor
            else:
                self.set_name(value.name)
        # field editor
        else:
            self.set_name('{}: {}'.format(self.field.get_ui_title()[basic_types.Language.get_active_language()], value))

    # ===========================================================================
    def replace_field_name(self, new_name):
        value = self.get_value()
        # convert the value to text for the node
        if isinstance(value, thing_.ListOfThings):
            self.set_name(new_name)
        elif isinstance(value, thing_.Thing):
            self.set_name('{}: {}'.format(new_name, value.name))
        else:
            self.set_name('{}: {}'.format(new_name, value))

    # ===========================================================================
    def set_selected(self, select):
        self.tree_item.setSelected(select)


# ===========================================================================
class TreeWidget_for_TreeOfThingsEditor(QtWidgets.QTreeWidget, Widget_for_Editor):
    _instances = set()

    # ===========================================================================
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # for enabling and disabling multi-selection
        self._instances.add(weakref.ref(self))

    # for enabling and disabling multi-selection ================================
    @classmethod
    def get_instances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead
