from mehdi_lib.generals import general_fields, general_ui_titles, general_editors, general_initial_values, general_enums
from mehdi_lib.basics import editor_, thing_, constants_, basic_types, prototype_
import pytest
from pytestqt.qt_compat import qt_api


pytestmark = pytest.mark.basics

"""
Parameters required for testing EditorDialog
"""

sample_things_ui_title_en = 'sample things'
sample_things_ui_title_fa = 'چیزهای نمونه'

sample_things_ui_titles = {
    basic_types.Language.AvailableLanguage.en: sample_things_ui_title_en,
    basic_types.Language.AvailableLanguage.fa: sample_things_ui_title_fa,
}


# ===========================================================================
class SampleThingPrototype(prototype_.ThingPrototype):
    pass


# ===========================================================================
class SampleSubThingPrototype(prototype_.ThingPrototype):
    pass


# ===========================================================================
class SampleThing(thing_.Thing):
    name = general_fields.NameField(initial_value=general_initial_values.name)
    version_number = general_fields.IntField(1, general_ui_titles.version_number, 'version_number', 1, constants_.Constants.MAX_INT, 1)
    amount_unit = general_fields.EnumField(2, general_ui_titles.amount_unit, 'amount_unit', general_enums.AmountUnit, general_enums.AmountUnit.number)
    sub_things = general_fields.ListField(11, sample_things_ui_titles, 'sub_things', SampleSubThingPrototype)


# ===========================================================================
class SampleSubThing(thing_.Thing):
    name = general_fields.NameField(initial_value='sub-thing')
    sub_thing_parent = general_fields.ForeignKeyField(1, general_ui_titles.dummy, 'sub_thing_parent',
                                                      SampleSubThingPrototype,
                                                      SampleThingPrototype)


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
        thing = SampleThing()
        editor = general_editors.NameEditor(thing, SampleThing.name)
        dialog = editor_.EditorDialog(editor, automatic_unregister=False)

        # check the name
        name = editor.owner.name
        while editor.parent_editor:
            editor = editor.parent_editor
            if hasattr(editor.owner, 'name'):
                name = '{}-{}'.format(editor.owner.name, name)
        if editor.field:
            name = '{}: {}'.format(name, editor.field.get_instance_ui_title(basic_types.Language.get_active_language()))
        assert dialog.windowTitle() == name

        # check name for list editor
        editor = general_editors.TableOfThingsEditor(thing, SampleThing.sub_things)
        dialog = editor_.EditorDialog(editor, automatic_unregister=False)
        assert dialog.windowTitle() == 'نام 1: ' + sample_things_ui_titles[basic_types.Language.get_active_language()]

        # check edit button and revive button (should be added to dialog)
        widgets = (dialog.header_layout.itemAt(i).widget() for i in range(dialog.header_layout.count()))
        assert dialog.edit_button in widgets
        assert dialog.revive_button in widgets


