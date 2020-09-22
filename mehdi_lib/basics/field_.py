# -*- coding: utf-8 -*-
"""Basic definitions of field

The most basic entity in this infrastructure is Field. Every 'Thing' has several fields.
Every field can automatically represent itself in class, database and in ui.
"""

import typing

from mehdi_lib.tools import tools
from mehdi_lib.basics import database_tools, basic_types, prototype_

from PyQt5 import QtCore


# ===========================================================================
class InClass:
    """Enables fields to express themselves in classes

    When 'Things' are fetched from database, each field should know its type in class in order to be able to convert
    the fetched value to correct format
    """

    # ===========================================================================
    def __init__(self, name: str, type_: type, initial_value):
        """

        :param name: name of this field in the class
        :param type_: type of this field.
        :param initial_value: for the first time when the class is created
        """
        # just for preventing common errors!
        if name.__contains__(' '):
            tools.Tools.fatal_error('in class name cannot have space: {}'.format(name))
        self.name = name  # type: str
        self._type = type_  # type: type
        self._initial_value = initial_value

    # ===========================================================================
    @property
    def initial_value(self):
        """
        for list fields, initial value actually stores element type of the list. (because the type_ field should be
        list field).
        :return:
        """
        # for list fields in which initial value is in fact element type
        if isinstance(self._initial_value, type):
            # get the main type if we have passed prototype
            if issubclass(self._initial_value, prototype_.Prototype):
                self._initial_value = self._initial_value.get_main_type()
        return self._initial_value

    # ===========================================================================
    @initial_value.setter
    def initial_value(self, value):
        self._initial_value = value

    # ===========================================================================
    @property
    def type(self) -> type:
        if self._type is None:
            return None
        if issubclass(self._type, prototype_.Prototype):
            self._type = self._type.get_main_type()
        return self._type

    # ===========================================================================
    def create_copy(self):
        return InClass(self.name, self.type, self.initial_value)

    # ===========================================================================
    def force_to_match(self, other_in_class):
        self.name = other_in_class.name
        self._type = other_in_class.type
        self.initial_value = other_in_class.initial_value

    # ===========================================================================
    def matches(self, other_in_class):
        return self.name == other_in_class.name and \
               self.type == other_in_class.type and \
               self.initial_value == other_in_class.initial_value

    # ===========================================================================
    def set_type(self, new_type):
        self._type = new_type


# ===========================================================================
class InDatabase:
    """Enables fields to express themselves in database

    For automatically creating tables, each field should be able to express its correct format in database.
    """
    # ===========================================================================
    def __init__(self, title: str, type_: str, default_value, condition: typing.Optional[str]):
        self.title = title  # type: str
        if self.title.upper() in database_tools.Database.reserved_words:
            self.title += '_'
        self.type = type_  # type: str
        self.default_value = default_value
        self.condition = condition  # type: typing.Optional[str]

    # ===========================================================================
    def create_copy(self):
        return InDatabase(self.title, self.type, self.default_value, self.condition)

    # ===========================================================================
    def get_creation_command(self) -> str:
        command = '{} {}'.format(self.title, self.type)
        if self.condition:
            command += ' {}'.format(self.condition)
        if self.default_value:
            command += ' DEFAULT {}'.format(self.default_value)
        return command

    # ===========================================================================
    def matches(self, other_in_database):
        return self.title == other_in_database.title and \
               self.type == other_in_database.type and \
               self.default_value == other_in_database.default_value and \
               self.condition == other_in_database.condition


# ===========================================================================
class InEditor:
    """Enables fields to express themselves in ui

    for automatically creating ui, each field should know its default ui editor and the required parameters for that.
    """
    # ===========================================================================
    def __init__(self, editor: typing.Type['editor_basics.Editor'], editor_parameters_list=None):
        self._editor = editor
        self.editor_parameters_list = editor_parameters_list

    # ===========================================================================
    @property
    def editor(self):
        if isinstance(self._editor, type):
            if issubclass(self._editor, prototype_.Prototype):
                self._editor = self._editor.get_main_type()
        return self._editor

    # ===========================================================================
    @editor.setter
    def editor(self, value):
        self._editor = value

    # ===========================================================================
    def create_copy(self):
        return InEditor(self.editor, self.editor_parameters_list)

    # ===========================================================================
    def force_to_match(self, other_in_editor):
        self.editor = other_in_editor.editor
        self.editor_parameters_list = other_in_editor.editor_parameters_list

    # ===========================================================================
    def matches(self, other_in_editor):
        if self.editor != other_in_editor.editor:
            return False

        if self.editor_parameters_list is not None:

            if other_in_editor.editor_parameters_list is None:
                return False
            if len(self.editor_parameters_list) != len(other_in_editor.editor_parameters_list):
                return False

            for i, parameter in enumerate(self.editor_parameters_list):
                if self.editor_parameters_list[i] != other_in_editor.editor_parameters_list[i]:
                    return False

        return True


