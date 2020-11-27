import pytest
from mehdi_lib.basics import database_tools, basic_types
import datetime
from mehdi_lib.tools import tools

"""Required parameters for the following tests."""
pytestmark = pytest.mark.basics

testing_date = datetime.date(1974, 9, 22)
testing_date_str = testing_date.strftime(database_tools.Types.date_strftime_format_string)
testing_datetime = datetime.datetime(1974, 9, 22, 12, 10, 5)
testing_datetime_str = testing_datetime.strftime(database_tools.Types.datetime_strftime_format_string)
hours = 3
minutes = 2
seconds = 1
testing_timedelta = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
testing_timedelta_str = database_tools.Types.time_delta_format_string.format(hours, minutes, seconds)


class TestingEnum(basic_types.UiTitleEnabledEnum):
    __test__ = False
    one = 1
    two = 2


"""Testing 'format_for_database' using different parameters."""


@pytest.mark.parametrize("value, type_in_class, expected_value", [
    (True, bool, 1),
    (False, bool, 0),
    (12, int, 12),
    (1.2, float, 1.2),
    (TestingEnum.one, TestingEnum, TestingEnum.one.value),
    (None, TestingEnum, database_tools.Types.enum_None_in_database),
    (testing_date, datetime.date, tools.Tools.add_missing_starting_and_ending_double_quotes(testing_date_str)),
    (testing_datetime, datetime.datetime,
     tools.Tools.add_missing_starting_and_ending_double_quotes(testing_datetime_str)),
    (testing_timedelta, datetime.timedelta,
     tools.Tools.add_missing_starting_and_ending_double_quotes(testing_timedelta_str)),
])
# ===========================================================================
def test_format_for_database(value, type_in_class, expected_value):
    assert database_tools.Types.format_for_database(value, type_in_class) == expected_value


# ===========================================================================
def test_format_for_database_for_multilingual_str():
    dummy_en = 'dummy'
    dummy_fa = 'بیخودی'
    multilingual_str = basic_types.MultilingualString({basic_types.Language.AvailableLanguage.en: dummy_en,
                                                       basic_types.Language.AvailableLanguage.fa: dummy_fa, })
    basic_types.Language.set_active_language(basic_types.Language.AvailableLanguage.en)
    assert database_tools.Types.format_for_database(multilingual_str, basic_types.MultilingualString) == dummy_en
    basic_types.Language.set_active_language(basic_types.Language.AvailableLanguage.fa)
    assert database_tools.Types.format_for_database(multilingual_str, basic_types.MultilingualString) == dummy_fa


"""Testing 'format for class' with different parameters."""


@pytest.mark.parametrize("value, type_in_class, expected_value", [
    (1, bool, True),
    (0, bool, False),
    (TestingEnum.one.value, TestingEnum, TestingEnum.one),
    (database_tools.Types.enum_None_in_database, TestingEnum, None),
    (tools.Tools.add_missing_starting_and_ending_double_quotes(testing_date_str), datetime.date, testing_date),
    (tools.Tools.add_missing_starting_and_ending_double_quotes(testing_datetime_str), datetime.datetime,
     testing_datetime),
    (tools.Tools.add_missing_starting_and_ending_double_quotes(testing_timedelta_str), datetime.timedelta,
     testing_timedelta),
])
# ===========================================================================
def test_format_for_class(value, type_in_class, expected_value):
    assert database_tools.Types.format_for_class(value, type_in_class) == expected_value


# ===========================================================================
def test_format_for_class_for_multilingual_str():
    dummy_en = 'dummy'
    dummy_fa = 'بیخودی'
    multilingual_str_en = basic_types.MultilingualString({basic_types.Language.AvailableLanguage.en: dummy_en})
    multilingual_str_fa = basic_types.MultilingualString({basic_types.Language.AvailableLanguage.en: dummy_fa})
    basic_types.Language.set_active_language(basic_types.Language.AvailableLanguage.en)
    assert database_tools.Types.format_for_class(dummy_en, basic_types.MultilingualString)[
               basic_types.Language.AvailableLanguage.en] == dummy_en
    basic_types.Language.set_active_language(basic_types.Language.AvailableLanguage.fa)
    assert database_tools.Types.format_for_class(dummy_fa, basic_types.MultilingualString)[
               basic_types.Language.AvailableLanguage.fa] == dummy_fa
