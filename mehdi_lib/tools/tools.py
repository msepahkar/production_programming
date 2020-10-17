# -*- coding: utf-8 -*-

import os
import glob
import datetime
import parser
import enum
import sys
import importlib

from PyQt5 import QtCore


# ===========================================================================
class OrderedDict(QtCore.QObject):

    # ===========================================================================
    def __init__(self):
        super().__init__()
        self._ordered_keys = []
        self._ordered_values = []

    # ===========================================================================
    def keys(self):
        return self._ordered_keys

    # ===========================================================================
    def values(self):
        return self._ordered_values

    # ===========================================================================
    def insert(self, index, key, value):
        self._ordered_keys.insert(index, key)
        self._ordered_values.insert(index, value)

    # ===========================================================================
    def reorder(self, key, new_index):
        current_index = self._ordered_keys.index(key)
        if current_index != new_index:
            value = self._ordered_values[current_index]
            del self._ordered_keys[current_index]
            del self._ordered_values[current_index]
            self._ordered_keys.insert(new_index, key)
            self._ordered_values.insert(new_index, value)

    # ===========================================================================
    def clear(self):
        self._ordered_keys.clear()
        self._ordered_values.clear()

    # ===========================================================================
    def __len__(self):
        return len(self._ordered_keys)

    # ===========================================================================
    def __contains__(self, item):
        return item in self._ordered_keys

    # ===========================================================================
    def __getitem__(self, item):
        index = self._ordered_keys.index(item)
        return self._ordered_values[index]

    # ===========================================================================
    def __delitem__(self, key):
        index = self._ordered_keys.index(key)

        del self._ordered_keys[index]
        del self._ordered_values[index]


