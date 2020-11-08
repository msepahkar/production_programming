# -*- coding: utf-8 -*-

from mehdi_lib.basics import constants_, field_, thing_
from mehdi_lib.generals import general_fields, general_enums, general_editors, general_things, general_ui_titles
from things import all_things_prototypes, producing_approach_things, buying_approach_things
from morphing_things_types import ui_titles, initial_values

# # ===========================================================================
# class Program(thing.Thing):
#
#     table_name = 'programs'
#     part = base_thing.ForeignKey(1, 'part_id', PartPrototype)
#     start_date = base_thing.DatetimeField(2, 'start date', 'start_date', constants.Constants.MAX_DATE)
#     quantity = base_thing.FloatField(3, 'quantity', 'quantity', 0, float('inf'), 2, 0)
#     deadline = base_thing.DatetimeField(4, 'deadline', 'deadline', constants.Constants.MAX_DATE)
#     hard_deadline = base_thing.DatetimeField(5, 'hard deadline', 'hard_deadline', constants.Constants.MAX_DATE_TIME)
#
#     # ===========================================================================
#     def load_latest_revision(self):
#         pass
#
#     # ===========================================================================
#     def calculate_required_parts(self):
#         pass
#
#     # ===========================================================================
#     def calculate_operations(self):
#         pass
#
#     # ===========================================================================
#     def fetch_initial_progress(self):
#         pass
#
#     # ===========================================================================
#     def calculate_required_resources(self):
#         pass
#
#     # ===========================================================================
#     def assign_resources(self):
#         pass
#
#     # ===========================================================================
#     def update_progress(self):
#         pass
#
#     # ===========================================================================
#     def create_new_revision(self):
#         self.calculate_required_parts()
#         self.calculate_operations()
#         self.fetch_initial_progress()
#         self.calculate_required_resources()
#         self.assign_resources()
#
#     # ===========================================================================
#     def save_revision(self):
#         pass

pass


# ===========================================================================
class Part(thing_.Thing):

    table_name = 'parts'

    name = general_fields.NameField(initial_value=initial_values.part)
    version_number = general_fields.IntField(1, ui_titles.version_number, 'version_number', 1, constants_.Constants.MAX_INT, 1)
    amount_unit = general_fields.EnumField(2, general_ui_titles.amount_unit, 'amount_unit', general_enums.AmountUnit, general_enums.AmountUnit.number)
    weight = general_fields.FloatField(3, ui_titles.weight, 'weight', 0, float('inf'), 2, 0)
    dimenstion_x_mm = general_fields.IntField(4, ui_titles.dimension_x_mm, 'dimension_x_mm', 0, constants_.Constants.MAX_INT, 0)
    dimenstion_y_mm = general_fields.IntField(5, ui_titles.dimension_y_mm, 'dimension_y_mm', 0, constants_.Constants.MAX_INT, 0)
    dimenstion_z_mm = general_fields.IntField(6, ui_titles.dimension_z_mm, 'dimension_z_mm', 0, constants_.Constants.MAX_INT, 0)
    prices = general_fields.ListField(7, ui_titles.prices, 'prices', all_things_prototypes.PartPricePrototype)
    buying_approaches = general_fields.ListField(8, ui_titles.buying_approaches, 'buying_approaches', buying_approach_things.BuyingApproach)
    producing_approaches = general_fields.ListField(9, ui_titles.producing_approaches, 'producing_approaches', producing_approach_things.ProducingApproach)
    attachments = general_fields.ListField(10, ui_titles.attachments, 'attachments', all_things_prototypes.PartAttachmentPrototype)
    sub_parts = general_fields.ListField(11, ui_titles.sub_parts, 'sub_parts', all_things_prototypes.SubPartPrototype)
    validity_start_date = general_fields.DateField(12, general_ui_titles.validity_start_date, 'start_date', constants_.Constants.MAX_DATE)
    validity_end_date = general_fields.DateField(13, general_ui_titles.validity_end_date, 'end_date', constants_.Constants.MAX_DATE)

    # ===========================================================================
    @property
    def sub_parts_as_parts(self):
        sub_parts = []
        # noinspection PyTypeChecker
        for part_as_sub_part in self[Part.sub_parts]:
            sub_parts.append(part_as_sub_part[SubPart.part])
        return sub_parts

    # ===========================================================================
    def immediate_assemblies(self):
        assemblies = []
        for part in Part.all():
            if part != self:
                for part_as_sub_part in part[Part.sub_parts]:
                    if part_as_sub_part[SubPart.part] == self:
                        assemblies.append(part)
                        break
        return assemblies

    # ===========================================================================
    def all_assemblies(self):

        assemblies = self.immediate_assemblies()
        parent_assemblies_array = []

        for assembly in assemblies:
            parent_assemblies_array.append(assembly.all_assemblies())

        for parent_assemblies in parent_assemblies_array:
            assemblies += parent_assemblies

        return assemblies

    # ===========================================================================
    def remove_sub_part(self, sub_part: 'Part'):
        for index, part_as_sub_part in enumerate(self[Part.sub_parts]):
            if sub_part == part_as_sub_part[SubPart.part]:
                del self[Part.sub_parts][index]


