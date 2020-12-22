from mehdi_lib.generals import general_fields, general_ui_titles, general_editors, general_initial_values, general_enums
from mehdi_lib.basics import editor_, thing_, constants_, basic_types, prototype_, widget_basics
import pytest
from pytestqt.qt_compat import qt_api
from PyQt5 import QtWidgets, QtCore
import typing

pytestmark = pytest.mark.basics

"""
Parameters required for testing EditorDialog
"""

sample_sub_things_ui_titles_en = 'sample sub-things'
sample_sub_things_ui_titles_fa = 'جزءهای نمونه'

sample_sub_things_ui_titles = {
    basic_types.Language.AvailableLanguage.en: sample_sub_things_ui_titles_en,
    basic_types.Language.AvailableLanguage.fa: sample_sub_things_ui_titles_fa,
}

sample_things_ui_titles_en = 'sample things'
sample_things_ui_titles_fa = 'چیزهای نمونه'

sample_things_ui_titles = {
    basic_types.Language.AvailableLanguage.en: sample_things_ui_titles_en,
    basic_types.Language.AvailableLanguage.fa: sample_things_ui_titles_fa,
}


# ===========================================================================
class SuperThingPrototype(prototype_.ThingPrototype):
    pass


# ===========================================================================
class ThingPrototype(prototype_.ThingPrototype):
    pass


# ===========================================================================
class SubThingPrototype(prototype_.ThingPrototype):
    pass


# ===========================================================================
class SuperThing(thing_.Thing):
    """A Thing which has a ListOfThings field for things"""
    name = general_fields.NameField(initial_value=general_initial_values.name)
    things = general_fields.ListField(1, sample_things_ui_titles, 'things', ThingPrototype)


# ===========================================================================
class Thing(thing_.Thing):
    """A Thing which as a ListOfThings field for sub-things"""
    name = general_fields.NameField(initial_value=general_initial_values.name)
    version_number = general_fields.IntField(1, general_ui_titles.version_number, 'version_number', 1,
                                             constants_.Constants.MAX_INT, 1)
    amount_unit = general_fields.EnumField(2, general_ui_titles.amount_unit, 'amount_unit', general_enums.AmountUnit,
                                           general_enums.AmountUnit.number)
    sub_things = general_fields.ListField(11, sample_sub_things_ui_titles, 'sub_things', SubThingPrototype)
    super_thing = general_fields.ForeignKeyField(12, general_ui_titles.dummy, 'thing_parent', ThingPrototype,
                                                 SuperThingPrototype)


# ===========================================================================
class SubThing(thing_.Thing):
    name = general_fields.NameField(initial_value='sub-thing')
    sub_thing_parent = general_fields.ForeignKeyField(1, general_ui_titles.dummy, 'sub_thing_parent',
                                                      SubThingPrototype,
                                                      ThingPrototype)


