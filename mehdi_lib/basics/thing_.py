# -*- coding: utf-8 -*-

import datetime
import importlib
import inspect
import sys
import threading
import typing

from PyQt5 import QtSql, QtCore

from mehdi_lib.tools import tools
from mehdi_lib.basics import field_, database_tools, basic_types, prototype_, constants_
from mehdi_lib.generals import general_fields, general_editors_prototypes, general_ui_titles, general_initial_values


# ===========================================================================
class DependencyParameters:
    """
    Information about the list on which a thing field is dependent

    For example a sub-part field of a part should be selected from list of parts.
    So this field is dependent on the list of parts.
    Whenever the main list (in our example: list of parts) is updated, the dependency list should be automatically
    updated in all UIs showing this element.
    """

    # ===========================================================================
    def __init__(self, dependent_on_list, field_for_retrieving_dependent_on_list_item, forbidden_items_creator):
        """

        :param dependent_on_list: the list on which a field of our thing is dependent on.
        :param field_for_retrieving_dependent_on_list_item: the field in our thing which gives us the dependent item.
        :param forbidden_items_creator: a function which generates a list containing items not allowed as the dependent
        field value (for example in the part list example, no part can be sub part of itself. So for each part, the part
        itself should be removed from the list of parts available as the dependent on list).
        """

        self.dependent_on_list = dependent_on_list
        self.field_for_retrieving_dependent_on_list_item = field_for_retrieving_dependent_on_list_item
        self.forbidden_items_creator = forbidden_items_creator


# ===========================================================================
class ForeignOwnerParameters:
    """Stores the list field in the foreign owner which contains this thing.

    For example a part has a list field called sub-parts. every part in the sub-parts list should have a
    foreign owner parameter which stores this list field of the main part.
    One part could have multiple foreign owners.
    """

    # ===========================================================================
    def __init__(self, list_field_in_foreign_owner):
        self.list_field_in_foreign_owner = list_field_in_foreign_owner


