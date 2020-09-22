# -*- coding: utf-8 -*-

import enum


# ===========================================================================
@enum.unique
class Dummy(enum.Enum):
    pass

# ===========================================================================
@enum.unique
class Explanation(enum.Enum):
    # common
    no_problem = 1
    # materials or parts
    not_ready = 2
    defected = 3


# ===========================================================================
@enum.unique
class ExplanationSource(enum.Enum):
    # common
    no_problem = 1
    bad_estimation = 2
    # resources
    damaged = 20
    # humans
    cheerful = 30
    not_cheerful = 31
    tired = 32
    outside_problem = 33
    absent = 34
    # providers
    bad_words = 40
    bad_transport = 41
    mistaken_delivery = 42







