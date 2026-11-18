def buscar(cursor, nombre):
    # ruleid: sql-armado-con-format
    cursor.execute("SELECT id FROM usuarios WHERE nombre = '{}'".format(nombre))

def bueno(cursor, nombre):
    # ok: sql-armado-con-concatenacion
    cursor.execute("SELECT id FROM usuarios WHERE nombre = ?", (nombre,))
