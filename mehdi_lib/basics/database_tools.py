# -*- coding: utf-8 -*-

import datetime
from mehdi_lib.basics import basic_types
from mehdi_lib.tools import tools

import dateutil.parser
from PyQt5 import QtSql

from mehdi_lib.tools import tools


# ===========================================================================
class Database:
    # noinspection PyCallByClass,PyTypeChecker,SpellCheckingInspection
    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName('./db.sqlite')
    reserved_words = [
        "ABORT",
        "ACTION",
        "ADD",
        "AFTER",
        "ALL",
        "ALTER",
        "ANALYZE",
        "AND",
        "AS",
        "ASC",
        "ATTACH",
        "AUTOINCREMENT",
        "BEFORE",
        "BEGIN",
        "BETWEEN",
        "BY",
        "CASCADE",
        "CASE",
        "CAST",
        "CHECK",
        "COLLATE",
        "COLUMN",
        "COMMIT",
        "CONFLICT",
        "CONSTRAINT",
        "CREATE",
        "CROSS",
        "CURRENT_DATE",
        "CURRENT_TIME",
        "CURRENT_TIMESTAMP",
        "DATABASE",
        "DEFAULT",
        "DEFERRABLE",
        "DEFERRED",
        "DELETE",
        "DESC",
        "DETACH",
        "DISTINCT",
        "DROP",
        "EACH",
        "ELSE",
        "END",
        "ESCAPE",
        "EXCEPT",
        "EXCLUSIVE",
        "EXISTS",
        "EXPLAIN",
        "FAIL",
        "FOR",
        "FOREIGN",
        "FROM",
        "FULL",
        "GLOB",
        "GROUP",
        "HAVING",
        "IF",
        "IGNORE",
        "IMMEDIATE",
        "IN",
        "INDEX",
        "INDEXED",
        "INITIALLY",
        "INNER",
        "INSERT",
        "INSTEAD",
        "INTERSECT",
        "INTO",
        "IS",
        "ISNULL",
        "JOIN",
        "KEY",
        "LEFT",
        "LIKE",
        "LIMIT",
        "MATCH",
        "NATURAL",
        "NO",
        "NOT",
        "NOTNULL",
        "NULL",
        "OF",
        "OFFSET",
        "ON",
        "OR",
        "ORDER",
        "OUTER",
        "PLAN",
        "PRAGMA",
        "PRIMARY",
        "QUERY",
        "RAISE",
        "RECURSIVE",
        "REFERENCES",
        "REGEXP",
        "REINDEX",
        "RELEASE",
        "RENAME",
        "REPLACE",
        "RESTRICT",
        "RIGHT",
        "ROLLBACK",
        "ROW",
        "SAVEPOINT",
        "SELECT",
        "SET",
        "TABLE",
        "TEMP",
        "TEMPORARY",
        "THEN",
        "TO",
        "TRANSACTION",
        "TRIGGER",
        "UNION",
        "UNIQUE",
        "UPDATE",
        "USING",
        "VACUUM",
        "VALUES",
        "VIEW",
        "VIRTUAL",
        "WHEN",
        "WHERE",
        "WITH",
        "WITHOUT",
    ]
    types = {
        str: "VARCHAR",
        int: "INTEGER",
        float: "REAL",
        datetime.date: "DATETIME",
        datetime.datetime: "DATETIME",
        datetime.timedelta: "DATETIME",
        bool: "INTEGER",
        basic_types.UiTitleEnabledEnum: "INTEGER"
    }


