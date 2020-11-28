# -*- coding: utf-8 -*-

from mehdi_lib.basics import thing_, constants_
from mehdi_lib.generals import general_fields, general_enums, general_ui_titles, general_initial_values


# ===========================================================================
class Attachment(thing_.Thing):

    table_name = None

    relative_path = general_fields.FilePathField(initial_value=general_initial_values.file_path)
    file_name = general_fields.FileNameField(initial_value=general_initial_values.name)


# ===========================================================================
class Cost(thing_.Thing):

    table_name = None

    name = general_fields.NameField(initial_value='cost')
    value = general_fields.FloatField(1, general_ui_titles.value, 'value', 0, float('inf'), 2, 0)
    currency = general_fields.EnumField(2, general_ui_titles.currency, 'currency', general_enums.Currency, general_enums.Currency.toman)
    duration_of_usefulness = general_fields.DurationField(3, general_ui_titles.duration_of_usefulness, 'duration_of_usefulness', constants_.Constants.ZERO_DURATION)
    validity_start_time = general_fields.DatetimeField(4, general_ui_titles.validity_start_time, 'validity_start_time', constants_.Constants.MAX_DATE_TIME)
    validity_end_time = general_fields.DatetimeField(5, general_ui_titles.validity_end_time, 'validity_end_time', constants_.Constants.MAX_DATE_TIME)


# ===========================================================================
class CostPerTimeInterval(Cost):

    time_interval = general_fields.DurationField(1, general_ui_titles.duration, 'duration', constants_.Constants.ZERO_DURATION)


# ===========================================================================
class DummyThing(thing_.Thing):
    pass


# ===========================================================================
class Dummy2(thing_.Thing):
    pass


# ===========================================================================
class ExpertLevel(thing_.Thing):

    table_name = None

    name = general_fields.NameField(initial_value='expert_level')
    level = general_fields.IntField(1, general_ui_titles.level, 'level', 0, 10, 5)


# ===========================================================================
class Price(Cost):

    name = general_fields.NameField(initial_value='price')
    amount = general_fields.FloatField(1, general_ui_titles.amount, 'amount', 0, float('inf'), 3, 0)
    amount_unit = general_fields.EnumField(2, general_ui_titles.amount_unit, 'amount_unit', general_enums.AmountUnit, general_enums.AmountUnit.number)
    type = general_fields.EnumField(3, general_ui_titles.type_, 'type', general_enums.PriceType, general_enums.PriceType.normal)


