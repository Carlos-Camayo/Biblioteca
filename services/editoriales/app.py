from conexion import *
from editoriales import mis_editoriales

programa = Flask(__name__)
api = Api(programa)

class ListaEditoriales(Resource):
    def get(self):
        editoriales = mis_editoriales.listar()
        return jsonify({"mensaje": "editoriales","data": editoriales})
    def post(self):
        nuevo=request.json
        resultado = mis_editoriales.consultar(nuevo["idEditorial"])
        if len(resultado)==0:
            mis_editoriales.agregar(nuevo["idEditorial"],nuevo["nombre"],nuevo["idPais"])
            return jsonify({"mensaje":"Editorial agregada con exito"})
        else:
            return jsonify({"mensaje":"Id de editorial ya existe"})

class Editorial(Resource):
    def get(self,idEditorial):
        resultado = mis_editoriales.consultar(idEditorial)
        if len(resultado)==0:
            return jsonify({"mensaje":"Id no encontrado"})
        else:
            return jsonify({"mensaje":"Editorial encontrado","editorial":resultado[0]})
    def put(self,idEditorial):
        nuevo=request.json
        resultado = mis_editoriales.consultar(idEditorial)
        if len(resultado)==0:
            return jsonify({"mensaje":"Editorial no existe"})
        else:
            mis_editoriales.modificar(nuevo["idEditorial"],nuevo["nombre"],nuevo["idPais"])
            return jsonify({"mensaje":"Editorial modificado con exito"})
    def delete(self,idEditorial):
        resultado = mis_editoriales.consultar(idEditorial)
        if len(resultado)==0:
            return jsonify({"mensaje":"Editorial no existe"})
        else:
            mis_editoriales.eliminar(idEditorial)
            return jsonify({"mensaje":"Editorial eliminada con exito"})
    
api.add_resource(ListaEditoriales, "/editoriales")
api.add_resource(Editorial,"/editoriales/<idEditorial>")

if __name__=="__main__":
    programa.run(host="0.0.0.0",debug=True,port=5088)
