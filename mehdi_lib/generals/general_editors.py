# -*- coding: utf-8 -*-

from mehdi_lib.basics import basic_types, editor_, widget_basics, thing_
from mehdi_lib.generals import widgets_for_editors, general_fields

from PyQt5 import QtCore
from PyQt5 import QtWidgets


# ===========================================================================
class AttachmentEditor(editor_.Editor):

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):
        self.widget = widgets_for_editors.LineEdit_for_AttachmentEditor()
        self.widget.value_changed_signal.connect(self.value_changed_by_me_signal)


# ===========================================================================
class BoolEditor(editor_.Editor):

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):

        self.widget = widgets_for_editors.CheckBox_for_BoolEditor(self.field.get_ui_title()[basic_types.Language.get_active_language()])
        self.widget.stateChanged.connect(self.value_changed_by_me_signal)


# ===========================================================================
class CommentEditor(editor_.Editor):

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):
        self.widget = widgets_for_editors.LineEdit_for_CommentEditor()
        self.widget.value_changed_signal.connect(self.value_changed_by_me_signal)


# ===========================================================================
class DateEditor(editor_.Editor):

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):
        self.widget = widgets_for_editors.LineEdit_for_DateEditor()
        self.widget.value_changed_signal.connect(self.value_changed_by_me_signal)


# ===========================================================================
class DatetimeEditor(editor_.Editor):

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):
        self.widget = widgets_for_editors.LineEdit_for_DateTimeEditor()
        self.widget.value_changed_signal.connect(self.value_changed_by_me_signal)


# ===========================================================================
class DummyEditor(editor_.Editor):
    pass


# ===========================================================================
class DurationEditor(editor_.Editor):

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):
        self.widget = widgets_for_editors.LineEdit_for_DurationEditor()
        self.widget.value_changed_signal.connect(self.value_changed_by_me_signal)


# ===========================================================================
class EnumItemSelectorEditor(editor_.Editor):

    # ===========================================================================
    def __init__(self, owner, enum_field, enum_: basic_types.UiTitleEnabledEnum, responsible=False, parent_editor=None):

        self._enum = enum_

        super().__init__(owner=owner, field=enum_field, responsible=responsible, parent_editor=parent_editor)
        self.editor_version_of_the_field.enum_changed_signal.connect(self.widget.set_enum)

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):
        self.widget = widgets_for_editors.ComboBox_for_EnumItemSelectorEditor(self._enum)
        self.widget.currentIndexChanged.connect(self.value_changed_by_me_signal)

    # ===========================================================================
    def unregister(self):
        super().unregister()
        self.editor_version_of_the_field.enum_changed_signal.disconnect(self.widget.set_enum)


# ===========================================================================
class FileNameEditor(editor_.Editor):

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):
        self.widget = widgets_for_editors.LineEdit_for_FileNameEditor()
        self.widget.value_changed_signal.connect(self.value_changed_by_me_signal)


# ===========================================================================
class FilePathEditor(editor_.Editor):

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):
        self.widget = widgets_for_editors.LineEdit_for_FilePathEditor()
        self.widget.value_changed_signal.connect(self.value_changed_by_me_signal)


# ===========================================================================
class FloatEditor(editor_.Editor):

    # ===========================================================================
    def __init__(self, owner, field, bottom: float, top: float, decimals: int, responsible=False, parent_editor=None):

        self.bottom = bottom
        self.top = top
        self.decimals = decimals

        super().__init__(owner=owner, field=field, responsible=responsible, parent_editor=parent_editor)

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):
        self.widget = widgets_for_editors.LineEdit_for_FloatEditor(self.bottom, self.top, self.decimals)
        self.widget.value_changed_signal.connect(self.value_changed_by_me_signal)


# ===========================================================================
class IntEditor(editor_.Editor):

    # ===========================================================================
    def __init__(self, owner, field, bottom: int, top: int, responsible=False, parent_editor=None):

        self.bottom = bottom
        self.top = top

        super().__init__(owner=owner, field=field, responsible=responsible, parent_editor=parent_editor)

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):
        self.widget = widgets_for_editors.LineEdit_for_IntEditor(self.bottom, self.top)
        self.widget.value_changed_signal.connect(self.value_changed_by_me_signal)


