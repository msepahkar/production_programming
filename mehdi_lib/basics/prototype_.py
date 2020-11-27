# -*- coding: utf-8 -*-

import importlib
import sys

from mehdi_lib.tools import tools


# ===========================================================================
class Prototype:
    """Base class for prototype classes.

    Since python does not support prototype classes, this base class simulates it.
    Name of prototype class should be exactly equal to the name of the main type with adding 'Prototype' word to the
     end of it.
    """

    prototype_suffix = 'Prototype'
    module_name = None

    # ===========================================================================
    @classmethod
    def get_main_type(cls):
        """returns the main class related to this prototype class."""

        if cls.__name__ == Prototype.prototype_suffix:
            tools.Tools.fatal_error('Prototype itself does not have any main type!')

        # name of the main type should be equal to the prototype name but with 'Prototype' word removed.
        name_of_main_type = cls.__name__.replace(Prototype.prototype_suffix, '')

        # find name of module which contains the main type of this prototype
        if cls.module_name is None:
            modules = sys.modules.copy()
            for module in modules:
                if name_of_main_type in dir(modules[module]):
                    cls.module_name = module

        # module name is not found?
        if cls.module_name is None:
            # cannot be tolerate
            tools.Tools.fatal_error('cannot find main type for "{}"'.format(cls.__name__))

        # return main type in the found module
        return getattr(importlib.import_module(cls.module_name), name_of_main_type)

    # ===========================================================================
    @staticmethod
    def get_prototype(main_type):
        """returns the prototype class of a class"""

        # name of prototype is exactly name of the main class but having an extra 'Prototype' word added to its end.
        name_of_prototype = main_type.__name__ + Prototype.prototype_suffix

        # search for the prototype class in all modules.
        for module in sys.modules:
            if name_of_prototype in dir(sys.modules[module]):
                module_of_prototype = importlib.import_module(module)
                return getattr(module_of_prototype, name_of_prototype)

        # prototype class not found
        return None


# ===========================================================================
class EditorPrototype(Prototype):
    pass


# ===========================================================================
class GeneralEditorPrototype(Prototype):
    pass


# ===========================================================================
class ListOfThingsPrototype(Prototype):
    pass


# ===========================================================================
class ThingPrototype(Prototype):

    # foreign thing should store the prototype of the thing it refers to
    _referencing_prototypes = None  # type: [ThingPrototype]

    # ===========================================================================
    @classmethod
    def referencing_prototypes(cls) -> ['ThingPrototype']:
        if cls._referencing_prototypes is None:
            cls._referencing_prototypes = []
        return cls._referencing_prototypes


# ===========================================================================
class GeneralThingPrototype(ThingPrototype):
    pass







