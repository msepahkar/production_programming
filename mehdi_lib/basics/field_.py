# -*- coding: utf-8 -*-
"""Basic definitions of field

The most basic entity in this infrastructure is 'Field'. Every 'Thing' has several Fields.
Every Field can automatically represent itself in class, database and in ui.
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
    def __init__(self, name: str, type_: type, initial_value: object):
        """

        :param name: str
            name of this field in the class
        :param type_: type
            type of this field.
        :param initial_value: object
            for the first time when the class is created
        """

        # just for preventing common errors!
        if name.__contains__(' '):
            tools.Tools.fatal_error('in class name cannot have space: {}'.format(name))
        self.name = name
        self._type = type_
        self._initial_value = initial_value

    # ===========================================================================
    @property
    def initial_value(self) -> object:
        """
        for list fields, initial value actually stores element type of the list. (because the type_ field should be
        list field).
        :return: object
        """

        # for list fields in which initial value is in fact element type
        if isinstance(self._initial_value, type):
            # get the main type if we have passed prototype
            if issubclass(self._initial_value, prototype_.Prototype):
                self._initial_value = self._initial_value.get_main_type()
        return self._initial_value

    # ===========================================================================
    @initial_value.setter
    def initial_value(self, value: object):
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
    def create_copy(self) -> 'InClass':
        """ Creates a new copy of this object with values equal to the values of this object.

        required for morphing thing
        :return:
        """

        return InClass(self.name, self.type, self.initial_value)

    # ===========================================================================
    def force_to_match(self, other_in_class: 'InClass'):
        """Makes values of this object equal to the values of the other object.

         required for morphing thing
        :param other_in_class: InClass
            the object whose values should be copied here.
        :return:
        """

        self.name = other_in_class.name
        self._type = other_in_class.type
        self.initial_value = other_in_class.initial_value

    # ===========================================================================
    def matches(self, other_in_class: 'InClass') -> bool:
        """checks if the values of this object is equal to the values of the object passed to it.

        required for morphing thing
        :param other_in_class:
        :return:
        """

        return self.name == other_in_class.name and \
               self.type == other_in_class.type and \
               self.initial_value == other_in_class.initial_value

    # ===========================================================================
    def set_type(self, new_type: type):
        self._type = new_type


# ===========================================================================
class InDatabase:
    """Enables fields to express themselves in database.

    For automatically creating tables, each field should be able to express its correct format in database.
    It should be noted that unlike InClass and InEditor, this class will not have any method called force_to_match
    because database tables could not be changed so easily!
    """

    # ===========================================================================
    def __init__(self, title: str, type_: str, default_value: object, condition: typing.Optional[str]):
        self.title = title  # type: str
        if self.title.upper() in database_tools.Database.reserved_words:
            self.title += '_'
        self.type = type_
        self.default_value = default_value
        self.condition = condition

    # ===========================================================================
    def create_copy(self) -> 'InDatabase':
        """creates a copy of this object with values exactly equal to the values of the current object.

         required for morphing thing
       :return: InDatabase
        """

        return InDatabase(self.title, self.type, self.default_value, self.condition)

    # ===========================================================================
    def get_creation_command(self) -> str:
        """Prepares the command required to create this field in the database.

        All these commands for all fields of one table will be combined to create a single command for creating the
        table.

        :return: str
        """

        command = '{} {}'.format(self.title, self.type)
        if self.condition:
            command += ' {}'.format(self.condition)
        if self.default_value:
            command += ' DEFAULT {}'.format(self.default_value)
        return command

    # ===========================================================================
    def matches(self, other_in_database: 'InDatabase') -> bool:
        """checks if the values of this object is equal to the values of the object passed as parameter.

         required for morphing thing

        :param other_in_database: InDatabase

        :return: bool
        """
        return self.title == other_in_database.title and \
               self.type == other_in_database.type and \
               self.default_value == other_in_database.default_value and \
               self.condition == other_in_database.condition


# ===========================================================================
class InEditor:
    """Enables fields to express themselves in UI.

    for automatically creating ui, each field should know its default ui editor and the required parameters for that.
    """

    # ===========================================================================
    def __init__(self, editor: typing.Type['editor_.Editor'], editor_parameters_list: list = None):
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
    def editor(self, value: typing.Type['editor_.Editor']):
        self._editor = value

    # ===========================================================================
    def create_copy(self) -> 'InEditor':
        """creates a copy of this object with values equal to the values of this object.

         required for morphing thing

       :return: InEditor
        """

        return InEditor(self.editor, self.editor_parameters_list)

    # ===========================================================================
    def force_to_match(self, other_in_editor: 'InEditor'):
        """Makes values of this object equal to the values of the object passes as the parameter.

         required for morphing thing

        :param other_in_editor: InEditor

        :return:
        """

        self.editor = other_in_editor.editor
        self.editor_parameters_list = other_in_editor.editor_parameters_list

    # ===========================================================================
    def matches(self, other_in_editor: 'InEditor') -> bool:
        """checks if the values of this object are equal to the values of the object passes as the parameter.

         required for morphing thing

        :param other_in_editor: InEditor

        :return: bool
        """

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
class Field(QtCore.QObject):
    """The most basic entity in our framework.

    each field should be able to express itself in class, database and ui.
    Field inherits from QObject for using signals.
    Field inherits from UiTitlesContainer for using ui title.
    """

    # for morphing things
    ui_titles_changed_signal = QtCore.pyqtSignal('PyQt_PyObject')
    # for morphing things
    hiding_status_changed_signal = QtCore.pyqtSignal('PyQt_PyObject')

    # ===========================================================================
    def __init__(self, order: int, ui_title: dict,
                 in_class: typing.Optional[InClass],
                 in_database: typing.Optional[InDatabase],
                 in_editor: typing.Optional[InEditor]):
        """

        :param order: int
            the order of this field in the UI
        :param ui_title: dict
            ui titles in different languages
        :param in_class: Optional[InClass]
        :param in_database: Optional[InDatabase]
        :param in_editor: Optional[InEditor]
        """
        self._base_params = []

        QtCore.QObject.__init__(self)
        self._ui_title = ui_title
        self.order = order
        self.in_class = in_class
        self.in_database = in_database
        self.in_editor = in_editor

        # for morphing things
        self._is_instance_specific = False

        # for morphing things
        self._is_hidden = False

    # ===========================================================================
    def create_copy(self) -> 'Field':
        """
        Creates a new object. The new object will force in_editor, in_class, and in_database to create copies of
        themselves.

         required for morphing thing

        :return: Field
        """

        parameters = self.get_copy_parameters()

        if parameters is None:
            copy_field = type(self)()
        else:
            copy_field = type(self)(*parameters)

        copy_field.set_instance_specific(self._is_instance_specific)
        copy_field.set_hidden(self._is_hidden)
        copy_field.set_instance_ui_title(self.get_ui_title())

        return copy_field

    # ===========================================================================
    def force_to_match(self, other_field: 'Field'):
        """Makes values of this object equal to the values of the object passes as parameter.

        required for morphing thing

        :param other_field: Field

        :return:
        """

        if (self.in_database is None and other_field.in_database is not None) or \
                (self.in_database is not None and other_field.in_database is None) or \
                (self.in_database is not None and other_field.in_database is not None and not self.in_database.matches(
                    other_field.in_database)):
            tools.Tools.fatal_error('cannot force in_database to match')
        self.in_class.force_to_match(other_field.in_class)
        self.in_editor.force_to_match(other_field.in_editor)
        self.set_instance_specific(other_field.is_instance_specific())
        self.set_hidden(other_field.is_hidden())
        self.set_instance_ui_title(other_field.get_ui_title())

    # ===========================================================================
    def get_copy_parameters(self) -> list:
        """Each inherited class will implement this method if the parameters required to be copied are different.

        These parameters are in fact parameters required in __init__
         required for morphing thing
       :return: list
        """

        # for field class itself (not inherited classes). Actually this is only for guide and ofcourse for test; because
        # Field class will itself will never be used; only its child classes will be used.
        if type(self) == Field:
            return [
                self.order,
                self.get_ui_title(),
                self.in_class.create_copy(),
                self.in_database.create_copy(),
                self.in_editor.create_copy()
            ]

        # For inherited classes. (They should implement this class themselves if they require any parameters)
        else:
            return []

    # ===========================================================================
    def get_ui_title(self) -> typing.Dict[basic_types.Language.AvailableLanguage, str]:
        """instance ui titles are useful only in morphing things.

         required for morphing thing

        :return: dict
        """
        return self._ui_title

    # ===========================================================================
    def has_same_ui_titles(self, other_field_or_other_ui_title: ['Field', typing.Dict[basic_types.Language.AvailableLanguage, str]]) -> bool:
        """checks equality of ui titles between two fields.

        required for morphing thing

        :param other_field_or_other_ui_title: ['Field', typing.Dict[basic_types.Language.AvailableLanguage], str]

        :return: bool
        """

        if isinstance(other_field_or_other_ui_title, Field):
            other_ui_title = other_field_or_other_ui_title.get_ui_title()
        else:
            other_ui_title = other_field_or_other_ui_title

        for language in self._ui_title:
            if language not in other_ui_title:
                return False
            if self._ui_title[language] != other_ui_title[language]:
                return False

        return True

    # ===========================================================================
    def is_hidden(self) -> bool:
        """used only in morphing things.

        :return: bool
        """

        return self._is_hidden

    # ===========================================================================
    def is_instance_specific(self) -> bool:
        """used only in morphing things.

        required for morphing thing

        :return: bool
        """

        return self._is_instance_specific

    # ===========================================================================
    def matches(self, other_field: 'Field') -> bool:
        """checks equality of values between two fields.

         required for morphing thing

        :param other_field: Field

        :return: bool
        """

        return self.order == other_field.order and \
               self.has_same_ui_titles(other_field) and \
               self.in_class.matches(other_field.in_class) and \
               self.in_editor.matches(other_field.in_editor) and \
               self.in_database.matches(other_field.in_database) and \
               self.is_instance_specific() == other_field.is_instance_specific() and \
               self.is_hidden() == other_field.is_hidden()

    # ===========================================================================
    def set_hidden(self, hidden: bool):
        """only used in morphing things.

        :param hidden: bool

        :return:
        """

        if self._is_hidden != hidden:
            self._is_hidden = hidden
            self.hiding_status_changed_signal.emit(self)

    # ===========================================================================
    def set_instance_specific(self, instance_specific: bool):
        """Marks this field as an instance specific field (changes in each instance) or removes this tag from the field.

        used only in morphing things.

        required for morphing thing

        :param instance_specific: bool

        :return:
        """

        self._is_instance_specific = instance_specific

    # ===========================================================================
    def set_instance_ui_title(self, new_titles: typing.Dict[basic_types.Language.AvailableLanguage, str]):
        """ Updates ui titles of instance specific ui_titles

        used only in morphing things.

        :param new_titles: typing.Dict[basic_types.Language.AvailableLanguage, str]

        :return:
        """
        if not self.has_same_ui_titles(new_titles):
            self._ui_title = new_titles
            self.ui_titles_changed_signal.emit(self)
