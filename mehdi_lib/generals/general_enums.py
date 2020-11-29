# -*- coding: utf-8 -*-

from mehdi_lib.basics import basic_types
import enum


# ===========================================================================
@enum.unique
class AmountUnit(basic_types.UiTitleEnabledEnum):
    number = 1
    kilo = 2

    # ===========================================================================
    def get_ui_title(self):
        if self == self.number:
            return basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'Number',
                basic_types.Language.AvailableLanguage.fa: 'عددی',
            })
        if self == self.kilo:
            return basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'Kilo',
                basic_types.Language.AvailableLanguage.fa: 'کیلو',
            })
        return self.name


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
    def get_ui_title(self):
        if self == self.rial:
            return basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'Rial',
                basic_types.Language.AvailableLanguage.fa: 'ریال',
            })
        if self == self.toman:
            return basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'Toman',
                basic_types.Language.AvailableLanguage.fa: 'تومن',
            })
        if self == self.usd:
            return basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'USD',
                basic_types.Language.AvailableLanguage.fa: 'دلار آمریکا',
            })
        if self == self.euro:
            return basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'Euro',
                basic_types.Language.AvailableLanguage.fa: 'یورو',
            })
        return self.name


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
    def get_ui_title(self):
        if self == self.normal:
            return basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'Normal',
                basic_types.Language.AvailableLanguage.fa: 'معمولی',
            })
        if self == self.competitive:
            return basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'Competitive',
                basic_types.Language.AvailableLanguage.fa: 'رقابتی',
            })
        if self == self.actual:
            return basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'Actual',
                basic_types.Language.AvailableLanguage.fa: 'واقعی',
            })
        return self.name


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
    def get_ui_title(self):
        if self == self.second:
            return basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'Second',
                basic_types.Language.AvailableLanguage.fa: 'ثانیه',
            })
        if self == self.minute:
            return basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'Minute',
                basic_types.Language.AvailableLanguage.fa: 'دقیقه',
            })
        if self == self.hour:
            return basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'Hour',
                basic_types.Language.AvailableLanguage.fa: 'ساعت',
            })
        if self == self.day:
            return basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'Day',
                basic_types.Language.AvailableLanguage.fa: 'روز',
            })
        if self == self.week:
            return basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'Week',
                basic_types.Language.AvailableLanguage.fa: 'هفته',
            })
        if self == self.month:
            return basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'Month',
                basic_types.Language.AvailableLanguage.fa: 'ماه',
            })
        if self == self.year:
            return basic_types.MultilingualString({
                basic_types.Language.AvailableLanguage.en: 'Year',
                basic_types.Language.AvailableLanguage.fa: 'سال',
            })
        return self.name

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








