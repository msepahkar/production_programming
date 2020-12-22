# -*- coding: utf-8 -*-

import enum
import typing

from PyQt5 import QtWidgets, QtCore

from mehdi_lib.basics import widget_basics, basic_types, thing_
from mehdi_lib.tools import tools
from mehdi_lib.generals import widgets_for_editors, general_fields, general_editors_prototypes, general_ui_titles

"""
For improving readability, Editor class is divided into several classes each of which containing several methods 
required for some part of Editor jobs. Each class will be derived from the previous class until the final Editor class
is created as could be seen from the following code.
"""

# ===========================================================================
class EditorTypes(enum.Enum):
    """Three types available for editors

    1- The simplest and most general form is editor for field. It edits only one single
     field.
    2- The second general form is the editor for "Thing" (the heart of this infrastructure).
    3- The third and the last type is editor for editing list of things. This last one will add or remove "Things" to
     or from the list.
    """

    field_of_thing = 1
    thing = 2
    list_of_things = 3


# ===========================================================================
class EditorValue:
    """Current value in editor

    The final values of fields are different from their value in editors until the user presses the "OK" button in the
    UI. After confirmation by the user, the editor will update the value of the field in memory.
    For field editors and thing editors there is no problem keeping track of changes in editor while still keeping the
    original value. But for list of things there are difficulties when items are added to the list or removed from it.
    So instead of really removing items from the list they will be marked for removal until the user presses "OK".
    Similar approach is used for added items to the list they will be stored in a list called new_items until the user
    presses "OK".
    """

    # ===========================================================================
    def __init__(self, value, new_items: typing.Optional[list] = None,
                 items_marked_for_removal: typing.Optional[list] = None):
        self.value = value
        self.new_items = new_items
        self.items_marked_for_removal = items_marked_for_removal


