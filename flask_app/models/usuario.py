from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.edad = data['edad']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO usuarios (nombre, apellido, email, edad, password) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(edad)s, %(password)s);"
        return connectToMySQL('db_querido_diario').query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connectToMySQL('db_querido_diario').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        results = connectToMySQL('db_querido_diario').query_db(query, data)
        return cls(results[0]) if results else False

    @staticmethod
    def validar_registro(formulario):
        es_valido = True

        if len(formulario.get('nombre', '')) < 2 or len(formulario.get('apellido', '')) < 2:
            flash("El nombre y el apellido deben tener al menos 2 caracteres.", "error_registro")
            es_valido = False

        # Validación sencilla de email sin librerías ni expresiones regulares
        email = formulario.get('email', '')
        if "@" not in email or "." not in email:
            flash("El email debe tener un formato válido.", "error_registro")
            es_valido = False

        if Usuario.get_by_email({'email': email}):
            flash("El email no puede repetirse en la BD.", "error_registro")
            es_valido = False

        try:
            if int(formulario.get('edad', 0)) < 18:
                flash("Debe de tener al menos 18 años.", "error_registro")
                es_valido = False
        except ValueError:
            flash("Ingresa una edad válida.", "error_registro")
            es_valido = False

        if formulario.get('password') != formulario.get('confirm_password'):
            flash("La contraseña y confirmación deben ser iguales.", "error_registro")
            es_valido = False

        return es_valido