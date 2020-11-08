# -*- coding: utf-8 -*-

from mehdi_lib.basics import field_, constants_, thing_
from mehdi_lib.generals import general_fields, general_editors, general_ui_titles
from things import specialty_things, all_things_prototypes, part_things
from morphing_things_types import machine_types, ui_titles, initial_values


# ===========================================================================
class Machine(thing_.MorphingThing):

    table_name = 'machines'

    name = general_fields.NameField(initial_value='machine')
    main_type = general_fields.EnumField(1, general_ui_titles.main_type, 'type', machine_types.MachineType, initial_value=None)


# ===========================================================================
class Operation(thing_.Thing):

    table_name = 'operations'

    name = general_fields.NameField(initial_value=initial_values.operation)
    producing_approach = general_fields.ForeignKeyField(1, ui_titles.producing_approach, 'producing_approach_id', all_things_prototypes.OperationPrototype, all_things_prototypes.ProducingApproachPrototype)
    sequence_number = general_fields.IntField(2, ui_titles.sequence_number, 'sequence_number', 0, constants_.Constants.MAX_INT, 0)
    setup_time = general_fields.DurationField(3, ui_titles.setup_time, 'setup_time', constants_.Constants.ZERO_DURATION)
    setup_time_in_batch = general_fields.DurationField(4, ui_titles.setup_time_in_batch, 'setup_time_in_batch', constants_.Constants.ZERO_DURATION)
    operation_time_min = general_fields.DurationField(5, ui_titles.operation_time_min, 'operation_time_min', constants_.Constants.ZERO_DURATION)
    operation_time_max = general_fields.DurationField(6, ui_titles.operation_time_max, 'operation_time_max', constants_.Constants.ZERO_DURATION)
    min_expert_levels = general_fields.ListField(7, ui_titles.min_expert_levels, 'min_expert_levels', all_things_prototypes.OperationSpecialtyExpertLevelPrototype)
    sub_parts = general_fields.ListField(8, ui_titles.sub_parts, 'sub_parts', all_things_prototypes.OperationSubPartPrototype, field_.InEditor(
        general_editors.MultipleItemSelectorEditor))
    machines = general_fields.ListField(9, ui_titles.machines, 'machines', all_things_prototypes.OperationMachinePrototype)
    tools = general_fields.ListField(10, ui_titles.tools, 'tools', all_things_prototypes.ToolPrototype)
    requires_help = general_fields.BoolField(11, ui_titles.requires_help, 'requires_help', False)

    # ===========================================================================
    def set_dependency_parameters(self):

        self.dependency_parameters[Operation.min_expert_levels] = thing_.DependencyParameters(
            specialty_things.Specialty.all(), OperationSpecialtyExpertLevel.specialty, None)

        producing_approach = self[Operation.producing_approach]
        if producing_approach:
            part = producing_approach[ProducingApproach.part]
            if part:
                sub_parts = part[part_things.Part.sub_parts]
                self.dependency_parameters[Operation.sub_parts] = thing_.DependencyParameters(sub_parts, OperationSubPart.sub_part, None)


# ===========================================================================
class OperationBatch(thing_.Thing):

    table_name = 'operation_batches'

    name = general_fields.NameField(initial_value='operation_batch')
    producing_approach = general_fields.ForeignKeyField(1, ui_titles.producing_approach, 'producing_approach_id', all_things_prototypes.OperationBatchPrototype, all_things_prototypes.ProducingApproachPrototype)
    setup_time = general_fields.DurationField(2, ui_titles.setup_time, 'setup_time', constants_.Constants.ZERO_DURATION)
    min_quantity = general_fields.FloatField(3, ui_titles.min_quantity, 'min_quantity', 0, float('inf'), 2, 0)
    max_quantity = general_fields.FloatField(4, ui_titles.max_quantity, 'max_quantity', 0, float('inf'), 2, 0)
    opt_quantity = general_fields.FloatField(5, ui_titles.opt_quantity, 'opt_quantity', 0, float('inf'), 2, 0)
    operations = general_fields.ListField(6, ui_titles.operations, 'operations', all_things_prototypes.OperationBatchOperationPrototype, field_.InEditor(
        general_editors.MultipleItemSelectorEditor))

    # ===========================================================================
    def set_dependency_parameters(self):
        producing_approach = self[OperationBatch.producing_approach]
        if producing_approach:
            operations = producing_approach[ProducingApproach.operations]
            self.dependency_parameters[OperationBatch.operations] = thing_.DependencyParameters(
                operations, OperationBatchOperation.operation, None)


# ===========================================================================
class OperationBatchOperation(thing_.Thing):

    table_name = 'operation_batches_operations'

    name = general_fields.NameField(initial_value='operation_batches_operation')
    operation_batch = general_fields.ForeignKeyField(1, ui_titles.operation_batch, 'operation_batch',
                                                     all_things_prototypes.OperationBatchOperationPrototype,
                                                     all_things_prototypes.OperationBatchPrototype)
    operation = general_fields.ForeignKeyField(2, ui_titles.operation, 'operation', all_things_prototypes.OperationBatchOperationPrototype,
                                               all_things_prototypes.OperationPrototype, field_.InEditor(
            general_editors.SingleItemSelectorEditor))

    # ===========================================================================
    def set_dependency_parameters(self):
        operation_batch = self[OperationBatchOperation.operation_batch]
        if operation_batch:
            producing_approach = operation_batch[OperationBatch.producing_approach]
            if producing_approach:
                self.dependency_parameters[OperationBatchOperation.operation] = \
                    thing_.DependencyParameters(producing_approach[ProducingApproach.operations], OperationBatchOperation.operation, self.used_operations)

    # ===========================================================================
    def used_operations(self):
        operations = []
        operation_batch = self[OperationBatchOperation.operation_batch]
        if operation_batch:
            operation_batch_operations = operation_batch[OperationBatch.operations]
            if operation_batch_operations.editors:
                operation_batch_operations = operation_batch_operations.get_responsible_editor().get_value().value
            for operation_batch_operation in operation_batch_operations:
                if operation_batch_operation != self:
                    operation = operation_batch_operation[OperationBatchOperation.operation]
                    if operation:
                        operations.append(operation)
        return operations


