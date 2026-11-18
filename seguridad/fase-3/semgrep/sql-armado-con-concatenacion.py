def buscar(cursor, nombre):
    # ruleid: sql-armado-con-concatenacion
    cursor.execute("SELECT id FROM usuarios WHERE nombre = '" + nombre + "'")

def bueno(cursor, nombre):
    # ok: sql-armado-con-concatenacion
    cursor.execute("SELECT id FROM usuarios WHERE nombre = ?", (nombre,))