# ===========================================================================
class Types:

    enum_None_in_database = -1
    date_and_datetime_format_string = '{}'
    time_delta_format_string = '{}:{}:{}'
    date_strftime_format_string = '%Y/%m/%d'
    datetime_strftime_format_string = '%Y/%m/%d %H:%M:%S'

    # ===========================================================================
    @staticmethod
    def format_for_database(value, type_in_class):
        """
        formats the value parameter to a suitable format for writing into database.

        :param value: the input parameter
        :param type_in_class: type of the input parameter in the class
        :return: converted form of the input value suitable for writing into database
        """
        if type_in_class == bool:
            if value:
                return 1
            else:
                return 0
        if type_in_class is str:
            new_value = tools.Tools.add_missing_starting_and_ending_double_quotes(value)
            return new_value
        if type_in_class is basic_types.MultilingualString:
            return value[basic_types.Language.get_active_language()]
        if type_in_class is datetime.date:
            new_value = value.strftime(Types.date_strftime_format_string)
            new_value = tools.Tools.add_missing_starting_and_ending_double_quotes(new_value)
            return new_value
        if type_in_class is datetime.datetime:
            new_value = value.strftime(Types.datetime_strftime_format_string)
            new_value = tools.Tools.add_missing_starting_and_ending_double_quotes(new_value)
            return new_value
        if issubclass(type_in_class, basic_types.UiTitleEnabledEnum):
            if value is None:
                return Types.enum_None_in_database
            return value.value
        if type_in_class == datetime.timedelta:
            hours = value.seconds // 3600 + value.days * 24
            minutes = (value.seconds // 60) % 60
            seconds = value.seconds % 60
            new_value = Types.time_delta_format_string.format(hours, minutes, seconds)
            new_value = tools.Tools.add_missing_starting_and_ending_double_quotes(new_value)
            return new_value

        return value

    # ===========================================================================
    @staticmethod
    def format_for_class(value, type_in_class):
        """
        the reverse of format_for_database function. converts the input value read from database to proper value to be
        saved in the class
        :param value: the input value (read from database)
        :param type_in_class: type of the input value in the class
        :return: converted value to be saved in the class
        """
        new_value = value

        if type_in_class is bool:
            if value:
                new_value = True
            else:
                new_value = False

        if issubclass(type_in_class, basic_types.UiTitleEnabledEnum):
            if value == Types.enum_None_in_database:
                new_value = None
            else:
                new_value = type_in_class(value)
        if type_in_class is datetime.datetime:
            new_value = tools.Tools.remove_starting_and_ending_double_quotes(value)
            new_value = dateutil.parser.parse(new_value)
        if type_in_class is datetime.date:
            new_value = tools.Tools.remove_starting_and_ending_double_quotes(value)
            new_value = dateutil.parser.parse(new_value).date()

        if type_in_class is datetime.timedelta:
            try:
                new_value = tools.Tools.remove_starting_and_ending_double_quotes(value)
                hours, minutes, seconds, *extra = new_value.split(':')
                hours = int(hours)
                minutes = int(minutes)
                seconds = int(seconds)
                # noinspection PyCallingNonCallable
                new_value = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
            except ValueError:
                raise ValueError('problem converting "{}" to timedelta'.format(value))
        if type_in_class is basic_types.MultilingualString:
            new_value = basic_types.MultilingualString({basic_types.Language.get_active_language(): value})

        return new_value


# ===========================================================================
class Conditions:
    not_null = "NOT NULL"
    unique = "UNIQUE"
    unique_not_null = "UNIQUE NOT NULL"
    primary_key = "PRIMARY KEY UNIQUE NOT NULL"
    primary_key_auto = "PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL"
    no_condition = ""


# ===========================================================================
class Commands:
    # ===========================================================================
    @staticmethod
    def exec_query(command: str) -> QtSql.QSqlQuery:
        if not Database.db:
            tools.Tools.warning('no database is specified')
            # noinspection PyTypeChecker
            return None
        if not Database.db.isOpen():
            if not Database.db.open():
                tools.Tools.warning('cannot open the database')
                # noinspection PyTypeChecker
                return None

        query = QtSql.QSqlQuery()
        if not query.exec(command):
            tools.Tools.warning('database query error:', query.lastError().text(), '\n', command)
            # noinspection PyTypeChecker
            return None

        return query


