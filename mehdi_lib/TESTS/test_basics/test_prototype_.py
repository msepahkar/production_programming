from mehdi_lib.basics import prototype_
import pytest


pytestmark = pytest.mark.basics


# ===========================================================================
class TestPrototype(prototype_.Prototype):
    pass


# ===========================================================================
class Test:
    pass


# ===========================================================================
def test_Prototype():
    assert TestPrototype.get_main_type() == Test
    assert prototype_.Prototype.get_prototype(Test) == TestPrototype
