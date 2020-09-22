# -*- coding: utf-8 -*-

import enum
from mehdi_lib.tools import tools


# ===========================================================================
class ParameterizedEnumBase:
    """
    base class for a new enum type which has adjustable parameters with ui titles
    """

    # ===========================================================================
    @staticmethod
    def can_satisfy(satisfying_parameterized_enum, satisfied_parameterized_enum):
        """
        checks if one enum has at least the abilities of the other enum

        suppose each enum expresses a tool. this method returns true if the first tool can do the job of the second tool

        :param satisfying_parameterized_enum: the one which should have the minimum capabilities
        :param satisfied_parameterized_enum: the one which specifies the minimum capabilities
        :return:
        """

        # should be implemented in each defined enum
        raise NotImplementedError

    # ===========================================================================
    @staticmethod
    def get_parameters_titles():
        """
        parameters have ui-titles expressed in different languages.

        :return: an array containing one dict for every parameter. each dict specifies ui-title of that parameter for
        different supported languages
        """
        return []


# ===========================================================================
class ContainerForParameterizedEnum(ParameterizedEnumBase):
    # something with attributes, each of which is a parameterized enum
    pass

    # ===========================================================================
    @staticmethod
    def get_parameterized_enums():
        # returns list of enums with parameters contained in this container. we can call them sub types.
        return []


# ===========================================================================
class UiTitlesContainer:

    # ===========================================================================
    @staticmethod
    def get_ui_titles():
        return {}

    # ===========================================================================
    def get_instance_ui_title(self, language):
        return type(self).get_ui_titles()[language]


# ===========================================================================
class UiTitleEnabledEnum(UiTitlesContainer, enum.Enum):

    # ===========================================================================
    def get_instance_ui_title(self, language):
        ui_titles = type(self).get_ui_titles()
        if ui_titles:
            return ui_titles[language][self]
        return self.name


# ===========================================================================
@enum.unique
class ParameterizedEnum(ParameterizedEnumBase, UiTitleEnabledEnum):
    pass


# ===========================================================================
class Language:

    _active_language = None

    # ===========================================================================
    @enum.unique
    class AvailableLanguage(UiTitleEnabledEnum):
        en = 1
        fa = 2

        # ===========================================================================
        @staticmethod
        def get_ui_titles():
            return {
                Language.en: {Language.en: 'English', Language.fa: 'Persian'},
                Language.fa: {Language.en: 'انگلیسی', Language.fa: 'فارسی'},
            }

        # ===========================================================================
        def is_right_to_left(self):
            if self in [Language.AvailableLanguage.fa]:
                return True
            return False

    # ===========================================================================
    @staticmethod
    def get_active_language():
        if Language._active_language is None:
            return Language.get_default_language()
        return Language._active_language

    # ===========================================================================
    @staticmethod
    def get_default_language():
        return Language.AvailableLanguage.en

    # ===========================================================================
    @staticmethod
    def set_active_language(language):
        Language._active_language = language


# ===========================================================================
class MultilingualString:

    # ===========================================================================
    def __init__(self, values):
        self._values = dict()
        for language in values.keys():
            self[language] = values[language]

    # ===========================================================================
    def __getitem__(self, language):
        if language not in self._values.keys():
            tools.Tools.warning('value for this language: "{}" is not set'.format(language))
        return self._values[language]

    # ===========================================================================
    def __setitem__(self, language, value):
        if language not in Language.AvailableLanguage:
            tools.Tools.warning('not a valid language: {}'.format(language))
        self._values[language] = value


# ===========================================================================
class SuperParameterizedEnum(UiTitleEnabledEnum):
    # is able to fetch corresponding class for each value of the enum

    # ===========================================================================
    @staticmethod
    def get_members_correspondent_classes():
        return {}

    # ===========================================================================
    def get_parameters_titles(self):
        # returns parameters titles for current value
        return type(self).get_members_correspondent_classes()[self].get_parameters_titles()

    # ===========================================================================
    def get_parameterized_enums(self):
        # in other words, returns sub types
        return type(self).get_members_correspondent_classes()[self].get_parameterized_enums()






