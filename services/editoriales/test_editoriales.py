from conexion import *
import pytest   

class Test_editoriales:

    def setup_class(self):
        # Preparacion del entorno de las pruebas
        self.url = "http://localhost:5088/editoriales"

        mi_cursor.execute("INSERT IGNORE INTO paises (idPais, nombre) VALUES ('CO', 'Colombia')")
        mi_cursor.execute("INSERT IGNORE INTO paises (idPais, nombre) VALUES ('MX', 'Mexico')")
        mi_cursor.execute("INSERT IGNORE INTO paises (idPais, nombre) VALUES ('PR', 'Puerto Rico')")
        mi_db.commit()

        mi_cursor.execute("INSERT IGNORE INTO editoriales (idEditorial, nombre, idPais) VALUES ('001', 'Editorial Norma', 'CO')")
        mi_db.commit()

    def teardown_class(self):
        # Limpiar editoriales creadas en los tests
        mi_cursor.execute("DELETE FROM editoriales WHERE idEditorial IN ('001', '002')")
        mi_db.commit()

    def test_lista_editoriales(self):
        esperado = "editoriales"
        calculado = requests.get(self.url)
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"] == esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada", "esperado_entrada"],
        [
            ({"idEditorial": "002", "nombre": "Editorial Prueba", "idPais": "PR"}, "Editorial agregada con exito"),
            ({"idEditorial": "001", "nombre": "Editorial Norma", "idPais": "MX"}, "Id de editorial ya existe"),
        ]
    )
    def test_agregar(self, nuevo_entrada, esperado_entrada):
        calculado = requests.post(self.url, json=nuevo_entrada)
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [
            ("001", "Editorial encontrado"),
            ("009", "Id no encontrado"),
        ]
    )
    def test_busqueda(self, id_entrada, esperado_entrada):
        idEditorial = id_entrada
        esperado = esperado_entrada
        calculado = requests.get(f"{self.url}/{idEditorial}")
        assert calculado.status_code == 200
        assert esperado == calculado.json()["mensaje"]

    def test_modifica1(self):
        idEditorial = "001"
        nombre = "Editorial Norma Modificada"
        idPais = "MX"
        nuevo = {"idEditorial": idEditorial, "nombre": nombre, "idPais": idPais}
        esperado = "Editorial modificado con exito"
        calculado = requests.put(f"{self.url}/{idEditorial}", json=nuevo)
        assert calculado.status_code == 200
        assert esperado == calculado.json()["mensaje"]
        sql = f"SELECT * FROM editoriales WHERE idEditorial='{idEditorial}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert nombre == datos[1] and idPais == datos[2]

    def test_modifica2(self):
        idEditorial = "009"
        nombre = "Editorial de Prueba Modificada"
        idPais = "MX"
        nuevo = {"idEditorial": idEditorial, "nombre": nombre, "idPais": idPais}
        esperado = "Editorial no existe"
        calculado = requests.put(f"{self.url}/{idEditorial}", json=nuevo)
        assert calculado.status_code == 200
        assert esperado == calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [
            ("001", "Editorial eliminada con exito"),
            ("009", "Editorial no existe"),
        ]
    )
    def test_elimina(self, id_entrada, esperado_entrada):
        idEditorial = id_entrada
        esperado = esperado_entrada
        calculado = requests.delete(f"{self.url}/{idEditorial}")
        assert calculado.status_code == 200
        assert esperado == calculado.json()["mensaje"]
        mi_db.commit()
        sql = f"SELECT * FROM editoriales WHERE idEditorial='{idEditorial}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()
        assert len(datos) == 0