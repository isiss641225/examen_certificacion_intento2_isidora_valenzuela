from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime, date

class Entrada:
    def __init__(self, data):
        self.id = data['id']
        self.fecha_entrada = data['fecha_entrada']
        self.notas = data['notas']
        self.usuario_id = data['usuario_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO entradas (fecha_entrada, notas, usuario_id) VALUES (%(fecha_entrada)s, %(notas)s, %(usuario_id)s);"
        return connectToMySQL('db_querido_diario').query_db(query, data)

    @classmethod
    def get_by_user_id(cls, data):
        query = "SELECT * FROM entradas WHERE usuario_id = %(usuario_id)s ORDER BY fecha_entrada DESC;"
        results = connectToMySQL('db_querido_diario').query_db(query, data)
        return [cls(row) for row in results]

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM entradas WHERE id = %(id)s;"
        results = connectToMySQL('db_querido_diario').query_db(query, data)
        return cls(results[0]) if results else None

    @classmethod
    def update(cls, data):
        query = "UPDATE entradas SET fecha_entrada = %(fecha_entrada)s, notas = %(notas)s WHERE id = %(id)s AND usuario_id = %(usuario_id)s;"
        return connectToMySQL('db_querido_diario').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM entradas WHERE id = %(id)s AND usuario_id = %(usuario_id)s;"
        return connectToMySQL('db_querido_diario').query_db(query, data)

    @classmethod
    def buscar_por_notas(cls, data):
        query = "SELECT * FROM entradas WHERE usuario_id = %(usuario_id)s AND notas LIKE %(termino)s ORDER BY fecha_entrada DESC;"
        results = connectToMySQL('db_querido_diario').query_db(query, data)
        return [cls(row) for row in results]

    @staticmethod
    def validar_entrada(formulario):
        es_valido = True
        fecha_str = formulario.get('fecha_entrada')
        notas = formulario.get('notas', '').strip()

        if not fecha_str or not notas:
            flash("Todos los campos son obligatorios.", "error_entrada")
            return False

        try:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            if fecha_obj > date.today():
                flash("No puede ingresar una fecha en el futuro.", "error_entrada")
                es_valido = False
        except ValueError:
            flash("Formato de fecha no válido.", "error_entrada")
            es_valido = False

        return es_valido