# ===========================================================================
class MultipleItemSelectorEditor(editor_.Editor):

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):
        self.widget = widgets_for_editors.CheckBoxGroup_for_MultipleItemSelectorEditor(
            editor_.Editor__Dependency.dependency_parameters(self.owner, self.class_version_of_the_field).field_for_retrieving_dependent_on_list_item)
        self.widget.value_changed_signal.connect(self.widget_value_changed)

    # ===========================================================================
    def widget_value_changed(self):
        i_changed_the_value = False

        items = self.widget.get_value()

        dependency_parameters = editor_.Editor__Dependency.dependency_parameters(self.owner, self.class_version_of_the_field)

        # add items not existing in sub editors but exist in items list
        for item in items:
            found = False
            for existing_item in self.sub_editors.keys():
                if item == existing_item[dependency_parameters.field_for_retrieving_dependent_on_list_item]:
                    if self.sub_editors[existing_item].is_marked_for_removal():
                        if self.sub_editors[existing_item].set_marked_for_removal(mark_for_removal=False):
                            i_changed_the_value = True
                    found = True
                    break
            if not found:
                new_item = self.representing_object.type(self.owner, item)
                self.append_new_immediate_sub_editor(new_item)
                i_changed_the_value = True

        # remove items existing in sub editors but not in items list
        for key in self.sub_editors.keys():
            if self.sub_editors[key].representing_object[dependency_parameters.field_for_retrieving_dependent_on_list_item] not in items:
                if self.sub_editors[key].set_marked_for_removal(mark_for_removal=True):
                    i_changed_the_value = True

        if i_changed_the_value:
            self.value_changed_by_me_signal.emit()

    # ===========================================================================
    def insert_sub_editor_or_sub_dialog(self, index, item, responsible=False):
        sub_editor = ThingEditor(item, responsible=responsible, parent_editor=self)
        self.sub_editors.insert(index, item, sub_editor)


# ===========================================================================
class NameEditor(editor_.Editor):

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):
        self.widget = widgets_for_editors.LineEdit_for_NameEditor()
        self.widget.value_changed_signal.connect(self.value_changed_by_me_signal)


# ===========================================================================
class SelectorEditor(editor_.Editor):

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):

        self.widget = widgets_for_editors.CheckBox_for_SelectorEditor(self.owner)
        self.widget.stateChanged.connect(self.value_changed_by_me_signal)


# ===========================================================================
class SingleItemSelectorEditor(editor_.Editor):

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):
        self.widget = widgets_for_editors.ComboBox_for_SingleItemSelectorEditor()
        self.widget.currentIndexChanged.connect(self.value_changed_by_me_signal)
        self.widget.create_new_item_signal.connect(self.create_new_item)
        self.widget.edit_item_signal.connect(self.edit_item)

    # ===========================================================================
    def create_new_item(self):
        new_item = self.field.in_class.type()
        temp_editor = ThingEditor(new_item)
        dialog = editor_.EditorDialog(temp_editor, automatic_unregister=True)
        if dialog.exec():
            # TODO: dependency_parameters(...) could return None, should be checked why (has happened, maybe because set dependency parameters has not been defined??)
            editor_.Editor__Dependency.dependency_parameters(self.owner, self.class_version_of_the_field).dependent_on_list.append(new_item)

    # ===========================================================================
    def edit_item(self):
        current_item = self.widget.currentData()
        if current_item:
            temp_editor = ThingEditor(current_item)
            editor_.EditorDialog(temp_editor, automatic_unregister=True).exec()


