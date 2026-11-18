def buscar_mal(cursor, texto):
    # ruleid: sql-armado-con-concatenacion

    cursor.execute(f"SELECT * FROM comercios WHERE nombre LIKE '" + "%{texto}%'" )
    
    
def buscar_bien(cursor, texto):
    # ok: sql-armado-con-concatenacion
    cursor.execute("SELECT * FROM comercios WHERE nombre LIKE ?", (f"%{texto}%",))