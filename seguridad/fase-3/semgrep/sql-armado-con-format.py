
def buscar_mal(cursor, texto):
    # ruleid: sql-armado-con-format
    template = "SELECT * FROM comercios WHERE nombre LIKE '{query}'"
    cursor.execute(template.format(query = texto))

def buscar_bien(cursor, texto):
    # ok: sql-armado-con-format
    cursor.execute("SELECT * FROM comercios WHERE nombre LIKE ?", (f"%{texto}%",))