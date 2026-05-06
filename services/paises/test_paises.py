from conexion import *
import pytest   

class Test_paises:

    def setup_class(self):
        # Preparación del entorno de las pruebas
        self.url = "http://localhost:5089/paises"
        idPais = "PR"
        nom = "Puerto Rico"
        cont = "América"
        sql = f"INSERT INTO paises (idPais,nombre,continente) VALUES ('{idPais}','{nom}','{cont}')"
        mi_cursor.execute(sql)
        mi_db.commit()


    def test_lista_paises(self):
        esperado = "paises"
        # Ejecutar la prueba
        calculado = requests.get(self.url)
        # Verificación
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"]==esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada","esperado_entrada"],
        [({"idPais":"MX","nombre":"Mexico","continente":"Sur America"},"Pais agregado con exito"),  
         ({"idPais":"PR","nombre":"Puerto Rico","continente":"América"},"Id de pais ya existe")]
    )
    def test_agregar(self,nuevo_entrada,esperado_entrada):
        # Ejecutar la prueba
        calculado = requests.post(self.url,json=nuevo_entrada)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"], 
        [("PR","Pais encontrado"),
         ("ARG","Id no encontrado")]
    )
    def test_busqueda(self,id_entrada,esperado_entrada):
        idPais = id_entrada
        esperado = esperado_entrada
        # Ejecutar la prueba
        calculado = requests.get(f"{self.url}/{idPais}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado == calculado.json()["mensaje"]
    
    #Para cuando el pais existe y se modifica con éxito
    def test_modifica1(self):
        idPais = "PR"
        nombre = "Puerto Rico Modificado"
        continente = "América"
        nuevo = {"idPais":idPais,"nombre":nombre,"continente":continente}
        esperado = "Pais modificado con exito"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{idPais}",json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado == calculado.json()["mensaje"]

        sql = f"SELECT * FROM paises WHERE idPais='{idPais}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert nombre==datos[1] and continente==datos[2]

    # Para cuando el país no existe y se intenta modificar
    def test_modifica2(self):
        idPais = "XXX"
        nombre = "Pais de Prueba Modificado"
        continente = "Europa"
        nuevo = {"idPais":idPais,"nombre":nombre,"continente":continente}
        esperado = "Pais no existe"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{idPais}",json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado == calculado.json()["mensaje"]
        
    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("PR","Pais eliminado con exito"),
         ("TEST","Pais no existe")]
    )

    

    def test_elimina(self,id_entrada,esperado_entrada):
        idPais = id_entrada
        esperado = esperado_entrada
        # Ejecutar la prueba
        calculado = requests.delete(f"{self.url}/{idPais}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado == calculado.json()["mensaje"]
        sql = f"SELECT * FROM paises WHERE idPais='{idPais}'"
        mi_db.commit()
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()
        assert len(datos)==0


def teardown_class(self):
        # Limpia la base de datos
        sql = f"DELETE FROM paises WHERE idPais='PR'"
        mi_cursor.execute(sql)
        mi_db.commit()
        