# ===========================================================================
class Field(basic_types.UiTitlesContainer, QtCore.QObject):
    """The most basic entity in our framework.

    each field should be able to express itself in class, database and ui.
    Field inherits from QObject for using signals.
    Field inherits from UiTitlesContainer for using ui title specially for morphing things.
    """

    ui_titles_changed_signal = QtCore.pyqtSignal('PyQt_PyObject')
    hiding_status_changed_signal = QtCore.pyqtSignal('PyQt_PyObject')

    # ===========================================================================
    def __init__(self, order: int, ui_titles: dict,
                 in_class: typing.Optional[InClass],
                 in_database: typing.Optional[InDatabase],
                 in_editor: typing.Optional[InEditor]):
        self._base_params = []

        basic_types.UiTitlesContainer.__init__(self)
        QtCore.QObject.__init__(self)
        self._ui_titles = ui_titles  # type: dict
        self.order = order  # type: int
        self.in_class = in_class  # type: typing.Optional[InClass]
        self.in_database = in_database  # type: typing.Optional[InDatabase]
        self.in_editor = in_editor  # type: typing.Optional[InEditor]
        self._is_instance_specific = False
        self._is_hidden = False

    # ===========================================================================
    def create_copy(self):
        parameters = self.get_copy_parameters()

        if parameters is None:
            copy_field = type(self)()
        else:
            copy_field = type(self)(*parameters)

        copy_field.set_instance_specific(self._is_instance_specific)
        copy_field.set_hidden(self._is_hidden)
        copy_field.set_instance_ui_titles(self.get_instance_ui_titles())

        return copy_field

    # ===========================================================================
    def force_to_match(self, other_field):
        if (self.in_database is None and other_field.in_database is not None) or \
            (self.in_database is not None and other_field.in_database is None) or \
                (self.in_database is not None and other_field.in_database is not None and not self.in_database.matches(other_field.in_database)):
            tools.Tools.fatal_error('cannot force in databases to match')
        self.in_class.force_to_match(other_field.in_class)
        self.in_editor.force_to_match(other_field.in_editor)
        self.set_instance_specific(other_field.is_instance_specific())
        self.set_hidden(other_field.is_hidden())
        self.set_instance_ui_titles(other_field.get_instance_ui_titles())

    # ===========================================================================
    def get_copy_parameters(self):

        # for field class
        if type(self) == Field:
            return [
                self.order,
                self.get_instance_ui_titles(),
                self.in_class.create_copy(),
                self.in_database.create_copy(),
                self.in_editor.create_copy()
            ]

        # for children classes with no parameters
        else:
            return []

    # ===========================================================================
    def get_instance_ui_titles(self):
        return self._ui_titles

    # ===========================================================================
    def get_instance_ui_title(self, language):
        """
        for retrieving ui title in a specific language
        :param language:
        :return:
        """
        return self._ui_titles[language]

    # ===========================================================================
    @classmethod
    def get_ui_titles(cls):
        return cls._ui_titles

    # ===========================================================================
    def has_same_ui_titles(self, other_field_or_other_ui_titles):

        if isinstance(other_field_or_other_ui_titles, Field):
            other_ui_titles = other_field_or_other_ui_titles.get_instance_ui_titles()
        else:
            other_ui_titles = other_field_or_other_ui_titles

        for language in self._ui_titles.keys():
            if language not in other_ui_titles:
                return False
            if self._ui_titles[language] != other_ui_titles[language]:
                return False

        return True

    # ===========================================================================
    def is_hidden(self):
        return self._is_hidden

    # ===========================================================================
    def is_instance_specific(self):
        return self._is_instance_specific

    # ===========================================================================
    def matches(self, other_field):
        return self.order == other_field.order and \
               self.has_same_ui_titles(other_field) and \
               self.in_class.matches(other_field.in_class) and \
               self.in_editor.matches(other_field.in_editor) and \
               self.in_database.matches(other_field.in_database) and \
               self.is_instance_specific() == other_field.is_instance_specific() and \
               self.is_hidden() == other_field.is_hidden()

    # ===========================================================================
    def set_hidden(self, hidden):
        if self._is_hidden != hidden:
            self._is_hidden = hidden
            self.hiding_status_changed_signal.emit(self)

    # ===========================================================================
    def set_instance_specific(self, instance_specific):
        self._is_instance_specific = instance_specific

    # ===========================================================================
    def set_instance_ui_titles(self, new_titles):
        if not self.has_same_ui_titles(new_titles):
            self._ui_titles = new_titles
            self.ui_titles_changed_signal.emit(self)