# ===========================================================================
class OperationMachine(Machine):

    table_name = 'operations_machines'

    name = general_fields.NameField(initial_value=initial_values.operation_machine)
    operation = general_fields.ForeignKeyField(1, ui_titles.operation, 'operation', all_things_prototypes.MachinePrototype, all_things_prototypes.OperationPrototype)


# ===========================================================================
class OperationSpecialtyExpertLevel(specialty_things.SpecialtyExpertLevel):

    table_name = 'operations_specialties_expert_levels'

    operation = general_fields.ForeignKeyField(1, ui_titles.operation, 'operation', all_things_prototypes.OperationSpecialtyExpertLevelPrototype, all_things_prototypes.OperationPrototype)

    # ===========================================================================
    def set_dependency_parameters(self):
        self.dependency_parameters[OperationSpecialtyExpertLevel.specialty] = thing_.DependencyParameters(
            specialty_things.Specialty.all(), OperationSpecialtyExpertLevel.specialty, self.used_specialties)

    # ===========================================================================
    def used_specialties(self):
        specialties = []
        operation = self[OperationSpecialtyExpertLevel.operation]
        if operation:
            operation_min_expert_levels = operation[Operation.min_expert_levels]
            if operation_min_expert_levels.editors:
                operation_min_expert_levels = operation_min_expert_levels.get_responsible_editor().get_value().value
            for operation_min_expert_level in operation_min_expert_levels:
                if operation_min_expert_level != self:
                    specialty = operation_min_expert_level[OperationSpecialtyExpertLevel.specialty]
                    if specialty:
                        specialties.append(specialty)
        return specialties


# ===========================================================================
class OperationSubPart(thing_.Thing):

    table_name = 'operations_sub_parts'

    name = general_fields.NameField(initial_value='operation_sub_part')
    operation = general_fields.ForeignKeyField(1, ui_titles.operation, 'operation', all_things_prototypes.OperationSubPartPrototype, all_things_prototypes.OperationPrototype)
    sub_part = general_fields.ForeignKeyField(2, ui_titles.sub_part, 'sub_part', all_things_prototypes.OperationSubPartPrototype, all_things_prototypes.SubPartPrototype, field_.InEditor(
        general_editors.SingleItemSelectorEditor))

    # ===========================================================================
    def set_dependency_parameters(self):
        operation = self[OperationSubPart.operation]
        if operation:
            producing_approach = operation[Operation.producing_approach]
            if producing_approach:
                part = producing_approach[ProducingApproach.part]
                if part:
                    self.dependency_parameters[OperationSubPart.sub_part] = \
                        thing_.DependencyParameters(part[part_things.Part.sub_parts], OperationSubPart.sub_part, self.used_sub_parts)

    # ===========================================================================
    def used_sub_parts(self):
        sub_parts = []
        operation = self[OperationSubPart.operation]
        if operation:
            operation_sub_parts = operation[Operation.sub_parts]
            if operation_sub_parts.editors:
                operation_sub_parts = operation_sub_parts.get_responsible_editor().get_value().value
            for operation_sub_part in operation_sub_parts:
                if operation_sub_part != self:
                    sub_part = operation_sub_part[OperationSubPart.sub_part]
                    if sub_part:
                        sub_parts.append(sub_part)
        return sub_parts


# ===========================================================================
class ProducingApproach(thing_.Thing):

    table_name = 'producing_approaches'

    name = general_fields.NameField(initial_value=initial_values.producing_approach)
    part = general_fields.ForeignKeyField(1, ui_titles.part, 'part_id', all_things_prototypes.ProducingApproachPrototype, all_things_prototypes.PartPrototype)
    operations = general_fields.ListField(2, ui_titles.operations, 'operations', Operation)
    operation_batches = general_fields.ListField(3, ui_titles.operation_batches, 'operation_batches', OperationBatch)


# ===========================================================================
class Tool(thing_.Thing):

    table_name = 'tools'

    name = general_fields.NameField(initial_value='tool')
    operation = general_fields.ForeignKeyField(1, ui_titles.operation, 'operation', all_things_prototypes.ToolPrototype, all_things_prototypes.OperationPrototype)
    # type = general_fields.EnumField(2, 'type', 'type', general_enums_1.ToolType, general_enums_1.ToolType.drill_bit)
    # parameter_1 = general_fields.IntField(3, 'parameter 1', 'parameter_1', 0, constants.Constants.MAX_INT, 0)
    # parameter_2 = general_fields.IntField(4, 'parameter 2', 'parameter_2', 0, constants.Constants.MAX_INT, 0)
    # parameter_3 = general_fields.IntField(5, 'parameter 3', 'parameter_3', 0, constants.Constants.MAX_INT, 0)


