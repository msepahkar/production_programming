from PyQt5 import QtSql
from mehdi_lib.tools import tools

db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName('./test_db.sqlite')

if not db.open():
    tools.Tools.fatal_error('cannot open test database.')

# TODO: testing thing.referencing_prototypes in prototype_ module should be done here.