# ===========================================================================
class Test__Editor__Removing_Reviving_AddingNew:
    """
    For ListOfThing there are currently two types of editors:
        1- tree editor
        2- table editor
    Tests are done for both types whenever applicable.
    If any new editor is added later, tests for that editor should be added too.
    """

    # ===========================================================================
    @staticmethod
    def test_append_new_item(qtbot):
        # ===========================================================================
        def add_to_top_editor(is_top_editor: bool, list_of_things_editor: [typing.Type[general_editors.TreeOfThingsEditor], typing.Type[general_editors.TreeOfThingsEditor]]):
            # list of super-things
            super_things = thing_.ListOfThings(SuperThing)

            # tree editor for list of super-things
            super_things_editor = list_of_things_editor(super_things, None)

            # check adding a new item to the list of super-things (nothing is selected yet)
            super_things_editor.append_new_item(is_top_editor=is_top_editor)
            assert len(super_things_editor.sub_editors) == (1 if is_top_editor else 0)

        # ===========================================================================
        def add_to_non_top_editor(is_top_editor: bool, list_of_things_editor: [typing.Type[general_editors.TreeOfThingsEditor], typing.Type[general_editors.TreeOfThingsEditor]]):

            # list of super-things
            super_things = thing_.ListOfThings(SuperThing)
            # adding one element to the list
            super_thing = SuperThing()
            super_things.append(super_thing)

            # tree editor for list of super-things
            super_things_editor = list_of_things_editor(super_things, None)

            # select the added super-thing to the list of super-things and call append_new_item again.
            #  this time we expect that a new Thing be added to the super-thing[things] field.
            super_things_editor.sub_editors[super_thing].sub_editors[SuperThing.things].set_selected(True)
            super_things_editor.append_new_item(is_top_editor=is_top_editor)
            assert len(super_things_editor.sub_editors) == 1
            assert len(
                super_things_editor.sub_editors[super_thing].sub_editors[SuperThing.things].sub_editors) == 1

        # ===========================================================================
        def add_while_non_list_field_is_selected(is_top_editor: bool, list_of_things_editor: [typing.Type[general_editors.TreeOfThingsEditor], typing.Type[general_editors.TreeOfThingsEditor]]):

            # list of super-things
            super_things = thing_.ListOfThings(SuperThing)
            # adding one element to the list
            super_thing = SuperThing()
            super_things.append(super_thing)

            # tree editor for list of super-things
            super_things_editor = list_of_things_editor(super_things, None)

            # select a non list of things field of the added super-thing to the list of super-things and call
            #  append_new_item. This time we expect that a new Thing be added to super_thing5
            super_things_editor.sub_editors[super_thing].sub_editors[SuperThing.name].set_selected(True)
            super_things_editor.append_new_item(is_top_editor=is_top_editor)
            assert len(super_things_editor.sub_editors) == 2

        # ===========================================================================
        def add_while_non_list_field_in_sub_thing_is_selected(is_top_editor: bool, list_of_things_editor: [typing.Type[general_editors.TreeOfThingsEditor], typing.Type[general_editors.TreeOfThingsEditor]]):

            # list of super-things
            super_things = thing_.ListOfThings(SuperThing)
            # adding one element to the list
            super_thing = SuperThing()
            super_things.append(super_thing)
            # create a thing
            thing = Thing()
            # add the thing to super-thing
            super_thing[SuperThing.things].append(thing)

            # tree editor for list of super-things
            super_things_editor = list_of_things_editor(super_things, None)

            # select a non list of things field of the thing7
            super_things_editor.sub_editors[super_thing].sub_editors[SuperThing.things].sub_editors[
                thing].sub_editors[Thing.name].set_selected(True)
            super_things_editor.append_new_item(is_top_editor=is_top_editor)
            assert len(super_things_editor.sub_editors) == 1
            assert len(
                super_things_editor.sub_editors[super_thing].sub_editors[SuperThing.things].sub_editors) == 2

        # create the application
        assert qt_api.QApplication.instance() is not None

        # **************************************************************
        # 1-adding new item to top editor with is_top_editor set to False
        add_to_top_editor(is_top_editor=False, list_of_things_editor=general_editors.TreeOfThingsEditor)
        add_to_top_editor(is_top_editor=False, list_of_things_editor=general_editors.TableOfThingsEditor)

        # **************************************************************
        # 2-adding new item to top editor with is_top_editor set to True
        add_to_top_editor(is_top_editor=True, list_of_things_editor=general_editors.TreeOfThingsEditor)
        add_to_top_editor(is_top_editor=True, list_of_things_editor=general_editors.TableOfThingsEditor)

        # **************************************************************
        # 3-adding new item to list of things editor which is not top editor with is_top_editor set to True
        # This scenario is not applicable to TableOfThingsEditor
        add_to_non_top_editor(True, list_of_things_editor=general_editors.TreeOfThingsEditor)

        # **************************************************************
        # 4-adding new item to list of things editor which is not top editor with is_top_editor set to False
        # This scenario is not applicable to TableOfThingsEditor
        add_to_non_top_editor(False, list_of_things_editor=general_editors.TreeOfThingsEditor)

        # **************************************************************
        # 5-adding new item while a non list of things field is selected with is_top_editor set to True
        #  select a non list of things field in super-thing and call append_new_item
        #  this time we expect that a new super-thing be added to the list of super-things
        # This scenario is not applicable to TableOfThingsEditor
        add_while_non_list_field_is_selected(True, list_of_things_editor=general_editors.TreeOfThingsEditor)

        # **************************************************************
        # 6-adding new item while a non list of things field is selected with is_top_editor set to False
        #  select a non list of things field in super-thing and call append_new_item
        #  this time we expect that a new super-thing be added to the list of super-things
        # This scenario is not applicable to TableOfThingsEditor
        add_while_non_list_field_is_selected(False, list_of_things_editor=general_editors.TreeOfThingsEditor)

        # **************************************************************
        # 7-adding new item while a non list of things field is selected in thing (not super-thing) with is_top_editor
        #  set to True
        # This scenario is not applicable to TableOfThingsEditor
        add_while_non_list_field_in_sub_thing_is_selected(True, list_of_things_editor=general_editors.TreeOfThingsEditor)

        # **************************************************************
        # 8-adding new item while a non list of things field is selected in thing (not super-thing) with is_top_editor
        #  set to False
        # This scenario is not applicable to TableOfThingsEditor
        add_while_non_list_field_in_sub_thing_is_selected(False, list_of_things_editor=general_editors.TreeOfThingsEditor)

    # ===========================================================================
    @staticmethod
    def test_mark_selected_sub_editor_for_removal(qtbot):
        # ===========================================================================
        def one_thing_with_one_sub_editor(list_of_things_editor: [typing.Type[general_editors.TreeOfThingsEditor], typing.Type[general_editors.TreeOfThingsEditor]]):

            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing = SuperThing()
            super_things.append(super_thing)

            # create a list of things editor
            super_things_editor = list_of_things_editor(super_things, None)

            # select an element inside the list
            sub_editor = super_things_editor.sub_editors[super_thing]
            sub_editor.set_selected(True)

            # mark it for removal and check the signal emissions
            with qtbot.wait_signal(super_things_editor.sub_editor_marked_for_removal_exists_signal, raising=True), \
                 qtbot.wait_signal(sub_editor.parent_editor.value_changed_by_me_signal, raising=True):
                super_things_editor.mark_selected_sub_editor_for_removal(is_top_editor=True)

            # check marked for removal
            assert sub_editor.is_marked_for_removal()
            # check presence of sub-editor in marked-for-removal list
            assert sub_editor in super_things_editor.sub_editors_marked_for_removal
            # check connected signal
            sub_editor.no_revival_possible_signal.disconnect(super_things_editor.sub_editor_revived_or_removed)

        # ===========================================================================
        def one_thing_with_two_sub_editors(list_of_things_editor: [typing.Type[general_editors.TreeOfThingsEditor], typing.Type[general_editors.TreeOfThingsEditor]]):
            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing_1 = SuperThing()
            super_thing_2 = SuperThing()
            super_things.append(super_thing_1)
            super_things.append(super_thing_2)

            # create a list of things editor
            super_things_editor = list_of_things_editor(super_things, None)

            # select an element inside the list
            previous_state = editor_.Editor__Selection.multiple_selection
            editor_.Editor__Selection.multiple_selection = True
            sub_editor_1 = super_things_editor.sub_editors[super_thing_1]
            sub_editor_2 = super_things_editor.sub_editors[super_thing_2]
            sub_editor_1.set_selected(True)
            sub_editor_2.set_selected(True)

            # mark it for removal and check the signal emissions
            with qtbot.wait_signal(super_things_editor.sub_editor_marked_for_removal_exists_signal, raising=True), \
                 qtbot.wait_signal(sub_editor_1.parent_editor.value_changed_by_me_signal, raising=True), \
                 qtbot.wait_signal(sub_editor_2.parent_editor.value_changed_by_me_signal, raising=True):
                super_things_editor.mark_selected_sub_editor_for_removal(is_top_editor=True)

            # check marked for removal
            assert sub_editor_1.is_marked_for_removal()
            assert sub_editor_2.is_marked_for_removal()

            # check presence of sub-editor in marked-for-removal list
            assert sub_editor_1 in super_things_editor.sub_editors_marked_for_removal
            assert sub_editor_2 in super_things_editor.sub_editors_marked_for_removal

            # check connected signal
            sub_editor_1.no_revival_possible_signal.disconnect(super_things_editor.sub_editor_revived_or_removed)
            sub_editor_2.no_revival_possible_signal.disconnect(super_things_editor.sub_editor_revived_or_removed)

            editor_.Editor__Selection.multiple_selection = previous_state

        # ===========================================================================
        def one_thing_with_one_sub_editor_and_one_sub_sub_editor(list_of_things_editor: [typing.Type[general_editors.TreeOfThingsEditor], typing.Type[general_editors.TreeOfThingsEditor]]):

            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing = SuperThing()
            super_things.append(super_thing)
            thing = Thing()
            super_thing[SuperThing.things].append(thing)

            # create a list of things editor
            super_things_editor = list_of_things_editor(super_things, None)

            # select an element inside the list
            sub_editor = super_things_editor.sub_editors[super_thing].sub_editors[SuperThing.things].sub_editors[
                thing]
            sub_editor.set_selected(True)

            # mark it for removal and check the signal emissions
            with qtbot.wait_signal(super_things_editor.sub_editor_marked_for_removal_exists_signal, raising=True), \
                 qtbot.wait_signal(sub_editor.parent_editor.value_changed_by_me_signal, raising=True):
                super_things_editor.mark_selected_sub_editor_for_removal(is_top_editor=True)

            # check marked for removal
            assert sub_editor.is_marked_for_removal()

            # check presence of sub-editor in marked-for-removal list
            assert sub_editor in super_things_editor.sub_editors_marked_for_removal

            # check connected signal
            sub_editor.no_revival_possible_signal.disconnect(super_things_editor.sub_editor_revived_or_removed)

            # check selection of the sibling or parent
            assert super_things_editor.sub_editors[super_thing].sub_editors[SuperThing.things].is_selected(
                go_deep=False)

        # create the application
        assert qt_api.QApplication.instance() is not None

        # **************************************************************
        # 1-simplest state. one thing with one selected sub-editor
        one_thing_with_one_sub_editor(list_of_things_editor=general_editors.TreeOfThingsEditor)
        one_thing_with_one_sub_editor(list_of_things_editor=general_editors.TableOfThingsEditor)

        # **************************************************************
        # 2-select two sub-editors for removal
        one_thing_with_two_sub_editors(list_of_things_editor=general_editors.TreeOfThingsEditor)
        one_thing_with_two_sub_editors(list_of_things_editor=general_editors.TableOfThingsEditor)

        # **************************************************************
        # 3-select sub-sub-editor for removal
        # This scenario is not applicable to TableOfThingsEditor
        one_thing_with_one_sub_editor_and_one_sub_sub_editor(list_of_things_editor=general_editors.TreeOfThingsEditor)

    # ===========================================================================
    @staticmethod
    def test_sub_editor_revived_or_removed(qtbot):
        # ===========================================================================
        def remove_marked_sub_editor(list_of_things_editor: [typing.Type[general_editors.TreeOfThingsEditor], typing.Type[general_editors.TreeOfThingsEditor]]):
            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing = SuperThing()
            super_things.append(super_thing)

            # create a list of things editor
            super_things_editor = list_of_things_editor(super_things, None)

            # select an element inside the list
            sub_editor = super_things_editor.sub_editors[super_thing]
            sub_editor.set_selected(True)

            # mark it for removal
            super_things_editor.mark_selected_sub_editor_for_removal(is_top_editor=True)

            # marked sub-editor should be in the sub_editors_marked_for_removal at first
            assert sub_editor in super_things_editor.sub_editors_marked_for_removal
            # as this is the only marked sub-editor, the no revival possible signal should be emitted.
            with qtbot.wait_signal(super_things_editor.no_sub_editor_marked_for_removal_exists_signal,
                                   raising=True):
                super_things_editor.remove_sub_editor(super_thing)
            # marked sub-editor should not be in the sub-editors-marked-for-removal any more
            assert sub_editor not in super_things_editor.sub_editors_marked_for_removal

        # ===========================================================================
        def revive_marked_sub_editor(list_of_things_editor: [typing.Type[general_editors.TreeOfThingsEditor], typing.Type[general_editors.TreeOfThingsEditor]]):
            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing = SuperThing()
            super_things.append(super_thing)

            # create a list of things editor
            super_things_editor = list_of_things_editor(super_things, None)

            # select an element inside the list
            sub_editor = super_things_editor.sub_editors[super_thing]
            sub_editor.set_selected(True)

            # mark it for removal
            super_things_editor.mark_selected_sub_editor_for_removal(is_top_editor=True)

            # marked sub-editor should be in the sub_editors_marked_for_removal at first
            assert sub_editor in super_things_editor.sub_editors_marked_for_removal
            # as this is the only marked sub-editor, the no revival possible signal should be emitted.
            with qtbot.wait_signal(super_things_editor.no_sub_editor_marked_for_removal_exists_signal,
                                   raising=True):
                super_things_editor.sub_editors[super_thing].set_marked_for_removal(mark_for_removal=False)
            # marked sub-editor should not be in the sub-editors-marked-for-removal any more
            assert sub_editor not in super_things_editor.sub_editors_marked_for_removal

        # create the application
        assert qt_api.QApplication.instance() is not None

        remove_marked_sub_editor(list_of_things_editor=general_editors.TreeOfThingsEditor)
        remove_marked_sub_editor(list_of_things_editor=general_editors.TableOfThingsEditor)

        revive_marked_sub_editor(list_of_things_editor=general_editors.TreeOfThingsEditor)
        revive_marked_sub_editor(list_of_things_editor=general_editors.TableOfThingsEditor)

    # ===========================================================================
    @staticmethod
    def test_revive_the_latest_sub_editor_marked_for_removal(qtbot):
        # ===========================================================================
        def remove_and_revive(list_of_things_editor: [typing.Type[general_editors.TreeOfThingsEditor], typing.Type[general_editors.TreeOfThingsEditor]]):
            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing_1 = SuperThing()
            super_thing_2 = SuperThing()
            super_things.append(super_thing_1)
            super_things.append(super_thing_2)

            # create a list of things editor
            super_things_editor = list_of_things_editor(super_things, None)

            # select an element inside the list and mark it for removal
            sub_editor_1 = super_things_editor.sub_editors[super_thing_1]
            sub_editor_1.set_selected(True)
            super_things_editor.mark_selected_sub_editor_for_removal(is_top_editor=True)

            # select an element inside the list and mark it for removal
            sub_editor_2 = super_things_editor.sub_editors[super_thing_2]
            sub_editor_2.set_selected(True)
            super_things_editor.mark_selected_sub_editor_for_removal(is_top_editor=True)

            # check marked for removal
            assert sub_editor_1.is_marked_for_removal()
            assert sub_editor_2.is_marked_for_removal()

            # revive the last removed one
            with qtbot.wait_signal(super_things_editor.value_changed_by_me_signal):
                super_things_editor.revive_the_latest_sub_editor_marked_for_removal()

            # check for the result
            assert sub_editor_1.is_marked_for_removal()
            assert not sub_editor_2.is_marked_for_removal()

            # check for selection
            assert sub_editor_2.is_selected(go_deep=False)

            # revive the last removed one again
            with qtbot.wait_signal(super_things_editor.value_changed_by_me_signal), \
                 qtbot.wait_signal(super_things_editor.no_sub_editor_marked_for_removal_exists_signal):
                super_things_editor.revive_the_latest_sub_editor_marked_for_removal()

            # check for the result
            assert not sub_editor_1.is_marked_for_removal()

            # check for selection
            assert sub_editor_1.is_selected(go_deep=False)
            assert not sub_editor_2.is_selected(go_deep=False)

        # create the application
        assert qt_api.QApplication.instance() is not None

        remove_and_revive(list_of_things_editor=general_editors.TreeOfThingsEditor)
        remove_and_revive(list_of_things_editor=general_editors.TableOfThingsEditor)


