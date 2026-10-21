from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_app.models.entrada import Entrada
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Ruta principal: muestra el formulario de login y registro
@app.route('/')
def index():
    # Si el usuario ya inició sesión, lo mandamos directo al dashboard
    if 'usuario_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

# Procesa el registro de nuevos usuarios
@app.route('/registrar', methods=['POST'])
def registrar():
    # Validamos que los datos ingresados cumplan con las reglas (edad, correo, etc.)
    if not Usuario.validar_registro(request.form):
        return redirect('/')
    
    # Encriptamos la contraseña antes de guardarla en la base de datos por seguridad
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'edad': request.form['edad'],
        'password': pw_hash
    }
    
    # Guardamos en la BD y guardamos el ID en la sesión
    usuario_id = Usuario.save(data)
    session['usuario_id'] = usuario_id
    
    return redirect('/dashboard')

# Procesa el inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    # Buscamos al usuario por su email
    usuario = Usuario.get_by_email({'email': request.form['email']})
    
    # Si no existe el correo, mostramos un error genérico por seguridad
    if not usuario:
        flash("Credenciales inválidas", "login")
        return redirect('/')
    
    # Comparamos la contraseña ingresada con el hash guardado
    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Credenciales inválidas", "login")
        return redirect('/')
    
    # Si la contraseña es correcta, iniciamos la sesión
    session['usuario_id'] = usuario.id
    return redirect('/dashboard')

# Cierra la sesión activa
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')