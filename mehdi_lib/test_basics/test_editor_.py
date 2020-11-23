from mehdi_lib.generals import general_fields, general_ui_titles, general_editors, general_initial_values, general_enums
from mehdi_lib.basics import database_tools, editor_, thing_, constants_, basic_types, prototype_
from mehdi_lib.tools import tools
from PyQt5 import QtWidgets, QtCore
import sys
import pytest
import pytestqt
from pytestqt.qt_compat import qt_api
# from pytestqt import qtbot
import faulthandler
faulthandler.enable()


pytestmark = pytest.mark.basics

sample_things_ui_title_en = 'sample things'
sample_things_ui_title_fa = 'چیزهای نمونه'

sample_things_ui_titles = {
    basic_types.Language.AvailableLanguage.en: sample_things_ui_title_en,
    basic_types.Language.AvailableLanguage.fa: sample_things_ui_title_fa,
}


class SampleSubThingPrototype(prototype_.Prototype):
    pass


class SampleThing(thing_.Thing):
    name = general_fields.NameField(initial_value=general_initial_values.name)
    version_number = general_fields.IntField(1, general_ui_titles.version_number, 'version_number', 1, constants_.Constants.MAX_INT, 1)
    amount_unit = general_fields.EnumField(2, general_ui_titles.amount_unit, 'amount_unit', general_enums.AmountUnit, general_enums.AmountUnit.number)
    sub_things = general_fields.ListField(11, sample_things_ui_titles, 'sub_things', SampleSubThingPrototype)


class SampleSubThing(thing_.Thing):
    name = general_fields.NameField(initial_value='sub-thing')


# ===========================================================================
class TestEditorDialog:
    """

    """

    # ===========================================================================
    @staticmethod
    def test_init(qtbot):
        # app = qt_api.QApplication.instance()
        assert qt_api.QApplication.instance() is not None
        # widget = qt_api.QWidget()
        # qtbot.addWidget(widget)
        # widget.setWindowTitle("W1")
        # widget.show()
        #
        # assert widget.isVisible()
        # assert widget.windowTitle() == "W1"
        #
        # widget = qt_api.QWidget()
        # qtbot.addWidget(widget)
        # pytestqt.qtbot.QtBot.mouseClick(widget.about_box., QtCore.Qt.LeftButton)
        # qtbot.waitUntil(widget.about_box.isVisible)
        # assert widget.about_box.text() == 'This is a GUI App'
        #
        # app = QtWidgets.QApplication(sys.argv)
        thing = SampleThing()
        editor = general_editors.NameEditor(thing, SampleThing.name)
        dialog = editor_.EditorDialog(editor, automatic_unregister=False)
        assert dialog.windowTitle() == 'نام 1: نام'
        editor = general_editors.TableOfThingsEditor(thing, SampleThing.sub_things)
        dialog = editor_.EditorDialog(editor, automatic_unregister=False)
        assert dialog.windowTitle() == 'نام 1: ' + sample_things_ui_titles[basic_types.Language.get_active_language()]
        widgets = (dialog.header_layout.itemAt(i).widget() for i in range(dialog.header_layout.count()))
        assert dialog.edit_button in widgets
        assert dialog.revive_button in widgets
        dialog.exec()

    # @staticmethod
    # def hello(qtbot):
    #     widget = qt_api.HelloWidget()
    #     qtbot.addWidget(widget)
    #
    #     click in the Greet button and make sure it updates the appropriate label
        # qtbot.mouseClick(widget.button_greet, QtCore.Qt.LeftButton)
        #
        # assert widget.greet_label.text() == "Hello!"



# TestEditorDialog.test_init()