# ===========================================================================
class ThingEditor(editor_.Editor):
    # ===========================================================================
    def __init__(self, owner: 'thing_.Thing', responsible=False, parent_editor=None):

        self.n_sub_dialogs = 0
        super().__init__(owner=owner, field=None, responsible=responsible, parent_editor=parent_editor)

    # ===========================================================================
    def add_button(self, index, field, responsible):
        self.n_sub_dialogs += 1
        self.widget.layout().insert_widget(index, widget_basics.ButtonWithActionParameters(
            field.get_ui_title()[basic_types.Language.get_active_language()], editor_.Editor__Basics.create_editor_and_open_dialog, [self.owner, field, responsible, self], self.widget))

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):
        self.widget = widgets_for_editors.Widget_for_ThingEditor()
        for field in self.owner.get_sorted_fields_of_instance(include_primary_key=True):
            self.insert_sub_editor_or_sub_dialog(len(self.sub_editors), field)

    # ===========================================================================
    def insert_sub_editor_or_sub_dialog(self, index, field, responsible=False):
        sub_editor = editor_.Editor__Basics.proper_editor(self.owner, field, responsible=responsible, parent_editor=self)
        if sub_editor:

            # simple field editor
            if sub_editor.type == editor_.EditorTypes.field_of_thing:
                responsible_editor = self.owner.get_responsible_editor(field)
                self.widget.insert_widget_with_label(index, responsible_editor.editor_version_of_the_field, sub_editor)
                # if field.is_instance_specific():
                #     responsible_editor.editor_version_of_the_field.ui_titles_changed_signal.connect(self.widget.change_label_text)
                #     responsible_editor.editor_version_of_the_field.hiding_status_changed_signal.connect(self.widget.change_hiding_status)

                # only simple field editors will be added to the sub_editor list
                self.sub_editors.insert(index, field, sub_editor)

            # either list field editor or thing editor (this will not be added to sub_editor array)
            else:
                self.add_button(index, field, responsible=False)

        else:
            self.hidden_values[self.owner.get_correspondent_class_field(field)] = self.owner[field]

    # ===========================================================================
    # def unregister(self):
    #     super().unregister()

        # for field in self.sub_editors.keys():
        #     if self.sub_editors[field].type == editor_.EditorTypes.field_of_thing and field.is_instance_specific():
        #         self.owner.get_responsible_editor(field).editor_version_of_the_field.ui_titles_changed_signal.disconnect(self.widget.change_label_text)


# ===========================================================================
class TableOfThingsEditor(editor_.Editor):
    # ===========================================================================
    class TableRowThingEditor(editor_.Editor):
        # ===========================================================================
        def __init__(self, owner, row, ignored_field, responsible=False, parent_editor=None):

            self.n_sub_dialogs = 0
            self.row = row
            self.ignored_field = ignored_field
            super().__init__(owner=owner, field=None, responsible=responsible, parent_editor=parent_editor)

        # ===========================================================================
        def eventFilter(self, object_, event):
            if super().eventFilter(object_, event):
                return True
            if event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
                for field in self.sub_editors.keys():
                    if self.sub_editors[field].widget == object_:
                        self.parent_editor.sub_editors.values()[self.row].set_selected(True)
                        break
            return False

        # ===========================================================================
        def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):
            self.widget = widgets_for_editors.Widget_for_TableRowThingEditor()
            for field in self.owner.get_sorted_fields_of_instance(include_primary_key=False):
                if field != self.ignored_field:
                    self.insert_sub_editor_or_sub_dialog(len(self.sub_editors), field)

        # ===========================================================================
        def set_selected(self, select):
            super().set_selected(select)
            for field in self.sub_editors.keys():
                sub_editor = self.sub_editors[field]
                if isinstance(sub_editor.widget, widgets_for_editors.LineEdit_for_LineEditor):
                    sub_editor.widget.set_selected(select)

        # ===========================================================================
        def insert_sub_editor_or_sub_dialog(self, index, field, responsible=False):
            sub_editor = editor_.Editor__Basics.proper_editor(self.owner, field, responsible=responsible, parent_editor=self)
            if sub_editor:
                # simple field editor
                if sub_editor.type == editor_.EditorTypes.field_of_thing:

                    sub_editor.widget.installEventFilter(self)

                    self.parent_editor.widget.setCellWidget(self.row, len(self.sub_editors) + self.n_sub_dialogs, sub_editor.widget)

                    # only simple field editors will be added to the sub_editor list
                    self.sub_editors.insert(index, field, sub_editor)

                # either list field editor or thing editor (this will not be added to sub_editor array)
                else:
                    self.add_button(field, responsible)

        # ===========================================================================
        def add_button(self, field, responsible):
            self.n_sub_dialogs += 1
            button = widget_basics.ButtonWithActionParameters(field.get_ui_title()[basic_types.Language.get_active_language()], editor_.Editor__Basics.create_editor_and_open_dialog, [self.owner, field, responsible, self], self.parent_editor.widget)
            button.installEventFilter(self)
            self.parent_editor.widget.setCellWidget(self.row, len(self.sub_editors) + self.n_sub_dialogs - 1, button)

    # ===========================================================================
    def __init__(self, owner: ['thing_.Thing', 'thing_.ListOfThings'], field: ['general_fields.ListField', None], responsible=False, parent_editor=None):

        self.ignored_field = None
        super().__init__(owner=owner, field=field, responsible=responsible, parent_editor=parent_editor)
        self.show_buttons = True

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):

        # headers
        headers = []

        if isinstance(self.owner, thing_.Thing):
            fields = self.field.in_class.initial_value.sorted_fields_of_class(include_primary_key=False)
        # owner is a list
        else:
            fields = self.owner.type.sorted_fields_of_class(include_primary_key=False)

        owner_of_foreign_key_skipped = not isinstance(self.owner, thing_.Thing)
        for field in fields:
            if not owner_of_foreign_key_skipped and isinstance(field, general_fields.ForeignKeyField) and \
                    isinstance(self.owner, field.foreign_prototype.get_main_type()):
                self.ignored_field = field
                owner_of_foreign_key_skipped = True
                continue
            active_language = basic_types.Language.get_active_language()
            headers.append(field.get_ui_title()[active_language])

        self.widget = widgets_for_editors.TableWidget_for_TableOfThingsEditor(headers)

        self.widget.verticalHeader().sectionDoubleClicked.connect(self.edit)
        self.widget.verticalHeader().sectionClicked.connect(lambda row: self.sub_editors.values()[row].set_selected(True))

    # ===========================================================================
    def insert_sub_editor_or_sub_dialog(self, index, item, responsible=False):
        self.widget.insertRow(index)
        sub_editor = TableOfThingsEditor.TableRowThingEditor(owner=item, row=index, ignored_field=self.ignored_field, responsible=responsible, parent_editor=self)
        self.sub_editors.insert(index, item, sub_editor)

    # ===========================================================================
    def remove_sub_editor_widget(self, item):
        row = self.sub_editors[item].row
        self.widget.removeRow(row)

    # ===========================================================================
    def set_hidden(self, item, hide: bool):
        row = self.sub_editors[item].row
        self.widget.setRowHidden(row, hide)


