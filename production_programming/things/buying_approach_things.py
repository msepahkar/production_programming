# -*- coding: utf-8 -*-

from mehdi_lib.basics import constants_, thing_
from mehdi_lib.generals import general_fields, general_things, general_ui_titles
from things import specialty_things, all_things_prototypes, part_things
from morphing_things_types import ui_titles, initial_values


# ===========================================================================
class BuyingApproach(thing_.Thing):

    table_name = 'buying_approaches'

    name = general_fields.NameField(initial_value=initial_values.buying_approach)
    part = general_fields.ForeignThingSelectorField(1, ui_titles.part, 'part_id', all_things_prototypes.BuyingApproachPrototype, all_things_prototypes.PartPrototype)
    provider = general_fields.ForeignThingSelectorField(2, ui_titles.provider, 'provider_id', all_things_prototypes.BuyingApproachPrototype, all_things_prototypes.ProviderPrototype)
    delivery_details = general_fields.ListField(3, ui_titles.delivery_details, 'details', all_things_prototypes.BuyingApproachDetailsPrototype)
    satisfaction_percent = general_fields.PercentField(4, ui_titles.satisfaction_percent, 'satisfaction_percent', initial_value=50)
    validity_start_date = general_fields.DateField(6, general_ui_titles.validity_start_date, 'validity_start_date', constants_.Constants.MAX_DATE)
    validity_end_date = general_fields.DateField(7, general_ui_titles.validity_end_date, 'validity_end_date', constants_.Constants.MAX_DATE)

    # ===========================================================================
    def set_dependency_parameters(self):
        self.dependency_parameters[BuyingApproach.part] = thing_.DependencyParameters(part_things.Part.all(), BuyingApproach.part, None)
        self.dependency_parameters[BuyingApproach.provider] = thing_.DependencyParameters(Provider.all(), BuyingApproach.provider, None)

    # ===========================================================================
    def set_foreign_owner_parameters(self):
        self.foreign_owner_parameters[BuyingApproach.part] = thing_.ForeignOwnerParameters(
            part_things.Part.buying_approaches)
        self.foreign_owner_parameters[BuyingApproach.provider] = thing_.ForeignOwnerParameters(Provider.deliveries)


# ===========================================================================
class BuyingApproachCost(general_things.Price):

    table_name = 'buying_approach_costs'

    delivery_details = general_fields.ForeignKeyField(1, ui_titles.delivery_details, 'delivery_details_id', all_things_prototypes.BuyingApproachCostPrototype, all_things_prototypes.BuyingApproachDetailsPrototype)


# ===========================================================================
class BuyingApproachDetails(thing_.Thing):

    table_name = 'buying_approaches_details'

    buying_approach = general_fields.ForeignKeyField(1, ui_titles.buying_approach, 'buying_approach_id', all_things_prototypes.BuyingApproachDetailsPrototype, all_things_prototypes.BuyingApproachPrototype)
    min_quantity = general_fields.FloatField(2, ui_titles.min_quantity, 'min_quantity', 0, float('inf'), 2, 0)
    max_quantity = general_fields.FloatField(3, ui_titles.max_quantity, 'max_quantity', 0, float('inf'), 2, 0)
    lead_time = general_fields.DurationField(4, ui_titles.lead_time, 'lead_time', constants_.Constants.ZERO_DURATION)
    delivery_time = general_fields.DurationField(5, ui_titles.delivery_time, 'delivery_time', constants_.Constants.ZERO_DURATION)
    costs = general_fields.ListField(6, ui_titles.costs, 'costs', BuyingApproachCost)
    min_expert_levels_for_inspection = general_fields.ListField(5, ui_titles.min_expert_levels_for_inspection, 'min_expert_levels_for_inspection', all_things_prototypes.BuyingApproachInspectionExpertLevelPrototype)
    inspection_time = general_fields.DurationField(7, ui_titles.inspection_time, 'inspection_time', constants_.Constants.ZERO_DURATION)
    probability_of_occurrence = general_fields.PercentField(8, ui_titles.probability_of_occurrence, 'probability_of_occurrence', 80)


# ===========================================================================
class BuyingApproachInspectionExpertLevel(thing_.Thing):

    table_name = 'delivery_inspection_expert_levels'

    buying_approach = general_fields.ForeignKeyField(1, ui_titles.buying_approach, 'buying_approach', all_things_prototypes.BuyingApproachInspectionExpertLevelPrototype, all_things_prototypes.BuyingApproachPrototype)
    specialty = general_fields.ForeignThingSelectorField(2, ui_titles.specialty, 'specialty', all_things_prototypes.SpecialtyExpertLevelPrototype, all_things_prototypes.SpecialtyPrototype)
    level = general_fields.IntField(3, ui_titles.level, 'level', 0, 10, 5)

    # ===========================================================================
    def set_dependency_parameters(self):
        self.dependency_parameters[specialty_things.SpecialtyExpertLevel.specialty] = thing_.DependencyParameters(
            specialty_things.Specialty.all(), specialty_things.SpecialtyExpertLevel.specialty, None)


# ===========================================================================
class Provider(thing_.Thing):

    table_name = 'providers'

    name = general_fields.NameField(initial_value='provider')
    reliability = general_fields.IntField(1, ui_titles.reliability, 'reliability', 0, 100, 50)
    is_suspended = general_fields.BoolField(2, ui_titles.is_suspended, 'is_suspended', False)

    # list fields
    deliveries = general_fields.ListField(3, ui_titles.deliveries, 'deliveries', BuyingApproach)


