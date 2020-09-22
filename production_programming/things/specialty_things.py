# -*- coding: utf-8 -*-

from mehdi_lib.basics import thing_
from mehdi_lib.generals import general_fields, general_enums, general_things
from things import all_things_prototypes
from morphing_things_types import ui_titles, initial_values


# ===========================================================================
class Specialty(thing_.Thing):

    table_name = 'specialties'

    name = general_fields.NameField(initial_value=initial_values.specialty)
    costs = general_fields.ListField(1, ui_titles.costs, 'costs', all_things_prototypes.SpecialtyCostPrototype)


# ===========================================================================
class SpecialtyCost(general_things.Cost):

    table_name = 'specialties_costs'

    name = general_fields.NameField(initial_value=initial_values.specialty_cost)
    specialty = general_fields.ForeignKeyField(1, ui_titles.specialty, 'specialty', all_things_prototypes.SpecialtyCostPrototype, all_things_prototypes.SpecialtyPrototype)
    timespan = general_fields.FloatField(2, ui_titles.time_span, 'timespan', 0, float('inf'), 2, 0)
    timespan_unit = general_fields.EnumField(3, ui_titles.time_span_unit, 'timespan_unit', general_enums.TimeSpanUnit, general_enums.TimeSpanUnit.hour)


# ===========================================================================
class SpecialtyExpertLevel(general_things.ExpertLevel):

    table_name = None

    specialty = general_fields.ForeignThingSelectorField(1, ui_titles.specialty, 'specialty', all_things_prototypes.SpecialtyExpertLevelPrototype, all_things_prototypes.SpecialtyPrototype)

    # ===========================================================================
    def set_dependency_parameters(self):
        super().set_dependency_parameters()
        self.dependency_parameters[SpecialtyExpertLevel.specialty] = thing_.DependencyParameters(Specialty.all(), SpecialtyExpertLevel.specialty, None)




