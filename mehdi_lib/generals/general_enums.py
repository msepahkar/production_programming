# -*- coding: utf-8 -*-

from mehdi_lib.basics import basic_types
import enum


# ===========================================================================
@enum.unique
class AmountUnit(basic_types.UiTitleEnabledEnum):
    number = 1
    kilo = 2

    # ===========================================================================
    @staticmethod
    def get_ui_titles():
        return {
            basic_types.Language.AvailableLanguage.en: {AmountUnit.number: 'number', AmountUnit.kilo: 'kilo'},
            basic_types.Language.AvailableLanguage.fa: {AmountUnit.number: 'عددی', AmountUnit.kilo: 'کیلویی'},
        }


# ===========================================================================
@enum.unique
class AttachmentType(basic_types.UiTitleEnabledEnum):
    document = 1
    image = 2
    design = 3
    drawing = 4


# ===========================================================================
@enum.unique
class Currency(basic_types.UiTitleEnabledEnum):
    rial = 1
    toman = 2
    usd = 3
    euro = 4

    # ===========================================================================
    @staticmethod
    def get_ui_titles():
        return {
            basic_types.Language.AvailableLanguage.en: {Currency.rial: 'rial', Currency.toman: 'toman', Currency.usd: 'usd', Currency.euro: 'euro'},
            basic_types.Language.AvailableLanguage.fa: {Currency.rial: 'ریال', Currency.toman: 'تومان', Currency.usd: 'دلار', Currency.euro: 'یورو'},
        }

# ===========================================================================
@enum.unique
class DesignType(basic_types.UiTitleEnabledEnum):
    catia = 1
    solidworks = 2


# ===========================================================================
@enum.unique
class DrawingType(basic_types.UiTitleEnabledEnum):
    catia = 1
    solidworks = 2
    autocad = 3
    hand = 4


# ===========================================================================
@enum.unique
class DocumentType(basic_types.UiTitleEnabledEnum):
    text = 1
    pdf = 2
    word = 3
    excel = 4


# ===========================================================================
@enum.unique
class ImageType(basic_types.UiTitleEnabledEnum):
    photo = 1
    photoshop = 2
    web = 3


# ===========================================================================
@enum.unique
class PriceType(basic_types.UiTitleEnabledEnum):
    normal = 1
    competitive = 2
    actual = 3

    # ===========================================================================
    @staticmethod
    def get_ui_titles():
        return {
            basic_types.Language.AvailableLanguage.en: {PriceType.normal: 'normal', PriceType.competitive: 'competitive', PriceType.actual: 'actual'},
            basic_types.Language.AvailableLanguage.fa: {PriceType.normal: 'معمولی', PriceType.competitive: 'رقابتی', PriceType.actual: 'واقعی'},
        }


# ===========================================================================
@enum.unique
class TimeSpanUnit(basic_types.UiTitleEnabledEnum):
    second = 1
    minute = 2
    hour = 3
    day = 4
    week = 5
    month = 6
    year = 7

    # ===========================================================================
    @staticmethod
    def get_ui_titles():
        return {
            basic_types.Language.AvailableLanguage.en: {TimeSpanUnit.second: 'second', TimeSpanUnit.minute: 'minute', TimeSpanUnit.hour: 'hour', TimeSpanUnit.day: 'day', TimeSpanUnit.week: 'week', TimeSpanUnit.month: 'month', TimeSpanUnit.year: 'year'},
            basic_types.Language.AvailableLanguage.fa: {TimeSpanUnit.second: 'ثانیه', TimeSpanUnit.minute: 'دقیقه', TimeSpanUnit.hour: 'ساعت', TimeSpanUnit.day: 'روز', TimeSpanUnit.week: 'هفته', TimeSpanUnit.month: 'ماه', TimeSpanUnit.year: 'سال'},
        }

    # ===========================================================================
    @staticmethod
    # only second, minute and hour are considered in this function
    def convert(value: float, current_unit: 'TimeSpanUnit', desired_unit: 'TimeSpanUnit') -> float:
        if current_unit == desired_unit:
            return value
        if current_unit == TimeSpanUnit.second:
            if desired_unit == TimeSpanUnit.minute:
                return float(value) / 60
            if desired_unit == TimeSpanUnit.hour:
                return float(value) / 3600
            # cannot convert more information is needed
            # noinspection PyTypeChecker
            return None
        if current_unit == TimeSpanUnit.minute:
            if desired_unit == TimeSpanUnit.second:
                return value * 60
            if desired_unit == TimeSpanUnit.hour:
                return float(value) / 60
            # cannot convert more information is needed
            # noinspection PyTypeChecker
            return None
        if current_unit == TimeSpanUnit.hour:
            if desired_unit == TimeSpanUnit.second:
                return value * 3600
            if desired_unit == TimeSpanUnit.minute:
                return value * 60
            # cannot convert more information is needed
            # noinspection PyTypeChecker
            return None
        # cannot convert more information is needed
        # noinspection PyTypeChecker
        return None








