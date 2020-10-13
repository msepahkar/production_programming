import pytest
from mehdi_lib.basics.database_tools import Types
import datetime

testing_datetime = datetime.datetime(1974,9,22,12,10,5)
testing_date = datetime.date(1974,9,22)

@pytest.mark.parametrize("value, type_in_class, expected_value", [
    (True, bool, 1),
    (False, bool, 0),
    (testing_datetime, datetime.datetime, '"{}"'.format(testing_datetime)),
    (testing_date, datetime.date, '"{}"'.format(testing_date)),
])
def test_format_for_database(value, type_in_class, expected_value):
    assert Types.format_for_database(value, type_in_class) == expected_value

