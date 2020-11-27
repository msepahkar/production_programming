from mehdi_lib.basics import prototype_, thing_
from mehdi_lib.generals import general_fields, general_editors, general_ui_titles
import pytest


pytestmark = pytest.mark.basics


# ===========================================================================
class TestingThingPrototype(prototype_.ThingPrototype):
    pass


# ===========================================================================
class TestingThing(thing_.Thing):
    pass


# ===========================================================================
def test_Prototype():
    assert TestingThingPrototype.get_main_type() == TestingThing
    assert prototype_.Prototype.get_prototype(TestingThing) == TestingThingPrototype
    assert TestingThingPrototype.referencing_prototypes() == []
