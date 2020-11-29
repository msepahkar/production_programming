# -*- coding: utf-8 -*-

import datetime
import typing
from mehdi_lib.generals import general_editors_prototypes, general_ui_titles, general_initial_values
from mehdi_lib.basics import basic_types, field_, database_tools, prototype_
from mehdi_lib.tools import tools

from PyQt5 import QtCore


# ===========================================================================
class BoolField(field_.Field):
    """
    For True/False values
    """
    # ===========================================================================
    def __init__(self, order: int, ui_title: dict, in_class_name: str, initial_value: bool):
        in_class = field_.InClass(in_class_name, bool, initial_value)

        in_database = field_.InDatabase(in_class_name,
                                        database_tools.Database.types[bool],
                                        database_tools.Types.format_for_database(initial_value, bool),
                                        database_tools.Conditions.not_null)

        in_editor = field_.InEditor(general_editors_prototypes.BoolEditorPrototype, None)

        super().__init__(order, ui_title, in_class, in_database, in_editor)

    # ===========================================================================
    def get_copy_parameters(self):
        return [
            self.order,
            self.get_ui_title(),
            self.in_class.name,
            self.in_class.initial_value,
        ]


# ===========================================================================
class CommentField(field_.Field):
    """
    For adding comment to a thing.
    """
    # ===========================================================================
    def __init__(self):
        """
        Order parameter is considered as 0 always. Because usually Comment field is the last field in the UI and
        it is not easy to know the number of the last field beforehand!
        """
        in_class = field_.InClass('comment', str, general_initial_values.dummy)  # type: InClass

        in_database = field_.InDatabase('comment',
                                        database_tools.Database.types[str],
                                        database_tools.Types.format_for_database('', str), None)  # type: InDatabase

        in_editor = field_.InEditor(general_editors_prototypes.CommentEditorPrototype, None)  # type: InEditor

        super().__init__(0, general_ui_titles.comment, in_class, in_database, in_editor)


# ===========================================================================
class DatetimeField(field_.Field):
    """
    For editing datetime
    """
    # ===========================================================================
    def __init__(self, order: int, ui_title: dict, in_class_name: str, initial_value: datetime.datetime):
        in_class = field_.InClass(in_class_name, datetime.datetime, initial_value)

        in_database = field_.InDatabase(in_class_name,
                                        database_tools.Database.types[datetime.datetime],
                                        database_tools.Types.format_for_database(initial_value, datetime.datetime),
                                        database_tools.Conditions.not_null)

        in_editor = field_.InEditor(general_editors_prototypes.DatetimeEditorPrototype, None)

        super().__init__(order, ui_title, in_class, in_database, in_editor)

    # ===========================================================================
    def get_copy_parameters(self):
        return [
            self.order,
            self.get_ui_title(),
            self.in_class.name,
            self.in_class.initial_value,
        ]


# ===========================================================================
class DateField(field_.Field):
    """
    For editing date only (without time)
    """
    # ===========================================================================
    def __init__(self, order: int, ui_title: dict, in_class_name: str, initial_value: datetime.date):
        in_class = field_.InClass(in_class_name, datetime.date, initial_value)

        in_database = field_.InDatabase(in_class_name,
                                        database_tools.Database.types[datetime.date],
                                        database_tools.Types.format_for_database(initial_value, datetime.date),
                                        database_tools.Conditions.not_null)

        in_editor = field_.InEditor(general_editors_prototypes.DateEditorPrototype, None)

        super().__init__(order, ui_title, in_class, in_database, in_editor)

    # ===========================================================================
    def get_copy_parameters(self):
        return [
            self.order,
            self.get_ui_title(),
            self.in_class.name,
            self.in_class.initial_value,
        ]


# ===========================================================================
class DurationField(field_.Field):
    """
    For editing durations (timedelta in python words!)
    """
    # ===========================================================================
    def __init__(self, order: int, ui_title: dict, in_class_name: str, initial_value: datetime.timedelta):
        in_class = field_.InClass(in_class_name, datetime.timedelta, initial_value)

        in_database = field_.InDatabase(in_class_name,
                                        database_tools.Database.types[datetime.timedelta],
                                        database_tools.Types.format_for_database(initial_value, datetime.timedelta),
                                        database_tools.Conditions.not_null)

        in_editor = field_.InEditor(general_editors_prototypes.DurationEditorPrototype, None)

        super().__init__(order, ui_title, in_class, in_database, in_editor)

    # ===========================================================================
    def get_copy_parameters(self):
        return [
            self.order,
            self.get_ui_title(),
            self.in_class.name,
            self.in_class.initial_value,
        ]


