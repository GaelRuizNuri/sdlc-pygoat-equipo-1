def buscar(cursor, nombre):
    # ruleid: sql-armado-con-format
    cursor.execute("SELECT id FROM usuarios WHERE nombre = '{}'".format(nombre))

    # ok: sql-armado-con-format
    cursor.execute("SELECT id FROM usuarios WHERE nombre = ?", (nombre,))