from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

# Expresión regular estándar para verificar formato de correo electrónico
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    db_name = 'db_querido_diario'

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.edad = data['edad']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Guarda un nuevo usuario en la BD
    @classmethod
    def save(cls, data):
        query = """INSERT INTO usuarios (nombre, apellido, email, edad, password, created_at, updated_at) 
                   VALUES (%(nombre)s, %(apellido)s, %(email)s, %(edad)s, %(password)s, NOW(), NOW());"""
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Busca un usuario por su correo para el login
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    # Obtiene los datos del usuario logueado usando su ID de sesión
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    # Validaciones del formulario de registro
    @staticmethod
    def validar_registro(usuario):
        is_valid = True

        # Nombre y apellido deben tener al menos 2 caracteres
        if len(usuario['nombre']) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            is_valid = False

        if len(usuario['apellido']) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "registro")
            is_valid = False

        # Validación del formato de e-mail
        if not EMAIL_REGEX.match(usuario['email']):
            flash("Dirección de e-mail inválida.", "registro")
            is_valid = False

        # Restricción de edad mínima (18 años)
        if int(usuario['edad']) < 18:
            flash("Debes tener al menos 18 años para registrarte.", "registro")
            is_valid = False

        # Contraseña mínima de 8 caracteres
        if len(usuario['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "registro")
            is_valid = False

        # Las contraseñas deben coincidir
        if usuario['password'] != usuario['confirm_password']:
            flash("Las contraseñas no coinciden.", "registro")
            is_valid = False

        return is_valid