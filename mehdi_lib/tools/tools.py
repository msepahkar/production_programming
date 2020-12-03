# -*- coding: utf-8 -*-

import os
import glob
import datetime
import parser
import enum
import sys
import importlib

import bcolors as bcolors
from PyQt5 import QtCore


# ===========================================================================
class IndexEnabledDict(QtCore.QObject):
    """
    A new dict which internally has three lists:
    1) keys
    2) values
    3) indexes
    All three lists are correspondent. for example element number three in 'keys' array has its value in the third
    position in 'values' array and th insertion index specified by user at the time of insertion in 'indexes' array.
    User can set any desired insertion index when inserting element. Insertion indexes will be inserted in 'indexes'
    array ordered from smallest to largest. If the specified index is already available the new index will be inserted
    right next to it.
    """

    # ===========================================================================
    def __init__(self):
        super().__init__()
        self._ordered_keys = []
        self._ordered_values = []
        self._ordered_indexes = []

    # ===========================================================================
    def keys(self):
        return self._ordered_keys

    # ===========================================================================
    def values(self):
        return self._ordered_values

    # ===========================================================================
    def insert(self, insertion_index, key, value):
        """
        key will be inserted to its own array in the proper position
        value will be inserted to its own array in the proper position
        insertion index will be inserted to its own array in the proper position
        :param insertion_index:
        :param key:
        :param value:
        :return:
        """

        # find the first place proper for inserting the new insertion index
        actual_insertion_index = 0
        if len(self._ordered_indexes) > 0:
            while actual_insertion_index < len(self._ordered_indexes) and \
                    self._ordered_indexes[actual_insertion_index] <= insertion_index:
                actual_insertion_index += 1

        self._ordered_keys.insert(actual_insertion_index, key)
        self._ordered_values.insert(actual_insertion_index, value)
        self._ordered_indexes.insert(actual_insertion_index, insertion_index)

    # ===========================================================================
    def reorder(self, key, new_insertion_index):
        """
        changes the index of a key in the key array and index of its correspondent value in the value array, and at the
        end the index of its correspondent index in the index array.
        :param key:
        :param new_insertion_index:
        :return:
        """
        current_actual_index = self._ordered_keys.index(key)
        current_insertion_index = self._ordered_indexes[current_actual_index]

        # if the new index is different, remove everything and insert them again
        if current_insertion_index != new_insertion_index:
            value = self._ordered_values[current_actual_index]
            del self._ordered_keys[current_actual_index]
            del self._ordered_values[current_actual_index]
            del self._ordered_indexes[current_actual_index]
            self.insert(new_insertion_index, key, value)

    # ===========================================================================
    def clear(self):
        """
        removes all keys and values
        :return:
        """
        self._ordered_keys.clear()
        self._ordered_values.clear()
        self._ordered_indexes.clear()

    # ===========================================================================
    def __len__(self):
        return len(self._ordered_keys)

    # ===========================================================================
    def __contains__(self, key):
        """
        checks if the key is available
        :param key:
        :return:
        """
        return key in self._ordered_keys

    # ===========================================================================
    def __getitem__(self, key):
        """
        returns the value related to key
        :param key:
        :return:
        """
        index = self._ordered_keys.index(key)
        return self._ordered_values[index]

    # ===========================================================================
    def __delitem__(self, key):
        """
        removes key from the key array and value from the value array
        :param key:
        :return:
        """
        index = self._ordered_keys.index(key)

        del self._ordered_keys[index]
        del self._ordered_values[index]
        del self._ordered_indexes[index]


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
        print(f"{bcolors.FAIL}FATAL ERROR: " + whole_message)
        exit(-1)

    # ===========================================================================
    @staticmethod
    def warning(*messages, sep=' '):
        whole_message = ""
        for message in messages:
            whole_message += message + sep
        print(f'{bcolors.WARN}WARNING: ' + whole_message)

    # ===========================================================================
    @staticmethod
    def find_available_name(path: str, base_name: str, extension: str, greatest_number: bool = False) -> str:
        """
            returns the first available name for a file by adding counter when the file exists

        :param path:
        :param base_name:
        :param extension:
        :param greatest_number:
        :return:
        """
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
            existing_names = os.listdir(path)
            # prepare for extracting existing numbers
            existing_numbers = []
            # iterate through existing names
            for name in existing_names:
                # please remove the name and the extension, only the number is needed
                name = name.replace(base_name + '_', '').replace(extension, '')
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
                # oh! this is also occupied, go further please
                counter += 1
        # Ah! ended at last. return the name
        return base_full_name + str(counter) + extension

    # ===========================================================================
    @staticmethod
    def parse_time_delta(s: str) -> datetime.timedelta:
        """
            converts a string of the form (dd:hh:mm:ss) to a timedelta duration

        :param s:
        :return:
        """

        seconds = 0
        minutes = 0
        hours = 0
        days = 0

        try:
            elements = s.split(':')
            if len(elements) == 1:
                seconds = int(elements[0])
            if len(elements) == 2:
                minutes = int(elements[0])
                seconds = int(elements[1])
            if len(elements) == 3:
                hours = int(elements[0])
                minutes = int(elements[1])
                seconds = int(elements[2])
            if len(elements) == 4:
                days = int(elements[0])
                hours = int(elements[1])
                minutes = int(elements[2])
                seconds = int(elements[3])

            t = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

        except ValueError:
            Tools.warning('cannot parse the time delta:', s)

        return t

    # ===========================================================================
    @staticmethod
    def remove_element_from_list_if_exists(list_, element):
        """
        removes the element from the list_ if it exists in the list.
        it is supposed that the element is not repeated in the list.
        :param list_:
        :param element:
        :return:
        """
        if element in list_:
            index = list_.index(element)
            del list_[index]

    # ===========================================================================
    @staticmethod
    def force_order_in_list_elements(list_, *elements_in_required_order, first_element=None,
                                     one_before_last_element=None, last_element=None):
        """
        Changes the order of specified elements in the list
        :param list_: the list which should be reordered
        :param elements_in_required_order: the order of these elements will be changed if they are in the list but not
        in the specified order
        :param first_element: this element will become the first element of the list (if it is already in the list)
        :param one_before_last_element: this element will be the one before last element (if already in the list)
        :param last_element: this element will be the last element of the list (if already in the list)
        :return:
        """
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

        if first_element is not None and first_element in list_:
            index = list_.index(first_element)
            if index != 0:
                del list_[index]
                list_.insert(0, first_element)

        if last_element is not None and last_element in list_:
            index = list_.index(last_element)
            if index != len(list_) - 1:
                del list_[index]
                list_.append(last_element)

        if one_before_last_element is not None and len(list_) > 1 and one_before_last_element in list_:
            index = list_.index(one_before_last_element)
            if index != len(list_) - 2:
                del list_[index]
                list_.insert(len(list_) - 1, one_before_last_element)

    # ===========================================================================
    @staticmethod
    def parent_type(cls):
        """
        Finds the immediate paret type of a class
        If the class has no parent the return type will be object
        If object is sent as the parameter it will return None
        :param cls:
        :return:
        """
        parents = cls.mro()
        if len(parents) > 1:
            return cls.mro()[1]
        return None

    # ===========================================================================
    @staticmethod
    def add_missing_starting_and_ending_double_quotes(s):
        """
        Double quotes will be added to the beginning and end of the string (if not present).
        :param s:
        :return:
        """
        if type(s) is not str:
            return s
        if not s.startswith('"'): s = '"' + s
        if not s.endswith('"'): s = s + '"'
        return s

    # ===========================================================================
    @staticmethod
    def remove_starting_and_ending_double_quotes(s):
        """
        Double quotes at the beginning and the end of string will be removed.
        :param s:
        :return:
        """
        if type(s) is not str:
            return s
        if s.startswith('"'):
            s = s[1:]
        if s.endswith('"'):
            s = s[:-1]
        return s

    # ===========================================================================
    @staticmethod
    def inheritors(class_):
        subclasses = set()
        work = [class_]
        while work:
            parent = work.pop()
            for child in parent.__subclasses__():
                if child not in subclasses:
                    subclasses.add(child)
                    work.append(child)
        return subclasses