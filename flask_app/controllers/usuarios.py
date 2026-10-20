from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def registro():
    if not Usuario.validar_registro(request.form):
        return redirect('/')

    pwd_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'edad': request.form['edad'],
        'password': pwd_hash
    }
    usuario_id = Usuario.save(data)
    session['usuario_id'] = usuario_id
    session['nombre'] = request.form['nombre']
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    usuario = Usuario.get_by_email({'email': request.form.get('email', '')})
    
    if not usuario:
        flash("El email debe estar registrado en BD", "error_login")
        return redirect('/')

    if not bcrypt.check_password_hash(usuario.password, request.form.get('password', '')):
        flash("La contraseña debe ser la correspondiente a la BD", "error_login")
        return redirect('/')

    session['usuario_id'] = usuario.id
    session['nombre'] = usuario.nombre
    return redirect('/dashboard')

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()
    return redirect('/')