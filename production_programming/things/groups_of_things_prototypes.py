# -*- coding: utf-8 -*-

from mehdi_lib.basics import prototype_


# ===========================================================================
class BuyingApproachThingPrototype(prototype_.ThingPrototype):
    module_name = 'things.buying_approach_things'


# ===========================================================================
class PartThingPrototype(prototype_.ThingPrototype):
    module_name = 'things.part_things'


# ===========================================================================
class ProducingApproachThingPrototype(prototype_.ThingPrototype):
    module_name = 'things.producing_approach_things'


# ===========================================================================
class SpecialtyThingPrototype(prototype_.ThingPrototype):
    module_name = 'things.specialty_things'
