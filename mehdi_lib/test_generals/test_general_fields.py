from mehdi_lib.generals import general_fields, general_ui_titles, general_editors, general_editors_prototypes, \
    general_initial_values
from mehdi_lib.basics import database_tools, basic_types
import datetime
import pytest

pytest_mark = pytest.mark.general_fields


# ===========================================================================
def test_bool_field():
    # parameters
    in_class_name = 'bool_field_1'
    initial_value = 'initial'
    order = 0

    # create the field
    bool_field = general_fields.BoolField(order, general_ui_titles.dummy, in_class_name, initial_value)

    # general parameters
    assert bool_field.order == order

    # in_class
    assert bool_field.in_class.name == in_class_name
    assert bool_field.in_class.type == bool
    assert bool_field.in_class.initial_value == initial_value

    # in_database
    assert bool_field.in_database.title == in_class_name
    assert bool_field.in_database.type == database_tools.Database.types[bool]
    assert bool_field.in_database.default_value == database_tools.Types.format_for_database(initial_value, bool)
    assert bool_field.in_database.condition == database_tools.Conditions.not_null

    # in_editor
    assert bool_field.in_editor.editor == general_editors.BoolEditor
    assert bool_field.in_editor.editor_parameters_list is None

    # copy_parameters
    assert bool_field.get_copy_parameters() == [order, bool_field.get_instance_ui_titles(), in_class_name,
                                                initial_value]


# ===========================================================================
def test_comment_field():
    # create the field
    comment_field = general_fields.CommentField()

    # in_class
    assert comment_field.in_class.name == 'comment'
    assert comment_field.in_class.type == str
    assert comment_field.in_class.initial_value == general_initial_values.dummy

    # in_database
    assert comment_field.in_database.title == 'comment'
    assert comment_field.in_database.type == database_tools.Database.types[str]
    assert comment_field.in_database.default_value == database_tools.Types.format_for_database('', str)
    assert comment_field.in_database.condition is None

    # in_editor
    assert comment_field.in_editor.editor == general_editors.CommentEditor
    assert comment_field.in_editor.editor_parameters_list is None


# ===========================================================================
def test_datetime_field():
    # parameters
    order = 0
    ui_titles = general_ui_titles.dummy
    in_class_name = 'date_time'
    initial_value = datetime.datetime(2000, 1, 1)

    # create the field
    datetime_field = general_fields.DatetimeField(order, ui_titles, in_class_name, initial_value)

    # general parameters
    assert datetime_field.order == order
    assert datetime_field.get_instance_ui_titles() == ui_titles

    # in_class
    assert datetime_field.in_class.name == in_class_name
    assert datetime_field.in_class.initial_value == initial_value

    # in_database
    assert datetime_field.in_database.title == in_class_name
    assert datetime_field.in_database.type == database_tools.Database.types[datetime.datetime]
    assert datetime_field.in_database.default_value == database_tools.Types.format_for_database(initial_value, datetime.datetime)
    assert datetime_field.in_database.condition == database_tools.Conditions.not_null

    # in_editor
    assert datetime_field.in_editor.editor == general_editors.DatetimeEditor
    assert datetime_field.in_editor.editor_parameters_list is None

    # copy_parameters
    assert datetime_field.get_copy_parameters() == [order, ui_titles, in_class_name, initial_value]


# ===========================================================================
def test_date_field():
    # parameters
    order = 0
    ui_titles = general_ui_titles.dummy
    in_class_name = 'date_time'
    initial_value = datetime.date(2000, 1, 1)

    # create the field
    date_field = general_fields.DateField(order, ui_titles, in_class_name, initial_value)

    # general parameters
    assert date_field.order == order
    assert date_field.get_instance_ui_titles() == ui_titles

    # in_class
    assert date_field.in_class.name == in_class_name
    assert date_field.in_class.initial_value == initial_value

    # in_database
    assert date_field.in_database.title == in_class_name
    assert date_field.in_database.type == database_tools.Database.types[datetime.date]
    assert date_field.in_database.default_value == database_tools.Types.format_for_database(initial_value, datetime.date)
    assert date_field.in_database.condition == database_tools.Conditions.not_null

    # in_editor
    assert date_field.in_editor.editor == general_editors.DateEditor
    assert date_field.in_editor.editor_parameters_list is None

    # copy_parameters
    assert date_field.get_copy_parameters() == [order, ui_titles, in_class_name, initial_value]


# ===========================================================================
def test_duration_field():
    order = 0
    ui_titles = general_ui_titles.dummy
    in_class_name = 'duration'
    initial_value = datetime.timedelta(12)

    # create the field
    duration_field = general_fields.DurationField(order, ui_titles, in_class_name, initial_value)

    # general parameters
    assert duration_field.order == order
    assert duration_field.get_instance_ui_titles() == ui_titles

    # in_class 
    assert duration_field.in_class.name == in_class_name
    assert duration_field.in_class.initial_value == initial_value

    # in_database
    assert duration_field.in_database.title == in_class_name
    assert duration_field.in_database.type == database_tools.Database.types[datetime.timedelta]
    assert duration_field.in_database.default_value == database_tools.Types.format_for_database(initial_value, datetime.timedelta)
    assert duration_field.in_database.condition == database_tools.Conditions.not_null

    # in_editor 
    assert duration_field.in_editor.editor == general_editors.DurationEditor
    assert duration_field.in_editor.editor_parameters_list is None

    # copy parameters
    assert duration_field.get_copy_parameters() == [order, ui_titles, in_class_name, initial_value]