# ===========================================================================
class Thing(field_.Field):
    """The heart of this infrastructure.

    The smallest entity is called 'Thing' in this infrastructure.
    A 'Thing' has several fields and has a table in database which stores these fields.
    A 'Thing' can automatically create its table and do CRUD operations on its table.
    A 'Thing' can automatically update its table when fields are added to or removed from its definition.
    """

    # will be emitted when a field is modified
    modified_signal = QtCore.pyqtSignal('PyQt_PyObject')

    primary_key = general_fields.PrimaryKeyField()
    order_number = general_fields.OrderNumberField()
    name = general_fields.NameField(initial_value=general_initial_values.name)

    # sometimes users want to just complete the information. so there should be a way to specify the inaccuracy of them
    precision_of_information = general_fields.PercentField(0, general_ui_titles.precision_of_information,
                                                           'precision_of_information', 90)

    # any information not present in other fields
    comment = general_fields.CommentField()

    # fields which are removed from the definition of this 'Thing' (for updating the table)
    removed_fields = []  # type: [Field]

    # should be defined in derived classes
    table_name = None  # type: str

    # any condition which should be included in CREATE command and could not be added to field conditions
    extra_table_condition = None  # type: str

    # for storing all instances of this 'Thing' (fetched from database or created in memory)
    _all = None  # type: 'ListOfThings'

    # ===========================================================================
    def __init__(self, *foreign_things, max_forbidden_number: int = 0, forbidden_names: [] = None):
        """

        :param foreign_things: 'Things' which own this instance (example: parts which have this thing as sub-part)
        NOTE: first foreign owner in the list is the main owner
        :param max_forbidden_number: order number of this 'Thing' should be greater than this parameter
        :param forbidden_names: these names should not be used for this 'Thing'
        """

        super().__init__(-1, general_ui_titles.dummy, None, None,
                         field_.InEditor(general_editors_prototypes.ThingEditorPrototype, []))

        # new thing is modified until it is added to the database or fetched from the database
        self.modified_fields = [type(self).primary_key]
        self._is_marked_for_removal = False
        self.lock = threading.Lock()
        self.editors = []
        self._responsible_editor = None
        self.dependent_editors = []
        self.field_editors = dict()  # keys are fields, values are arrays
        self._field_responsible_editors = dict()  # keys are fields, values are responsible editors
        self.dependency_parameters = dict()
        self.foreign_owner_parameters = dict()
        # self.instance_specific_fields = dict()
        self.lists_of_things = []

        self.init_fields()

        # initialize the name field
        self[Thing.name] = type(self).find_unique_name(
                           forbidden_names=forbidden_names,
                           foreign_thing=foreign_things[0] if foreign_things else None)

        # initialize the order number field
        self[Thing.order_number] = type(self).find_unique_order_number(
                           max_forbidden_number=max_forbidden_number,
                           foreign_thing=foreign_things[0] if foreign_things else None)

        # setting foreign things in order of foreign keys
        self.set_foreign_owners(foreign_things)

        # now editors which are specific for this instance
        self.set_dependency_parameters()
        self.set_foreign_owner_parameters()

    # ===========================================================================
    @classmethod
    def all(cls) -> 'ListOfThings':
        """
        This array will store all instances of this class read from database or created in memory.

        :return: The array containing all instances of this class
        """
        if cls._all is None:
            cls._all = ListOfThings(cls)
            if cls.table_exists():
                cls.get_things('', consider_all=False)

        return cls._all

    # ===========================================================================
    @classmethod
    def create_table(cls, check_existence: bool=False) -> bool:
        """
        Creates a proper table for storing instances of this class

        :param check_existence: determines if existence of the table should be checked.
        :return: True if the table is created successfully and False otherwise.
        """

        if check_existence:
            command = 'CREATE TABLE IF NOT EXISTS {} ('.format(cls.table_name)
        else:
            command = 'CREATE TABLE {} ('.format(cls.table_name)

        # add fields
        for field__ in cls.sorted_fields_of_class(include_primary_key=True):
            if field__.in_database:
                command += field__.in_database.get_creation_command() + ','

        # extra condition
        if cls.extra_table_condition is not None:
            command += cls.extra_table_condition

        # remove the last comma
        else:
            command = command[:-1]

        # foreign keys (owner, other owner, ...)
        for field__ in cls.sorted_foreign_key_fields_of_class():
            command += ',FOREIGN KEY({}) REFERENCES {}'.format(field__.in_database.title,
                                                               field__.foreign_prototype.get_main_type().table_name)

        command += ')'

        # create the table
        query = database_tools.Commands.exec_query(command)

        # check for error
        if query is None:
            tools.Tools.warning('cannot create table: "{}"'.format(cls.table_name))
            return False

        return True

    # ===========================================================================
    @classmethod
    def fetch_by_foreign_thing(cls: 'typing.Type[Thing]', foreign_thing: 'Thing',
                               check_all_foreign_keys: bool = False) -> '[Thing]':
        """

        :param foreign_thing:
        :param check_all_foreign_keys:
        :return:
        """
        # NOTE: when check_all_foreign_keys is false, checks only the first foreign key matching foreign thing

        foreign_keys = []

        # find the foreign key
        for key in cls.sorted_foreign_key_fields_of_class():
            if type(foreign_thing) == key.foreign_prototype.get_main_type():
                foreign_keys.append(key)
                if not check_all_foreign_keys:
                    break

        if len(foreign_keys) == 0:
            tools.Tools.warning('cannot find the foreign key for {} in {}'.format(type(foreign_thing), cls))

        # init an empty array
        fetched_things = ListOfThings(cls)

        for foreign_key in foreign_keys:
            # create the command
            condition = '{}={}'.format(foreign_key.in_database.title,
                                       foreign_thing[foreign_key.foreign_prototype.get_main_type().primary_key])

            fetched_things.add(cls.get_things(condition))

        return fetched_things

    # ===========================================================================
    @classmethod
    def find_unique_name(cls, forbidden_names: [] = None, foreign_thing: 'Thing' = None) -> str:

        # this foreign thing is in fact the owner of the new thing for which a name is being created
        if foreign_thing:
            foreign_keys = cls.sorted_foreign_key_fields_of_class(type(foreign_thing))
            if not foreign_keys:
                tools.Tools.fatal_error('you may have forgotten to add foreign thing field of {} into the sub-thing: {}!'.format(type(foreign_thing), cls))
            foreign_key = foreign_keys[0]
        else:
            foreign_key = None

        i = 1
        if isinstance(cls.name.in_class.initial_value, basic_types.MultilingualString):
            base_name = cls.name.in_class.initial_value[basic_types.Language.get_active_language()]
        else:
            base_name = cls.name.in_class.initial_value

        while True:
            name = '{} {}'.format(base_name, i)
            if forbidden_names and name in forbidden_names:
                i += 1
                continue

            exists = False
            for thing in cls.all():
                if not thing.is_marked_for_removal():

                    # same name exists in all() array for a thing with the same owner
                    if thing.name == name and (foreign_thing is None or thing[foreign_key] == foreign_thing):
                        exists = True
                        break
            if exists:
                i += 1
            else:
                break

        return '{} {}'.format(base_name, i)

    # ===========================================================================
    @classmethod
    def find_unique_order_number(cls, max_forbidden_number: int = 0, foreign_thing: 'Thing' = None) -> str:

        # this foreign thing is in fact the owner of the new thing for which a order number is being found
        if foreign_thing:
            foreign_key = cls.sorted_foreign_key_fields_of_class(type(foreign_thing))[0]
        else:
            foreign_key = None

        unique_order_number = max_forbidden_number + 1

        for thing in cls.all():

            if not thing.is_marked_for_removal():

                # equal or greater order number exists in all() array for a thing with the same owner
                if unique_order_number <= thing.order_number and (foreign_thing is None or thing[foreign_key] == foreign_thing):
                    unique_order_number = thing.order_number + 1

        return unique_order_number

    # ===========================================================================
    @classmethod
    def get_thing(cls, key: int, limit_to_all: bool = False) -> typing.Optional['Thing']:

        for thing in cls.all():
            if thing[cls.primary_key] == key:
                return thing

        if not limit_to_all:
            things = cls.get_things('{}={}'.format(cls.primary_key.in_database.title, key, consider_all=False))
            if things:
                return things[0]

        return None

    # ===========================================================================
    @classmethod
    def get_things(cls, condition: str, consider_all: bool = True) -> ['Thing']:

        fetched_things = []

        command = 'SELECT '

        # add fields
        for field in cls.sorted_fields_of_class(include_primary_key=True):
            if field.in_database:
                command += '{},'.format(field.in_database.title)

        # remove the last comma
        if command.endswith(','):
            command = command[:-1]

        # add the rest
        command += ' FROM {}'.format(cls.table_name)
        if condition:
            command += ' WHERE {}'.format(condition)

        # do the fetching
        query = database_tools.Commands.exec_query(command)

        # check for the error
        if query is None:
            tools.Tools.warning('cannot fetch with condition "{}" from table "{}"'.format(condition, cls.table_name))
        else:

            # retrieve the fetched thing
            while query.next():
                if consider_all:
                    id_ = query.value(query.record().indexOf(cls.primary_key.in_database.title))
                    thing = cls.get_thing(id_, limit_to_all=True)
                    if thing:
                        fetched_things.append(thing)
                        continue

                # it will be automatically added to the all array
                fetched_thing = cls()

                # fetch fields from the query
                fetched_thing.fetch_fields(query)

                # newly fetched thing is not modified
                fetched_thing.reset_modified()

                fetched_things.append(fetched_thing)

            # now list fields
            for fetched_thing in fetched_things:

                # fetch the list fields
                fetched_thing.fetch_list_fields()

                # this should be done again, because of change in fields
                fetched_thing.set_dependency_parameters()

                # TODO: newly fetched thing is not modified?
                # fetched_thing.reset_modified()

        return fetched_things

    # ===========================================================================
    @classmethod
    def remove_extra_from_database(cls: 'typing.Type[Thing]', foreign_thing: 'Thing',
                                   existing_things: ['Thing']) -> bool:

        fetched_things = cls.fetch_by_foreign_thing(foreign_thing)

        # suppose success
        problem = False

        # remove extra
        for fetched_thing in fetched_things:

            # suppose this thing is extra
            if fetched_thing:
                is_extra = True
                for existing_thing in existing_things:
                    if existing_thing:
                        if existing_thing[cls.primary_key] == fetched_thing[cls.primary_key]:
                            is_extra = False
                            break
                if is_extra:
                    if not fetched_thing.remove_from_database():
                        problem = True

        if problem:
            return False

        return True

    # ===========================================================================
    @classmethod
    def replace_parent_table(cls) -> bool:

        parent_type = tools.Tools.parent_type(cls)  # type: typing.Type['Thing']

        # check for prototype definition
        cls_prototype = prototype_.ThingPrototype.get_prototype(cls)
        parent_prototype = prototype_.ThingPrototype.get_prototype(parent_type)
        if cls_prototype and cls_prototype == parent_prototype:
            tools.Tools.fatal_error('defining prototype is forgotten for {}'.format(cls))

        # check for table names
        if cls.table_name != parent_type.table_name:
            tools.Tools.fatal_error(
                'table name is changed in the child type: "{}" <> "{}"'.format(cls.table_name, parent_type.table_name))

        # fetch all parent things first
        # parent_type.get_things('')

        # drop the parent table
        query = database_tools.Commands.exec_query('DROP TABLE {}'.format(parent_type.table_name))

        # check for error
        if query is None:
            tools.Tools.warning('cannot drop table:"{}"'.format(parent_type.table_name))
            return False

        # create the child table
        if not cls.create_table():
            return False

        # create an _all attribute for the child
        cls._all = None

        # create child thing for every parent thing
        problem = False
        for parent_thing in parent_type.all():
            thing = cls().copy_from_parent(parent_thing)
            if not thing.update_in_database():
                problem = True
                if thing[cls.primary_key] is None:
                    continue

            # referencing types
            parent_prototype = prototype_.ThingPrototype.get_prototype(parent_type)
            if parent_prototype:
                for referencing_prototype in parent_prototype.referencing_prototypes():
                    for referencing_thing in referencing_prototype.get_main_type().\
                            fetch_by_foreign_thing(parent_thing, check_all_foreign_keys=True):
                        for foreign_key in referencing_thing.sorted_foreign_key_fields_of_class(parent_type):
                            if referencing_thing[foreign_key][type(referencing_thing).primary_key] == \
                                    parent_thing[parent_type.primary_key]:
                                referencing_thing[foreign_key] = thing
                        if not referencing_thing.update_in_database():
                            problem = True

        parent_type.removed_fields = cls.removed_fields

        return not problem

    # ===========================================================================
    @classmethod
    def sorted_fields_of_class(cls, include_primary_key: bool) -> [field_.Field]:
        fields = []

        # check parent type
        parent_type = tools.Tools.parent_type(cls)
        if issubclass(parent_type, Thing):
            parent_fields = parent_type.sorted_fields_of_class(include_primary_key)
            dir_parent_type = dir(parent_type)
        else:
            dir_parent_type = []
            parent_fields = []

        # add fields
        for field_name in dir(cls):
            field = getattr(cls, field_name)
            if isinstance(field, field_.Field) and field not in cls.removed_fields:
                if include_primary_key or not isinstance(field, general_fields.PrimaryKeyField):
                    # replace same fields in parent
                    if field_name in dir_parent_type:
                        index = parent_fields.index(getattr(parent_type, field_name))
                        parent_fields[index] = field
                    else:
                        fields.append(field)

        # sort the fields
        fields.sort(key=lambda x: x.order)

        # now add parent fields
        fields = parent_fields + fields

        if include_primary_key:
            tools.Tools.force_order_in_list_elements(fields,
                                                     cls.order_number,
                                                     cls.name,
                                                     first_element=cls.primary_key,
                                                     one_before_last_element=cls.precision_of_information,
                                                     last_element=cls.comment)
        else:
            tools.Tools.force_order_in_list_elements(fields,
                                                     cls.order_number,
                                                     cls.name,
                                                     first_element=None,
                                                     one_before_last_element=cls.precision_of_information,
                                                     last_element=cls.comment)
        return fields

    # ===========================================================================
    @classmethod
    def sorted_foreign_key_fields_of_class(cls, foreign_type: typing.Type['Thing']=None) -> [field_.Field]:
        # parameters: foreign_type limits the type of foreign keys which are supposed to be fetched

        fields = []

        # add other fields
        for field in cls.sorted_fields_of_class(include_primary_key=False):
            if isinstance(field, general_fields.ForeignKeyField):
                if foreign_type is None or field.foreign_prototype.get_main_type() is foreign_type:
                    fields.append(field)

        return fields

    # ===========================================================================
    @classmethod
    def sorted_list_fields_of_class(cls) -> [general_fields.ListField]:
        list_fields = []

        # add list fields
        for field in cls.sorted_fields_of_class(include_primary_key=False):
            if isinstance(field, general_fields.ListField):
                list_fields.append(field)

        return list_fields

    # ===========================================================================
    @classmethod
    def table_exists(cls):
        query = database_tools.Commands.exec_query(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(cls.table_name))
        if query and query.next():
            return True

        return False

    # ===========================================================================
    @staticmethod
    def all_thing_classes():

        # first modules
        modules = []
        for module in sys.modules:
            modules.append(module)

        # now thing classes
        things = []
        for module in modules:
            imported_module = importlib.import_module(module)
            for item in dir(sys.modules[module]):
                try:
                    cls = getattr(imported_module, item)
                except ImportError:
                    continue

                if inspect.isclass(cls) and cls != Thing and Thing in inspect.getmro(cls) and cls not in things:
                    things.append(cls)
        return things

    # ===========================================================================
    @staticmethod
    def create_tables():

        for thing in Thing.all_thing_classes():
            if thing.table_name is not None:
                thing.create_table()

    # ===========================================================================
    def copy_from_parent(self, parent_thing) -> 'Thing':
        for field in parent_thing.sorted_fields_of_class(include_primary_key=False):
            if isinstance(field, general_fields.ListField):
                self[field].clear()
                for thing in parent_thing[field]:
                    self[field].append(thing)
            else:
                self[field] = parent_thing[field]

        # returning self makes chain of commands possible
        return self

    # ===========================================================================
    def fetch_fields(self, query: QtSql.QSqlQuery) -> bool:

        problem = False

        for field in self.get_sorted_fields_of_instance(include_primary_key=True):
            if field.in_database:
                val = query.value(query.record().indexOf(field.in_database.title))
                if isinstance(field, general_fields.ForeignKeyField):
                    if val != -1:
                        self[field] = field.foreign_prototype.get_main_type().get_thing(val)
                        if self[field] is None:
                            tools.Tools.warning('cannot fetch the foreign thing with id "{}" for "{}"'.format(val,
                                                                                                              self))
                            problem = True
                else:
                    self[field] = database_tools.Types.format_for_class(val, field.in_class.type)

        return not problem

    # ===========================================================================
    def fetch_list_fields(self):
        for list_field in type(self).sorted_list_fields_of_class():
            self[list_field].clear()
            self[list_field].add(list_field.in_class.initial_value.fetch_by_foreign_thing(self))
            self[list_field].reset_modified()

    # ===========================================================================
    def get_correspondent_class_field(self, field):
        # if not field.is_instance_specific():
            return field
        # return next(class_field for class_field, instance_field in self.instance_specific_fields.items() if instance_field == field)

    # ===========================================================================
    def get_correspondent_instance_field(self, field):
        # if field in self.instance_specific_fields:
        #     return self.instance_specific_fields[field]
        # else:
            return field

    # ===========================================================================
    def get_responsible_editor(self, field=None):

        # the thing itself
        if field is None:
            if self._responsible_editor is None:
                self._responsible_editor = prototype_.EditorPrototype.get_main_type().create_responsible_editor(self, None)
            responsible_editor = self._responsible_editor

        # field of thing
        else:

            # list field
            if isinstance(field, general_fields.ListField):
                responsible_editor = self[field].get_responsible_editor()

            # normal field
            else:
                instance_field = self.get_correspondent_instance_field(field)
                if self._field_responsible_editors[instance_field] is None:
                    self._field_responsible_editors[instance_field] = prototype_.EditorPrototype.get_main_type().create_responsible_editor(self, instance_field)
                responsible_editor = self._field_responsible_editors[instance_field]

        return responsible_editor

    # ===========================================================================
    def get_sorted_fields_of_instance(self, include_primary_key):
        fields = type(self).sorted_fields_of_class(include_primary_key)
        # for i, field in enumerate(fields):
        #     if field.is_instance_specific():
        #         fields[i] = self.instance_specific_fields[field]
        return fields

    # ===========================================================================
    def init_fields(self):

        # find instance specific fields
        # for field_list in self.affected_fields.values():
        #     for field in field_list:
        #         field.set_instance_specific(True)

        # create instance specific fields
        # for field in type(self).sorted_fields_of_class(include_primary_key=True):
        #     if field.is_instance_specific():
        #         self.instance_specific_fields[field] = field.create_copy()

        # substitute class fields with instance fields in affected_fields dict
        # for field_list in self.affected_fields.keys():  # keys
        #     for i, field in enumerate(field_list):
        #         if field.is_instance_specific():
        #             field_list[i] = self.instance_specific_fields[field]
        # for field_list in self.affected_fields.values():  # values
        #     for i, field in enumerate(field_list):
        #         if field.is_instance_specific():
        #             field_list[i] = self.instance_specific_fields[field]

        # set editors and responsible editors
        for field in self.get_sorted_fields_of_instance(include_primary_key=True):
            if not isinstance(field, general_fields.ListField):
                self.field_editors[field] = []
                self._field_responsible_editors[field] = None

        # add fields to the class
        for field in self.get_sorted_fields_of_instance(include_primary_key=True):

            # list field
            if isinstance(field, general_fields.ListField):
                # new list is created for each list field
                list_field_instance = field.in_class.type(field.in_class.initial_value)
                setattr(self, field.in_class.name, list_field_instance)

            # normal field
            else:
                if isinstance(field.in_class.initial_value, basic_types.MultilingualString):
                    initial_value = field.in_class.initial_value[basic_types.Language.get_active_language()]
                else:
                    initial_value = field.in_class.initial_value
                setattr(self, field.in_class.name, initial_value)

    # ===========================================================================
    def is_marked_for_removal(self):
        return self._is_marked_for_removal

    # ===========================================================================
    def is_modified(self):
        if self.modified_fields or self.is_marked_for_removal():
            return True
        for list_field in type(self).sorted_list_fields_of_class():
            if self[list_field].is_modified():
                return True
        return False

    # ===========================================================================
    def mark_for_removal(self) -> bool:

        if not self._is_marked_for_removal:
            self._is_marked_for_removal = True
            self.modified_signal.emit(type(self).primary_key)

            # check the id
            if self[type(self).primary_key] is not None and self[type(self).primary_key] != -1:

                # first remove things in list fields
                for list_field in type(self).sorted_list_fields_of_class():
                    # noinspection PyTypeChecker
                    for inner_thing in self[list_field]:
                        inner_thing.mark_for_removal()

                # remove all referencing types first
                prototype = prototype_.ThingPrototype.get_prototype(type(self))
                if prototype:
                    for referencing_prototype in prototype.referencing_prototypes():
                        for referencing_thing in referencing_prototype.get_main_type().fetch_by_foreign_thing(
                                self, check_all_foreign_keys=True):
                            referencing_thing.mark_for_removal()

        return True

    # ===========================================================================
    def remove_from_database(self) -> bool:

        # check the id
        if self[type(self).primary_key] is not None and self[type(self).primary_key] != -1:

            # first remove things in list fields
            for list_field in type(self).sorted_list_fields_of_class():
                # noinspection PyTypeChecker
                for inner_thing in self[list_field]:
                    inner_thing.remove_from_database()

            # remove all referencing types first
            prototype = prototype_.ThingPrototype.get_prototype(type(self))
            if prototype:
                for referencing_prototype in prototype.referencing_prototypes():
                    for referencing_thing in referencing_prototype.get_main_type().fetch_by_foreign_thing(
                            self, check_all_foreign_keys=True):
                        referencing_thing.remove_from_database()

            # now remove the thing itself
            query = database_tools.Commands.exec_query('''
            DELETE FROM {}
            WHERE id={}
            '''.format(type(self).table_name, self[type(self).primary_key]))

            # check for error
            if query is None:
                tools.Tools.warning('cannot remove from table "{}" with id equal to "{}".'.format(
                    type(self).table_name, self[type(self).primary_key]))
                return False

        # remove from all
        if self in type(self).all():
            del type(self).all()[type(self).all().index(self)]

        # primary key is not valid anymore
        self[type(self).primary_key] = -1

        return True

    # ===========================================================================
    def reset_modified(self):
        self.modified_fields.clear()
        self._is_marked_for_removal = False

        # TODO: should we add self to all here???
        if self not in type(self).all():
            type(self).all().append(self)

    # ===========================================================================
    def set_dependency_parameters(self):
        pass

    # ===========================================================================
    def set_foreign_owner_parameters(self):
        pass

    # ===========================================================================
    def set_foreign_owners(self, foreign_things):
        # setting foreign things in order of foreign keys
        foreign_keys = type(self).sorted_foreign_key_fields_of_class()
        for foreign_thing in foreign_things:
            # index for the assigned foreign key
            j = -1
            for i, foreign_key in enumerate(foreign_keys):
                if isinstance(foreign_thing, foreign_key.foreign_prototype.get_main_type()):
                    self[foreign_key] = foreign_thing
                    j = i
                    break
            # remove the assigned foreign key
            if j >= 0:
                del foreign_keys[j]
            else:
                tools.Tools.warning('inappropriate foreign thing: {},  in __init__ for {}'.format(foreign_thing, self))

    # ===========================================================================
    def summary(self, thing_to_be_excluded: 'Thing') -> str:
        summary_sentence = ''
        exclusion_done = False
        for foreign_field in type(self).sorted_foreign_key_fields_of_class():
            if not exclusion_done and foreign_field.foreign_prototype.get_main_type() == type(thing_to_be_excluded):
                exclusion_done = True
                continue

            if self[foreign_field]:
                summary_sentence += self[foreign_field].name + ' '

        return summary_sentence

    # ===========================================================================
    def update_in_database(self) -> bool:

        # first check for removal
        if self._is_marked_for_removal:
            return self.remove_from_database()

        # the thing itself
        if self.modified_fields:

            # invalid things will not be processed at all
            if self[type(self).primary_key] == -1:
                return False

            # no primary key yet?
            if self[type(self).primary_key] is None:

                # do an insert
                command = 'INSERT INTO {} ('.format(self.table_name)

                # add fields
                for field in self.get_sorted_fields_of_instance(include_primary_key=False):
                    if field.in_database:
                        command += field.in_database.title + ','

                # remove the last comma
                if command.endswith(','):
                    command = command[:-1] + ') VALUES ('

                # add values
                for field in self.get_sorted_fields_of_instance(include_primary_key=False):
                    if field.in_database:
                        value = self[field]
                        in_class_type = field.in_class.type
                        # foreign key
                        if isinstance(field, general_fields.ForeignKeyField):
                            # check for foreign key with value None and replace it with -1
                            if value is None:
                                value = -1
                            else:
                                # noinspection PyUnresolvedReferences
                                if value[type(value).primary_key] is None:
                                    # noinspection PyUnresolvedReferences
                                    value.update_in_database()
                                # noinspection PyUnresolvedReferences
                                value = value[field.foreign_prototype.get_main_type().primary_key]
                                in_class_type = int
                        formatted_value = database_tools.Types.format_for_database(value, in_class_type)
                        command += '{},'.format(formatted_value)

                # remove the last comma
                if command.endswith(','):
                    command = command[:-1]

                command += ')'

                # do the insert
                query = database_tools.Commands.exec_query(command)

                # check for error
                if query is None:
                    tools.Tools.warning('cannot insert into table: {}'.format(self.table_name))
                    return False

                # set the primary key
                self[type(self).primary_key] = query.lastInsertId()

            # valid primary key is available
            else:

                # do an update
                command = 'UPDATE {} SET '.format(self.table_name)

                # add fields
                for field in self.get_sorted_fields_of_instance(include_primary_key=False):
                    if field.in_database:
                        value = self[field]
                        in_class_type = field.in_class.type
                        # foreign key
                        if isinstance(field, general_fields.ForeignKeyField):
                            # check for foreign key with value None and replace it with -1
                            if value is None:
                                value = -1
                            else:
                                # noinspection PyUnresolvedReferences
                                if value[field.foreign_prototype.get_main_type().primary_key] is None:
                                    # noinspection PyUnresolvedReferences
                                    value.update_in_database()
                                # noinspection PyUnresolvedReferences
                                value = value[field.foreign_prototype.get_main_type().primary_key]
                                in_class_type = int
                        formatted_value = database_tools.Types.format_for_database(value, in_class_type)
                        command += '{}={},'.format(field.in_database.title, formatted_value)

                # remove the last comma
                if command.endswith(','):
                    command = command[:-1]

                # add the condition
                command += ' WHERE {}={}'.format(type(self).primary_key.in_database.title, self[type(self).primary_key])

                # perform the update
                query = database_tools.Commands.exec_query(command)

                # check for error
                if query is None:
                    tools.Tools.warning('cannot update table: {}'.format(self.table_name))
                    return False

            # normal fields are saved, list fields will be saved next, for avoiding loop we have to reset modified here
            self.reset_modified()

        # now list fields of the thing
        problem = False

        for list_field in type(self).sorted_list_fields_of_class():

            # noinspection PyTypeChecker
            for thing in self[list_field]:
                if thing:
                    thing.update_in_database()

            # remove the extra things of this list field
            if not list_field.in_class.initial_value.remove_extra_from_database(self, self[list_field]):
                problem = True

        return not problem

    # ===========================================================================
    def __getitem__(self, field: field_.Field) -> typing.Optional[field_.Field]:

        # field
        if isinstance(field, field_.Field):
            return getattr(self, field.in_class.name)

        # error
        tools.Tools.warning('only fields or list fields can be used in __getitem__, not "{}"'.format(type(field)))
        return None

    # ===========================================================================
    def __setitem__(self, field: field_.Field, value):

        field = self.get_correspondent_instance_field(field)

        # first check for change in the value
        if getattr(self, field.in_class.name) != value:

            # convert date to datetime for datetime
            if field.in_class.type is datetime.datetime and type(value) is datetime.date:
                # noinspection PyCallingNonCallable
                value = datetime.datetime(value.year, value.month, value.day)
            # primary key
            if isinstance(field, general_fields.PrimaryKeyField):
                if value is not None and not isinstance(value, field.in_class.type):
                    raise ValueError('not a valid primary key')
            # foreign key
            elif isinstance(field, general_fields.ForeignKeyField):
                #TODO: maybe foreign key should never be None???
                if not isinstance(value, field.foreign_prototype.get_main_type()) and value is not None:
                    raise ValueError('not a valid foreign key')
            # general field
            elif not isinstance(value, field.in_class.type):
                # enum fields are allowed to be assigned None
                if value is None and isinstance(field, general_fields.EnumField):
                    pass
                else:
                    raise ValueError('not a valid value: "{}" for this field: "{}"'.format(value, field))

            # list fields cannot be assigned in this way
            elif isinstance(value, general_fields.ListField):
                raise ValueError('list fields cannot be assigned to')

            setattr(self, field.in_class.name, value)

            if isinstance(self, MorphingThing):
                self.update_affected_fields(field, is_in_the_thing=True)

            if field not in self.modified_fields:
                self.modified_fields.append(field)
            self.modified_signal.emit(field)

    # ===========================================================================
    def __str__(self) -> str:
        return self.name


