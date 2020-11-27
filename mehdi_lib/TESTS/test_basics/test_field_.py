import pytest
from mehdi_lib.basics import field_, database_tools, thing_
from mehdi_lib.generals import general_editors


pytestmark = pytest.mark.basics


# ===========================================================================
def test_InClass():
    """Testing the InClass class"""
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


# ===========================================================================
def test_InDatabase():
    """Testing the InDatabase class"""
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


# ===========================================================================
def test_InEditor():
    """Testing the InEditor class"""
    parameters_list = [thing_.Thing(), field_.Field(0, [], None, None, None), False, None]
    in_editor_1 = field_.InEditor(general_editors.FloatEditor, parameters_list)
    in_editor_2 = field_.InEditor(general_editors.FloatEditor, parameters_list)
    in_editor_3 = field_.InEditor(general_editors.BoolEditor, parameters_list)
    in_editor_4 = field_.InEditor(general_editors.FloatEditor, [thing_.Thing()] + parameters_list[1:])
    in_editor_5 = field_.InEditor(general_editors.FloatEditor, parameters_list[0:1] + [field_.Field(0, [], None, None, None)] + parameters_list[2:])
    in_editor_6 = field_.InEditor(general_editors.FloatEditor, parameters_list[0:2] + [True] + parameters_list[3:])
    in_editor_7 = field_.InEditor(general_editors.FloatEditor, parameters_list[0:3] + [thing_.Thing()])
    in_editor_8 = field_.InEditor(general_editors.FloatEditor)
    in_editor_9 = in_editor_1.create_copy()
    assert in_editor_1.matches(in_editor_2)
    assert not in_editor_1.matches(in_editor_3)
    assert not in_editor_1.matches(in_editor_4)
    assert not in_editor_1.matches(in_editor_5)
    assert not in_editor_1.matches(in_editor_6)
    assert not in_editor_1.matches(in_editor_7)
    assert not in_editor_1.matches(in_editor_8)
    in_editor_3.force_to_match(in_editor_1)
    in_editor_4.force_to_match(in_editor_1)
    in_editor_5.force_to_match(in_editor_1)
    in_editor_6.force_to_match(in_editor_1)
    in_editor_7.force_to_match(in_editor_1)
    in_editor_8.force_to_match(in_editor_1)
    assert in_editor_1.matches(in_editor_3)
    assert in_editor_1.matches(in_editor_4)
    assert in_editor_1.matches(in_editor_5)
    assert in_editor_1.matches(in_editor_6)
    assert in_editor_1.matches(in_editor_7)
    assert in_editor_1.matches(in_editor_8)