# ===========================================================================
def test_enum_field():

    class TestingEnum(basic_types.UiTitleEnabledEnum):
        value_1 = 1
        value_2 = 2

    class TestingEnum2(basic_types.UiTitleEnabledEnum):
        value_1 = 1
        value_2 = 2

    class SignalChecker:
        def __init__(self):
            self.signal_emitted = False
        def signal_emitted_handler(self):
            self.signal_emitted = True

    order = 0
    ui_titles = general_ui_titles.dummy
    in_class_name = 'duration'
    initial_value = TestingEnum.value_1

    # create the field
    enum_field = general_fields.EnumField(order, ui_titles, in_class_name, TestingEnum, initial_value)

    # general parameters
    assert enum_field.order == order
    assert enum_field.get_instance_ui_titles() == ui_titles

    # in_class 
    assert enum_field.in_class.name == in_class_name
    assert enum_field.in_class.initial_value == initial_value

    # in_database
    assert enum_field.in_database.title == in_class_name
    assert enum_field.in_database.type == database_tools.Database.types[basic_types.UiTitleEnabledEnum]
    assert enum_field.in_database.default_value == database_tools.Types.format_for_database(initial_value, TestingEnum)
    assert enum_field.in_database.condition == database_tools.Conditions.not_null

    # in_editor 
    assert enum_field.in_editor.editor == general_editors.EnumItemSelectorEditor
    assert enum_field.in_editor.editor_parameters_list == [TestingEnum]

    # copy parameters
    assert enum_field.get_copy_parameters() == [order, ui_titles, in_class_name, TestingEnum, initial_value]

    # enum changed signal
    signal_checker = SignalChecker()
    enum_field.enum_changed_signal.connect(signal_checker.signal_emitted_handler)

    # other enum
    enum_field_2 = general_fields.EnumField(order, ui_titles, in_class_name, TestingEnum2, initial_value)
    enum_field.force_to_match(enum_field_2)
    assert enum_field.in_class.type == TestingEnum2
    assert signal_checker.signal_emitted

    # set enum
    signal_checker.signal_emitted = False
    enum_field.set_enum(TestingEnum)
    assert enum_field.in_class.type == TestingEnum
    assert signal_checker.signal_emitted


# ===========================================================================
def test_file_name_field():

    # parameters
    initial_value = 'initial'

    # create the field
    file_name_field = general_fields.FileNameField(initial_value)

    # general parameters
    assert file_name_field.order == 0
    assert file_name_field.get_instance_ui_titles() == general_ui_titles.file_name

    # in_class
    assert file_name_field.in_class.name == 'file_name'
    assert file_name_field.in_class.type == str
    assert file_name_field.in_class.initial_value == initial_value

    # in_database
    assert file_name_field.in_database.title == 'file_name'
    assert file_name_field.in_database.type == database_tools.Database.types[str]
    assert file_name_field.in_database.default_value == database_tools.Types.format_for_database(initial_value, str)
    assert file_name_field.in_database.condition == database_tools.Conditions.not_null

    # in_editor
    assert file_name_field.in_editor.editor == general_editors.FileNameEditor
    assert file_name_field.in_editor.editor_parameters_list is None

    # copy parameters
    assert file_name_field.get_copy_parameters() == [initial_value]


# ===========================================================================
def test_file_path_field():

    # parameters
    initial_value = 'initial'

    # create the field
    file_path_field = general_fields.FilePathField(initial_value)

    # general parameters
    assert file_path_field.order == 0
    assert file_path_field.get_instance_ui_titles() == general_ui_titles.file_path

    # in_class
    assert file_path_field.in_class.name == 'file_path'
    assert file_path_field.in_class.type == str
    assert file_path_field.in_class.initial_value == initial_value

    # in_database
    assert file_path_field.in_database.title == 'file_path'
    assert file_path_field.in_database.type == database_tools.Database.types[str]
    assert file_path_field.in_database.default_value == database_tools.Types.format_for_database(initial_value, str)
    assert file_path_field.in_database.condition == database_tools.Conditions.not_null

    # in_editor
    assert file_path_field.in_editor.editor == general_editors.FilePathEditor
    assert file_path_field.in_editor.editor_parameters_list is None

    # copy parameters
    assert file_path_field.get_copy_parameters() == [initial_value]


# ===========================================================================
def test_float_field():

    # parameters
    order = 0
    ui_titles = general_ui_titles.dummy
    in_class_name = 'float_field'
    bottom = 1.5
    top = 99.5
    decimals = 1
    initial_value = 2.3

    # create the field
    float_field = general_fields.FloatField(order, ui_titles, in_class_name, bottom, top, decimals, initial_value)

    # general parameters
    assert float_field.order == order
    assert float_field.get_instance_ui_titles() == ui_titles

    # in_class
    assert float_field.in_class.name == in_class_name
    assert float_field.in_class.type == float
    assert float_field.in_class.initial_value == initial_value

    # in_database
    assert float_field.in_database.title == in_class_name
    assert float_field.in_database.type == database_tools.Database.types[float]
    assert float_field.in_database.default_value == database_tools.Types.format_for_database(initial_value, float)
    assert float_field.in_database.condition == database_tools.Conditions.not_null

    # in_editor
    assert float_field.in_editor.editor == general_editors.FloatEditor
    assert float_field.in_editor.editor_parameters_list == [bottom, top, decimals]

    # copy parameters
    assert float_field.get_copy_parameters() == [order, ui_titles, in_class_name, bottom, top, decimals, initial_value]


# ===========================================================================
def test_foreign_key_field():
    pass