# ===========================================================================
class EnumField(field_.Field):
    """
    For editing enums. Enum itself is passed as the initial value when class is created and then the field will allow
    the user to set the value of the enum.
    """

    # will be emitted whenever the enum of the class is changed (not the enum value but the enum itself!)
    enum_changed_signal = QtCore.pyqtSignal('PyQt_PyObject')

    # ===========================================================================
    def __init__(self, order: int, ui_title: dict, in_class_name: str, enum_: typing.Type[basic_types.UiTitleEnabledEnum], initial_value):
        in_class = field_.InClass(in_class_name, enum_, initial_value)

        in_database = field_.InDatabase(in_class_name,
                                        database_tools.Database.types[basic_types.UiTitleEnabledEnum],
                                        database_tools.Types.format_for_database(initial_value, enum_),
                                        database_tools.Conditions.not_null)

        in_editor = field_.InEditor(general_editors_prototypes.EnumItemSelectorEditorPrototype, [enum_])

        super().__init__(order, ui_title, in_class, in_database, in_editor)

    # ===========================================================================
    def get_copy_parameters(self):
        return [
            self.order,
            self.get_ui_title(),
            self.in_class.name,
            self.in_class.type,
            self.in_class.initial_value,
        ]

    # ===========================================================================
    def force_to_match(self, other_field):
        previous_enum = self.in_class.type
        super().force_to_match(other_field)
        if self.in_class.type != previous_enum:
            self.enum_changed_signal.emit(self.in_class.type)

    # ===========================================================================
    def set_enum(self, new_enum):
        """
        For changing current enum of the class
        :param new_enum:
        :return:
        """
        if self.in_class.type != new_enum:
            self.in_class.set_type(new_enum)
            self.in_editor.editor_parameters_list = [new_enum]
            self.enum_changed_signal.emit(new_enum)


# ===========================================================================
class FileNameField(field_.Field):
    """
    For editing file names.
    """
    # ===========================================================================
    def __init__(self, initial_value: str):
        in_class = field_.InClass('file_name', str, initial_value)  # type: InClass

        in_database = field_.InDatabase('file_name',
                                        database_tools.Database.types[str],
                                        database_tools.Types.format_for_database(initial_value, str),
                                        database_tools.Conditions.not_null)  # type: InDatabase

        in_editor = field_.InEditor(general_editors_prototypes.FileNameEditorPrototype, None)  # type: InEditor

        super().__init__(0, general_ui_titles.file_name, in_class, in_database, in_editor)

    # ===========================================================================
    def get_copy_parameters(self):
        return [self.in_class.initial_value]


# ===========================================================================
class FilePathField(field_.Field):
    """
    For editing file paths
    """
    # ===========================================================================
    def __init__(self, initial_value: str):
        in_class = field_.InClass('file_path', str, initial_value)  # type: InClass

        in_database = field_.InDatabase('file_path',
                                        database_tools.Database.types[str],
                                        database_tools.Types.format_for_database(initial_value, str),
                                        database_tools.Conditions.not_null)  # type: InDatabase

        in_editor = field_.InEditor(general_editors_prototypes.FilePathEditorPrototype, None)  # type: InEditor

        super().__init__(0, general_ui_titles.file_path, in_class, in_database, in_editor)

    # ===========================================================================
    def get_copy_parameters(self):
        return [self.in_class.initial_value]


# ===========================================================================
class FloatField(field_.Field):
    """
    For editing float numbers
    """
    # ===========================================================================
    def __init__(self, order: int, ui_title: dict, in_class_name: str, bottom: float, top: float, decimals: int,
                 initial_value: float):
        """

        :param order:
        :param ui_title:
        :param in_class_name:
        :param bottom: minimum allowed number
        :param top: maximum allowed number
        :param decimals: number of digits after the floating point
        :param initial_value:
        """
        in_class = field_.InClass(in_class_name, float, initial_value)

        in_database = field_.InDatabase(in_class_name,
                                        database_tools.Database.types[float],
                                        database_tools.Types.format_for_database(initial_value, float),
                                        database_tools.Conditions.not_null)

        in_editor = field_.InEditor(general_editors_prototypes.FloatEditorPrototype, [bottom, top, decimals])

        self.bottom = bottom
        self.top = top
        self.decimals = decimals

        super().__init__(order, ui_title, in_class, in_database, in_editor)

    # ===========================================================================
    def get_copy_parameters(self):
        return [
            self.order,
            self.get_ui_title(),
            self.in_class.name,
            self.bottom,
            self.top,
            self.decimals,
            self.in_class.initial_value,
        ]


# ===========================================================================
class ForeignKeyField(field_.Field):
    """
    For storing foreign keys whenever our 'Thing' is related to another 'Thing'
    """
    # ===========================================================================
    def __init__(self, order: int, ui_title: dict, in_class_name: str,
                 referencing_prototype: typing.Type['ThingPrototype'],
                 foreign_prototype: typing.Type['ThingPrototype'],
                 in_editor=None):

        in_class = field_.InClass(in_class_name, foreign_prototype, None)  # type: InClass
        in_database = field_.InDatabase(in_class_name,
                                        database_tools.Database.types[int],
                                        None,
                                        # TODO: do we need the condition of not null for foreign key field?
                                        database_tools.Conditions.not_null)  # type: InDatabase

        super().__init__(order, ui_title, in_class, in_database, in_editor)

        self.referencing_prototype = referencing_prototype
        if referencing_prototype not in foreign_prototype.referencing_prototypes():
            foreign_prototype.referencing_prototypes().append(referencing_prototype)

        self.foreign_prototype = foreign_prototype  # type: typing.Type['ThingPrototype']

    # ===========================================================================
    def get_copy_parameters(self):
        return [
            self.order,
            self.get_ui_title(),
            self.in_class.name,
            self.referencing_prototype,
            self.foreign_prototype,
            self.in_editor.create_copy(),
        ]


