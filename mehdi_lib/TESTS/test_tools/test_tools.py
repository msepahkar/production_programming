from mehdi_lib.generals import general_fields, general_ui_titles, general_editors
from mehdi_lib.basics import database_tools
from mehdi_lib.tools import tools
import pytest


pytestmark = pytest.mark.tools


# ===========================================================================
def test_ordered_dict():

    ordered_dict = tools.IndexEnabledDict()
    key1 = 1
    value1 = 'one'
    key2 = 2
    value2 = 'two'
    key3 = 3
    value3 = 'three'
    key4 = 4
    value4 = 'four'
    key5 = 5
    value5 = 'five'

    ordered_dict.insert(5, key1, value1)
    ordered_dict.insert(5, key2, value2)
    ordered_dict.insert(10, key3, value3)
    ordered_dict.insert(10, key4, value4)
    ordered_dict.insert(10, key5, value5)

    assert len(ordered_dict) == 5
    assert key1 in ordered_dict and key2 in ordered_dict and key3 in ordered_dict and key4 in ordered_dict and \
        key5 in ordered_dict
    assert ordered_dict[key1] == value1 and ordered_dict[key2] == value2 and ordered_dict[key3] == value3 and \
        ordered_dict[key4] == value4 and ordered_dict[key5] == value5
    assert ordered_dict.keys() == [key1, key2, key3, key4, key5] and ordered_dict.values() == [value1, value2, value3,
                                                                                               value4, value5]

    ordered_dict.reorder(key2, 3)
    assert ordered_dict.keys() == [key2, key1, key3, key4, key5] and ordered_dict.values() == [value2, value1, value3,
                                                                                               value4, value5]

    del ordered_dict[key3]
    assert ordered_dict.keys() == [key2, key1, key4, key5] and ordered_dict.values() == [value2, value1, value4, value5]

    ordered_dict.clear()
    assert len(ordered_dict) == 0


# ===========================================================================
class TestTools:

    # ===========================================================================
    @staticmethod
    def test_find_available_name(tmp_path):
        d = tmp_path / 'sub'
        d.mkdir()
        base_name = 'base_name'
        extension = 'ext'
        f = d / (base_name + '.' + extension)
        assert tools.Tools.find_available_name(str(d), base_name, extension) == str(f)

        f.write_text('h')
        f1 = d / (base_name + '_1.' + extension)
        assert tools.Tools.find_available_name(str(d), base_name, extension) == str(f1)

        f1.write_text('hi')
        f2 = d / (base_name + '_2.' + extension)
        assert tools.Tools.find_available_name(str(d), base_name, extension) == str(f2)

        f2.write_text('hii')
        f1.unlink()
        assert tools.Tools.find_available_name(str(d), base_name, extension) == str(f1)

        f1.write_text('hi')
        f1.unlink()
        f3 = d / (base_name + '_3.' + extension)
        assert tools.Tools.find_available_name(str(d), base_name, extension, greatest_number=True) == str(f3)

        f3.write_text('hiii')  # for potential later tests which might be added!

    # ===========================================================================
    @staticmethod
    def test_parse_time_delta():
        s = '40'
        t = tools.Tools.parse_time_delta(s)
        assert t.days == 0 and t.seconds // 3600 == 0 and (t.seconds // 60) % 60 == 0 and t.seconds % 60 == 40

        s = '14:40'
        t = tools.Tools.parse_time_delta(s)
        assert t.days == 0 and t.seconds // 3600 == 0 and (t.seconds // 60) % 60 == 14 and t.seconds % 60 == 40

        s = '12:14:40'
        t = tools.Tools.parse_time_delta(s)
        assert t.days == 0 and t.seconds // 3600 == 12 and (t.seconds // 60) % 60 == 14 and t.seconds % 60 == 40

        s = '3:12:14:40'
        t = tools.Tools.parse_time_delta(s)
        assert t.days == 3 and t.seconds // 3600 == 12 and (t.seconds // 60) % 60 == 14 and t.seconds % 60 == 40

    # ===========================================================================
    @staticmethod
    def test_remove_element_from_list_if_exists():
        li = ['x', 'y']
        tools.Tools.remove_element_from_list_if_exists(li, 'x')
        assert 'x' not in li and 'y' in li

    # ===========================================================================
    @staticmethod
    def test_force_order_in_list_elements():
        li = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        tools.Tools.force_order_in_list_elements(li, 5, 4, 3, first_element=10, one_before_last_element=8, last_element=7)
        assert li[0] == 10
        assert li[-1] == 7
        assert li[-2] == 8
        assert li.index(5) < li.index(4) < li.index(3)

    # ===========================================================================
    @staticmethod
    def test_parent_type():
        class B:
            pass
        class C(B):
            pass
        class D(C):
            pass
        class E:
            pass
        class F(E,B):
            pass

        assert tools.Tools.parent_type(C) == B
        assert tools.Tools.parent_type(D) == C
        assert tools.Tools.parent_type(E) == object
        assert tools.Tools.parent_type(F) == E
        assert tools.Tools.parent_type(object) is None

    # ===========================================================================
    @staticmethod
    def test_add_missing_starting_and_ending_double_quotes():
        assert tools.Tools.add_missing_starting_and_ending_double_quotes('hi') == '"hi"'
        assert tools.Tools.add_missing_starting_and_ending_double_quotes('"hi') == '"hi"'
        assert tools.Tools.add_missing_starting_and_ending_double_quotes('hi"') == '"hi"'

    # ===========================================================================
    @staticmethod
    def test_remove_starting_and_ending_double_quotes():
        assert tools.Tools.remove_starting_and_ending_double_quotes('"hi"') == 'hi'
        assert tools.Tools.remove_starting_and_ending_double_quotes('"hi') == 'hi'
        assert tools.Tools.remove_starting_and_ending_double_quotes('hi"') == 'hi'

    # ===========================================================================
    @staticmethod
    def test_inheritors():
        class B:
            pass

        class C1(B):
            pass

        class C2(B):
            pass

        class D1(C1):
            pass

        class D2(C2):
            pass
        inheritors = tools.Tools.inheritors(B)
        assert C1 in inheritors
        assert C2 in inheritors
        assert D1 in inheritors
        assert D2 in inheritors