# ===========================================================================
class MorphingThing(Thing):

    table_name = None

    name = general_fields.NameField(initial_value='morphing thing')
    main_type = general_fields.EnumField(2, general_ui_titles.main_type, 'type', basic_types.ParameterizedEnum, initial_value=None)
    sub_type_1 = general_fields.EnumField(3, general_ui_titles.sub_type_1, 'sub_type_1', basic_types.ParameterizedEnum, initial_value=None)
    sub_type_2 = general_fields.EnumField(3, general_ui_titles.sub_type_2, 'sub_type_2', basic_types.ParameterizedEnum, initial_value=None)
    float_field_1 = general_fields.FloatField(4, general_ui_titles.float_field_1, 'float_parameter_1', -float('inf'), float('inf'), 2, 0)
    float_field_2 = general_fields.FloatField(5, general_ui_titles.float_field_2, 'float_parameter_2', -float('inf'), float('inf'), 2, 0)
    float_field_3 = general_fields.FloatField(6, general_ui_titles.float_field_3, 'float_parameter_3', -float('inf'), float('inf'), 2, 0)
    int_field_1 = general_fields.IntField(7, general_ui_titles.int_field_1, 'int_parameter1', 0, constants_.Constants.MAX_INT, 0)
    int_field_2 = general_fields.IntField(8, general_ui_titles.int_field_2, 'int_parameter2', 0, constants_.Constants.MAX_INT, 0)
    int_field_3 = general_fields.IntField(9, general_ui_titles.int_field_3, 'int_parameter3', 0, constants_.Constants.MAX_INT, 0)
    int_field_4 = general_fields.IntField(10, general_ui_titles.int_field_4, 'int_parameter4', 0, constants_.Constants.MAX_INT, 0)
    int_field_5 = general_fields.IntField(11, general_ui_titles.int_field_5, 'int_parameter5', 0, constants_.Constants.MAX_INT, 0)
    int_field_6 = general_fields.IntField(12, general_ui_titles.int_field_6, 'int_parameter6', 0, constants_.Constants.MAX_INT, 0)
    int_field_7 = general_fields.IntField(13, general_ui_titles.int_field_7, 'int_parameter7', 0, constants_.Constants.MAX_INT, 0)
    int_field_8 = general_fields.IntField(14, general_ui_titles.int_field_8, 'int_parameter8', 0, constants_.Constants.MAX_INT, 0)
    int_field_9 = general_fields.IntField(15, general_ui_titles.int_field_9, 'int_parameter9', 0, constants_.Constants.MAX_INT, 0)

    sub_type_fields = []
    parameter_fields = []

    # ===========================================================================
    def cal_cost(self, morphing_thing):  # for renting
        pass

    # ===========================================================================
    def cal_price(self, morphing_thing):  # for buying
        pass

    # ===========================================================================
    def can_satisfy(self, other_morphing_thing):
        pass

    # ===========================================================================
    def get_affecting_fields(self):
        affecting_fields = []
        class_affecting_fields = [MorphingThing.main_type] + MorphingThing.sub_type_fields
        for class_field in class_affecting_fields:
            # if class_field.is_instance_specific():
            #     affecting_fields.append(self.instance_specific_fields[class_field])
            # else:
            affecting_fields.append(class_field)
        return affecting_fields

    # ===========================================================================
    def get_updated_version_of_sub_type_fields(self):
        updated_affected_fields = dict()

        # get the latest value of type field in editors
        responsible_editor = self.get_responsible_editor(MorphingThing.main_type)
        value = responsible_editor.get_value().value
        if value is not None:
            sub_types = value.get_parameterized_enums()
            for i, affected_field in enumerate(MorphingThing.parameter_fields):

                # create a copy of the field
                updated_affected_field = affected_field.create_copy()

                if i < len(sub_types):
                    new_enum_type = sub_types[i]
                else:
                    new_enum_type = basic_types.ParameterizedEnum

                updated_affected_field.set_enum(new_enum_type)

                # add the updated field to the dict
                updated_affected_fields[affected_field] = updated_affected_field

        return updated_affected_fields

    # ===========================================================================
    def get_updated_version_of_parameter_fields(self):

        updated_parameter_fields = dict()

        new_ui_titles = {}
        value = self.get_responsible_editor(MorphingThing.main_type).get_value().value
        if value is not None:
            new_ui_titles = value.get_parameters_titles()

            if self.get_responsible_editor(MorphingThing.sub_type_1).get_value().value is not None:
                new_ui_titles += self.get_responsible_editor(MorphingThing.sub_type_1).get_value().value.get_parameters_titles()
                if self.get_responsible_editor(MorphingThing.sub_type_2).get_value().value is not None:
                    new_ui_titles += self.get_responsible_editor(MorphingThing.sub_type_2).get_value().value.get_parameters_titles()

        # update ui titles
        for parameter_field in new_ui_titles:
            updated_parameter_field = parameter_field.create_copy()
            updated_parameter_field.set_instance_ui_title(new_ui_titles[parameter_field])
            updated_parameter_field.set_hidden(False)

            updated_parameter_fields[parameter_field] = updated_parameter_field

        return updated_parameter_fields

    # ===========================================================================
    def update_affected_fields(self, affecting_field, is_in_the_thing):

        class_version_of_the_field = self.get_correspondent_class_field(affecting_field)
        if affecting_field in self.get_affecting_fields():

            # main type affecting sub types
            updated_fields = self.get_updated_version_of_sub_type_fields()
            for affected_field in updated_fields.keys():
                if is_in_the_thing:
                    affected_field.force_to_match(updated_fields[affected_field])
                else:
                    responsible_editor = self.get_responsible_editor(affected_field)
                    responsible_editor.update_my_editor_version_of_the_field(updated_fields[affected_field])

            # main type and sub types affecting fields
            updated_fields = self.get_updated_version_of_parameter_fields()
            for affected_field in updated_fields.keys():
                if is_in_the_thing:
                    affected_field.force_to_match(updated_fields[affected_field])
                else:
                    responsible_editor = self.get_responsible_editor(affected_field)
                    responsible_editor.update_my_editor_version_of_the_field(updated_fields[affected_field])