# ===========================================================================
class Editor__Removing_Reviving_AddingNew(QtCore.QObject):
    """Required methods for adding and removing

    This class is specially designed for list of things (although its methods will be used in thing editors too but even
    those usages are for things which are in lists of things). Adding items to the list and removing items from it have
    difficulties because the memory version of the list should be untouched until the user presses "OK" button in the
    UI. All methods for keeping track of removed items in the UI and new items in the UI are included in this class.
    """

    # these two signals make the UI able to enable or disable the revive button (the button which revives the last
    #  removed item).
    sub_editor_marked_for_removal_exists_signal = QtCore.pyqtSignal()
    no_sub_editor_marked_for_removal_exists_signal = QtCore.pyqtSignal()

    # when the sub editor is totally removed or when it is revived this signal will be emitted
    no_revival_possible_signal = QtCore.pyqtSignal()

    # ===========================================================================
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # for "Thing" which is marked for removal
        self._is_marked_for_removal = False

        # for "Thing" which is created in the editor for list of things
        self._is_new = False

        # list of sub editors which are marked for removal
        self.sub_editors_marked_for_removal = []

        # thing editor will have sub editors for editing its fields
        self.sub_editors = tools.IndexEnabledDict()

        self.keys_for_immediate_sub_editors_created_by_me = []

    # ===========================================================================
    def is_marked_for_removal(self):
        return self._is_marked_for_removal

    # ===========================================================================
    # TODO: write test function for this method
    def set_marked_for_removal(self, mark_for_removal) -> bool:

        if mark_for_removal:
            # only thing editors could be marked for removal
            if self.type == EditorTypes.thing and not self._is_marked_for_removal:
                found_editors = []
                # check for dependency
                if self.parent_editor:
                    dependent_editors = self.parent_editor.all_dependent_responsible_editors()
                    for dependent_editor in dependent_editors:
                        dependency_parameters = Editor__Dependency.dependency_parameters(dependent_editor.owner, dependent_editor.class_version_of_the_field)
                        # this item has been used somewhere, we cannot mark it for removal
                        if dependent_editor.representing_object[
                            dependency_parameters.field_for_retrieving_dependent_on_list_item] == \
                                self.representing_object:
                            found_editors.append(dependent_editor)
                    if found_editors:
                        dialog = widget_basics.Dialog()
                        sub_dialogs = []
                        dialog.add_widget(QtWidgets.QLabel('dependent editors:'))
                        for editor in found_editors:
                            sub_dialogs.append(EditorDialog(Editor__Basics.proper_editor(editor.owner, editor.field),
                                                            automatic_unregister=True))
                            dialog.add_widget(widget_basics.Button(editor.owner.name, sub_dialogs[-1].exec, dialog))
                        dialog.exec()
                        return False

                self._is_marked_for_removal = True
                return True

        elif self._is_marked_for_removal:
            self._is_marked_for_removal = False

            # this signal is required for removing revived sub editor from the removed sub editors array
            self.no_revival_possible_signal.emit()

            return True

        return False

    # ===========================================================================
    def is_new(self):
        return self._is_new

    # ===========================================================================
    def set_is_new(self, is_new):
        if is_new:
            # only thing editors could be marked as new
            if self.type == EditorTypes.thing and not self._is_new:
                self._is_new = True
        elif self._is_new:
            self._is_new = False

    # ===== should be implemented in each editor
    # TODO: could it be not implemented error?
    def insert_sub_editor_or_sub_dialog(self, index, item):
        pass

    # ===== should be implemented in each editor
    # TODO: could it be not implemented error?
    def remove_sub_editor_widget(self, item):
        pass

    # ===========================================================================
    # TODO: add comment for this method
    # TODO: add test for this method
    def remove_sub_editor(self, item):
        self.remove_sub_editor_widget(item)
        self.sub_editors[item].unregister()
        self.sub_editors[item].no_revival_possible_signal.emit()
        del self.sub_editors[item]

    # ===========================================================================
    # TODO: newly added item should become the center of focus in the UI
    def append_new_item(self, is_top_editor: bool) -> bool:
        """Appends a new item to the currently selected item.

        First, sub-editors will be checked to see if they or their children or grand-children or ... are selected. If
         so, the new item will be appended to the selected editor regardless of is_top_editor value.
        If nothing is selected but is_top_editor is set to True, self.editor will be considered as the selected editor.
        When the selected editor is found, it is time to check for list of things. As new item could only be added to
         list of things, the selected editor or its parent or grand-parent or ... which is list of things will be the
         final candidate for adding new item. If no list of things editor is found, adding new item will not be done!

        :param is_top_editor: bool
            When this parameter is True, self.editor will be considered as the selected editor. Although, its
             sub-editors will still be checked to see if they are selected too. And if yes, they will be the candidate
             for adding the new item.
        :return: bool
            If adding new item is done successfully True is returned, otherwise False will be returned.
        """

        # check for possible selected sub editor
        #  if found, new item should be added to that
        for sub_editor in self.sub_editors.values():
            if sub_editor.is_selected(go_deep=True):
                return sub_editor.append_new_item(is_top_editor=False)

        editor = None

        # we are the main editor calling for appending new item or we are the selected node?
        if is_top_editor or self.is_selected(go_deep=False):
            editor = self
            while editor.type is not EditorTypes.list_of_things and editor.parent_editor:
                editor = editor.parent_editor

            # only list of things can add new item!
            if editor.type is not EditorTypes.list_of_things:
                editor = None

        # found the proper editor?
        if editor:

            # create the new thing first
            new_thing = editor.create_new_thing_for_immediate_sub_editor()
            if new_thing:

                # now create the sub-editor for the new thing
                editor.append_new_immediate_sub_editor(new_thing)

                # update the ui for showing the newly created item
                editor.redraw_items()

                # tell other editors of the same thing about the change
                editor.value_changed_by_me_signal.emit()

                return True

        return False

    # ===========================================================================
    def mark_selected_sub_editor_for_removal(self, is_top_editor: bool) -> list:
        """Marks the selected editor for removal

        it searches all sub-editors and their children and grand children and ... to reach selected sub-editors.
        when selected sub-editor is found, searching will not go further in depth. it means that children of the
         selected sub-editors will not be searched. the reason is that when selected sub-editor is marked for removal,
         automatically the children will be removed. so there is no need for going further in depth.
        for each found selected sub-editor, first it will be marked by removal by calling the proper method. then it
         will be added to the marked_sub_editors array to be returned at the end of the method.

        :param is_top_editor: bool
            if is set to True:
                connects signal for revivial button
                emits signal for marking a sub-editor for removal
                parent-editor will inform other editors about the marking for removal
        :return: list
            list of sub-editors marked for removal
        """

        marked_sub_editors = []

        # look for a selected sub editor
        for key in self.sub_editors.keys():

            # is this node selected itself?
            if self.sub_editors[key].is_selected(go_deep=False):

                # try marking it for removal
                if self.sub_editors[key].set_marked_for_removal(mark_for_removal=True):
                    marked_sub_editors.append(self.sub_editors[key])

            # seems you should go deeper!
            elif self.sub_editors[key].is_selected(go_deep=True):
                for marked_sub_editor in self.sub_editors[key].mark_selected_sub_editor_for_removal(is_top_editor=False):
                    marked_sub_editors.append(marked_sub_editor)

        # some editor is marked for removal and we are in the main window
        if len(marked_sub_editors) > 0 and is_top_editor:

            # keep track of the removed sub editor for possible reviving
            for marked_sub_editor in marked_sub_editors:
                self.sub_editors_marked_for_removal.append(marked_sub_editor)

                # become aware when no revival is possible
                marked_sub_editor.no_revival_possible_signal.connect(self.sub_editor_revived_or_removed)

                # parent editor should tell other editors about the change
                marked_sub_editor.parent_editor.value_changed_by_me_signal.emit()

            # tell the revival button that we have removed items which can be revived
            self.sub_editor_marked_for_removal_exists_signal.emit()

            # select the sibling editor
            marked_sub_editors[-1].select_the_first_sibling_not_marked_for_removal_or_parent()

            # removed items should be hidden
            self.redraw_items()

        return marked_sub_editors

    # ===========================================================================
    def sub_editor_revived_or_removed(self):
        """Called when a sub-editor marked for removal is either revived or totally removed.

        It removes the sub-editor from the sub-editors-marked-for-removal-by-me list.
        It redraws items if the sub-editor has been removed by itself (to be shown if it is revived now).

        :return:
        """

        # find who called us
        sub_editor = self.sender()

        # have we marked this sub editor for removal?
        if sub_editor in self.sub_editors_marked_for_removal:

            # remove it from this list
            index = self.sub_editors_marked_for_removal.index(sub_editor)
            del self.sub_editors_marked_for_removal[index]

            # TODO: is this only for showing revived editor or also for hiding removed editor???
            # show it in case it has been revived.
            self.redraw_items()

        # check the revive array again
        if len(self.sub_editors_marked_for_removal) <= 0:
            self.no_sub_editor_marked_for_removal_exists_signal.emit()

    # ===========================================================================
    def revive_the_latest_sub_editor_marked_for_removal(self):
        """The name perfectly explains function job.

        The revived sub-editor will be selected.
        Parent editor will emit the value-changed-by-me-signal.
        The length of sub-editors-marked-for-removal array will be checked for emitting the no-sub-editor-marked-for-
         removal-exists-signal.

        :return:
        """

        # any sub editor available for revival?
        if len(self.sub_editors_marked_for_removal) > 0:

            sub_editor = self.sub_editors_marked_for_removal[-1]

            # the revived sub editor will be removed from the sub_editors_marked_for_removal array by a signal
            #  emitted in set_mark_for_removal(False) method
            if sub_editor.set_marked_for_removal(mark_for_removal=False):
                sub_editor.set_selected(True)
                sub_editor.parent_editor.value_changed_by_me_signal.emit()

        # check the revival list again
        if len(self.sub_editors_marked_for_removal) <= 0:
            self.no_sub_editor_marked_for_removal_exists_signal.emit()

    # ===========================================================================
    # TODO: add comment and test function
    def update_foreign_owners(self, previous_foreign_owner, new_foreign_owner):
        # ===========================================================================
        def foreign_owner_list_field_responsible_editor(owner, field, foreign_owner):
            responsible_editor = None

            if foreign_owner and field:

                class_version_of_the_field = owner.get_correspondent_class_field(field)

                # defined in foreign owner parameters, TODO: this part seems extra
                if class_version_of_the_field in owner.foreign_owner_parameters:
                    foreign_owner_parameters = owner.foreign_owner_parameters[class_version_of_the_field]
                    if foreign_owner_parameters:
                        list_field = foreign_owner_parameters.list_field_in_foreign_owner
                        responsible_editor = foreign_owner.get_responsible_editor(list_field)

                # should be found automatically
                # TODO: only the first list field of the owner will be detected (each thing can have only one
                #  list field containing certain thing type), it seems that things should be aware of their
                #  container list field
                elif isinstance(field, general_fields.ForeignKeyField):
                    for list_field in type(foreign_owner).sorted_list_fields_of_class():
                        if isinstance(owner, list_field.in_class.initial_value):
                            responsible_editor = foreign_owner.get_responsible_editor(list_field)
                            break

            return responsible_editor

        responsible_editor = foreign_owner_list_field_responsible_editor(self.owner, self.field, previous_foreign_owner)
        if responsible_editor:
            if self.owner in responsible_editor.sub_editors.keys():
                responsible_editor.remove_sub_editor(self.owner)
                responsible_editor.value_changed_by_me_signal.emit()

        # new_foreign_owner
        responsible_editor = foreign_owner_list_field_responsible_editor(self.owner, self.field, new_foreign_owner)
        if responsible_editor:
            if self.owner not in responsible_editor.sub_editors.keys():
                responsible_editor.insert_sub_editor_or_sub_dialog(len(self.sub_editors), self.owner)
                responsible_editor.value_changed_by_me_signal.emit()

    # ===========================================================================
    # TODO: we removed the function self.keys_for_immediate_sub_editors_marked_for_removal() check any possible malfunctionning
    def clear_tracking_information_regarding_sub_editors(self):
        self.keys_for_immediate_sub_editors_created_by_me.clear()

    # ===========================================================================
    # TODO: add comment and test method
    def create_new_thing_for_immediate_sub_editor(self):

        # check if any allowed dependent item is available
        new_thing = None
        allowed_dependent_on_list_items = []
        dependency_parameters = self.get_dependency_parameters()
        
        if self.get_dependency_parameters():
            for item in self.allowed_dependent_on_list_items():
                already_exists = False
                for sub_editor_key in self.sub_editors.keys():
                    if sub_editor_key[dependency_parameters.field_for_retrieving_dependent_on_list_item] == item:
                        already_exists = True
                        break
                if not already_exists:
                    allowed_dependent_on_list_items.append(item)
                    break

        # either we are not dependent or there still are available items
        if not dependency_parameters or allowed_dependent_on_list_items:

            # names already in the editor are forbidden (they may be absent in the all array because they are new
            forbidden_names = [sub_editor.owner.name for sub_editor in self.sub_editors.values()]

            # orden numbers already in the editor are forbidden (they may be absent in the all array because they
            # are new
            max_forbidden_number = max(sub_editor.owner.order_number
                                       for sub_editor in self.sub_editors.values()) if self.sub_editors else 0

            # list field of a thing
            if self.field:
                new_thing = self.field.in_class.initial_value(self.owner, max_forbidden_number=max_forbidden_number,
                                                              forbidden_names=forbidden_names)

            # an independent list
            else:
                new_thing = self.owner.type(max_forbidden_number=max_forbidden_number, forbidden_names=forbidden_names)

            # assign the dependent field for dependent editors
            if dependency_parameters:
                new_thing[dependency_parameters.field_for_retrieving_dependent_on_list_item] = \
                    allowed_dependent_on_list_items[0]
                
        return new_thing

    # ===========================================================================
    # TODO: add comment and test method
    def append_new_immediate_sub_editor(self, new_thing):
        self.insert_sub_editor_or_sub_dialog(len(self.sub_editors), new_thing)
        self.sub_editors[new_thing].set_is_new(True)
        self.sub_editors[new_thing].set_selected(True)
        self.keys_for_immediate_sub_editors_created_by_me.append(new_thing)