# ===========================================================================
class PartAttachment(general_things.Attachment):

    table_name = 'parts_attachments'

    part = general_fields.ForeignKeyField(1, ui_titles.part, 'part_id', all_things_prototypes.PartAttachmentPrototype, all_things_prototypes.PartPrototype)


# ===========================================================================
class PartPrice(general_things.Price):

    table_name = 'parts_prices'

    part = general_fields.ForeignKeyField(1, ui_titles.part, 'part_id', all_things_prototypes.PartPricePrototype, all_things_prototypes.PartPrototype)


# ===========================================================================
class SubPart(thing_.Thing):

    table_name = 'sub_parts'

    name = general_fields.NameField(initial_value=initial_values.sub_part)
    assembly = general_fields.ForeignKeyField(1, ui_titles.assembly, 'assembly_id', all_things_prototypes.SubPartPrototype, all_things_prototypes.PartPrototype)
    part = general_fields.ForeignKeyField(2, ui_titles.part, 'part_id', all_things_prototypes.SubPartPrototype, all_things_prototypes.PartPrototype, field_.InEditor(
        general_editors.SingleItemSelectorEditor))
    quantity = general_fields.FloatField(3, ui_titles.quantity, 'quantity', 0, float('inf'), 2, 1)

    # ===========================================================================
    def set_dependency_parameters(self):
        self.dependency_parameters[SubPart.part] = thing_.DependencyParameters(Part.all(), SubPart.part, self.find_all_assemblies)

    # ===========================================================================
    def set_foreign_owner_parameters(self):
        self.foreign_owner_parameters[SubPart.part] = None
        self.foreign_owner_parameters[SubPart.assembly] = thing_.ForeignOwnerParameters(Part.sub_parts)

    # ===========================================================================
    def find_all_assemblies(self):

        if self[SubPart.assembly] is None:
            return []

        all_assemblies = [self[SubPart.assembly]]  # type: [Part]
        assemblies = [self[SubPart.assembly]]  # type: [Part]
        while assemblies:
            new_assemblies = []
            for assembly in assemblies:
                if assembly is not None:
                    # noinspection PyUnresolvedReferences
                    new_assemblies += assembly.immediate_assemblies()

            all_assemblies += new_assemblies

            assemblies = new_assemblies

        return all_assemblies

    # ===========================================================================
    def find_all_children_parts(self):

        if self[SubPart.part] is None:
            return []

        all_children_parts = [self[SubPart.part]]
        child_parts = [self[SubPart.part]]  # type: [Part]
        while child_parts:
            new_child_parts = []
            for child_part in child_parts:
                if child_part is not None:
                    # noinspection PyUnresolvedReferences
                    new_child_parts += [sub_part[SubPart.part] for sub_part in child_part.sub_parts_as_parts()]

            all_children_parts += new_child_parts

            child_parts = new_child_parts

        return all_children_parts