# ===========================================================================
class TreeOfThingsEditor(editor_.Editor):
    # ===========================================================================
    class TreeNodeThingEditor(editor_.Editor):
        # ===========================================================================
        def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):
            self.widget = widgets_for_editors.TreeWidgetItem_for_TreeNodeThingEditor(self.parent().widget, self.field)
            if self.type == editor_.EditorTypes.thing:
                for field in self.owner.get_sorted_fields_of_instance(include_primary_key=False):
                    if field.in_editor:
                        self.insert_sub_editor_or_sub_dialog(len(self.sub_editors), field)

            elif self.type == editor_.EditorTypes.list_of_things:
                for thing in self.representing_object:
                    self.insert_sub_editor_or_sub_dialog(len(self.sub_editors), thing)

        # ===========================================================================
        def save_expand(self):

            self.widget.save_expand()
            for editor in self.sub_editors.values():
                editor.save_expand()

        # ===========================================================================
        def restore_expand(self):

            self.widget.restore_expand()
            for editor in self.sub_editors.values():
                editor.restore_expand()

        # ===========================================================================
        def context_menu(self, event, event_pos=None):
            if self.widget.is_selected():
                menu = QtWidgets.QMenu(None)
                if self.type == editor_.EditorTypes.list_of_things or (self.parent_editor and self.parent_editor.type == editor_.EditorTypes.list_of_things):
                    new_item_action = menu.addAction('new item ...')
                edit_item_action = menu.addAction('edit item ...')

                action = menu.exec(event_pos)

                if self.type == editor_.EditorTypes.list_of_things and action == new_item_action:
                    self.append_new_item(is_top_editor=True)
                elif self.parent_editor and self.parent_editor.type == editor_.EditorTypes.list_of_things and action == new_item_action:
                    self.parent_editor.append_new_item(is_top_editor=True)

                if action == edit_item_action:
                    editor_.EditorDialog(editor_.Editor__Basics.proper_editor(self.owner, self.field), automatic_unregister=True).exec()
            else:
                for editor in self.sub_editors.values():
                    if editor.is_selected(go_deep=True):
                        editor.context_menu(event, event_pos)
                        break

        # ===========================================================================
        def update_selection(self):
            for sub_editor in self.sub_editors.values():
                if sub_editor.widget.is_selected():
                    sub_editor.set_selected(True)
                else:
                    sub_editor.set_selected(False)
                sub_editor.update_selection()

        # ===========================================================================
        def insert_sub_editor_or_sub_dialog(self, index, item, responsible=False):
            sub_editor = None

            # thing
            if self.type == editor_.EditorTypes.thing:
                sub_editor = TreeOfThingsEditor.TreeNodeThingEditor(self.owner, item, responsible=responsible, parent_editor=self)

            # list of things
            elif self.type == editor_.EditorTypes.list_of_things:
                sub_editor = TreeOfThingsEditor.TreeNodeThingEditor(item, None, responsible=responsible, parent_editor=self)

            if sub_editor:
                self.sub_editors.insert(index, item, sub_editor)

        # ===========================================================================
        def remove_sub_editor_widget(self, item):
            self.widget.remove_child(self.sub_editors[item].widget)

        # ===========================================================================
        def remove_sub_editor(self, item):
            # first remove sub editors of this sub editor
            for sub_item in self.sub_editors[item].sub_editors.keys():
                self.sub_editors[item].remove_sub_editor(sub_item)

            # now it is the turn of this sub editor
            super().remove_sub_editor(item)

        # ===========================================================================
        def set_hidden(self, item, hide: bool):
            self.sub_editors[item].widget.set_hidden(hide)

    # ===========================================================================
    def __init__(self, owner: ['thing_.Thing', 'thing_.ListOfThings'],
                 field: ['general_fields.ListField', None],
                 responsible=False, parent_editor=None):

        super().__init__(owner=owner, field=field, responsible=responsible, parent_editor=parent_editor)
        self.show_buttons = True

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):
        self.widget = widgets_for_editors.TreeWidget_for_TreeOfThingsEditor()
        self.widget.itemSelectionChanged.connect(self.update_selection)
        self.widget.viewport().installEventFilter(self)

    # ===========================================================================
    def eventFilter(self, object_, event):
        if super().eventFilter(object_, event):
            return True
        if event.type() == QtCore.QEvent.MouseButtonDblClick and event.button() == QtCore.Qt.LeftButton:
            self.edit()
        if event.type() == QtCore.QEvent.ContextMenu:
            self.context_menu(event)
            return True
        return False

    # ===========================================================================
    def context_menu(self, event):
        for editor in self.sub_editors.values():
            if editor.is_selected(go_deep=True):
                editor.context_menu(event, self.widget.viewport().mapToGlobal(event.pos()))
                break

    # ===========================================================================
    def update_selection(self):
        for sub_editor in self.sub_editors.values():
            if sub_editor.widget.is_selected():
                sub_editor.set_selected(True)
            else:
                sub_editor.set_selected(False)
            sub_editor.update_selection()

    # ===========================================================================
    def insert_sub_editor_or_sub_dialog(self, index, item, responsible=False):
        sub_editor = TreeOfThingsEditor.TreeNodeThingEditor(owner=item, field=None, responsible=responsible, parent_editor=self)
        self.sub_editors.insert(index, item, sub_editor)

    # ===========================================================================
    def remove_sub_editor_widget(self, item):
        self.widget.invisibleRootItem().removeChild(self.sub_editors[item].widget.tree_item)

    # ===========================================================================
    def set_hidden(self, item, hide: bool):
        self.sub_editors[item].widget.set_hidden(hide)

    # ===========================================================================
    @staticmethod
    def new_tree_editor_from_node(node_editor):
        list_ = None
        if node_editor.type == editor_.EditorTypes.thing:
            list_ = thing_.ListOfThings(type(node_editor.representing_object))
            list_.append(node_editor.representing_object)
        elif node_editor.type == editor_.EditorTypes.list_of_things:
            list_ = node_editor.representing_object

        if list_:
            tree_editor = TreeOfThingsEditor(list_, None, responsible=False, parent_editor=None)
        else:
            tree_editor = None
        return tree_editor