# ===========================================================================
class Editor__Selection(Editor__Removing_Reviving_AddingNew):

    multiple_selection = False

    # for enabling edit button
    sub_editor_selected_signal = QtCore.pyqtSignal()

    # for disabling edit button
    no_sub_editor_selected_signal = QtCore.pyqtSignal()

    # ===========================================================================
    def __init__(self, parent=None):

        super().__init__(parent=parent)

        self._is_selected = False

        # for enabling and disabling edit button
        self.selected_sub_editors = []

        self.multiple_selection = False

    # ===========================================================================
    def eventFilter(self, object_, event):

        # enabling multi selection by pressing shift or control key
        if event.type() == QtCore.QEvent.KeyPress and (event.key() == QtCore.Qt.Key_Control or event.key() == QtCore.Qt.Key_Shift):
            Editor__Selection.multiple_selection = True

        # disabling multi selection by releasing shift or control key
        if event.type() == QtCore.QEvent.KeyRelease and (event.key() == QtCore.Qt.Key_Control or event.key() == QtCore.Qt.Key_Shift):
            Editor__Selection.multiple_selection = False

        return False

    # ===========================================================================
    def is_selected(self, go_deep: bool) -> bool:
        if self._is_selected or self.widget.is_selected():
            return True
        if go_deep:
            for editor in self.sub_editors.values():
                if editor.is_selected(go_deep=True):
                    return True
        return False

    # ===========================================================================
    def set_selected(self, select: bool):
        """Sets selection state of the editor

        If select parameter is True and multiple selection is not allowed, all other selected editors should be
         deselected. Operation starts from the top-most editor.

        :param select: bool
        :return: None
        """
        # ===========================================================================
        def deselect_all_other_editors(selected_editor):
            # ===========================================================================
            def deselect_all_sub_editors_except_the_exception_editor(editor, exception_editor):
                for sub_editor in editor.sub_editors.values():
                    if sub_editor != exception_editor:
                        sub_editor.set_selected(False)
                    deselect_all_sub_editors_except_the_exception_editor(sub_editor, exception_editor)

            # start from the top parent editor
            parent_editor = selected_editor
            while parent_editor.parent_editor:
                parent_editor = parent_editor.parent_editor

            # deselect the top parent editor
            parent_editor.set_selected(False)

            # now time for all sub-editors
            deselect_all_sub_editors_except_the_exception_editor(parent_editor, exception_editor=selected_editor)

        # select
        if select:
            if not self._is_selected:
                self._is_selected = True
                self.widget.set_selected(True)
                if self.parent_editor:
                    # for enabling and disabling edit button
                    self.parent_editor.sub_editor_selected(self)
            if not Editor__Selection.multiple_selection:
                deselect_all_other_editors(selected_editor=self)

        # deselect
        elif self.is_selected(go_deep=False):
            self._is_selected = False
            self.widget.set_selected(False)
            if self.parent_editor:
                # for enabling and disabling edit button
                self.parent_editor.sub_editor_deselected(self)

    # ===========================================================================
    def selected_item_editor(self) -> 'Editor':
        """returns the editor of the selected item.

        if the selected item is this editor itself, then this editor itself will be returned!
        the actual usefulness of this method is when it is called on a parent editor. it will go down through its
         children until it reaches the selected editor.

        :return: Editor
        """

        editor = self
        if not self.is_selected(go_deep=False) and self.is_selected(go_deep=True):
            for sub_editor in self.sub_editors.values():
                if sub_editor.is_selected(go_deep=True):
                    editor = sub_editor.selected_item_editor()
                    break
        return editor

    # ===========================================================================
    def select_the_first_sibling_not_marked_for_removal_or_parent(self):
        """
        When a selected node is removed, its sibling should be selected, or its parent if there is no sibling.
        That is what this function does for us.
        :return: None
        """

        index_of_me = self.parent_editor.sub_editors.values().index(self)

        # first try the next siblings
        index = index_of_me + 1
        while index < len(self.parent_editor.sub_editors) and self.parent_editor.sub_editors.values()[index].is_marked_for_removal():
            index += 1

        # if none found, try the previous siblings
        if index >= len(self.parent_editor.sub_editors):
            index = index_of_me - 1
            while index >= 0 and self.parent_editor.sub_editors.values()[index].is_marked_for_removal():
                index -= 1

        # if found, please select it.
        if 0 <= index <= len(self.parent_editor.sub_editors):
            self.parent_editor.sub_editors.values()[index].set_selected(True)
        # otherwise select the parent
        else:
            self.parent_editor.set_selected(True)

    # ===========================================================================
    def sub_editor_selected(self, sub_editor: 'Editor'):
        """for keeping track of selected sub editors for enabling and disabling of the edit button

        when a sub-editor is selected, a signal which is connected to this method will be emitted.
        this method will add the selected sub-editor to an array and will call the same method in its parent.

        :param sub_editor: Editor
            the selected sub-editor
        :return:
        """

        if sub_editor not in self.selected_sub_editors:

            # for enabling and disabling edit button
            self.selected_sub_editors.append(sub_editor)

            # for enabling edit button
            self.sub_editor_selected_signal.emit()

        if self.parent_editor:
            self.parent_editor.sub_editor_selected(sub_editor)

    # ===========================================================================
    def sub_editor_deselected(self, sub_editor):
        """for keeping track of selected sub editors for enabling and disabling of the edit button

        when a sub-editor is deselected, a signal which is connected to this method will be emitted.
        this method will remove the selected sub-editor from the array and will call the same method in its parent.

        :param sub_editor: Editor
            the deselected sub-editor
        :return:
        """

        if sub_editor in self.selected_sub_editors:
            index = self.selected_sub_editors.index(sub_editor)
            del self.selected_sub_editors[index]

            if len(self.selected_sub_editors) <= 0:

                # for disabling edit button
                self.no_sub_editor_selected_signal.emit()

        if self.parent_editor:
            self.parent_editor.sub_editor_deselected(sub_editor)


