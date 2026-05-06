""" 
Se tendrá aquí el modelo para la gestión de paoíses,
es decir todo aquello que tenga que ver con la persistencia
(SQL)
"""
from conexion import *

class Paises:
    def listar(self):
        sql = "SELECT * FROM paises"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado
    def consultar(self, idPais):
        sql = f"SELECT * FROM paises WHERE idPais = %s"
        mi_cursor.execute(sql, (idPais,))
        resultado = mi_cursor.fetchall()
        return resultado
    def agregar(self,idPais,nom,cont):
        sql = f"INSERT INTO paises (idPais,nombre,continente) VALUES (%s,%s,%s)"
        mi_cursor.execute(sql, (idPais, nom, cont))
        mi_db.commit()
    def modificar(self, idPais, nom, cont):
        sql = f"UPDATE paises SET nombre=%s, continente=%s WHERE idPais=%s"
        mi_cursor.execute(sql, (nom, cont, idPais))
        mi_db.commit()
        return self.consultar(idPais)
    def eliminar(self, idPais):
        sql = f"DELETE FROM paises WHERE idPais = %s"
        mi_cursor.execute(sql, (idPais,))
        mi_db.commit()
    
mis_paises = Paises()