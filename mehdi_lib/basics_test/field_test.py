import pytest
from mehdi_lib.basics import field_, database_tools, thing_
from mehdi_lib.generals import general_editors
from mehdi_lib.tools import tools


pytest_mark = pytest.mark.field_


def test_InClass():
    in_class_1 = field_.InClass('test', str, 'initial')
    in_class_2 = field_.InClass('test', str, 'initial')
    in_class_3 = field_.InClass('test1', str, 'initial')
    in_class_4 = field_.InClass('test', int, 'initial')
    in_class_5 = field_.InClass('test', str, 'initial1')
    in_class_6 = in_class_1.create_copy()

    assert in_class_1.matches(in_class_2)
    assert in_class_1.matches(in_class_6)
    assert not in_class_1.matches(in_class_3)
    assert not in_class_1.matches(in_class_4)
    assert not in_class_1.matches(in_class_5)
    in_class_3.force_to_match(in_class_1)
    assert in_class_1.matches(in_class_3)
    in_class_4.force_to_match(in_class_1)
    assert in_class_1.matches(in_class_4)
    in_class_5.force_to_match(in_class_1)
    assert in_class_1.matches(in_class_5)


def test_InDatabase():
    in_database_1 = field_.InDatabase('test', database_tools.Database.types[str], '0', 'unique')
    in_database_2 = field_.InDatabase('test', database_tools.Database.types[str], '0', 'unique')
    in_database_3 = field_.InDatabase('test1', database_tools.Database.types[str], '0', 'unique')
    in_database_4 = field_.InDatabase('test', database_tools.Database.types[int], '0', 'unique')
    in_database_5 = field_.InDatabase('test', database_tools.Database.types[str], '1', 'unique')
    in_database_6 = field_.InDatabase('test', database_tools.Database.types[str], '0', 'primary')
    in_database_7 = in_database_1.create_copy()
    assert in_database_1.matches(in_database_2)
    assert not in_database_1.matches(in_database_3)
    assert not in_database_1.matches(in_database_4)
    assert not in_database_1.matches(in_database_5)
    assert not in_database_1.matches(in_database_6)
    assert in_database_1.matches(in_database_7)
    assert in_database_1.get_creation_command() == "test {} unique DEFAULT 0".format(database_tools.Database.types[str])


def test_InEditor():
    in_editor_1 = field_.InEditor(general_editors.FloatEditor)
    in_editor_2 = field_.InEditor(general_editors.FloatEditor)
    in_editor_3 = field_.InEditor(general_editors.BoolEditor)
    in_editor_4 = in_editor_1.create_copy()
    assert in_editor_1.matches(in_editor_2)
    assert not in_editor_1.matches(in_editor_3)
    in_editor_3.force_to_match(in_editor_1)
    assert in_editor_1.matches(in_editor_3)
    assert in_editor_1.matches(in_editor_4)