# ===========================================================================
class Test__Editor__Selection:

    # ===========================================================================
    @staticmethod
    def test_eventFilter(qtbot):
        # ===========================================================================
        def multiple_selection(list_of_things_editor: typing.Type[editor_.Editor]):
            assert not editor_.Editor__Selection.multiple_selection
            editor = list_of_things_editor(thing_.ListOfThings(SuperThing), None)
            qtbot.add_widget(editor.widget)

            # control key
            qtbot.keyPress(editor.widget, qt_api.Qt.Key.Key_Control)
            assert editor_.Editor__Selection.multiple_selection
            qtbot.keyRelease(editor.widget, qt_api.Qt.Key.Key_Control)
            assert not editor_.Editor__Selection.multiple_selection

            # shift key
            qtbot.keyPress(editor.widget, qt_api.Qt.Key.Key_Shift)
            assert editor_.Editor__Selection.multiple_selection
            qtbot.keyRelease(editor.widget, qt_api.Qt.Key.Key_Shift)
            assert not editor_.Editor__Selection.multiple_selection

        # create the application
        assert qt_api.QApplication.instance() is not None
        multiple_selection(list_of_things_editor=general_editors.TreeOfThingsEditor)
        multiple_selection(list_of_things_editor=general_editors.TableOfThingsEditor)

    # ===========================================================================
    @staticmethod
    def test_is_selected(qtbot):

        # ===========================================================================
        def select_editor(list_of_things_editor: typing.Type[editor_.Editor]):

            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing = SuperThing()
            super_things.append(super_thing)

            # create a list of things editor
            super_things_editor = list_of_things_editor(super_things, None)

            # select an element inside the list
            sub_editor = super_things_editor.sub_editors[super_thing]
            sub_editor.set_selected(True)

            # check selections
            assert super_things_editor.is_selected(go_deep=True)
            assert not super_things_editor.is_selected(go_deep=False)
            assert sub_editor.is_selected(go_deep=True)
            assert sub_editor.is_selected(go_deep=False)

        # ===========================================================================
        def select_editor_widget(list_of_things_editor: typing.Type[editor_.Editor]):

            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing = SuperThing()
            super_things.append(super_thing)

            # create a list of things editor
            super_things_editor = list_of_things_editor(super_things, None)

            # select an element inside the list
            sub_editor = super_things_editor.sub_editors[super_thing]
            sub_editor.widget.set_selected(True)

            # check selections
            assert super_things_editor.is_selected(go_deep=True)
            assert not super_things_editor.is_selected(go_deep=False)
            assert sub_editor.is_selected(go_deep=True)
            assert sub_editor.is_selected(go_deep=False)

        # ===========================================================================
        def select_sub_editor():

            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing = SuperThing()
            super_things.append(super_thing)
            thing = Thing()
            super_thing[SuperThing.things].append(thing)

            # create a list of things editor
            super_things_tree_editor = general_editors.TreeOfThingsEditor(super_things, None)

            # select the sub-thing
            sub_editor = super_things_tree_editor.sub_editors[super_thing].sub_editors[SuperThing.things].sub_editors[thing]
            sub_editor.set_selected(True)

            # check selections
            assert super_things_tree_editor.is_selected(go_deep=True)
            assert not super_things_tree_editor.is_selected(go_deep=False)

        # ===========================================================================
        def select_sub_editor_widget():

            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing = SuperThing()
            super_things.append(super_thing)
            thing = Thing()
            super_thing[SuperThing.things].append(thing)

            # create a list of things editor
            super_things_tree_editor = general_editors.TreeOfThingsEditor(super_things, None)

            # select the sub-thing
            sub_editor = super_things_tree_editor.sub_editors[super_thing].sub_editors[SuperThing.things].sub_editors[thing]
            sub_editor.widget.set_selected(True)

            # check selections
            assert super_things_tree_editor.is_selected(go_deep=True)
            assert not super_things_tree_editor.is_selected(go_deep=False)

        # create the application
        assert qt_api.QApplication.instance() is not None

        select_editor(list_of_things_editor=general_editors.TreeOfThingsEditor)
        select_editor(list_of_things_editor=general_editors.TableOfThingsEditor)

        # table editor widget does not need selection!
        select_editor_widget(list_of_things_editor=general_editors.TreeOfThingsEditor)

        select_sub_editor()
        select_sub_editor_widget()

    # ===========================================================================
    @staticmethod
    def test_set_selected(qtbot):

        # ===========================================================================
        def create_super_things_and_editors(list_of_things_editor_type: [typing.Type[general_editors.TreeOfThingsEditor], typing.Type[general_editors.TableOfThingsEditor]]) -> (typing.List[SuperThing], typing.List[editor_.Editor]):
            """Creates required things and editors

            three super things will be created and added to a list of things

            :param list_of_things_editor_type: [typing.Type[general_editors.TreeOfThingsEditor], typing.Type[general_editors.TableOfThingsEditor]]
            :return: (typing.List[SuperThing], typing.List[editor_.Editor])
                the first list contains things, and the second list contains editors
                the first element of the first list is list of things
                the first element of the second list is list of things editor
            """

            super_things = thing_.ListOfThings(SuperThing)
            super_thing_1 = SuperThing()
            super_things.append(super_thing_1)
            super_thing_2 = SuperThing()
            super_things.append(super_thing_2)
            super_thing_3 = SuperThing()
            super_things.append(super_thing_3)

            # create a list of things editor
            super_things_editor = list_of_things_editor_type(super_things, None)
            super_thing_1_editor = super_things_editor.sub_editors[super_thing_1]
            super_thing_2_editor = super_things_editor.sub_editors[super_thing_2]
            super_thing_3_editor = super_things_editor.sub_editors[super_thing_3]

            return ([super_things, super_thing_1, super_thing_2, super_thing_3],
                    [super_things_editor, super_thing_1_editor, super_thing_2_editor, super_thing_3_editor])

        # ===========================================================================
        def center(editor: typing.Type[editor_.Editor], super_thing: SuperThing, thing: Thing = None) -> QtCore.QPoint:
            """returns center position of the widget for clicking.

            this method is used only for tree editor.
            in table editor clicking is done in another way.

            :param editor: typing.Type[editor_.Editor]
                the main editor
            :param super_thing: SuperThing
                level one element of the editor
            :param thing: Thing
                level two element of the editor
            :return: QtCore.QPoint
                center point of the widget
            """

            # level one widget
            if thing is None:
                item = editor.sub_editors[super_thing].widget.tree_item
            # level two widget
            else:
                editor.widget.expandAll()
                item = editor.sub_editors[super_thing].sub_editors[SuperThing.things].sub_editors[thing].widget.tree_item
            rect = editor.widget.visualItemRect(item)
            return rect.center()

        # ===========================================================================
        def click(editor: [general_editors.TreeOfThingsEditor, general_editors.TableOfThingsEditor], super_thing: SuperThing, modifier=None):
            """clicks inside editor on the specified thing

            :param editor: [general_editors.TreeOfThingsEditor, general_editors.TableOfThingsEditor]
                the editor inside which click should be performed.
            :param super_thing: SuperThing
                the super-thing on which click should be done.
            :param modifier: int
                specified the modifier key of the keyboard during click
            :return: None
            """

            # with modifier
            if modifier is not None:

                # tree editor
                if type(editor) is general_editors.TreeOfThingsEditor:
                    qtbot.mouseClick(editor.widget.viewport(), QtCore.Qt.LeftButton, modifier=modifier, pos=center(editor, super_thing))

                # table editor
                else:
                    qtbot.mouseClick(editor.sub_editors[super_thing].sub_editors[SuperThing.name].widget, QtCore.Qt.LeftButton, modifier=modifier)

            # no modifier
            else:

                # tree editor
                if type(editor) is general_editors.TreeOfThingsEditor:
                    qtbot.mouseClick(editor.widget.viewport(), QtCore.Qt.LeftButton, pos=center(editor, super_thing))

                # table editor
                else:
                    qtbot.mouseClick(editor.sub_editors[super_thing].sub_editors[SuperThing.name].widget, QtCore.Qt.LeftButton)

        # ===========================================================================
        def single_selection(list_of_things_editor: typing.Type[editor_.Editor]):

            # create
            super_things, editors = create_super_things_and_editors(list_of_things_editor)

            # initial check
            assert not editors[1].is_selected(go_deep=False)
            assert not editors[2].is_selected(go_deep=False)
            assert not editors[3].is_selected(go_deep=False)

            # select one item
            click(editors[0], super_things[1])
            assert editors[1].is_selected(go_deep=False)
            assert not editors[2].is_selected(go_deep=False)
            assert not editors[3].is_selected(go_deep=False)

            # select another item, the first selected item should be deselected
            click(editors[0], super_things[3])
            assert not editors[1].is_selected(go_deep=False)
            assert not editors[2].is_selected(go_deep=False)
            assert editors[3].is_selected(go_deep=False)

        # ===========================================================================
        def multiple_selection_ctl(list_of_things_editor: typing.Type[editor_.Editor]):

            # create
            super_things, editors = create_super_things_and_editors(list_of_things_editor)

            # initial check
            assert not editors[1].is_selected(go_deep=False)
            assert not editors[2].is_selected(go_deep=False)
            assert not editors[3].is_selected(go_deep=False)

            # first item
            click(editors[0], super_things[1])

            # press control
            qtbot.keyPress(editors[0].widget, QtCore.Qt.Key_Control)

            # second item
            click(editors[0], super_things[3], QtCore.Qt.ControlModifier)

            # release control
            qtbot.keyRelease(editors[0].widget, QtCore.Qt.Key_Control)

            assert editors[1].is_selected(go_deep=False)
            assert not editors[2].is_selected(go_deep=False)
            assert editors[3].is_selected(go_deep=False)

        # ===========================================================================
        def multiple_selection_shift(list_of_things_editor: typing.Type[editor_.Editor]):

            # create
            super_things, editors = create_super_things_and_editors(list_of_things_editor)

            # initial check
            assert not editors[1].is_selected(go_deep=False)
            assert not editors[2].is_selected(go_deep=False)
            assert not editors[3].is_selected(go_deep=False)

            # first item
            click(editors[0], super_things[1])

            # press shift
            qtbot.keyPress(editors[0].widget, QtCore.Qt.Key_Shift)

            # next item
            click(editors[0], super_things[3], QtCore.Qt.ShiftModifier)

            # release shift
            qtbot.keyRelease(editors[0].widget, QtCore.Qt.Key_Shift)

            # tree editor
            if list_of_things_editor is general_editors.TreeOfThingsEditor:

                # all three items should be selected
                assert editors[1].is_selected(go_deep=False)
                assert editors[2].is_selected(go_deep=False)
                assert editors[3].is_selected(go_deep=False)

            # table editor
            else:

                # currently, for table editor, list selection is not working!
                assert editors[1].is_selected(go_deep=False)
                # assert editors[2].is_selected(go_deep=False)
                assert editors[3].is_selected(go_deep=False)

        # ===========================================================================
        def selecting_child_while_parent_is_selected():
            """
            this method works only for tree editor.
            in table editor parent and child are not simultaneously visible.
            :return:
            """

            # prepare things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing = SuperThing()
            super_things.append(super_thing)
            thing = Thing()
            super_thing[SuperThing.things].append(thing)

            # create a list of things editor
            super_things_tree_editor = general_editors.TreeOfThingsEditor(super_things, None)
            super_thing_editor = super_things_tree_editor.sub_editors[super_thing]
            thing_editor = super_thing_editor.sub_editors[SuperThing.things].sub_editors[thing]

            # calculate centers
            super_thing_center = center(super_things_tree_editor, super_thing)
            thing_center = center(super_things_tree_editor, super_thing, thing)

            tree_widget = super_things_tree_editor.widget

            # click on parent
            qtbot.mouseClick(tree_widget.viewport(), QtCore.Qt.LeftButton, pos=super_thing_center)
            assert super_thing_editor.is_selected(go_deep=False)
            assert not thing_editor.is_selected(go_deep=False)

            # click on child
            qtbot.mouseClick(tree_widget.viewport(), QtCore.Qt.LeftButton, pos=thing_center)
            assert thing_editor.is_selected(go_deep=False)
            assert not super_thing_editor.is_selected(go_deep=False)

            # now pressing control
            qtbot.mouseClick(tree_widget.viewport(), QtCore.Qt.LeftButton, pos=super_thing_center)
            assert super_thing_editor.is_selected(go_deep=False)
            assert not thing_editor.is_selected(go_deep=False)
            qtbot.keyPress(tree_widget, QtCore.Qt.Key_Control)
            qtbot.mouseClick(tree_widget.viewport(), QtCore.Qt.LeftButton, modifier=QtCore.Qt.ControlModifier, pos=thing_center)
            qtbot.keyRelease(tree_widget, QtCore.Qt.Key_Control)
            assert super_thing_editor.is_selected(go_deep=False)
            assert thing_editor.is_selected(go_deep=False)

        # create the application
        assert qt_api.QApplication.instance() is not None

        # single
        single_selection(list_of_things_editor=general_editors.TreeOfThingsEditor)
        single_selection(list_of_things_editor=general_editors.TableOfThingsEditor)

        # control
        multiple_selection_ctl(list_of_things_editor=general_editors.TreeOfThingsEditor)
        multiple_selection_ctl(list_of_things_editor=general_editors.TableOfThingsEditor)

        # shift
        multiple_selection_shift(list_of_things_editor=general_editors.TreeOfThingsEditor)
        multiple_selection_shift(list_of_things_editor=general_editors.TableOfThingsEditor)

        # parent, child
        selecting_child_while_parent_is_selected()

    # ===========================================================================
    @staticmethod
    def test_selected_item_editor(qtbot):

        # ===========================================================================
        def select_item_editor(list_of_things_editor_type: [typing.Type[general_editors.TreeOfThingsEditor], typing.Type[general_editors.TableOfThingsEditor]]):

            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing = SuperThing()
            super_things.append(super_thing)
            thing = Thing()
            super_thing[SuperThing.things].append(thing)

            # create a list of things editor
            super_things_editor = list_of_things_editor_type(super_things, None)

            super_things_editor.set_selected(True)
            assert super_things_editor.selected_item_editor() == super_things_editor

            super_things_editor.set_selected(False)
            if list_of_things_editor_type == general_editors.TreeOfThingsEditor:
                editor = super_things_editor.sub_editors[super_thing].sub_editors[SuperThing.things].sub_editors[thing]
            else:
                editor = super_things_editor.sub_editors[super_thing]
            editor.set_selected(True)
            assert super_things_editor.selected_item_editor() == editor

        # create the application
        assert qt_api.QApplication.instance() is not None

        select_item_editor(general_editors.TreeOfThingsEditor)
        select_item_editor(general_editors.TableOfThingsEditor)

    # ===========================================================================
    @staticmethod
    def test_select_the_first_sibling_not_marked_for_removal_or_parent(qtbot):

        # ===========================================================================
        def create_remove_test_selection(list_of_things_editor_type: [typing.Type[general_editors.TreeOfThingsEditor], typing.Type[general_editors.TableOfThingsEditor]]):

            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing = SuperThing()
            super_things.append(super_thing)
            thing_1 = Thing()
            super_thing[SuperThing.things].append(thing_1)
            thing_2 = Thing()
            super_thing[SuperThing.things].append(thing_2)
            thing_3 = Thing()
            super_thing[SuperThing.things].append(thing_3)

            # tree editor
            if list_of_things_editor_type == general_editors.TreeOfThingsEditor:
                super_things_editor = list_of_things_editor_type(super_things, None)
                super_thing_editor = super_things_editor.sub_editors[super_thing]
                things_editor = super_thing_editor.sub_editors[SuperThing.things]
            # table editor
            else:
                things_editor = list_of_things_editor_type(super_thing, SuperThing.things)

            thing_1_editor = things_editor.sub_editors[thing_1]
            thing_2_editor = things_editor.sub_editors[thing_2]
            thing_3_editor = things_editor.sub_editors[thing_3]

            # remove thing 2
            thing_2_editor.set_marked_for_removal(True)
            assert not things_editor.is_selected(go_deep=False)
            assert not thing_1_editor.is_selected(go_deep=False)
            assert not thing_3_editor.is_selected(go_deep=False)

            # select sibling
            thing_2_editor.select_the_first_sibling_not_marked_for_removal_or_parent()
            assert not things_editor.is_selected(go_deep=False)
            assert not thing_1_editor.is_selected(go_deep=False)
            assert not thing_2_editor.is_selected(go_deep=False)
            assert thing_3_editor.is_selected(go_deep=False)

            # remove thing 3
            thing_3_editor.set_marked_for_removal(True)
            assert not things_editor.is_selected(go_deep=False)
            assert not thing_1_editor.is_selected(go_deep=False)

            # select sibling
            thing_3_editor.select_the_first_sibling_not_marked_for_removal_or_parent()
            assert not things_editor.is_selected(go_deep=False)
            assert thing_1_editor.is_selected(go_deep=False)
            assert not thing_2_editor.is_selected(go_deep=False)
            assert not thing_3_editor.is_selected(go_deep=False)

            # remove thing 1
            thing_1_editor.set_marked_for_removal(True)
            assert not things_editor.is_selected(go_deep=False)

            # select sibling (for tree editor, parent will be selected this time)
            thing_1_editor.select_the_first_sibling_not_marked_for_removal_or_parent()
            if list_of_things_editor_type == general_editors.TreeOfThingsEditor:
                assert things_editor.is_selected(go_deep=False)
            assert not thing_1_editor.is_selected(go_deep=False)
            assert not thing_2_editor.is_selected(go_deep=False)
            assert not thing_3_editor.is_selected(go_deep=False)

        # create the application
        assert qt_api.QApplication.instance() is not None

        create_remove_test_selection(general_editors.TreeOfThingsEditor)
        create_remove_test_selection(general_editors.TableOfThingsEditor)

    # ===========================================================================
    @staticmethod
    def test_sub_editor_selected(qtbot):

        # ===========================================================================
        def perform_the_test(list_of_things_editor_type: [typing.Type[general_editors.TreeOfThingsEditor], typing.Type[general_editors.TableOfThingsEditor]]):

            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing = SuperThing()
            super_things.append(super_thing)
            thing = Thing()
            super_thing[SuperThing.things].append(thing)

            # create a list of things editor
            super_things_editor = list_of_things_editor_type(super_things, None)
            sub_editor_1 = super_things_editor.sub_editors[super_thing]

            # sub_editor_2 is used only for tree editor
            sub_editor_2 = None
            if list_of_things_editor_type == general_editors.TreeOfThingsEditor:
                sub_editor_2 = sub_editor_1.sub_editors[SuperThing.things].sub_editors[thing]

            # select
            if sub_editor_2 is not None:
                with qtbot.wait_signal(sub_editor_1.sub_editor_selected_signal, raising=True), \
                     qtbot.wait_signal(super_things_editor.sub_editor_selected_signal, raising=True):
                    sub_editor_2.set_selected(True)
                    assert sub_editor_2 in sub_editor_1.selected_sub_editors and sub_editor_2 in super_things_editor.selected_sub_editors
            else:
                with qtbot.wait_signal(super_things_editor.sub_editor_selected_signal, raising=True):
                    sub_editor_1.set_selected(True)
                    assert sub_editor_1 in super_things_editor.selected_sub_editors

        perform_the_test(general_editors.TreeOfThingsEditor)
        perform_the_test(general_editors.TableOfThingsEditor)

    # ===========================================================================
    @staticmethod
    def test_sub_editor_deselected(qtbot):

        # ===========================================================================
        def perform_the_test(list_of_things_editor_type: [typing.Type[general_editors.TreeOfThingsEditor], typing.Type[general_editors.TableOfThingsEditor]]):

            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing = SuperThing()
            super_things.append(super_thing)
            thing = Thing()
            super_thing[SuperThing.things].append(thing)

            # create a list of things editor
            super_things_editor = list_of_things_editor_type(super_things, None)
            sub_editor_1 = super_things_editor.sub_editors[super_thing]

            # sub_editor_2 is used only for tree editor
            sub_editor_2 = None
            if list_of_things_editor_type == general_editors.TreeOfThingsEditor:
                sub_editor_2 = sub_editor_1.sub_editors[SuperThing.things].sub_editors[thing]

            if sub_editor_2 is not None:
                sub_editor_2.set_selected(True)
                with qtbot.wait_signal(sub_editor_1.no_sub_editor_selected_signal, raising=True), \
                     qtbot.wait_signal(super_things_editor.no_sub_editor_selected_signal, raising=True):
                    sub_editor_2.set_selected(False)
                    assert sub_editor_2 not in sub_editor_1.selected_sub_editors and sub_editor_2 not in super_things_editor.selected_sub_editors
            else:
                sub_editor_1.set_selected(True)
                with qtbot.wait_signal(super_things_editor.no_sub_editor_selected_signal, raising=True):
                    sub_editor_1.set_selected(False)
                    assert sub_editor_1 not in super_things_editor.selected_sub_editors

        perform_the_test(general_editors.TreeOfThingsEditor)
        perform_the_test(general_editors.TableOfThingsEditor)