# ===========================================================================
class Editor__Basics(Editor__Selection):

    # ===========================================================================
    def __init__(self, owner: ['thing_.Thing', None], field: ['field_.Field', None], parent=None):

        super().__init__(parent=parent)

        self.widget = None
        self.owner = owner
        self.field = field
        self.setting_representing_object_value = False
        self.hidden_values = dict()
        self._is_invisible = False
        self.show_buttons = False

        # determine representing object and type of this editor
        if self.field:

            # list field editor of a thing
            if isinstance(self.owner[self.field], thing_.ListOfThings):
                self.representing_object = self.owner[self.field]
                self.type = EditorTypes.list_of_things

            # non-list field editor of a thing
            else:
                self.representing_object = self.owner
                self.type = EditorTypes.field_of_thing

        # an independent list
        elif isinstance(self.owner, thing_.ListOfThings):
            self.representing_object = self.owner
            self.type = EditorTypes.list_of_things

        # a thing
        else:
            self.representing_object = self.owner
            self.type = EditorTypes.thing

        if field is not None:
            # TODO: reconsider editor version of the field (is it really necessary???)
            self.editor_version_of_the_field = field.create_copy()
            self.class_version_of_the_field = self.owner.get_correspondent_class_field(field)
        else:
            self.editor_version_of_the_field = None
            self.class_version_of_the_field = None

    # ===========================================================================
    def representing_object_editors(self) -> typing.List['Editor']:
        """

        depending on representing object, editors are stored in field_editors property of the owner or in editors
         property of the owner

        :return: List[Editor]
            list of editors created for the representing object
        """
        if self.type == EditorTypes.field_of_thing:
            editors = self.owner.field_editors[self.field]
        else:
            editors = self.representing_object.editors
        return editors

    # ===========================================================================
    def is_invisible(self):
        return self._is_invisible

    # ===========================================================================
    def edit(self):

        # this node is selected
        if self.is_selected(go_deep=False):
            EditorDialog(Editor__Basics.proper_editor(self.owner, self.field), automatic_unregister=True).exec()

        # check for sub editors
        elif self.is_selected(go_deep=True):
            for sub_editor in self.sub_editors.values():
                if sub_editor.is_selected(go_deep=True):
                    sub_editor.edit()
                    break

    # ===========================================================================
    def is_valid(self, prompt: bool = False) -> bool:
        for sub_editor in self.sub_editors.values():
            if not sub_editor.is_valid(prompt):
                return False
        return True

    # ===== this method should be implemented in derived classes
    def set_hidden(self, item, hide: bool):
        pass

    # ===========================================================================
    def redraw_items(self):
        for item in self.sub_editors.keys():
            sub_editor = self.sub_editors[item]
            if sub_editor.is_invisible():
                hide = True
            elif sub_editor.is_marked_for_removal():
                hide = True
            elif sub_editor.field and sub_editor.editor_version_of_the_field.is_hidden():
                hide = True
            else:
                hide = False
            self.set_hidden(item, hide)

            sub_editor.redraw_items()

    # ===========================================================================
    def get_responsible_editor(self):
        return self.owner.get_responsible_editor(self.field)

    # ===========================================================================
    def is_responsible(self):
        return self == self.get_responsible_editor()

    # ===========================================================================
    @staticmethod
    def create_editor_and_open_dialog(owner, field, responsible, parent_editor=None):
        editor = Editor__Basics.proper_editor(owner, field, responsible, parent_editor)
        if editor:
            EditorDialog(editor, automatic_unregister=True).exec()

    # ===========================================================================
    # TODO: add test for this method
    @staticmethod
    def create_responsible_editor(owner, field):

        responsible_editor = Editor__Basics.proper_editor(owner, field, responsible=True, parent_editor=None)

        if responsible_editor:

            # set the value equal to the representing object value (any change should be done via this editor)
            if field:
                value = owner[field]
            else:
                value = owner
            responsible_editor.set_value(EditorValue(value))

            # now dependent on list
            if field:
                class_version_of_the_field = owner.get_correspondent_class_field(field)
                if class_version_of_the_field in owner.dependency_parameters:
                    owner.dependency_parameters[class_version_of_the_field].dependent_on_list.dependent_editors.append(responsible_editor)
                    if owner.dependency_parameters[class_version_of_the_field].dependent_on_list.get_responsible_editor():
                        owner.dependency_parameters[class_version_of_the_field].dependent_on_list.get_responsible_editor().value_changed_by_me_signal.connect(responsible_editor.dependent_on_list_modified)

            # now dependent editors (for thing editors, list of things editors, and list field editors but not simple field editors
            dependent_editors = []
            if field is None:
                dependent_editors = owner.dependent_editors
            elif isinstance(owner[field], thing_.ListOfThings):
                dependent_editors = owner[field].dependent_editors

            # all editors in dependent_editors array are responsible editors
            for dependent_editor in dependent_editors:
                responsible_editor.value_changed_by_me_signal.connect(dependent_editor.dependent_on_list_modified)

            # field change
            responsible_editor.value_changed_by_me_signal.connect(responsible_editor.update_fields_affected_by_me)

            # connect to owner signal
            owner.modified_signal.connect(responsible_editor.representing_object_modified)

        return responsible_editor

    # ===========================================================================
    @staticmethod
    def proper_editor(owner, field, responsible=False, parent_editor=None):

        editor = None

        if field:
            in_editor = field.in_editor

            if in_editor:

                if in_editor.editor_parameters_list is None:
                    editor = in_editor.editor(owner, field, responsible=responsible, parent_editor=parent_editor)
                else:
                    editor = in_editor.editor(owner, field, *in_editor.editor_parameters_list, responsible=responsible, parent_editor=parent_editor)

        elif isinstance(owner, thing_.Thing):
            editor = general_editors_prototypes.ThingEditorPrototype.get_main_type()(owner, responsible=responsible, parent_editor=parent_editor)

        elif isinstance(owner, thing_.ListOfThings):
            editor = general_editors_prototypes.TableOfThingsEditorPrototype.get_main_type()(owner, None, responsible=responsible, parent_editor=parent_editor)

        return editor

    # ===========================================================================
    def __del__(self):

        try:
            self.unregister()

        # for re-disconnecting signals
        except TypeError:
            pass