# # ===========================================================================
# class Ability:
#     # ===========================================================================
#     def __init__(self):
#         self.id = None  # type: int
#         self.name = ''  # type: str
#         self.grade = ''  # type: str
#         self.priority = 0  # type: int
#         self.efficiency = 0  # type: float
#
#     # ===========================================================================
#     def can_do(self, specialty: Specialty):
#         if self.name == specialty.name:
#             return True
#         return False
#


pass
# # ===========================================================================
# class ResourceCost(general_things.Cost):
#     # ===========================================================================
#     # fields
#     resource_title = 'resource'
#
#     # ===========================================================================
#     def __init__(self, resource: 'Resource'):
#         super(ResourceCost, self).__init__()
#         self.resource = resource
#
#     # ===========================================================================
#     def __getitem__(self, item):
#         # resource
#         if item == ResourceCost.resource_title:
#             return self.resource
#
#         # other fields
#         return super(ResourceCost, self).__getitem__(item)
#
#     # ===========================================================================
#     def __setitem__(self, key, value):
#         # resource
#         if key == ResourceCost.resource_title:
#             if not isinstance(value, Resource):
#                 raise ValueError
#             if self.resource != value:
#                 self.resource = value
#                 self.modified_signal.emit()
#         # other fields
#         else:
#             super(ResourceCost, self).__setitem__(key, value)
#
pass
# # ===========================================================================
# class Resource:
#     resources = base_general.ListDiscrete()  # type: base_general.ListDiscrete
#
#     # ===========================================================================
#     def __init__(self):
#         self.id = None  # type: int
#         self.name = 'unnamed resource'  # type: str
#         self.abilities = base_general.ListDiscrete(Ability)  # type: base_general.ListDiscrete
#         self.availability_intervals = base_general.ListDiscrete(SuperInterval)  # type: base_general.ListDiscrete
#         self.assigned_intervals = base_general.ListDiscrete(Interval)  # type: base_general.ListDiscrete
#
#     # ===========================================================================
#     def find_ability(self, specialty: Specialty) -> Ability:
#
#         for ability in self.abilities:
#             if ability.can_do(specialty):
#                 return ability
#
#         # noinspection PyTypeChecker
#         return None
#
#     # ===========================================================================
#     def sort_availability_intervals(self):
#         self.availability_intervals = sorted(self.availability_intervals, key=lambda x: (
#             x.start_time.year, x.start_time.month, x.start_time.day, x.start_time.hour, x.start_time.minute))
#
#     # ===========================================================================
#     def find_finish_time(self, operation: Operation, start_time: datetime.datetime,
#                          required_time: datetime.timedelta) -> datetime.datetime:
#
#         # init
#         finish_time = constants.Constants.MAX_DATE_TIME
#         next_start_time = start_time
#
#         # find the ability of this resource for this specialty
#         ability = self.find_ability(operation.required_specialty)
#
#         # check for the existence of ability
#         if ability is not None:
#
#             # update total time according to efficiency
#             total_minutes = required_time.total_seconds() / 60
#             remained_required_minutes = int(total_minutes * ability.efficiency)
#
#             # sort intervals
#             self.sort_availability_intervals()
#
#             # start counting available intervals
#             for availability_interval in self.availability_intervals:
#                 remained_required_minutes, next_start_time = \
#                     availability_interval.evaluate_doing_operation_in_this_interval(next_start_time,
#                                                                                     remained_required_minutes)
#                 if remained_required_minutes == 0:
#                     finish_time = next_start_time
#                     break
#
#         return finish_time
#
#     # ===========================================================================
#     def assign_operation(self, operation: Operation, start_time: datetime.datetime,
#                          required_time: datetime.timedelta) -> (int, datetime.datetime):
#
#         # init
#         finish_time = constants.Constants.MAX_DATE_TIME
#         next_start_time = start_time
#         # update total time according to efficiency
#         required_minutes = required_time.total_seconds() / 60
#         remained_required_minutes = required_minutes
#
#         # find the abilities of this resource for the specialties
#         ability = self.find_ability(operation.required_specialty)
#
#         if ability is not None:
#
#             efficiency = ability.efficiency
#
#             # update total time according to efficiency
#             remained_required_minutes = int(required_minutes * efficiency)
#
#             # sort time intervals
#             self.sort_availability_intervals()
#
#             # start counting available intervals
#             for interval in self.availability_intervals:
#                 # a minimum available time should be checked
#                 if interval.remained_minutes_from_now(
#                         next_start_time) >= constants.Constants.MIN_REQUIRED_MINUTES_FOR_AVAILABILITY:
#                     # assign the job
#                     remained_required_minutes, next_start_time = \
#                         interval.assign_operation_in_this_interval(self, operation, next_start_time,
#                                                                    remained_required_minutes)
#                     # all of the remaining job assigned to this interval?
#                     if remained_required_minutes == 0:
#                         finish_time = next_start_time
#                         break
#
#             # remove the effect of efficiency
#             remained_required_minutes /= efficiency
#
#         # this is what we were able to do!
#         return remained_required_minutes, finish_time
#
pass
# # ===========================================================================
# class BomPath:
#     def __init__(self):
#         self.parts = []  # type: [Part]
#         self.min_start_time = constants.Constants.MAX_DATE_TIME
#         self.required_time = 0
#         self.loose_time = 0

