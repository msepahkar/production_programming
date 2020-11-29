# -*- coding: utf-8 -*-

import enum
from mehdi_lib.basics import basic_types, thing_
from mehdi_lib.generals import general_things


# ===========================================================================
class Boring(basic_types.ContainerForParameterizedEnum):

    # ===========================================================================
    @staticmethod
    def can_satisfy(satisfying_morph_thing, satisfied_morph_thing):
        pass

    # ===========================================================================
    @staticmethod
    def get_parameters_titles():
        return {
            thing_.MorphingThing.int_field_1: {
                basic_types.Language.AvailableLanguage.en: 'table x',
                basic_types.Language.AvailableLanguage.fa: 'طول میز',
            },
            thing_.MorphingThing.int_field_2: {
                basic_types.Language.AvailableLanguage.en: 'table y',
                basic_types.Language.AvailableLanguage.fa: 'عرض میز',
            },
            thing_.MorphingThing.int_field_3: {
                basic_types.Language.AvailableLanguage.en: 'height',
                basic_types.Language.AvailableLanguage.fa: 'ارتفاع',
            },
        }


# ===========================================================================
class Cutter(basic_types.ContainerForParameterizedEnum):
    # ===========================================================================
    @enum.unique
    class CutterType(basic_types.ParameterizedEnum):
        disk = 1
        lame = 2
        band = 3

        # ===========================================================================
        def get_parameters_titles(self):
            return [
                {
                    basic_types.Language.AvailableLanguage.en: 'max width',
                    basic_types.Language.AvailableLanguage.fa: 'حداکثر طول',
                },
                {
                    basic_types.Language.AvailableLanguage.en: 'max height',
                    basic_types.Language.AvailableLanguage.fa: 'حداکثر ارتفاع',
                },
            ]

        # ===========================================================================
        @staticmethod
        def get_ui_title():
            return {
                basic_types.Language.AvailableLanguage.en: {Cutter.CutterType.disk: 'disk', Cutter.CutterType.lame: 'lame', Cutter.CutterType.band: 'band'},
                basic_types.Language.AvailableLanguage.fa: {Cutter.CutterType.disk: 'دیسکی', Cutter.CutterType.lame: 'لنگ', Cutter.CutterType.band: 'نواری'},
            }

    # ===========================================================================
    @enum.unique
    class FeedingType(basic_types.ParameterizedEnum):
        manual_feed = 1
        auto_feed = 2

        # ===========================================================================
        def get_parameters_titles(self):
            return [
                {
                    basic_types.Language.AvailableLanguage.en: 'feeding rate',
                    basic_types.Language.AvailableLanguage.fa: 'نرخ تغذیه',
                },
            ]

        # ===========================================================================
        @staticmethod
        def get_ui_title():
            return {
                basic_types.Language.AvailableLanguage.en: {Cutter.FeedingType.manual_feed: 'manual feed', Cutter.FeedingType.auto_feed: 'auto fieed'},
                basic_types.Language.AvailableLanguage.fa: {Cutter.FeedingType.manual_feed: 'تغذیه دستی', Cutter.FeedingType.auto_feed: 'تغذیه خودکار'},
            }

    # ===========================================================================
    @staticmethod
    def get_parameterized_enums():
        return [Cutter.CutterType, Cutter.FeedingType]


# ===========================================================================
class Drill:
    pass


# ===========================================================================
class Grinder:
    pass


# ===========================================================================
class Lathe:
    pass


# ===========================================================================
class Mill:
    pass


# ===========================================================================
class Press:
    pass


# ===========================================================================
class Shaper:
    pass


# ===========================================================================
class Welder:
    pass


# ===========================================================================
@enum.unique
class MachineType(basic_types.ContainerFor_ContainerForParameterizedEnum):
    # boring = 1
    cutter = 2
    # drill = 3
    # grinder = 4
    # lathe = 5
    # mill = 6
    # press = 7
    # shaper = 8
    # welder = 9

    # ===========================================================================
    @staticmethod
    def get_members_correspondent_classes():
        return {
            # MachineType.boring: Boring,
            MachineType.cutter: Cutter,
        }

    # ===========================================================================
    @staticmethod
    def get_ui_title():
        return {
            basic_types.Language.AvailableLanguage.en: {MachineType.cutter: 'cutter'},#{MachineType.boring: 'boring', MachineType.cutter: 'cutter'},
            basic_types.Language.AvailableLanguage.fa: {MachineType.cutter: 'اره'},#{MachineType.boring: 'بورینگ', MachineType.cutter: 'اره'},
        }

