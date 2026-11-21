def buscar_nombre(cursor, nombre):
    # ruleid: sql-armado-con-format
    cursor.execute("SELECT id FROM usuarios WHERE nombre = '{}'".format(nombre))
    # bien
    # ok: sql-armado-con-format
    cursor.execute("SELECT id FROM usuarios WHERE nombre = ?", (nombre,))