pass
# # ===========================================================================
# class Timings:
#     # ===========================================================================
#     def __init__(self):
#         self.min_start = constants.Constants.MAX_DATE_TIME  # type: datetime.datetime
#         self.max_start = constants.Constants.MAX_DATE_TIME  # type: datetime.datetime
#         self.min_finish = constants.Constants.MAX_DATE_TIME  # type: datetime.datetime
#         self.max_finish = constants.Constants.MAX_DATE_TIME  # type: datetime.datetime
#         self.real_finish = constants.Constants.MAX_DATE_TIME  # type: datetime.datetime
#         self.loose = constants.Constants.ZERO_DURATION  # type: datetime.timedelta
#         self.required = constants.Constants.ZERO_DURATION  # type: datetime.timedelta
pass

# # ===========================================================================
# class ProcessingParameters:
#     # ===========================================================================
#     def __init__(self):
#         self.level = 0  # type: int
#         self.full_path = ""  # type: str
#         self.resources_assigned = False  # type: bool
#         self.timings = Timings()

pass
# # ===========================================================================
# class Interval:
#     # ===========================================================================
#     def __init__(self, operation: 'Operation'):
#         self.resource = None  # type: Resource
#         self.start_time = constants.Constants.MAX_DATE_TIME  # type: datetime.datetime
#         self.end_time = constants.Constants.MAX_DATE_TIME  # type: datetime.datetime
#         self.operation = operation
#
#     # ===========================================================================
#     def duration(self) -> datetime.timedelta:
#         if self.end_time > self.start_time:
#             return self.end_time - self.start_time
#         return datetime.timedelta(0)
#
#     # ===========================================================================
#     def total_minutes(self) -> int:
#         if self.end_time > self.start_time:
#             return int((self.end_time - self.start_time).total_seconds() // 60)
#         return 0
#
#     # ===========================================================================
#     def remained_minutes_from_now(self, now: datetime.datetime) -> int:
#         remained_minutes = 0
#         if self.end_time > now:
#             remained_minutes = (self.end_time - now).total_seconds() / 60
#         return remained_minutes

