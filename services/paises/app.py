from conexion import *
from paises import mis_paises

programa = Flask(__name__)
api = Api(programa)

class ListaPaises(Resource):
    def get(self):
        paises = mis_paises.listar()
        return jsonify({"mensaje": "paises","data": paises})
    def post(self):
        nuevo=request.json
        resultado = mis_paises.consultar(nuevo["idPais"])
        if len(resultado)==0:
            mis_paises.agregar(nuevo["idPais"],nuevo["nombre"],nuevo["continente"])
            return jsonify({"mensaje":"Pais agregado con exito"})
        else:
            return jsonify({"mensaje":"Id de pais ya existe"})

class Pais(Resource):
    def get(self,idPais):
        resultado = mis_paises.consultar(idPais)
        if len(resultado)==0:
            return jsonify({"mensaje":"Id no encontrado"})
        else:
            return jsonify({"mensaje":"Pais encontrado","pais":resultado[0]})
    def put(self,idPais):
        nuevo=request.json
        resultado = mis_paises.consultar(idPais)
        if len(resultado)==0:
            return jsonify({"mensaje":"Pais no existe"})
        else:
            mis_paises.modificar(nuevo["idPais"],nuevo["nombre"],nuevo["continente"])
            return jsonify({"mensaje":"Pais modificado con exito"})
    def delete(self,idPais):
        resultado = mis_paises.consultar(idPais)
        if len(resultado)==0:
            return jsonify({"mensaje":"Pais no existe"})
        else:
            mis_paises.eliminar(idPais)
            return jsonify({"mensaje":"Pais eliminado con exito"})
    
api.add_resource(ListaPaises, "/paises")
api.add_resource(Pais,"/paises/<idPais>")

if __name__=="__main__":
    programa.run(host="0.0.0.0",debug=True,port=5089)
