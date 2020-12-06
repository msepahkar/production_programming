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

        # create the application
        assert qt_api.QApplication.instance() is not None

        # **************************************************************
        # 1-adding new item to top editor with is_top_editor set to False

        # list of super-things
        super_things1 = thing_.ListOfThings(SuperThing)

        # tree editor for list of super-things
        super_things_tree_editor1 = general_editors.TreeOfThingsEditor(super_things1, None)

        # check adding a new item to the list of super-things (nothing is selected yet)
        super_things_tree_editor1.append_new_item(is_top_editor=False)
        assert len(super_things_tree_editor1.sub_editors) == 0  # nothing will be added

        # **************************************************************
        # 2-adding new item to top editor with is_top_editor set to True

        # list of super-things
        super_things2 = thing_.ListOfThings(SuperThing)

        # tree editor for list of super-things
        super_things_tree_editor2 = general_editors.TreeOfThingsEditor(super_things2, None)

        # check adding a new item to the list of super-things (nothing is selected yet)
        super_things_tree_editor2.append_new_item(is_top_editor=True)
        assert len(super_things_tree_editor2.sub_editors) == 1

        # **************************************************************
        # 3-adding new item to list of things editor which is not top editor with is_top_editor set to True

        # list of super-things
        super_things3 = thing_.ListOfThings(SuperThing)
        # adding one element to the list
        super_thing3 = SuperThing()
        super_things3.append(super_thing3)

        # tree editor for list of super-things
        super_things_tree_editor3 = general_editors.TreeOfThingsEditor(super_things3, None)

        # select the added super-thing to the list of super-things and call append_new_item again.
        #  this time we expect that a new Thing be added to the super-thing[things] field.
        super_things_tree_editor3.sub_editors[super_thing3].sub_editors[SuperThing.things].set_selected(True)
        super_things_tree_editor3.append_new_item(is_top_editor=True)
        assert len(super_things_tree_editor3.sub_editors) == 1
        assert len(super_things_tree_editor3.sub_editors[super_thing3].sub_editors[SuperThing.things].sub_editors) == 1

        # **************************************************************
        # 4-adding new item to list of things editor which is not top editor with is_top_editor set to False

        # list of super-things
        super_things4 = thing_.ListOfThings(SuperThing)
        # adding one element to the list
        super_thing4 = SuperThing()
        super_things4.append(super_thing4)

        # tree editor for list of super-things
        super_things_tree_editor4 = general_editors.TreeOfThingsEditor(super_things4, None)

        # select the added super-thing to the list of super-things and call append_new_item again.
        #  this time we expect that a new Thing be added to the super-thing[things] field.
        super_things_tree_editor4.sub_editors[super_thing4].sub_editors[SuperThing.things].set_selected(True)
        super_things_tree_editor4.append_new_item(is_top_editor=False)
        assert len(super_things_tree_editor4.sub_editors) == 1
        assert len(super_things_tree_editor4.sub_editors[super_thing4].sub_editors[SuperThing.things].sub_editors) == 1

        # **************************************************************
        # 5-adding new item while a non list of things field is selected with is_top_editor set to True
        #  select a non list of things field in super-thing and call append_new_item
        #  this time we expect that a new super-thing be added to the list of super-things

        # list of super-things
        super_things5 = thing_.ListOfThings(SuperThing)
        # adding one element to the list
        super_thing5 = SuperThing()
        super_things5.append(super_thing5)

        # tree editor for list of super-things
        super_things_tree_editor5 = general_editors.TreeOfThingsEditor(super_things5, None)

        # select a non list of things field of the added super-thing to the list of super-things and call
        #  append_new_item. This time we expect that a new Thing be added to super_thing5
        super_things_tree_editor5.sub_editors[super_thing5].sub_editors[SuperThing.name].set_selected(True)
        super_things_tree_editor5.append_new_item(is_top_editor=True)
        assert len(super_things_tree_editor5.sub_editors) == 2

        # **************************************************************
        # 6-adding new item while a non list of things field is selected with is_top_editor set to False
        #  select a non list of things field in super-thing and call append_new_item
        #  this time we expect that a new super-thing be added to the list of super-things

        # list of super-things
        super_things6 = thing_.ListOfThings(SuperThing)
        # adding one element to the list
        super_thing6 = SuperThing()
        super_things6.append(super_thing6)

        # tree editor for list of super-things
        super_things_tree_editor6 = general_editors.TreeOfThingsEditor(super_things6, None)

        # select a non list of things field of the added super-thing to the list of super-things and call
        #  append_new_item. This time we expect that a new Thing be added to super_thing6
        super_things_tree_editor6.sub_editors[super_thing6].sub_editors[SuperThing.name].set_selected(True)
        super_things_tree_editor6.append_new_item(is_top_editor=False)
        assert len(super_things_tree_editor6.sub_editors) == 2

        # **************************************************************
        # 7-adding new item while a non list of things field is selected in thing (not super-thing) with is_top_editor set to True

        # list of super-things
        super_things7 = thing_.ListOfThings(SuperThing)
        # adding one element to the list
        super_thing7 = SuperThing()
        super_things7.append(super_thing7)
        # create a thing
        thing7 = Thing()
        # add the thing to super-thing
        super_thing7[SuperThing.things].append(thing7)

        # tree editor for list of super-things
        super_things_tree_editor7 = general_editors.TreeOfThingsEditor(super_things7, None)

        # select a non list of things field of the thing7
        super_things_tree_editor7.sub_editors[super_thing7].sub_editors[SuperThing.things].sub_editors[thing7].sub_editors[Thing.name].set_selected(True)
        super_things_tree_editor7.append_new_item(is_top_editor=True)
        assert len(super_things_tree_editor7.sub_editors) == 1
        assert len(super_things_tree_editor7.sub_editors[super_thing7].sub_editors[SuperThing.things].sub_editors) == 2

        # **************************************************************
        # 8-adding new item while a non list of things field is selected in thing (not super-thing) with is_top_editor set to False

        # list of super-things
        super_things8 = thing_.ListOfThings(SuperThing)
        # adding one element to the list
        super_thing8 = SuperThing()
        super_things8.append(super_thing8)
        # create a thing
        thing8 = Thing()
        # add the thing to super-thing
        super_thing8[SuperThing.things].append(thing8)

        # tree editor for list of super-things
        super_things_tree_editor8 = general_editors.TreeOfThingsEditor(super_things8, None)

        # select a non list of things field of the thing8
        super_things_tree_editor8.sub_editors[super_thing8].sub_editors[SuperThing.things].sub_editors[thing8].sub_editors[Thing.name].set_selected(True)
        super_things_tree_editor8.append_new_item(is_top_editor=False)
        assert len(super_things_tree_editor8.sub_editors) == 1
        assert len(super_things_tree_editor8.sub_editors[super_thing8].sub_editors[SuperThing.things].sub_editors) == 2

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
            super_things_tree_editor.sub_editors[super_thing].set_selected(True)

            # mark it for removal
            super_things_tree_editor.mark_selected_sub_editor_for_removal(is_top_editor=True)

            # check
            assert super_things_tree_editor.sub_editors[super_thing].is_marked_for_removal()

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
            super_things_tree_editor.sub_editors[super_thing_1].set_selected(True)
            super_things_tree_editor.sub_editors[super_thing_2].set_selected(True)

            # mark it for removal
            super_things_tree_editor.mark_selected_sub_editor_for_removal(is_top_editor=True)

            # check
            assert super_things_tree_editor.sub_editors[super_thing_1].is_marked_for_removal()
            assert super_things_tree_editor.sub_editors[super_thing_2].is_marked_for_removal()

            editor_.Editor__Selection.multiple_selection = previous_state

        # create the application
        assert qt_api.QApplication.instance() is not None

        # 1-simplest state. one thing with one selected sub-editor
        one_thing_with_one_sub_editor()

        # 2-select two sub-editors for removal
        one_thing_with_two_sub_editors()



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