pass
# # ===========================================================================
# class SuperInterval:
#     # ===========================================================================
#     def __init__(self, resource: 'Resource'):
#         self.resource = resource
#         # noinspection PyTypeChecker
#         self._interval = Interval(None)
#         self._interval.resource = resource
#         self._interval.start_time = constants.Constants.MAX_DATE_TIME  # type: datetime.datetime
#         self._interval.end_time = constants.Constants.MAX_DATE_TIME  # type: datetime.datetime
#         self.assigned_sub_intervals = []  # type: [Interval]
#         self.free_sub_intervals = [self._interval]  # type: [Interval]
#
#     # ===========================================================================
#     @property
#     def start_time(self):
#         return self._interval.start_time
#
#     # ===========================================================================
#     @start_time.setter
#     def start_time(self, value):
#         if value > self._interval.end_time:
#             tools.Tools.warning('the specified start time is later than the end time of super interval \
#                         (while setting start time of super interval)')
#         self._interval.start_time = value
#
#     # ===========================================================================
#     @property
#     def end_time(self):
#         return self._interval.end_time
#
#     # ===========================================================================
#     def total_minutes(self) -> int:
#         return self._interval.total_minutes()
#
#     # ===========================================================================
#     def remained_minutes_from_now(self, now: datetime.datetime) -> int:
#         return self._interval.remained_minutes_from_now(now)
#
#     # ===========================================================================
#     def remained_available_minutes_from_now(self, now: datetime.datetime) -> int:
#
#         # init
#         remained_available_minutes = 0
#
#         # add up all remained free minutes
#         for sub_interval in self.free_sub_intervals:
#             # check the threshold
#             if sub_interval.remained_minutes_from_now(now) > constants.Constants.MIN_REQUIRED_MINUTES_FOR_AVAILABILITY:
#                 remained_available_minutes += sub_interval.remained_minutes_from_now(now)
#
#         return remained_available_minutes
#
#     # ===========================================================================
#     # returns: (remained minutes of the operation, ending time of the operation)
#     def evaluate_doing_operation_in_this_interval(self, start_time: datetime.datetime,
#                                                   required_minutes: int) -> (int, datetime.datetime):
#
#         # sort the free sub-intervals according to their start times
#         self.free_sub_intervals = sorted(self.free_sub_intervals, key=lambda x: x.start_time)
#
#         # init
#         new_start_time = start_time
#         end_time = start_time
#         remained_required_minutes = required_minutes
#
#         # iterate through the sorted sub intervals
#         for sub_interval in self.free_sub_intervals:
#
#             # is there enough time for doing the rest of the operation?
#             if sub_interval.remained_minutes_from_now(new_start_time) >= remained_required_minutes:
#                 # bingo! the rest of the operation will be done right here!
#                 end_time = max(new_start_time, sub_interval.start_time) + datetime.timedelta(0,
#                                                                                              remained_required_minutes * 60)
#                 remained_required_minutes = 0
#                 break
#
#             # any time remained in this interval (more than the threshold of course)?
#             if sub_interval.remained_minutes_from_now(
#                     new_start_time) > constants.Constants.MIN_REQUIRED_MINUTES_FOR_AVAILABILITY:
#
#                 # consider part of the operation which will be done in this sub-interval
#                 remained_required_minutes -= sub_interval.remained_minutes_from_now(new_start_time)
#                 # now go to the end of the sub-interval
#                 new_start_time = sub_interval.end_time
#                 # record this time as the end time, because some operation is done here
#                 #  and we are not sure if we can do anything more!
#                 end_time = new_start_time
#
#             # this sub-interval is useless, either is passed or does not have time more than the threshold
#             #  go to the end of it
#             else:
#                 if sub_interval.end_time > new_start_time:
#                     # end time will not be updated here because no operation is done here
#                     new_start_time = sub_interval.end_time
#
#         return remained_required_minutes, end_time
#
#     # ===========================================================================
#     # returns: (remained minutes for the rest of the operation, ending time of the operation in this interval)
#     def assign_operation_in_this_interval(self, resource: 'Resource', operation: 'Operation',
#                                           start_time: datetime.datetime,
#                                           required_minutes: int) -> (int, datetime.datetime):
#
#         # sort the free sub-intervals according to their start times
#         self.free_sub_intervals = sorted(self.free_sub_intervals, key=lambda x: x.start_time)
#
#         # init
#         new_start_time = start_time
#         end_time = start_time
#         remained_required_minutes = required_minutes
#
#         # iterate through the sorted sub intervals
#         for free_sub_interval in self.free_sub_intervals:
#
#             # how much time this interval has?
#             available_minutes = free_sub_interval.remained_minutes_from_now(new_start_time)
#             # any non-trivial time available?
#             if available_minutes >= constants.Constants.MIN_REQUIRED_MINUTES_FOR_AVAILABILITY:
#                 # find the start time
#                 new_start_time = max(new_start_time, free_sub_interval.start_time)
#                 # more than enough time?
#                 if available_minutes > remained_required_minutes:
#                     # bingo! the rest of the operation will be done right here!
#                     end_time = new_start_time + datetime.timedelta(0, remained_required_minutes * 60)
#                     remained_required_minutes = 0
#                 # only part of operation will be done here
#                 else:
#                     # consider part of the operation which will be done in this sub-interval
#                     remained_required_minutes -= available_minutes
#                     # now go to the end of the sub-interval
#                     # record this time as the end time, because some operation is done here
#                     #  and we are not sure if we can do anything more!
#                     end_time = free_sub_interval.end_time
#
#                 # a new sub-interval should be created because operation is done in it
#                 assigned_sub_interval = Interval(operation)
#                 assigned_sub_interval.resource = resource
#                 assigned_sub_interval.start_time = new_start_time
#                 assigned_sub_interval.end_time = end_time
#                 # update assigned sub intervals of the interval
#                 self.assigned_sub_intervals.append(assigned_sub_interval)
#                 # add this sub-interval to the operation intervals
#                 operation.assigned_intervals.append(assigned_sub_interval)
#                 # update the free sub-interval
#                 free_sub_interval.start_time = end_time
#
#                 # all done?
#                 if remained_required_minutes == 0:
#                     break
#
#             # this sub-interval is useless, either is passed or does not have time more than the threshold
#             #  go to the end of it
#             else:
#                 if free_sub_interval.end_time > new_start_time:
#                     # end time will not be updated here because no operation is done here
#                     new_start_time = free_sub_interval.end_time
#
#         # remove the zero length free sub-intervals
#         for i in range(len(self.free_sub_intervals) - 1, -1, -1):
#             if self.free_sub_intervals[i].total_minutes() == 0:
#                 del self.free_sub_intervals[i]
#
#         return remained_required_minutes, end_time
#
#     # ===========================================================================
#     def chop(self):
#         chopped_intervals = []  # type:[SuperInterval]
#
#         # noinspection PyTypeChecker
#         temp_super_interval = SuperInterval(None)
#         temp_super_interval.resource = self.resource
#         temp_super_interval.start_time = self.start_time
#         temp_super_interval.end_time = self.end_time
#
#         while not date.Date.is_same_day(temp_super_interval.start_time.date(), temp_super_interval.end_time.date()):
#             new_end_time = datetime.datetime(temp_super_interval.start_time.year, temp_super_interval.start_time.month,
#                                              temp_super_interval.start_time.day, 23, 59, 59)
#             # noinspection PyTypeChecker
#             chopped_intervals.append(
#                 SuperInterval(None))
#             chopped_intervals[-1].resource = temp_super_interval.resource
#             chopped_intervals[-1].start_time = temp_super_interval.start_time
#             chopped_intervals[-1].end_time = new_end_time
#
#             temp_super_interval.start_time = new_end_time + datetime.timedelta(0, 1)
#
#         chopped_intervals.append(temp_super_interval)
#
#         return chopped_intervals

pass
# # ===========================================================================
# class DeadlinedQuantity:
#     # ===========================================================================
#     def __init__(self):
#         self.quantity = 0  # type: float
#         self.deadline = constants.Constants.MAX_DATE_TIME  # type: datetime.datetime
#         self.hard_deadline = constants.Constants.MAX_DATE_TIME  # type: datetime.datetime

pass


# # ===========================================================================
# class Part2(Part):
#     removed_fields = [Part.version_number]
#     new_int = thing_.IntField(12, 'new int', 'new_int', 0, 100, 55)
#
#

