from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Entrada:
    db_name = 'db_querido_diario'

    def __init__(self, data):
        self.id = data['id']
        self.fecha = data['fecha_entrada']
        self.notas = data['notas']
        self.usuario_id = data['usuario_id']

    # Guarda una nueva entrada usando el campo 'fecha_entrada' de tu BD
    @classmethod
    def save(cls, data):
        query = """INSERT INTO entradas (fecha_entrada, notas, usuario_id) 
                   VALUES (%(fecha)s, %(notas)s, %(usuario_id)s);"""
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Obtiene las entradas por usuario ordenadas por fecha_entrada
    @classmethod
    def get_by_user(cls, data):
        query = "SELECT * FROM entradas WHERE usuario_id = %(usuario_id)s ORDER BY fecha_entrada DESC;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        entradas = []
        if results:
            for row in results:
                entradas.append(cls(row))
        return entradas

    # Obtiene una entrada específica por su ID
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM entradas WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if not results or len(results) < 1:
            return False
        return cls(results[0])

    # Actualiza la fecha y notas usando 'fecha_entrada'
    @classmethod
    def update(cls, data):
        query = """UPDATE entradas 
                   SET fecha_entrada = %(fecha)s, notas = %(notas)s 
                   WHERE id = %(id)s;"""
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Elimina una entrada de la BD
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM entradas WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Búsqueda por palabra clave dentro de las notas del usuario
    @classmethod
    def search(cls, data):
        query = """SELECT * FROM entradas 
                   WHERE usuario_id = %(usuario_id)s 
                   AND notas LIKE %(termino)s 
                   ORDER BY fecha_entrada DESC;"""
        data_search = {
            'usuario_id': data['usuario_id'],
            'termino': f"%{data['termino']}%"
        }
        results = connectToMySQL(cls.db_name).query_db(query, data_search)
        entradas = []
        if results:
            for row in results:
                entradas.append(cls(row))
        return entradas

    # Validación del formulario
    @staticmethod
    def validar_entrada(entrada):
        is_valid = True
        if not entrada.get('fecha'):
            flash("La fecha es obligatoria.", "entrada")
            is_valid = False
        if not entrada.get('notas') or len(entrada['notas'].strip()) < 1:
            flash("Las notas no pueden estar vacías.", "entrada")
            is_valid = False
        return is_valid