# ===========================================================================
class Test__Editor__Basics:

    # ===========================================================================
    @staticmethod
    def test_init(qtbot):
        super_thing = SuperThing()
        super_things = thing_.ListOfThings(SuperThing)

        # thing editor
        editor_1 = general_editors.ThingEditor(super_thing, None)
        assert editor_1.representing_object == super_thing
        assert editor_1.type == editor_.EditorTypes.thing

        # field editor (non-list-field)
        editor_2 = general_editors.NameEditor(super_thing, SuperThing.name)
        assert editor_2.representing_object == super_thing
        assert editor_2.type == editor_.EditorTypes.field_of_thing

        # field editor (list-field)
        editor_3 = general_editors.TreeOfThingsEditor(super_thing, SuperThing.things)
        assert editor_3.representing_object == super_thing[SuperThing.things]
        assert editor_3.type == editor_.EditorTypes.list_of_things

        # independent list-field editor
        editor_4 = general_editors.TableOfThingsEditor(super_things, None)
        assert editor_4.representing_object == super_things
        assert editor_4.type == editor_.EditorTypes.list_of_things

    # ===========================================================================
    @staticmethod
    def test_representing_object_editors(qtbot):
        super_thing = SuperThing()
        super_things = thing_.ListOfThings(SuperThing)

        # thing editor
        editor_1 = general_editors.ThingEditor(super_thing, None)
        assert editor_1 in editor_1.representing_object_editors()

        # field editor (non-list-field)
        editor_2 = general_editors.NameEditor(super_thing, SuperThing.name)
        assert editor_2 in editor_2.representing_object_editors()

        # field editor (list-field)
        editor_3 = general_editors.TreeOfThingsEditor(super_thing, SuperThing.things)
        assert editor_3 in editor_3.representing_object_editors()

        # independent list-field editor
        editor_4 = general_editors.TableOfThingsEditor(super_things, None)
        assert editor_4 in editor_4.representing_object_editors()


