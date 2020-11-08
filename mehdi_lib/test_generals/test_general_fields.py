from mehdi_lib.generals import general_fields, general_ui_titles, general_editors, general_editors_prototypes, general_initial_values
from mehdi_lib.basics import database_tools
import datetime


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

    # in_class parameters
    assert bool_field.in_class.name == in_class_name
    assert bool_field.in_class.type == bool
    assert bool_field.in_class.initial_value == initial_value

    # in_editor parameters
    assert bool_field.in_editor.editor == general_editors.BoolEditor
    assert bool_field.in_editor.editor_parameters_list is None

    # copy_parameters
    assert bool_field.get_copy_parameters() == [order, bool_field.get_instance_ui_titles(), in_class_name, initial_value]


# ===========================================================================
def test_comment_field():

    # create the field
    comment_field = general_fields.CommentField()

    # in_class parameters
    assert comment_field.in_class.name == 'comment'
    assert comment_field.in_class.type == str
    assert comment_field.in_class.initial_value == general_initial_values.dummy

    # in_database parameters
    assert comment_field.in_database.title == 'comment'
    assert comment_field.in_database.type == database_tools.Database.types[str]
    assert comment_field.in_database.condition is None

    # in_editor parameters
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

    # in_class parameters
    assert datetime_field.in_class.name == in_class_name
    assert datetime_field.in_class.initial_value == initial_value

    # in_editor parameters
    assert datetime_field.in_editor.editor == general_editors.DatetimeEditor
    assert datetime_field.in_editor.editor_parameters_list is None

    # copy_parameters
    assert datetime_field.get_copy_parameters() == [order, datetime_field.get_instance_ui_titles(), in_class_name, initial_value]


# ===========================================================================
def test_date_field():

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

    # in_class parameters
    assert datetime_field.in_class.name == in_class_name
    assert datetime_field.in_class.initial_value == initial_value

    # in_editor parameters
    assert datetime_field.in_editor.editor == general_editors.DatetimeEditor
    assert datetime_field.in_editor.editor_parameters_list is None

    # copy_parameters
    assert datetime_field.get_copy_parameters() == [order, datetime_field.get_instance_ui_titles(), in_class_name, initial_value]