# ===========================================================================
class ForeignThingSelectorField(ForeignKeyField):
    """
    something like a combo box for selecting foreign thing related to this thing
    """
    # ===========================================================================
    def __init__(self, order: int, ui_title: dict, in_class_name: str,
                 referencing_prototype: typing.Type['ThingPrototype'],
                 thing_prototype: typing.Type['ThingPrototype'],
                 # TODO: why forbidden item creator is not used????
                 forbidden_items_creator: callable = None):
        super().__init__(order, ui_title, in_class_name, referencing_prototype, thing_prototype)

        self.in_editor = field_.InEditor(general_editors_prototypes.SingleItemSelectorEditorPrototype)

    # ===========================================================================
    def get_copy_parameters(self):
        return [
            self.order,
            self.get_ui_title(),
            self.in_class.name,
            self.referencing_prototype,
            self.foreign_prototype,
        ]


# ===========================================================================
class IntField(field_.Field):
    """
    general int field
    """
    # ===========================================================================
    def __init__(self, order: int, ui_title: dict, in_class_name: str, bottom: int, top: int, initial_value: int):
        in_class = field_.InClass(in_class_name, int, initial_value)

        in_database = field_.InDatabase(in_class_name,
                                        database_tools.Database.types[int],
                                        database_tools.Types.format_for_database(initial_value, int),
                                        database_tools.Conditions.not_null)

        in_editor = field_.InEditor(general_editors_prototypes.IntEditorPrototype, [bottom, top])

        self.bottom = bottom
        self.top = top

        super().__init__(order, ui_title, in_class, in_database, in_editor)

    # ===========================================================================
    def get_copy_parameters(self):
        return [
            self.order,
            self.get_ui_title(),
            self.in_class.name,
            self.bottom,
            self.top,
            self.in_class.initial_value,
        ]


# ===========================================================================
class ListField(field_.Field):
    """
    for storing list of things
    """
    # ===========================================================================
    def __init__(self, order: int, ui_title: dict, in_class_name: str, element_type: 'typing.Type[Thing]', in_editor=None):
        if in_editor is None:
            in_editor = field_.InEditor(general_editors_prototypes.TableOfThingsEditorPrototype, [])

        super().__init__(order, ui_title,
                         field_.InClass(in_class_name, prototype_.ListOfThingsPrototype, element_type),
                         None,
                         in_editor)

    # ===========================================================================
    def get_copy_parameters(self):
        return [
            self.order,
            self.get_ui_title(),
            self.in_class.name,
            self.in_class.initial_value,
            self.in_editor.create_copy(),
        ]


# ===========================================================================
class NameField(field_.Field):
    """
    general name field
    """
    # ===========================================================================
    def __init__(self, initial_value: str):
        in_class = field_.InClass('name', str, initial_value)  # type: InClass

        in_database = field_.InDatabase('name',
                                        database_tools.Database.types[str],
                                        database_tools.Types.format_for_database(initial_value, str),
                                        database_tools.Conditions.not_null)  # type: InDatabase

        in_editor = field_.InEditor(general_editors_prototypes.NameEditorPrototype, None)  # type: InEditor

        super().__init__(0, general_ui_titles.name, in_class, in_database, in_editor)

    # ===========================================================================
    def get_copy_parameters(self):
        return [self.in_class.initial_value]


# ===========================================================================
class OrderNumberField(field_.Field):
    """
    general order number field
    """
    # ===========================================================================
    def __init__(self):
        in_class = field_.InClass('order_number', int, 0)
        in_database = field_.InDatabase('order_number',
                                        database_tools.Database.types[int],
                                        None,
                                        database_tools.Conditions.not_null)
        in_editor = field_.InEditor(general_editors_prototypes.IntEditorPrototype, [0, tools.Tools.max_allowed_int])

        super().__init__(0, general_ui_titles.order_number, in_class, in_database, in_editor)


# ===========================================================================
class PercentField(IntField):
    """
    general percent field
    """
    # ===========================================================================
    def __init__(self, order, ui_title, in_class_name, initial_value):
        super().__init__(order, ui_title, in_class_name, 0, 100, initial_value)

    # ===========================================================================
    def get_copy_parameters(self):
        return [
            self.order,
            self.get_ui_title(),
            self.in_class.name,
            self.in_class.initial_value,
        ]


# ===========================================================================
class PrimaryKeyField(field_.Field):
    """
    general primary key field
    """
    # ===========================================================================
    def __init__(self):
        in_class = field_.InClass('id', int, None)
        in_database = field_.InDatabase('id',
                                        database_tools.Database.types[int],
                                        None,
                                        database_tools.Conditions.primary_key_auto)

        super().__init__(0, general_ui_titles.dummy, in_class, in_database, None)




