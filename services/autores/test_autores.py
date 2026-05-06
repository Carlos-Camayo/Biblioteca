"""
Pruebas unitarias para el microservicio de AUTORES
Proyecto: Biblioteca - SENA ADSO
"""
from conexion import *
import pytest
import requests

class Test_autores:

    def setup_class(self):
        #Preparación 
        self.url = "http://localhost:5087/autores"
        sql_pais = "INSERT IGNORE INTO paises (idPais, nombre, continente) VALUES ('CA', 'Canada', 'America')"
        mi_cursor.execute(sql_pais)
        mi_db.commit()
        
        sql = "INSERT IGNORE INTO autores (idAutor, nombre, email, idPais) VALUES ('001', 'Autor de Prueba', 'prueba@test.com', 'CA')"
        mi_cursor.execute(sql)
        mi_db.commit()
        
    #prueba 1
    def test_lista_autores(self):
        esperado = "autores"
        # Ejecutar la prueba
        calculado = requests.get(self.url)
        # Verificación
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"] == esperado

    #prueba 2
    @pytest.mark.parametrize(
        ["nuevo_entrada", "esperado_entrada"],
        [
            ({"id": "0000", "nombre": "Nuevo Autor", "email": "nuevo@test.com", "idPais": "CA"}, "Autor agregado con exito"),
            #autor ya existe
            ({"id": "001", "nombre": "Autor de Prueba", "email": "prueba@test.com", "idPais": "CA"}, "Id de autor ya existe"),
        ]
    )
    def test_agregar(self, nuevo_entrada, esperado_entrada):
        # Ejecutar la prueba
        calculado = requests.post(self.url, json=nuevo_entrada)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]

    # buscar
    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [
            ("001","Autor encontrado"),   
            ("999","Autor no encontrado"),
        ]
    )
    def test_busqueda(self, id_entrada, esperado_entrada):
        id = id_entrada
        esperado = esperado_entrada
        # Ejecutar la prueba
        calculado = requests.get(f"{self.url}/{id}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    def test_modifica1(self):
        id = "001"
        nombre = "Autor Modificado"
        email = "modificado@test.com"
        idPais = "CA"
        nuevo = {"nombre": nombre, "email": email, "idPais": idPais}
        esperado = "Autor modificado con exito"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}", json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        # Verificar en la base de datos que el cambio quedó guardado
        sql = f"SELECT * FROM autores WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert nombre == datos[1] and email == datos[2]

    def test_modifica2(self):
        id = "noesta"
        nuevo = {"nombre": "Nadie", "email": "modifica@test.com", "idPais": "CA"}
        esperado = "Autor no existe"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}", json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]


    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [
            ("0000","Autor eliminado con exito"),
            ("noesta","Autor no existe"),             
        ]
    )
    def test_elimina(self, id_entrada, esperado_entrada):
        id = id_entrada
        esperado = esperado_entrada
        # Ejecutar la prueba
        calculado = requests.delete(f"{self.url}/{id}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        # Si se eliminó, verificar que ya no esté en la BD
        if "éxito" in esperado_entrada:
            mi_db.commit()
            sql = f"SELECT * FROM autores WHERE idAutor='{id}'"
            mi_cursor.execute(sql)
            datos = mi_cursor.fetchall()
            assert len(datos) == 0