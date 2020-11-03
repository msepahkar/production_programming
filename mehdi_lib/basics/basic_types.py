# -*- coding: utf-8 -*-

import enum
from mehdi_lib.tools import tools

"""
Enums have members which require ui titles. That is where UiTitleEnabledEnum is required.
On the other hand, enums represent things which should have adjustable parameters. 
For example we have an enum for classifying chairs based on their material:
class Chair(Enum):
    wood = 1
    steel = 2
'plastic' and 'steel' need ui titles which could be different from what is used in the code and certainly not the same
in different languages.
But parameters could be for example 'chair height', 'chair weight', ...
"""

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
        it should be noted that these ui titles are for parameters not for elements of the enum!

        :return: an array containing one dict for every parameter. each dict specifies ui-title of that parameter for
        different supported languages
        """
        return []


# ===========================================================================
class ContainerForParameterizedEnum(ParameterizedEnumBase):
    """
    this class represents something with attributes, each of which is a parameterized enum
    Consider the chair example again but this time as a container of parameterized enum:

    class Chair(ContainerForParameterizedEnum):
        class ChairType(ParameterizedEnum):
            home = 1
            office = 2
        class ChairMaterial(ParameterizedEnum):
            wood = 1
            steel = 2

    Parameterized enums are ChairType and ChairMaterial. Each of these can have parameters for themselves. For example
    chair type parameters could be 'height', 'weight', ... and chair material parameters could be 'quality of maeterial'
    , 'price of material', ...
    """
    pass

    # ===========================================================================
    @staticmethod
    def get_parameterized_enums():
        """
        returns list of enums with parameters contained in this container. we can call them sub types.
        :return: list of attributes (parameterized enums)
        """
        return []


# ===========================================================================
class UiTitlesContainer:
    """
    base class for any object which requires ui titles for its elements (mostly enums)
    """
    # ===========================================================================
    @staticmethod
    def get_ui_titles():
        """
        ui titles of the enum are stored in a dict. for each language, proper ui title should be generated.
        example: {
                    english: {enum.item_one: 'ui title 1 in english', enum.item_two: 'ui title 2 in english'},
                    persian: {enum.item_one: 'ui title 1 in persian', enum.item_two: 'ui title 2 in persian'}
            }
        """
        return {}

    # ===========================================================================
    def get_instance_ui_title(self, language):
        """
        each enum item that calls this method, will receive its proper ui title based on the input language
        :param language: retrieves ui title based on this specific language
        """
        ui_titles = type(self).get_ui_titles()
        if ui_titles:
            return ui_titles[language][self]
        # if no ui_titles is available we have no other choice, we have to use the name used in code!
        return self.name


# ===========================================================================
class UiTitleEnabledEnum(UiTitlesContainer, enum.Enum):
    """
    This class is created just for making creation of ui enabled enums easier.
    (Simply there enums will inherit from one class instead of two!)
    """
    pass


# ===========================================================================
@enum.unique
class ParameterizedEnum(ParameterizedEnumBase, UiTitleEnabledEnum):
    """
    This class is created just for making creation of ui enabled parameterized enums easier.
    (Simply there enums will inherit from one class instead of two!)
    """
    pass


# ===========================================================================
class Language:
    """
    Prepares methods required for working with languages.
    """

    _active_language = None

    # ===========================================================================
    @enum.unique
    class AvailableLanguage(UiTitleEnabledEnum):
        en = 1
        fa = 2

        # ===========================================================================
        @staticmethod
        def get_ui_titles():
            """
            ui titles for languages themselves in available languages!
            :return: a dict whose keys are available languages. Data for each key is again a dict.
                keys in the new dict are again available languages and data for each key in the new dict is the name
                of that language in the language which is the key in the first dict. (a bit complicated!)
            """
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
    """
    Creates strings which have value in all available languages.
    """

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
class ContainerFor_ContainerForParameterizedEnum(UiTitleEnabledEnum):
    """
    consider this example:

    class Chair(ContainerForParameterizedEnum):
        class ChairType(ParameterizedEnum):
            home = 1
            office = 2
        class ChairMaterial(ParameterizedEnum):
            wood = 1
            steel = 2

    class Table(ContainerForParameterizedEnum):
        class TableSize(ParameterizedEnum):
            FourPeople = 1
            SixPeople = 2
        class TableMaterial(ParameterizedEnum):
            wood = 1
            steel = 2
    class Furniture(ContainerFor_ContainerForParameterizedEnum):
        chair = 1
        table = 2

    As could be seen, Furniture is the super container (container for containers). Chair is one of the containers
    inside the super container and Table is another container in the super container. The point is that these containers
    are expressed as enum members not the actual classes. So a method is required for retrieving actual classes based
    on enum name. For example actual class for 'chair' is 'Chair' and actual class for 'table' is 'Table'.
    """

    # ===========================================================================
    @staticmethod
    def get_members_correspondent_classes():
        """
            returns the corresponding classes of parameterized enums containers available in this container
        :return: A dict is returned. Keys are members of this class (which are containers for parameterized enums but
            are expressed as enum members).
            values are actual classes representing these containers
        """
        return {}

    # ===========================================================================
    def get_parameters_titles(self):
        """
        Shortcut for retrieving parameter titles for members of this super container.
        Considering the example above (Furniture), if chair calls this method, the corresponding method in Chair class
        will be called.
        :return: the returned dict from the same method in ParameterizedEnumBase class will be returned.
        """
        # returns parameters titles for current value
        return type(self).get_members_correspondent_classes()[self].get_parameters_titles()

    # ===========================================================================
    def get_parameterized_enums(self):
        """
        Another shortcut for retrieving parameterized enums in the container.
        Considering the Furniture example again, this function returns Chair and Table.
        :return: the list returned by the same method in ContainerForParameterizedEnum will be returned.
        """
        # in other words, returns sub types
        return type(self).get_members_correspondent_classes()[self].get_parameterized_enums()






