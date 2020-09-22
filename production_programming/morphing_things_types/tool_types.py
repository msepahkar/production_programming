# -*- coding: utf-8 -*-

import enum
from mehdi_lib.basics import basic_types


# ===========================================================================
@enum.unique
class ToolType(basic_types.UiTitleEnabledEnum):
    drill_bit = 1
    tap = 2
    tap_turner = 3
    wrench_normal = 4
    wrench_ring = 5
    wrench_L = 6
    wrench_start = 7
    wrench_french = 8
    wrench_pipe = 9
    wrench_crow = 10
    wrench_hole = 11
    pliers = 12
    pliers_long_nose = 13
    pliers_locking = 14
    hammer = 15
    wire_cutter = 16
    screw_driver_2 = 17
    screw_driver_4 = 18

