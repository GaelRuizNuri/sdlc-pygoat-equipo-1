def buscar_nombre(cursor, nombre):
    # ruleid: sql-armado-con-concatenacion
    cursor.execute("SELECT id FROM usuarios WHERE nombre = '" + nombre + "'")
    # bien
    # ok: sql-armado-con-concatenacion
    cursor.execute("SELECT id FROM usuarios WHERE nombre = ?", (nombre,))