# ===========================================================================
class Editor__Dependency(Editor__Basics):
    # ===========================================================================
    def __init__(self, owner, field, parent=None):
        super().__init__(owner=owner, field=field, parent=parent)
        self.tracked_items_in_dependent_on_list = []
        # when new items of dependent on list are used in a dependent editor and that editor is accepted, the new items in dependent on list editor should be accepted too.
        self.used_items_from_dependent_on_list = []

    # ===========================================================================
    def dependent_editors(self):
        if self.type == EditorTypes.list_of_things:
            return self.representing_object.dependent_editors
        return []

    # ===========================================================================
    def allowed_dependent_on_list_items(self):
        allowed_items = []

        dependency_parameters = Editor__Dependency.dependency_parameters(self.owner, self.class_version_of_the_field)

        # any editor for the dependent on list?
        if len(dependency_parameters.dependent_on_list.editors) > 0:
            dependent_on_list = thing_.ListOfThings(dependency_parameters.dependent_on_list.type)
            editor_value = dependency_parameters.dependent_on_list.get_responsible_editor().get_value()

            # all items which are not marked for removal
            for item in editor_value.value:
                if item not in editor_value.items_marked_for_removal:
                    dependent_on_list.append(item)
        else:
            dependent_on_list = dependency_parameters.dependent_on_list

        for item in dependent_on_list:

            if item.is_marked_for_removal():
                continue
            if item.editors and item.get_responsible_editor().is_marked_for_removal():
                continue
            if dependency_parameters.forbidden_items_creator and item in dependency_parameters.forbidden_items_creator():
                continue

            allowed_items.append(item)

        return allowed_items

    # ===========================================================================
    def all_dependent_responsible_editors(self):
        dependent_responsible_editors = []

        for thing_class in thing_.Thing.all_thing_classes():
            for thing in thing_class.all():
                if not thing.dependency_parameters:
                    # ignore other instances of this type, because they do not have dependency parameters
                    break
                found = False
                for class_version_of_the_field in thing_class.sorted_fields_of_class(include_primary_key=False):
                    if class_version_of_the_field in thing.dependency_parameters:
                        if thing.dependency_parameters[class_version_of_the_field].dependent_on_list.type == self.representing_object.type:
                            # this type may depend on us
                            found = True
                            if thing.dependency_parameters[class_version_of_the_field].dependent_on_list == self.representing_object:
                                dependent_responsible_editors.append(thing.get_responsible_editor(thing.dependency_parameters[class_version_of_the_field].field_for_retrieving_dependent_on_list_item))
                # do not consider the rest of instances, because none of them will depend on such a list
                if not found:
                    break

        return dependent_responsible_editors

    # ===========================================================================
    def dependent_on_list_modified(self):

        dependency_parameters = Editor__Dependency.dependency_parameters(self.owner, self.class_version_of_the_field)
        if dependency_parameters:

            # remove signal connections for removed items
            for item in self.tracked_items_in_dependent_on_list:
                if item not in self.allowed_dependent_on_list_items():
                    item.modified_signal.disconnect(self.dependent_on_list_modified)
                    if item.get_responsible_editor():
                        item.get_responsible_editor().value_changed_by_me_signal.disconnect(self.dependent_on_list_modified)

                    index = item.dependent_editors.index(self)
                    del item.dependent_editors[index]

                    index = self.tracked_items_in_dependent_on_list.index(item)
                    del self.tracked_items_in_dependent_on_list[index]

            # add signal connections for new items
            for item in self.allowed_dependent_on_list_items():
                if item not in self.tracked_items_in_dependent_on_list:
                    item.dependent_editors.append(self)
                    item.modified_signal.connect(self.dependent_on_list_modified)
                    item.get_responsible_editor().value_changed_by_me_signal.connect(self.dependent_on_list_modified)
                    self.tracked_items_in_dependent_on_list.append(item)

            # finally update widget items
            self.widget.blockSignals(True)
            self.widget.update_items(self.allowed_dependent_on_list_items())
            self.widget.blockSignals(False)

    # ===========================================================================
    def get_dependency_parameters(self):
        return Editor__Dependency.dependency_parameters(self.owner, self.class_version_of_the_field)
    
    # ===========================================================================
    @staticmethod
    def dependency_parameters(owner, field):
        # this is field editor and there exists a dependency parameter in the owner for this field
        if field and field in owner.dependency_parameters:
            return owner.dependency_parameters[field]
        return None


