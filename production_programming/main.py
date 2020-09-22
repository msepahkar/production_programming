# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from mehdi_lib.basics import thing_, basic_types
from things import part_things
from mehdi_lib.basics import database_tools

from PyQt5 import QtWidgets

from modules import mdi

basic_types.Language.set_active_language(basic_types.Language.AvailableLanguage.en)
database_tools.Database.db.setDatabaseName('db.sqlite')
app = QtWidgets.QApplication(sys.argv)

if True:
    print('creating the database ...')
    thing_.Thing.create_tables()
    part_things.Part().update_in_database()

main_window = mdi.MainWindow()

main_window.show()

app.exec_()


