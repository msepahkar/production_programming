from mehdi_lib.generals import general_fields, general_ui_titles, general_editors, general_editors_prototypes, \
    general_initial_values, general_things_prototypes, general_things
from mehdi_lib.basics import database_tools, basic_types, field_, prototype_, thing_
from mehdi_lib.tools import tools
import datetime
import pytest


pytestmark = pytest.mark.generals


# ===========================================================================
def test_bool_field():
    # parameters
    in_class_name = 'bool_field_1'
    initial_value = 'initial'
    order = 10

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
    assert bool_field.get_copy_parameters() == [order, bool_field.get_ui_title(), in_class_name,
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
    order = 10
    ui_titles = general_ui_titles.dummy
    in_class_name = 'date_time'
    initial_value = datetime.datetime(2000, 1, 1)

    # create the field
    datetime_field = general_fields.DatetimeField(order, ui_titles, in_class_name, initial_value)

    # general parameters
    assert datetime_field.order == order
    assert datetime_field.get_ui_title() == ui_titles

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
    order = 10
    ui_titles = general_ui_titles.dummy
    in_class_name = 'date_time'
    initial_value = datetime.date(2000, 1, 1)

    # create the field
    date_field = general_fields.DateField(order, ui_titles, in_class_name, initial_value)

    # general parameters
    assert date_field.order == order
    assert date_field.get_ui_title() == ui_titles

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
    order = 10
    ui_titles = general_ui_titles.dummy
    in_class_name = 'duration'
    initial_value = datetime.timedelta(12)

    # create the field
    duration_field = general_fields.DurationField(order, ui_titles, in_class_name, initial_value)

    # general parameters
    assert duration_field.order == order
    assert duration_field.get_ui_title() == ui_titles

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

    order = 10
    ui_titles = general_ui_titles.dummy
    in_class_name = 'duration'
    initial_value = TestingEnum.value_1

    # create the field
    enum_field = general_fields.EnumField(order, ui_titles, in_class_name, TestingEnum, initial_value)

    # general parameters
    assert enum_field.order == order
    assert enum_field.get_ui_title() == ui_titles

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
    assert file_name_field.get_ui_title() == general_ui_titles.file_name

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
    assert file_path_field.get_ui_title() == general_ui_titles.file_path

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
    order = 10
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
    assert float_field.get_ui_title() == ui_titles

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
    
    # parameters
    order = 10
    ui_titles = general_ui_titles.dummy
    in_class_name = 'foreign_key'
    referencing_prototype = general_things_prototypes.DummyPrototype
    foreign_prototype = general_things_prototypes.DummyPrototype2
    in_editor = field_.InEditor(general_editors.DummyEditor)

    # create the field
    foreign_key_field = general_fields.ForeignKeyField(order, ui_titles, in_class_name, referencing_prototype,
                                                       foreign_prototype, in_editor)

    # general parameters
    assert foreign_key_field.order == order
    assert foreign_key_field.get_ui_title() == ui_titles
    assert foreign_key_field.referencing_prototype == referencing_prototype
    assert referencing_prototype in foreign_prototype.referencing_prototypes()

    # in_class
    assert foreign_key_field.in_class.name == in_class_name
    assert foreign_key_field.in_class.type == foreign_prototype.get_main_type()
    assert foreign_key_field.in_class.initial_value is None

    # in_database
    assert foreign_key_field.in_database.title == in_class_name
    assert foreign_key_field.in_database.type == database_tools.Database.types[int]
    assert foreign_key_field.in_database.default_value is None
    assert foreign_key_field.in_database.condition == database_tools.Conditions.not_null

    # in_editor
    assert foreign_key_field.in_editor.editor == general_editors.DummyEditor
    assert foreign_key_field.in_editor.editor_parameters_list is None

    # copy parameters
    assert foreign_key_field.get_copy_parameters()[:-1] == [order, ui_titles, in_class_name,
                                                       referencing_prototype, foreign_prototype]
    assert foreign_key_field.get_copy_parameters()[-1].editor == in_editor.editor
    assert foreign_key_field.get_copy_parameters()[-1].editor_parameters_list is None


# ===========================================================================
def test_foreign_thing_selector_field():

    # parameters
    order = 10
    ui_titles = general_ui_titles.dummy
    in_class_name = 'foreign_thing_selector'
    referencing_prototype = general_things_prototypes.DummyPrototype
    thing_prototype = general_things_prototypes.DummyPrototype2

    # create the field
    foreign_thing_selector_field = general_fields.ForeignThingSelectorField(order, ui_titles, in_class_name,
                                                                            referencing_prototype, thing_prototype)

    # general parameters
    assert foreign_thing_selector_field.order == order
    assert foreign_thing_selector_field.get_ui_title() == ui_titles
    assert foreign_thing_selector_field.referencing_prototype == referencing_prototype

    # in_class
    assert foreign_thing_selector_field.in_class.name == in_class_name
    assert foreign_thing_selector_field.in_class.type == thing_prototype.get_main_type()
    assert foreign_thing_selector_field.in_class.initial_value is None

    # in_database
    assert foreign_thing_selector_field.in_database.title == in_class_name
    assert foreign_thing_selector_field.in_database.type == database_tools.Database.types[int]
    assert foreign_thing_selector_field.in_database.default_value is None
    assert foreign_thing_selector_field.in_database.condition == database_tools.Conditions.not_null

    # in_editor
    assert foreign_thing_selector_field.in_editor.editor == general_editors.SingleItemSelectorEditor
    assert foreign_thing_selector_field.in_editor.editor_parameters_list is None

    # copy parameters
    assert foreign_thing_selector_field.get_copy_parameters() == [order, ui_titles, in_class_name,
                                                                  referencing_prototype, thing_prototype]


# ===========================================================================
def test_int_field():

    # parameters
    order = 10
    ui_titles = general_ui_titles.dummy
    in_class_name = 'int_field'
    bottom = 1
    top = 100
    initial_value = 50

    # create the field
    int_field = general_fields.IntField(order, ui_titles, in_class_name, bottom, top, initial_value)

    # general parameters
    assert int_field.order == order
    assert int_field.get_ui_title() == ui_titles

    # in_class
    assert int_field.in_class.name == in_class_name
    assert int_field.in_class.type == int
    assert int_field.in_class.initial_value == initial_value

    # in_database
    assert int_field.in_database.title == in_class_name
    assert int_field.in_database.type == database_tools.Database.types[int]
    assert int_field.in_database.default_value == database_tools.Types.format_for_database(initial_value, int)
    assert int_field.in_database.condition == database_tools.Conditions.not_null

    # in_editor
    assert int_field.in_editor.editor == general_editors.IntEditor
    assert int_field.in_editor.editor_parameters_list == [bottom, top]

    # copy parameters
    int_field.get_copy_parameters() == [order, ui_titles, in_class_name, bottom, top, initial_value]


# ===========================================================================
def test_list_field():

    # parameters
    order = 10
    ui_titles = general_ui_titles.dummy
    in_class_name = 'list_field'
    element_type = general_things.DummyThing
    in_editor = field_.InEditor(general_editors.DummyEditor)

    # create the field
    list_field = general_fields.ListField(order, ui_titles, in_class_name, element_type, in_editor)

    # general parameters
    assert list_field.order == order
    assert list_field.get_ui_title() == ui_titles

    # in_class
    assert list_field.in_class.name == in_class_name
    assert list_field.in_class.type == thing_.ListOfThings
    assert list_field.in_class.initial_value == element_type

    # in_database
    assert list_field.in_database is None

    # in_editor
    assert list_field.in_editor.editor == general_editors.DummyEditor
    assert list_field.in_editor.editor_parameters_list is None

    # copy parameters
    assert list_field.get_copy_parameters()[:-1] == [order, ui_titles, in_class_name, element_type]
    assert list_field.get_copy_parameters()[-1].editor == general_editors.DummyEditor
    assert list_field.get_copy_parameters()[-1].editor_parameters_list is None


# ===========================================================================
def test_name_field():

    # parameters
    ui_titles = general_ui_titles.name
    in_class_name = 'name'
    initial_value = 'name'

    # create the field
    name_field = general_fields.NameField(initial_value)

    # general parameters
    assert name_field.order == 0
    assert name_field.get_ui_title() == ui_titles

    # in_class
    assert name_field.in_class.name == in_class_name
    assert name_field.in_class.type == str
    assert name_field.in_class.initial_value == initial_value

    # in_database
    assert name_field.in_database.title == in_class_name
    assert name_field.in_database.type == database_tools.Database.types[str]
    assert name_field.in_database.default_value == database_tools.Types.format_for_database(initial_value, str)
    assert name_field.in_database.condition == database_tools.Conditions.not_null

    # in_editor
    assert name_field.in_editor.editor == general_editors.NameEditor
    assert name_field.in_editor.editor_parameters_list is None


# ===========================================================================
def test_order_number_field():

    # create the field
    order_number_field = general_fields.OrderNumberField()

    # general parameters
    assert order_number_field.order == 0
    assert order_number_field.get_ui_title() == general_ui_titles.order_number

    # in_class
    assert order_number_field.in_class.name == 'order_number'
    assert order_number_field.in_class.type == int
    assert order_number_field.in_class.initial_value == 0

    # in_database
    assert order_number_field.in_database.title == 'order_number'
    assert order_number_field.in_database.type == database_tools.Database.types[int]
    assert order_number_field.in_database.default_value is None
    assert order_number_field.in_database.condition == database_tools.Conditions.not_null

    # in_editor
    assert order_number_field.in_editor.editor == general_editors.IntEditor
    assert order_number_field.in_editor.editor_parameters_list == [0, tools.Tools.max_allowed_int]


# ===========================================================================
def test_percent_field():

    # parameters
    order = 10
    ui_titles = general_ui_titles.dummy
    in_class_name = 'percent_field'
    initial_value = 50

    # create the field
    percent_field = general_fields.PercentField(order, ui_titles, in_class_name, initial_value)

    # general parameters
    assert percent_field.order == order
    assert percent_field.get_ui_title() == ui_titles

    # in_class
    assert percent_field.in_class.name == in_class_name
    assert percent_field.in_class.type == int
    assert percent_field.in_class.initial_value == initial_value

    # in_database
    assert percent_field.in_database.title == in_class_name
    assert percent_field.in_database.type == database_tools.Database.types[int]
    assert percent_field.in_database.default_value == database_tools.Types.format_for_database(initial_value, int)
    assert percent_field.in_database.condition == database_tools.Conditions.not_null

    # in_editor
    assert percent_field.in_editor.editor == general_editors.IntEditor
    assert percent_field.in_editor.editor_parameters_list == [0, 100]

    # copy parameters
    percent_field.get_copy_parameters() == [order, ui_titles, in_class_name, initial_value]


# ===========================================================================
def test_primary_key_field():

    # create the field
    primary_key_field = general_fields.PrimaryKeyField()

    # general parameters
    assert primary_key_field.order == 0
    assert primary_key_field.get_ui_title() == general_ui_titles.dummy

    # in_class
    assert primary_key_field.in_class.name == 'id'
    assert primary_key_field.in_class.type == int
    assert primary_key_field.in_class.initial_value is None

    # in_database
    assert primary_key_field.in_database.title == 'id'
    assert primary_key_field.in_database.type == database_tools.Database.types[int]
    assert primary_key_field.in_database.default_value is None
    assert primary_key_field.in_database.condition == database_tools.Conditions.primary_key_auto

    # in_editor
    assert primary_key_field.in_editor is None


