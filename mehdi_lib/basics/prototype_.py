# -*- coding: utf-8 -*-

import importlib
import sys

from mehdi_lib.tools import tools


# ===========================================================================
class Prototype:
    prototype_suffix = 'Prototype'
    module_name = None

    # ===========================================================================
    @classmethod
    def get_main_type(cls):

        name_of_main_type = cls.__name__.replace(Prototype.prototype_suffix, '')

        if cls.module_name is not None:
            return getattr(importlib.import_module(cls.module_name), name_of_main_type)

        for module in sys.modules:
            if name_of_main_type in dir(sys.modules[module]):
                module_of_main_type = importlib.import_module(module)
                return getattr(module_of_main_type, name_of_main_type)

        tools.Tools.fatal_error('cannot find main type for "{}"'.format(cls.__name__))

    # ===========================================================================
    @staticmethod
    def get_prototype(main_type):
        name_of_prototype = main_type.__name__ + Prototype.prototype_suffix

        for module in sys.modules:
            if name_of_prototype in dir(sys.modules[module]):
                module_of_prototype = importlib.import_module(module)
                return getattr(module_of_prototype, name_of_prototype)

        return None


# ===========================================================================
class EditorPrototype(Prototype):
    module_name = 'mehdi_lib.basics.editor_'


# ===========================================================================
class GeneralEditorPrototype(Prototype):
    module_name = 'mehdi_lib.generals.general_editors'


# ===========================================================================
class ListOfThingsPrototype(Prototype):
    module_name = 'mehdi_lib.basics.thing_'
    pass


# ===========================================================================
class ThingPrototype(Prototype):
    module_name = 'mehdi_lib.basics.thing_'
    _referencing_prototypes = None  # type: [ThingPrototype]

    # ===========================================================================
    @classmethod
    def referencing_prototypes(cls) -> ['ThingPrototype']:
        if cls._referencing_prototypes is None:
            cls._referencing_prototypes = []
        return cls._referencing_prototypes


# ===========================================================================
class GeneralThingPrototype(ThingPrototype):
    module_name = 'mehdi_lib.generals.general_things'