# initializing MorphingThing
MorphingThing.sub_type_fields = [MorphingThing.sub_type_1, MorphingThing.sub_type_2]
MorphingThing.parameter_fields = [
    MorphingThing.float_field_1,
    MorphingThing.float_field_2,
    MorphingThing.float_field_3,
    MorphingThing.int_field_1,
    MorphingThing.int_field_2,
    MorphingThing.int_field_3,
    MorphingThing.int_field_4,
    MorphingThing.int_field_5,
    MorphingThing.int_field_6,
    MorphingThing.int_field_7,
    MorphingThing.int_field_8,
    MorphingThing.int_field_9
]

# for field in MorphingThing.sub_type_fields:
#     field.set_instance_specific(True)
# for field in MorphingThing.parameter_fields:
#     field.set_instance_specific(True)

MorphingThing.float_field_2.set_hidden(True)
MorphingThing.float_field_3.set_hidden(True)
MorphingThing.int_field_4.set_hidden(True)
MorphingThing.int_field_5.set_hidden(True)
MorphingThing.int_field_6.set_hidden(True)
MorphingThing.int_field_7.set_hidden(True)
MorphingThing.int_field_8.set_hidden(True)
MorphingThing.int_field_9.set_hidden(True)


# ===========================================================================
class ListOfThings(QtCore.QObject):
    modified_signal = QtCore.pyqtSignal()

    # ===========================================================================
    def __init__(self, type_):
        QtCore.QObject.__init__(self)

        self._inner_list = []  # type: [type_]
        self._type = type_
        self._is_modified = False
        self.lock = threading.Lock()
        self.editors = []
        self._responsible_editor = None
        self.dependent_editors = []

    # ===========================================================================
    @property
    def type(self):
        if issubclass(self._type, prototype_.Prototype):
            self._type = self._type.get_main_type()
        return self._type

    # ===========================================================================
    @type.setter
    def type(self, value):
        self._type = type

    # ===========================================================================
    def get_responsible_editor(self, field=None):  # signature should be same as method in Thing
        if self._responsible_editor is None:
            self._responsible_editor = prototype_.EditorPrototype.get_main_type().create_responsible_editor(self, None)
        return self._responsible_editor

    # ===========================================================================
    def is_modified(self):
        if self._is_modified:
            return True
        for item in self._inner_list:
            if item.is_modified():
                return True
        return False

    # ===========================================================================
    def set_modified(self):
        self._is_modified = True
        self.modified_signal.emit()

    # ===========================================================================
    def reset_modified(self):
        self._is_modified = False

    # ===========================================================================
    def __iter__(self):
        return self._inner_list.__iter__()

    # ===========================================================================
    def __len__(self):
        return len(self._inner_list)

    # ===========================================================================
    def clear(self):
        if self._inner_list:
            for thing in self._inner_list:
                if self in thing.lists_of_things:
                    index = thing.lists_of_things.index(self)
                    del thing.lists_of_things[index]
            self._inner_list.clear()
            self.set_modified()

    # ===========================================================================
    def __delitem__(self, index):
        if self in self._inner_list[index].lists_of_things:
            index_in_thing = self._inner_list[index].lists_of_things.index(self)
            del self._inner_list[index].lists_of_things[index_in_thing]
        self._inner_list.__delitem__(index)
        self.set_modified()

    # ===========================================================================
    def insert(self, index, value) -> bool:
        if self.type is None:
            self.type = type(value)

        if type(value) is not self.type:
            raise ValueError('cannot inert type "{}" into a list of type "{}".'.format(type(value), self.type))

        if value not in self._inner_list:
            self._inner_list.insert(index, value)
            if self not in value.lists_of_things:
                value.lists_of_things.append(self)

            self.set_modified()
            return True

        return False

    # ===========================================================================
    def append(self, value) -> bool:
        if self.type is None:
            self.type = type(value)

        if type(value) is not self.type:
            raise ValueError('cannot append type "{}" to a list of type "{}".'.format(type(value), self.type))

        if value not in self._inner_list:
            self._inner_list.insert(len(self._inner_list), value)

            self.set_modified()
            return True

        return False

    # ===========================================================================
    def index(self, value):
        return self._inner_list.index(value)

    # ===========================================================================
    def add(self, l):
        for item in l:
            self.append(item)

    # ===========================================================================
    def update_in_database(self):
        updated = True
        for item in self._inner_list:
            if item.is_modified():
                if not item.update_in_database():
                    updated = False
        return updated

    # ===========================================================================
    def __contains__(self, item):
        return self._inner_list.__contains__(item)

    # ===========================================================================
    def __getitem__(self, index):
        return self._inner_list[index]

    # ===========================================================================
    def __setitem__(self, index, value):
        if type(value) is not self.type:
            raise ValueError('cannot set type "{}" in a list of type "{}".'.format(type(value), self.type))
        if value not in self._inner_list:
            if self._inner_list[index]:
                index_of_thing = self._inner_list[index].lists_of_things.index(self)
                del self._inner_list[index].lists_of_things[index_of_thing]
            self._inner_list.__setitem__(index, value)
            if self not in value.lists_of_things:
                value.lists_of_things.append(self)
        else:
            raise ValueError('{} is already in the list'.format(value))