# ===========================================================================
class Editor(Editor__Dependency):
    value_changed_by_me_signal = QtCore.pyqtSignal()
    field_changed_by_me_signal = QtCore.pyqtSignal()

    # ===========================================================================
    def __init__(self, owner, field, responsible=False, parent_editor=None):

        super().__init__(owner=owner, field=field, parent=parent_editor)

        self.last_values_made_by_non_responsible_editors = tools.IndexEnabledDict()

        self.setting_value = False

        self.parent_editor = parent_editor

        self.create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs()

        # TODO: add comment for this command ???
        self.widget.installEventFilter(self)

        dependency_parameters = Editor__Dependency.dependency_parameters(self.owner, self.class_version_of_the_field)
        if dependency_parameters:

            self.widget.blockSignals(True)
            self.widget.update_items(self.allowed_dependent_on_list_items())
            self.widget.blockSignals(False)

        if not responsible:
            self.register()

    # ===========================================================================
    def accept(self):

        # acceptance of sub editors should be done for both responsible and non-responsible editors
        for sub_editor in self.sub_editors.values():
            sub_editor.accept()

        if self.is_responsible():
            if self.is_modified():
                if self.type == EditorTypes.field_of_thing:
                    previous_value = self.owner[self.field]
                    new_value = self.get_value().value
                    self.update_foreign_owners(previous_value, new_value)

                # first accept the list on which we depend (if any)
                dependency_parameters = Editor__Dependency.dependency_parameters(self.owner, self.class_version_of_the_field)
                if dependency_parameters:
                    if dependency_parameters.dependent_on_list.get_responsible_editor():
                        dependency_parameters.dependent_on_list.get_responsible_editor().dependent_editor_accepted(self)

                if self.field:
                    self.field.force_to_match(self.editor_version_of_the_field)
                self.set_value_of_representing_object()

                # if we are an affecting field, all other affecting fields should be accepted too, because they are related
                if self.field and isinstance(self.owner, thing_.MorphingThing):
                    if self.class_version_of_the_field in self.owner.get_affecting_fields():
                        for affecting_field in self.owner.get_affecting_fields():
                            if affecting_field != self.class_version_of_the_field:
                                self.owner.get_responsible_editor(affecting_field).accept()

            self.last_values_made_by_non_responsible_editors.clear()
            for editor in self.representing_object_editors():
                editor.clear_tracking_information_regarding_sub_editors()
        else:
            self.get_responsible_editor().accept()

    # ===========================================================================
    def accept_new_items(self):
        # representing a list
        if self.type == EditorTypes.list_of_things:
            for sub_editor in list(self.sub_editors.values()):
                if sub_editor.is_new():
                    type(sub_editor.representing_object).all().append(sub_editor.representing_object)
                    with self.representing_object.lock:
                        self.setting_representing_object_value = True
                        self.representing_object.append(sub_editor.representing_object)
                        self.setting_representing_object_value = False

    # ===========================================================================
    def accept_removed_items(self):
        # representing a list
        if self.type == EditorTypes.list_of_things:
            for item in list(self.sub_editors.keys()):
                sub_editor = self.sub_editors[item]
                if sub_editor.is_marked_for_removal():
                    sub_editor.representing_object.mark_for_removal()
                    if sub_editor.representing_object in self.representing_object:
                        index = self.representing_object.index(sub_editor.representing_object)
                        with self.representing_object.lock:
                            self.setting_representing_object_value = True
                            del self.representing_object[index]
                            self.setting_representing_object_value = False
                    self.remove_sub_editor(item)

    # ===========================================================================
    def create_widget_and_tie_signals__create_sub_editors_and_sub_dialogs(self):
        raise NotImplementedError

    # ===========================================================================
    def dependent_editor_accepted(self, dependent_editor):
        # when some dependent editor accept its values, if any of the accepted values are among new items here, this editor should accept its new items.
        if self.type == EditorTypes.list_of_things:
            for item in dependent_editor.used_items_from_dependent_on_list:

                # any new item used in the dependent editor?
                if self.sub_editors[item].is_new():

                    # add all new items to the array
                    self.accept_new_items()

                    # no need for further check
                    break

    # ===========================================================================
    def find_the_last_value_before_the_rejecter_value(self, rejecter):
        # for emiting signal when changes are made
        value_changed_by_me = False

        # do we have any history for this rejecter?
        if rejecter in self.last_values_made_by_non_responsible_editors.keys():

            # is rejecter the last editor?
            if rejecter == self.last_values_made_by_non_responsible_editors.keys()[-1]:

                # any other editor?
                if len(self.last_values_made_by_non_responsible_editors.keys()) > 1:

                    # go for the previous last editor
                    self.set_value(self.last_values_made_by_non_responsible_editors.keys()[-2].get_value())

                # no other editor?
                else:
                    # go for representing object value
                    self.reset_to_representing_object_value(self.field)

                value_changed_by_me = True

            # check removed and new items made by the rejecter editor
            if self.type == EditorTypes.list_of_things:
                # remove new sub editors created by the rejecter
                for key in rejecter.keys_for_immediate_sub_editors_created_by_me:
                    if key in self.sub_editors.keys():
                        self.remove_sub_editor(key)
                        value_changed_by_me = True

                # revive all immediate sub editor removed by the rejecter
                for sub_editor in rejecter.sub_editors_marked_for_removal:
                    if sub_editor.owner in self.sub_editors:
                        if self.sub_editors[sub_editor.owner].set_marked_for_removal(mark_for_removal=False):
                            value_changed_by_me = True

                # no more need for the tracking information
                rejecter.clear_tracking_information_regarding_sub_editors()

            # no more need for the tracking information
            del self.last_values_made_by_non_responsible_editors[rejecter]

        # emit signal in case of any change
        if value_changed_by_me:
            self.value_changed_by_me_signal.emit()

    # ===========================================================================
    def get_value(self):

        # representing list of things
        if self.type == EditorTypes.list_of_things:
            value = thing_.ListOfThings(self.representing_object.type)
            new_items = []
            items_marked_for_removal = []

            for sub_editor in self.sub_editors.values():
                value.append(sub_editor.owner)
                if sub_editor.is_new():
                    new_items.append(sub_editor.owner)
                if sub_editor.is_marked_for_removal():
                    items_marked_for_removal.append(sub_editor.owner)

        # representing a thing
        elif self.type == EditorTypes.thing:

            # create a new thing
            value = type(self.owner)()

            # set correct in class type for instance specific fields
            # for field in type(value).sorted_fields_of_class(include_primary_key=True):
            #     if field.is_instance_specific():
            #         value.instance_specific_fields[field].force_to_match(self.owner.instance_specific_fields[field])

            # now set the values for fields
            for field in self.owner.get_sorted_fields_of_instance(include_primary_key=True):
                if not isinstance(field, general_fields.ListField):
                    # if field.is_instance_specific():
                    #     class_field = self.owner.get_correspondent_class_field(field)
                    #     value_field = value.get_correspondent_instance_field(class_field)
                    #     value_field.force_to_match(self.sub_editors[field].editor_version_of_the_field)
                    # else:
                    value_field = field
                    # get value should return a complete value for the thing
                    if field in self.sub_editors.keys():
                        value[value_field] = self.sub_editors[field].get_value().value
                    else:
                        value[value_field] = self.hidden_values[self.owner.get_correspondent_class_field(field)]
            new_items = []
            items_marked_for_removal = []

        # representing field of a thing
        else:
            value = self.widget.get_value()
            new_items = []
            items_marked_for_removal = []

        return EditorValue(value, new_items, items_marked_for_removal)

    # ===========================================================================
    def is_modified(self) -> bool:

        if self.type == EditorTypes.field_of_thing and self.get_value().value != self.owner[self.field]:
            return True

        if self.type == EditorTypes.thing:
            for field in self.hidden_values.keys():
                if self.hidden_values[field] != self.owner[field]:
                    return True

        for sub_editor in self.sub_editors.values():
            if sub_editor.owner in self.keys_for_immediate_sub_editors_created_by_me:
                return True
            if self.is_responsible():
                for editor in self.owner.editors:
                    if sub_editor.owner in editor.keys_for_immediate_sub_editors_created_by_me:
                        return True
            if sub_editor in self.sub_editors_marked_for_removal:
                return True
            if self.is_responsible():
                for editor in self.owner.editors:
                    if sub_editor in editor.sub_editors_marked_for_removal:
                        return True
            if sub_editor.is_modified():
                return True

        return False

    # ===========================================================================
    def non_responsible_editor_modified_the_value(self):

        # only non-responsible editor should respond to this alert
        if self.is_responsible():

            new_value = self.sender().get_value()

            # remove the previous saved value
            if self.sender() in self.last_values_made_by_non_responsible_editors.keys():
                del self.last_values_made_by_non_responsible_editors[self.sender()]

            # save the new value at the end of the array
            self.last_values_made_by_non_responsible_editors.insert(len(self.last_values_made_by_non_responsible_editors), self.sender(), new_value)

            # set value of responsible editor
            self.set_value(new_value)
            self.value_changed_by_me_signal.emit()

    # ===========================================================================
    def register(self):

        representing_object_editors = self.representing_object_editors()

        # already not in the editors list?
        if self not in representing_object_editors:

            # append the editor to the editors list
            representing_object_editors.append(self)

            self.set_value(self.owner.get_responsible_editor(self.field).get_value())
            self.value_changed_by_me_signal.connect(self.get_responsible_editor().non_responsible_editor_modified_the_value)
            self.get_responsible_editor().value_changed_by_me_signal.connect(self.responsible_editor_modified_the_value)
            self.get_responsible_editor().field_changed_by_me_signal.connect(self.responsible_editor_modified_the_field)

    # ===========================================================================
    def reject(self, rejecter=None):

        # rejection of sub editors should be done for both responsible and non-responsible editors
        for item in list(self.sub_editors.keys()):
            self.sub_editors[item].reject()

        if self.is_responsible():

            # for emiting signal when changes are made
            value_changed_by_me = False

            # do we have any history for this rejecter?
            if rejecter in self.last_values_made_by_non_responsible_editors.keys():

                # is rejecter the last editor?
                if rejecter == self.last_values_made_by_non_responsible_editors.keys()[-1]:

                    # any other editor?
                    if len(self.last_values_made_by_non_responsible_editors.keys()) > 1:

                        # go for the previous last editor
                        self.set_value(self.last_values_made_by_non_responsible_editors.keys()[-2].get_value())

                    # no other editor?
                    else:
                        # go for representing object value
                        self.reset_to_representing_object_value(self.field)

                    value_changed_by_me = True

                # check removed and new items made by the rejecter editor
                if self.type == EditorTypes.list_of_things:
                    # remove new sub editors created by the rejecter
                    for key in rejecter.keys_for_immediate_sub_editors_created_by_me:
                        if key in self.sub_editors.keys():
                            self.remove_sub_editor(key)
                            value_changed_by_me = True

                    # revive all immediate sub editor removed by the rejecter
                    for sub_editor in rejecter.sub_editors_marked_for_removal:
                        if sub_editor.owner in self.sub_editors:
                            if self.sub_edtiors[sub_editor.owner].set_marked_for_removal(mark_for_removal=False):
                                value_changed_by_me = True

                    # no more need for the tracking information
                    rejecter.clear_tracking_information_regarding_sub_editors()

                # no more need for the tracking information
                del self.last_values_made_by_non_responsible_editors[rejecter]

            # emit signal in case of any change
            if value_changed_by_me:
                self.value_changed_by_me_signal.emit()

        else:
            self.get_responsible_editor().reject(self)

    # ===========================================================================
    def representing_object_modified(self, field=None):
        if self.is_responsible() and not self.setting_representing_object_value:
            if field == self.field:
                if field and not self.editor_version_of_the_field.matches(field):
                    self.reset_to_representing_object_field(field)
                    self.field_changed_by_me_signal.emit()
            self.reset_to_representing_object_value(field)
            self.value_changed_by_me_signal.emit()

    # ===========================================================================
    def reset_to_representing_object_field(self, field):

        # representing a field in a thing
        if field == self.field:
            self.editor_version_of_the_field.force_to_match(self.field)

    # ===========================================================================
    def reset_to_representing_object_value(self, field):
        # representing a list
        if self.type == EditorTypes.list_of_things:

            # existing items
            for item in self.representing_object:
                if not item.is_marked_for_removal():
                    if item not in list(self.sub_editors.keys()):
                        self.insert_sub_editor_or_sub_dialog(len(self.sub_editors), item)

            # removed items
            for item in list(self.sub_editors.keys()):
                if item in self.representing_object:
                    if item.is_marked_for_removal():
                        self.remove_sub_editor(item)
                elif not self.sub_editors[item].is_new():
                    self.remove_sub_editor(item)

        # representing a thing
        elif self.type == EditorTypes.thing:
            self.set_value(EditorValue(self.representing_object))

        # representing a field in a thing
        elif field == self.field:
            self.set_value(EditorValue(self.owner[self.field]))

    # ===========================================================================
    def responsible_editor_modified_the_field(self):

        # only responsible editor should do this
        if not self.is_responsible():
            self.editor_version_of_the_field.force_to_match(self.get_responsible_editor().editor_version_of_the_field)

    # ===========================================================================
    def responsible_editor_modified_the_value(self):

        # only responsible editor should do this
        if not self.is_responsible():
            self.set_value(self.get_responsible_editor().get_value())

    # ===========================================================================
    def set_value(self, editor_value):
        self.setting_value = True

        # representing a list
        if self.type == EditorTypes.list_of_things:

            # remove sub editors for removed items
            for item in list(self.sub_editors.keys()):
                if item not in editor_value.value:
                    self.remove_sub_editor(item)

            # add new editors
            for i, item in enumerate(editor_value.value):

                # check existence
                if item in self.sub_editors.keys():
                    # check for correct index
                    index = self.sub_editors.keys().index(item)
                    # remove in case of wrong index
                    if index != i:
                        self.sub_editors.reorder(item, i)

                # add if not exists
                if item not in self.sub_editors.keys():
                    self.insert_sub_editor_or_sub_dialog(i, item)

                self.sub_editors[item].set_is_new(item in editor_value.new_items if editor_value.new_items else False)
                self.sub_editors[item].set_marked_for_removal(item in editor_value.items_marked_for_removal if editor_value.items_marked_for_removal else False)

            self.redraw_items()

        # representing a thing
        elif self.type == EditorTypes.thing:
            for field in self.representing_object.get_sorted_fields_of_instance(include_primary_key=True):
                if not isinstance(field, general_fields.ListField):
                    if field not in self.sub_editors.keys():
                        self.hidden_values[self.representing_object.get_correspondent_class_field(field)] = editor_value.value[field]

        # sometimes widget set value should be called even for non field editors (tree nodes for example)
        if self.type == EditorTypes.list_of_things and editor_value.items_marked_for_removal:
            value_for_widget = thing_.ListOfThings(editor_value.value.type)
            for item in editor_value.value:
                if item not in editor_value.items_marked_for_removal:
                    value_for_widget.append(item)
        else:
            value_for_widget = editor_value.value

        self.widget.blockSignals(True)
        self.widget.set_value(value_for_widget)
        self.widget.blockSignals(False)

        self.setting_value = False

    # ===========================================================================
    def set_value_of_representing_object(self):

        # representing a list
        if self.type == EditorTypes.list_of_things:
            self.accept_removed_items()
            self.accept_new_items()

        # representing a thing
        elif self.type == EditorTypes.thing:
            for field in self.owner.get_get_sorted_fields_of_instance(include_primary_key=True):
                if not isinstance(field, general_fields.ListField):
                    if field not in self.sub_editors.keys():
                        self.owner[field] = self.hidden_values[self.owner.get_correspondent_class_field(field)]

        # representing field of a thing
        else:
            with self.owner.lock:
                self.setting_representing_object_value = True
                if not self.editor_version_of_the_field.matches(self.field):
                    self.field.force_to_match(self.editor_version_of_the_field)
                self.owner[self.field] = self.get_value().value
                self.setting_representing_object_value = False

    # ===========================================================================
    def unregister(self):

        representing_object_editors = self.representing_object_editors()

        if self in representing_object_editors:
            for representing_object_editor in representing_object_editors:
                if representing_object_editor == self:
                    continue
            self.value_changed_by_me_signal.disconnect(self.get_responsible_editor().non_responsible_editor_modified_the_value)
            self.get_responsible_editor().value_changed_by_me_signal.disconnect(self.responsible_editor_modified_the_value)
            self.get_responsible_editor().field_changed_by_me_signal.disconnect(self.responsible_editor_modified_the_field)
            index = representing_object_editors.index(self)
            del representing_object_editors[index]

        # sub editors
        for sub_editor in self.sub_editors.values():
            sub_editor.unregister()

    # ===========================================================================
    def update_fields_affected_by_me(self):
        if self.type == EditorTypes.field_of_thing:
            if self.is_responsible() and isinstance(self.owner, thing_.MorphingThing):
                affecting_fields = self.owner.get_affecting_fields()
                if self.field in affecting_fields and isinstance(self.owner, thing_.MorphingThing):
                    self.owner.update_affected_fields(affecting_field=self.field, is_in_the_thing=False)

    # ===========================================================================
    def update_my_editor_version_of_the_field(self, field_to_match_with):
        self.editor_version_of_the_field.force_to_match(field_to_match_with)
        if self.is_responsible():
            self.field_changed_by_me_signal.emit()


