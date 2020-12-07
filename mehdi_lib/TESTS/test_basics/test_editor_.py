from mehdi_lib.generals import general_fields, general_ui_titles, general_editors, general_initial_values, general_enums
from mehdi_lib.basics import editor_, thing_, constants_, basic_types, prototype_, widget_basics
import pytest
from pytestqt.qt_compat import qt_api


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
    version_number = general_fields.IntField(1, general_ui_titles.version_number, 'version_number', 1, constants_.Constants.MAX_INT, 1)
    amount_unit = general_fields.EnumField(2, general_ui_titles.amount_unit, 'amount_unit', general_enums.AmountUnit, general_enums.AmountUnit.number)
    sub_things = general_fields.ListField(11, sample_sub_things_ui_titles, 'sub_things', SubThingPrototype)
    super_thing = general_fields.ForeignKeyField(12, general_ui_titles.dummy, 'thing_parent', ThingPrototype, SuperThingPrototype)


# ===========================================================================
class SubThing(thing_.Thing):
    name = general_fields.NameField(initial_value='sub-thing')
    sub_thing_parent = general_fields.ForeignKeyField(1, general_ui_titles.dummy, 'sub_thing_parent',
                                                      SubThingPrototype,
                                                      ThingPrototype)


# ===========================================================================
class Test__Editor__Removing_Reviving_AddingNew:
    # ===========================================================================
    @staticmethod
    def test_append_new_item(qtbot):
        # ===========================================================================
        def add_to_top_editor(is_top_editor: bool):
            # list of super-things
            super_things = thing_.ListOfThings(SuperThing)

            # tree editor for list of super-things
            super_things_tree_editor = general_editors.TreeOfThingsEditor(super_things, None)

            # check adding a new item to the list of super-things (nothing is selected yet)
            super_things_tree_editor.append_new_item(is_top_editor=is_top_editor)
            assert len(super_things_tree_editor.sub_editors) == (1 if is_top_editor else 0)

        # ===========================================================================
        def add_to_non_top_editor(is_top_editor: bool):

            # list of super-things
            super_things = thing_.ListOfThings(SuperThing)
            # adding one element to the list
            super_thing = SuperThing()
            super_things.append(super_thing)

            # tree editor for list of super-things
            super_things_tree_editor = general_editors.TreeOfThingsEditor(super_things, None)

            # select the added super-thing to the list of super-things and call append_new_item again.
            #  this time we expect that a new Thing be added to the super-thing[things] field.
            super_things_tree_editor.sub_editors[super_thing].sub_editors[SuperThing.things].set_selected(True)
            super_things_tree_editor.append_new_item(is_top_editor=is_top_editor)
            assert len(super_things_tree_editor.sub_editors) == 1
            assert len(super_things_tree_editor.sub_editors[super_thing].sub_editors[SuperThing.things].sub_editors) == 1

        # ===========================================================================
        def add_while_non_list_field_is_selected(is_top_editor: bool):

            # list of super-things
            super_things = thing_.ListOfThings(SuperThing)
            # adding one element to the list
            super_thing = SuperThing()
            super_things.append(super_thing)

            # tree editor for list of super-things
            super_things_tree_editor = general_editors.TreeOfThingsEditor(super_things, None)

            # select a non list of things field of the added super-thing to the list of super-things and call
            #  append_new_item. This time we expect that a new Thing be added to super_thing5
            super_things_tree_editor.sub_editors[super_thing].sub_editors[SuperThing.name].set_selected(True)
            super_things_tree_editor.append_new_item(is_top_editor=is_top_editor)
            assert len(super_things_tree_editor.sub_editors) == 2

        # ===========================================================================
        def add_while_non_list_field_in_sub_thing_is_selected(is_top_editor: bool):
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
            super_things_tree_editor = general_editors.TreeOfThingsEditor(super_things, None)

            # select a non list of things field of the thing7
            super_things_tree_editor.sub_editors[super_thing].sub_editors[SuperThing.things].sub_editors[thing].sub_editors[Thing.name].set_selected(True)
            super_things_tree_editor.append_new_item(is_top_editor=is_top_editor)
            assert len(super_things_tree_editor.sub_editors) == 1
            assert len(super_things_tree_editor.sub_editors[super_thing].sub_editors[SuperThing.things].sub_editors) == 2


        # create the application
        assert qt_api.QApplication.instance() is not None

        # **************************************************************
        # 1-adding new item to top editor with is_top_editor set to False
        add_to_top_editor(is_top_editor=False)

        # **************************************************************
        # 2-adding new item to top editor with is_top_editor set to True
        add_to_top_editor(is_top_editor=True)

        # **************************************************************
        # 3-adding new item to list of things editor which is not top editor with is_top_editor set to True
        add_to_top_editor(True)

        # **************************************************************
        # 4-adding new item to list of things editor which is not top editor with is_top_editor set to False
        add_to_non_top_editor(False)

        # **************************************************************
        # 5-adding new item while a non list of things field is selected with is_top_editor set to True
        #  select a non list of things field in super-thing and call append_new_item
        #  this time we expect that a new super-thing be added to the list of super-things
        add_while_non_list_field_is_selected(True)

        # **************************************************************
        # 6-adding new item while a non list of things field is selected with is_top_editor set to False
        #  select a non list of things field in super-thing and call append_new_item
        #  this time we expect that a new super-thing be added to the list of super-things
        add_while_non_list_field_is_selected(False)

        # **************************************************************
        # 7-adding new item while a non list of things field is selected in thing (not super-thing) with is_top_editor set to True
        add_while_non_list_field_in_sub_thing_is_selected(True)

        # **************************************************************
        # 8-adding new item while a non list of things field is selected in thing (not super-thing) with is_top_editor set to False
        add_while_non_list_field_in_sub_thing_is_selected(False)

    # ===========================================================================
    @staticmethod
    def test_mark_selected_sub_editor_for_removal(qtbot):
        # ===========================================================================
        def one_thing_with_one_sub_editor():
            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing = SuperThing()
            super_things.append(super_thing)

            # create a list of things editor
            super_things_tree_editor = general_editors.TreeOfThingsEditor(super_things, None)

            # select an element inside the list
            sub_editor = super_things_tree_editor.sub_editors[super_thing]
            sub_editor.set_selected(True)

            # mark it for removal and check the signal emissions
            with qtbot.wait_signal(super_things_tree_editor.sub_editor_marked_for_removal_exists_signal, raising=True), \
                 qtbot.wait_signal(sub_editor.parent_editor.value_changed_by_me_signal, raising=True):
                super_things_tree_editor.mark_selected_sub_editor_for_removal(is_top_editor=True)

            # check marked for removal
            assert sub_editor.is_marked_for_removal()
            # check presence of sub-editor in marked-for-removal list
            assert sub_editor in super_things_tree_editor.sub_editors_marked_for_removal
            # check connected signal
            sub_editor.no_revival_possible_signal.disconnect(super_things_tree_editor.sub_editor_revived_or_removed)

        # ===========================================================================
        def one_thing_with_two_sub_editors():
            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing_1 = SuperThing()
            super_thing_2 = SuperThing()
            super_things.append(super_thing_1)
            super_things.append(super_thing_2)

            # create a list of things editor
            super_things_tree_editor = general_editors.TreeOfThingsEditor(super_things, None)

            # select an element inside the list
            previous_state = editor_.Editor__Selection.multiple_selection
            editor_.Editor__Selection.multiple_selection = True
            sub_editor_1 = super_things_tree_editor.sub_editors[super_thing_1]
            sub_editor_2 = super_things_tree_editor.sub_editors[super_thing_2]
            sub_editor_1.set_selected(True)
            sub_editor_2.set_selected(True)

            # mark it for removal and check the signal emissions
            with qtbot.wait_signal(super_things_tree_editor.sub_editor_marked_for_removal_exists_signal, raising=True), \
                 qtbot.wait_signal(sub_editor_1.parent_editor.value_changed_by_me_signal, raising=True), \
                 qtbot.wait_signal(sub_editor_2.parent_editor.value_changed_by_me_signal, raising=True):
                super_things_tree_editor.mark_selected_sub_editor_for_removal(is_top_editor=True)

            # check marked for removal
            assert sub_editor_1.is_marked_for_removal()
            assert sub_editor_2.is_marked_for_removal()

            # check presence of sub-editor in marked-for-removal list
            assert sub_editor_1 in super_things_tree_editor.sub_editors_marked_for_removal
            assert sub_editor_2 in super_things_tree_editor.sub_editors_marked_for_removal

            # check connected signal
            sub_editor_1.no_revival_possible_signal.disconnect(super_things_tree_editor.sub_editor_revived_or_removed)
            sub_editor_2.no_revival_possible_signal.disconnect(super_things_tree_editor.sub_editor_revived_or_removed)

            editor_.Editor__Selection.multiple_selection = previous_state

        # ===========================================================================
        def one_thing_with_one_sub_editor_and_one_sub_sub_editor():
            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing = SuperThing()
            super_things.append(super_thing)
            thing = Thing()
            super_thing[SuperThing.things].append(thing)

            # create a list of things editor
            super_things_tree_editor = general_editors.TreeOfThingsEditor(super_things, None)

            # select an element inside the list
            sub_editor = super_things_tree_editor.sub_editors[super_thing].sub_editors[SuperThing.things].sub_editors[thing]
            sub_editor.set_selected(True)

            # mark it for removal and check the signal emissions
            with qtbot.wait_signal(super_things_tree_editor.sub_editor_marked_for_removal_exists_signal, raising=True), \
                 qtbot.wait_signal(sub_editor.parent_editor.value_changed_by_me_signal, raising=True):
                 super_things_tree_editor.mark_selected_sub_editor_for_removal(is_top_editor=True)

            # check marked for removal
            assert sub_editor.is_marked_for_removal()

            # check presence of sub-editor in marked-for-removal list
            assert sub_editor in super_things_tree_editor.sub_editors_marked_for_removal

            # check connected signal
            sub_editor.no_revival_possible_signal.disconnect(super_things_tree_editor.sub_editor_revived_or_removed)

            # check selection of the sibling or parent
            assert super_things_tree_editor.sub_editors[super_thing].sub_editors[SuperThing.things].is_selected(go_deep=False)

        # create the application
        assert qt_api.QApplication.instance() is not None

        # **************************************************************
        # 1-simplest state. one thing with one selected sub-editor
        one_thing_with_one_sub_editor()

        # **************************************************************
        # 2-select two sub-editors for removal
        one_thing_with_two_sub_editors()

        # **************************************************************
        # 3-select sub-sub-editor for removal
        one_thing_with_one_sub_editor_and_one_sub_sub_editor()

    # ===========================================================================
    @staticmethod
    def test_sub_editor_revived_or_removed(qtbot):
        # ===========================================================================
        def remove_marked_sub_editor():
            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing = SuperThing()
            super_things.append(super_thing)

            # create a list of things editor
            super_things_tree_editor = general_editors.TreeOfThingsEditor(super_things, None)

            # select an element inside the list
            sub_editor = super_things_tree_editor.sub_editors[super_thing]
            sub_editor.set_selected(True)

            # mark it for removal
            super_things_tree_editor.mark_selected_sub_editor_for_removal(is_top_editor=True)

            # marked sub-editor should be in the sub_editors_marked_for_removal at first
            assert sub_editor in super_things_tree_editor.sub_editors_marked_for_removal
            # as this is the only marked sub-editor, the no revival possible signal should be emitted.
            with qtbot.wait_signal(super_things_tree_editor.no_sub_editor_marked_for_removal_exists_signal, raising=True):
                super_things_tree_editor.remove_sub_editor(super_thing)
            # marked sub-editor should not be in the sub-editors-marked-for-removal any more
            assert sub_editor not in super_things_tree_editor.sub_editors_marked_for_removal

        # ===========================================================================
        def revive_marked_sub_editor():
            # create the things
            super_things = thing_.ListOfThings(SuperThing)
            super_thing = SuperThing()
            super_things.append(super_thing)

            # create a list of things editor
            super_things_tree_editor = general_editors.TreeOfThingsEditor(super_things, None)

            # select an element inside the list
            sub_editor = super_things_tree_editor.sub_editors[super_thing]
            sub_editor.set_selected(True)

            # mark it for removal
            super_things_tree_editor.mark_selected_sub_editor_for_removal(is_top_editor=True)

            # marked sub-editor should be in the sub_editors_marked_for_removal at first
            assert sub_editor in super_things_tree_editor.sub_editors_marked_for_removal
            # as this is the only marked sub-editor, the no revival possible signal should be emitted.
            with qtbot.wait_signal(super_things_tree_editor.no_sub_editor_marked_for_removal_exists_signal, raising=True):
                super_things_tree_editor.sub_editors[super_thing].set_marked_for_removal(mark_for_removal=False)
            # marked sub-editor should not be in the sub-editors-marked-for-removal any more
            assert sub_editor not in super_things_tree_editor.sub_editors_marked_for_removal

        # create the application
        assert qt_api.QApplication.instance() is not None
        remove_marked_sub_editor()
        revive_marked_sub_editor()

    # ===========================================================================
    @staticmethod
    def test_revive_the_latest_sub_editor_marked_for_removal(qtbot):
        # create the things
        super_things = thing_.ListOfThings(SuperThing)
        super_thing_1 = SuperThing()
        super_thing_2 = SuperThing()
        super_things.append(super_thing_1)
        super_things.append(super_thing_2)

        # create a list of things editor
        super_things_tree_editor = general_editors.TreeOfThingsEditor(super_things, None)

        # select an element inside the list and mark it for removal
        sub_editor_1 = super_things_tree_editor.sub_editors[super_thing_1]
        sub_editor_1.set_selected(True)
        super_things_tree_editor.mark_selected_sub_editor_for_removal(is_top_editor=True)
        # select an element inside the list and mark it for removal
        sub_editor_2 = super_things_tree_editor.sub_editors[super_thing_2]
        sub_editor_2.set_selected(True)
        super_things_tree_editor.mark_selected_sub_editor_for_removal(is_top_editor=True)

        # check marked for removal
        assert sub_editor_1.is_marked_for_removal()
        assert sub_editor_2.is_marked_for_removal()

        # revive the last removed one
        with qtbot.wait_signal(super_things_tree_editor.value_changed_by_me_signal):
            super_things_tree_editor.revive_the_latest_sub_editor_marked_for_removal()

        # check for the result
        assert sub_editor_1.is_marked_for_removal()
        assert not sub_editor_2.is_marked_for_removal()

        # revive the last removed one again
        with qtbot.wait_signal(super_things_tree_editor.value_changed_by_me_signal),\
                qtbot.wait_signal(super_things_tree_editor.no_sub_editor_marked_for_removal_exists_signal):
            super_things_tree_editor.revive_the_latest_sub_editor_marked_for_removal()

        # check for the result
        assert not sub_editor_1.is_marked_for_removal()


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
        assert dialog.windowTitle() == 'نام 1: ' + sample_sub_things_ui_titles[basic_types.Language.get_active_language()]

        # check edit button and revive button (should be present in the dialog and should be disabled)
        widgets = list(dialog.header_layout.itemAt(i).widget() for i in range(dialog.header_layout.count()))
        assert dialog.edit_button in widgets
        assert not dialog.edit_button.isEnabled()
        assert dialog.revive_button in widgets
        assert not dialog.revive_button.isEnabled()

        # check new button and del button (should be present in the dialog)
        names = list(widgets[i].text() if isinstance(widgets[i], widget_basics.Button) else None for i in range(len(widgets)))
        assert general_ui_titles.new[basic_types.Language.get_active_language()] in names
        assert general_ui_titles.delete[basic_types.Language.get_active_language()] in names

    # TODO: create tests for accept, reject, and __del__ methods.