# ===========================================================================
class Test__Editor__Dependency:

    # ===========================================================================
    @staticmethod
    @pytest.mark.current
    def test_(qtbot):
        super_thing = SuperThing()
        super_things = thing_.ListOfThings(SuperThing)


# ===========================================================================
class TestEditorDialog:
    """Prepares required methods for testing EditorDialog"""

    # ===========================================================================
    @staticmethod
    def test_init(qtbot):
        """Checks correct operation of all the things done in __init__ method"""

        # create the application
        assert qt_api.QApplication.instance() is not None

        # first check the field editor
        thing = Thing()
        editor = general_editors.NameEditor(thing, Thing.name)
        dialog = editor_.EditorDialog(editor, automatic_unregister=False)

        # check the title
        assert dialog.windowTitle() == editor_.EditorDialog.create_full_name_for_editor_title(editor)

        # check name for list editor
        editor = general_editors.TableOfThingsEditor(thing, Thing.sub_things)
        dialog = editor_.EditorDialog(editor, automatic_unregister=False)
        assert dialog.windowTitle() == 'نام 1: ' + sample_sub_things_ui_titles[
            basic_types.Language.get_active_language()]

        # check edit button and revive button (should be present in the dialog and should be disabled)
        widgets = list(dialog.header_layout.itemAt(i).widget() for i in range(dialog.header_layout.count()))
        assert dialog.edit_button in widgets
        assert not dialog.edit_button.isEnabled()
        assert dialog.revive_button in widgets
        assert not dialog.revive_button.isEnabled()

        # check new button and del button (should be present in the dialog)
        names = list(
            widgets[i].text() if isinstance(widgets[i], widget_basics.Button) else None for i in range(len(widgets)))
        assert general_ui_titles.new[basic_types.Language.get_active_language()] in names
        assert general_ui_titles.delete[basic_types.Language.get_active_language()] in names

    # TODO: create tests for accept, reject, and __del__ methods.
