from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.entrada import Entrada

def usuario_autenticado():
    return 'usuario_id' in session

@app.route('/dashboard')
def dashboard():
    if not usuario_autenticado():
        flash("Debe haber iniciado sesión para ver esta página.", "error_login")
        return redirect('/')

    entradas = Entrada.get_by_user_id({'usuario_id': session['usuario_id']})
    return render_template('dashboard.html', entradas=entradas)

@app.route('/nueva')
def nueva():
    if not usuario_autenticado():
        flash("El usuario debe haber iniciado sesión para ver esta página", "error_login")
        return redirect('/')
    return render_template('nueva.html')

@app.route('/nueva/crear', methods=['POST'])
def crear_entrada():
    if not usuario_autenticado():
        return redirect('/')

    if not Entrada.validar_entrada(request.form):
        return redirect('/nueva')

    data = {
        'fecha_entrada': request.form['fecha_entrada'],
        'notas': request.form['notas'],
        'usuario_id': session['usuario_id']
    }
    Entrada.save(data)
    return redirect('/dashboard')

@app.route('/editar/<int:id>')
def editar(id):
    if not usuario_autenticado():
        return redirect('/')

    entrada = Entrada.get_by_id({'id': id})
    if not entrada or entrada.usuario_id != session['usuario_id']:
        flash("No puedes acceder a esta entrada.", "error")
        return redirect('/dashboard')

    return render_template('editar.html', entrada=entrada)

@app.route('/editar/actualizar/<int:id>', methods=['POST'])
def actualizar_entrada(id):
    if not usuario_autenticado():
        return redirect('/')

    entrada = Entrada.get_by_id({'id': id})
    if not entrada or entrada.usuario_id != session['usuario_id']:
        return redirect('/dashboard')

    if not Entrada.validar_entrada(request.form):
        return redirect(f'/editar/{id}')

    data = {
        'id': id,
        'fecha_entrada': request.form['fecha_entrada'],
        'notas': request.form['notas'],
        'usuario_id': session['usuario_id']
    }
    Entrada.update(data)
    return redirect('/dashboard')

@app.route('/borrar/<int:id>')
def borrar(id):
    if not usuario_autenticado():
        return redirect('/')

    Entrada.delete({'id': id, 'usuario_id': session['usuario_id']})
    return redirect('/dashboard')

@app.route('/ver/<int:id>')
def ver(id):
    if not usuario_autenticado():
        return redirect('/')

    entrada = Entrada.get_by_id({'id': id})
    if not entrada or entrada.usuario_id != session['usuario_id']:
        flash("Acceso no autorizado.", "error")
        return redirect('/dashboard')

    return render_template('ver.html', entrada=entrada)

@app.route('/buscar', methods=['POST'])
def procesar_busqueda():
    termino = request.form.get('termino', '').strip()
    return redirect(f'/buscar/{termino}')

@app.route('/buscar/<termino>')
def buscar(termino=""):
    if not usuario_autenticado():
        return redirect('/')

    data = {
        'usuario_id': session['usuario_id'],
        'termino': f"%{termino}%"
    }
    resultados = Entrada.buscar_por_notas(data)
    return render_template('buscar.html', entradas=resultados, termino=termino)