# ===========================================================================
class Tools:
    max_allowed_int = 999999999
    date_time_format = "%Y-%m-%d %H:%M:%S"

    # ===========================================================================
    @staticmethod
    def fatal_error(*messages, sep=' '):
        whole_message = ""
        for message in messages:
            whole_message += message + sep
        print("FATAL ERROR: " + whole_message)
        exit(-1)

    # ===========================================================================
    @staticmethod
    def warning(*messages, sep=' '):
        whole_message = ""
        for message in messages:
            whole_message += message + sep
        print('WARNING: ' + whole_message)

    # ===========================================================================
    @staticmethod
    # returns the first available name for a file by adding counter when the file exists
    def find_available_name(path: str, base_name: str, extension: str, greatest_number: bool = False) -> str:
        # prepare base full name
        base_full_name = os.path.join(path, base_name)
        # check for dot
        if extension and not extension.startswith('.'):
            extension = '.' + extension
        # first check for the original name
        if not os.path.exists(base_full_name + extension):
            return base_full_name + extension
        # don't forget the underline
        base_full_name += '_'
        # start with one
        counter = 1
        # should it go to the end?
        if greatest_number:
            # find all existing files
            existing_names = glob.glob(base_full_name + '*')
            # prepare for extracting existing numbers
            existing_numbers = []
            # iterate through existing names
            for name in existing_names:
                # please remove the name and the extension, only the number is needed
                name = name.replace(base_full_name, '').replace(extension, '')
                # pure number is left?
                if name.isdigit():
                    # ok then, we need it
                    existing_numbers.append(int(name))
            # any number found?
            if existing_numbers:
                # go to the end
                counter = max(existing_numbers) + 1
        # just any available number
        else:
            # iterate from the beginning
            while os.path.exists(base_full_name + str(counter) + extension):
                # oh! this is also available, go further please
                counter += 1
        # Ah! ended at last. return the name
        return base_full_name + str(counter) + extension

    # ===========================================================================
    @staticmethod
    # converts a string of the form (hh:mm:ss) to a timedelta duration
    def parse_time_delta(s: str) -> datetime.timedelta:

        t = datetime.timedelta()

        try:
            hours, minutes, seconds, *extra = s.split(':')
            t += datetime.timedelta(hours=int(hours))
            t += datetime.timedelta(minutes=int(minutes))
            t += datetime.timedelta(seconds=int(seconds))

        except ValueError:
            Tools.warning('cannot parse the time delta:', s)

        return t

    # ===========================================================================
    @staticmethod
    # returns values of all static fields (non functions) of a class
    def class_field_values(class_):
        return [getattr(class_, attr) for attr in dir(class_) if
                not callable(getattr(class_, attr)) and not attr.startswith("__")]

    # ===========================================================================
    @staticmethod
    # extracts the value of all fields in Titles call of obj and assigns it to the obj[title] after converting its type
    def extract_fields_from_query(query, obj):
        for title in Tools.class_field_values(obj.Titles):
            val = query.value(query.record().indexOf(obj.database_titles[title]))
            if isinstance(obj.field_types[title], enum.EnumMeta):
                obj[title] = obj.field_types[title](val)
            elif obj.field_types[title] == datetime.datetime:
                obj[title] = parser.parse(val)
            elif obj.field_types[title] == datetime.date:
                obj[title] = parser.parse(val).date()
            else:
                obj[title] = val

    # ===========================================================================
    @staticmethod
    def enum_members(enum_):
        names = []
        for item_name, item_value in enum_.__members__.items():
            names.append(item_name)
        return names

    # ===========================================================================
    @staticmethod
    def find_bases_of_class(cls, bases=None):
        if bases is None:
            bases = []
        if cls.__bases__:
            for c in cls.__bases__:
                if c not in bases:
                    bases.append(c)
                    bases.append(Tools.find_bases_of_class(c, bases))
        return bases

    # ===========================================================================
    @staticmethod
    def remove_element_from_list_if_exists(list_, element):
        if element in list_:
            index = list_.index(element)
            del list_[index]

    # ===========================================================================
    @staticmethod
    def force_order_in_list_elements(list_, *elements_in_required_order, first_element=None, one_before_last_element=None, last_element=None):
        # TODO: does not check existence of elements in the list_
        for i in range(len(elements_in_required_order)):
            if i < len(elements_in_required_order) - 1:
                a = elements_in_required_order[i]
                if a in list_:
                    for j in range(i + 1, len(elements_in_required_order)):
                        b = elements_in_required_order[j]
                        if b in list_:
                            index_a = list_.index(a)
                            index_b = list_.index(b)
                            if index_a > index_b:
                                list_[index_a], list_[index_b] = list_[index_b], list_[index_a]

        if first_element is not None:
            index = list_.index(first_element)
            if index != 0:
                del list_[index]
                list_.insert(0, first_element)

        if last_element is not None:
            index = list_.index(last_element)
            if index != len(list_) - 1:
                del list_[index]
                list_.append(last_element)

        if one_before_last_element is not None and len(list_) > 1:
            index = list_.index(one_before_last_element)
            if index != len(list_) - 2:
                del list_[index]
                list_.insert(len(list_) - 1, one_before_last_element)

    # ===========================================================================
    @staticmethod
    def get_class(class_name):

        # first modules
        modules = []
        for module in sys.modules:
            modules.append(module)

        # now the class
        for module in modules:
            imported_module = importlib.import_module(module)
            if class_name in dir(sys.modules[module]):
                return getattr(imported_module, class_name)

        return None

    # ===========================================================================
    @staticmethod
    def get_current_module(module_name):
        return sys.modules[module_name]

    # ===========================================================================
    @staticmethod
    def parent_type(cls):
        return cls.mro()[1]

    # ===========================================================================
    @staticmethod
    def add_missing_starting_and_ending_double_quotes(s):
        if type(s) is not str:
            return s
        if not s.startswith('"'): s = '"' + s
        if not s.endswith('"'): s = s + '"'
        return s

    # ===========================================================================
    @staticmethod
    def remove_starting_and_ending_double_quotes(s):
        if type(s) is not str:
            return s
        if s.startswith('"'): s = s[1:]
        if s.endswith('"'): s = s[:-1]
        return s