# ===========================================================================
class EditorDialog(widget_basics.DialogWithOkCancel):
    """
    Creates a dialog for the specified editor. The title of the window will be the name of the owner of the specified
    editor. If the specified editor has parent, the name of the parent will be added to the beginning of the title.
    If the parent of the specified editor also has parent, the name of the great parent will be added to the beginning
    of the title too. And so on ... .
    When the specified editor is actually a list of things editor, four buttons are needed which will be shown at the
    top of the dialog:

    edit button: If a thing is the list is selected, this button will be enabled to let the user press it. A new dialog
        will be shown for editing the selected item.
    new button: When this button is pressed, a new thing will be added to the list. It should be noted however that if
        an element is selected in the dialog, and that element is list of things itself, a new thing will be added to
        that list of things instead of the main list of things for which this dialog has been shown. (a bit ambiguous
        maybe!)
    del button: For removing the selected item from the list.
    revive button: For reviving the latest removed item.

    It may be useful to remind that sub-editors of list of things editors are thing editors and sub-editors of thing
     editors are field editors.
    """

    # ===========================================================================
    @staticmethod
    def create_full_name_for_editor_title(editor):

        # first name of the main editor
        main_editor = editor
        # TODO work on this part when the owner is only ListOfThings. it has no name!!!
        name = ''
        if hasattr(main_editor.owner, 'name'):
            name = main_editor.owner.name

        # then name of all parents of the editor
        while editor.parent_editor:
            editor = editor.parent_editor
            if hasattr(editor.owner, 'name'):
                name = '{}-{}'.format(editor.owner.name, name)

        # if we are working on a field editor add the field name too
        if main_editor.field:
            return '{}: {}'.format(name, main_editor.field.get_ui_title()[basic_types.Language.get_active_language()])
        else:
            return name

    # ===========================================================================
    def __init__(self, editor: Editor, automatic_unregister, parent=None):
        """

        :param editor: The editor for which dialog will be created
        :param automatic_unregister: Should the editor be automatically unregistered when the dialog is closed?
        :param parent: Parent of the dialog
        """

        super().__init__(parent=parent)

        self.editor = editor
        self.automatic_unregister = automatic_unregister

        # certainly unregister will be done when the dialog will be closed (if automatic_unregister is enabled)
        self.unregister_done = False

        # editors for 'things' and 'fields' do not need these buttons
        # also some list of things editors may not need these buttons
        # that's why show_button is set to False by default and should be enabled for list of things editors which want
        #  these buttons to be shown
        if self.editor.show_buttons:

            # edit button should launch edit method of the editor when clicked. this method will automatically find the
            #  selected sub-editor and will launch the proper dialog for editing the selected 'thing'
            self.edit_button = widget_basics.Button(general_ui_titles.edit, self.editor.edit)

            # edit button should be disabled by default and enabled only when some 'thing' in the list is selected
            self.edit_button.setEnabled(False)

            # enable edit button whenever a sub editor is selected
            self.editor.sub_editor_selected_signal.connect(lambda: self.edit_button.setEnabled(True))

            # disable edit button when no sub editor is selected
            self.editor.no_sub_editor_selected_signal.connect(lambda: self.edit_button.setEnabled(False))

            new_button = widget_basics.Button(general_ui_titles.new, lambda: self.editor.append_new_item(is_top_editor=True))
            del_button = widget_basics.Button(general_ui_titles.delete, lambda: self.editor.mark_selected_sub_editor_for_removal(is_top_editor=True))

            self.revive_button = widget_basics.Button(general_ui_titles.revive, self.editor.revive_the_latest_sub_editor_marked_for_removal)

            # revive button is disabled by default and will be enabled only if some 'thing' is deleted
            self.revive_button.setEnabled(False)

            # revive button should be disable when no removed 'thing' is available for reviving
            self.editor.no_sub_editor_marked_for_removal_exists_signal.connect(lambda: self.revive_button.setEnabled(False))
            # revive button should be enabled when some removed 'thing' is available for reviving
            self.editor.sub_editor_marked_for_removal_exists_signal.connect(lambda: self.revive_button.setEnabled(True))

            # these four buttons should be added to the header layout of the dialog
            self.header_layout.add_widgets(
                self.edit_button, new_button, widget_basics.Dialog.stretch, del_button, self.revive_button)

        # now time to add the main widget of the dialog which is the editor widget
        self.add_widget(self.editor.widget)

        # time to create the name which should be displayed as the title of the dialog
        self.setWindowTitle(EditorDialog.create_full_name_for_editor_title(self.editor))

    # ===========================================================================
    def accept(self):
        self.editor.accept()
        QtWidgets.QDialog.accept(self)
        if self.automatic_unregister:
            self.editor.unregister()
            self.unregister_done = True

    # ===========================================================================
    def reject(self):
        if self.editor.is_modified():
            save = widget_basics.YesNoCancelMessageBox('save changes?').show()
            if save == widget_basics.YesNoCancelMessageBox.Yes:
                self.accept()
            elif save == widget_basics.YesNoCancelMessageBox.No:
                self.editor.reject()
                QtWidgets.QDialog.reject(self)
        else:
            QtWidgets.QDialog.reject(self)

        if self.automatic_unregister:
            self.editor.unregister()
            self.unregister_done = True

    # ===========================================================================
    def __del__(self):
        if self.automatic_unregister and not self.unregister_done:
            self.editor.unregister()

