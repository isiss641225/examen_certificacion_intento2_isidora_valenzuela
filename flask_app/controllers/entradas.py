from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.entrada import Entrada
from flask_app.models.usuario import Usuario

# Vista principal del usuario donde ve sus entradas
@app.route('/dashboard')
def dashboard():
    # Protección de ruta: no pueden entrar si no han iniciado sesión
    if 'usuario_id' not in session:
        return redirect('/')
    
    usuario = Usuario.get_by_id({'id': session['usuario_id']})
    # Se usa get_by_user que es como está nombrado en tu modelo entrada.py
    entradas = Entrada.get_by_user({'usuario_id': session['usuario_id']})
    
    return render_template('dashboard.html', usuario=usuario, entradas=entradas)

# Renderiza la plantilla para crear una entrada nueva
@app.route('/nueva')
def nueva():
    if 'usuario_id' not in session:
        return redirect('/')
    return render_template('nueva.html')

# Recibe el formulario y guarda la nueva entrada
@app.route('/crear_entrada', methods=['POST'])
def crear_entrada():
    if 'usuario_id' not in session:
        return redirect('/')
    
    # Validamos que la fecha sea obligatoria y no venga vacía
    if not Entrada.validar_entrada(request.form):
        return redirect('/nueva')
    
    data = {
        'fecha': request.form['fecha'],
        'notas': request.form['notas'],
        'usuario_id': session['usuario_id']
    }
    
    Entrada.save(data)
    return redirect('/dashboard')

# Muestra una entrada específica
@app.route('/ver/<int:id>')
def ver(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    entrada = Entrada.get_by_id({'id': id})
    
    # Validación de seguridad: aseguramos que el usuario solo pueda ver sus propias notas
    if not entrada or entrada.usuario_id != session['usuario_id']:
        return redirect('/dashboard')
        
    return render_template('ver.html', entrada=entrada)

# Vista para editar una entrada existente
@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    entrada = Entrada.get_by_id({'id': id})
    
    # Verificamos autoría antes de permitir cargar la pantalla de edición
    if not entrada or entrada.usuario_id != session['usuario_id']:
        return redirect('/dashboard')
        
    return render_template('editar.html', entrada=entrada)

# Procesa los cambios enviados desde el formulario de edición
@app.route('/actualizar_entrada/<int:id>', methods=['POST'])
def actualizar_entrada(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    entrada_existente = Entrada.get_by_id({'id': id})
    
    # Doble chequeo de seguridad por si intentan modificar la URL manualmente
    if not entrada_existente or entrada_existente.usuario_id != session['usuario_id']:
        return redirect('/dashboard')
        
    if not Entrada.validar_entrada(request.form):
        return redirect(f'/editar/{id}')
    
    data = {
        'id': id,
        'fecha': request.form['fecha'],
        'notas': request.form['notas']
    }
    
    Entrada.update(data)
    return redirect('/dashboard')

# Borra una entrada
@app.route('/borrar/<int:id>')
def borrar(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    entrada = Entrada.get_by_id({'id': id})
    
    # Aseguramos que solo el dueño original pueda eliminar la entrada
    if entrada and entrada.usuario_id == session['usuario_id']:
        Entrada.delete({'id': id})
        
    return redirect('/dashboard')

# Búsqueda por palabra clave dentro del contenido de las notas
@app.route('/buscar', methods=['POST'])
def buscar():
    if 'usuario_id' not in session:
        return redirect('/')
    
    termino = request.form['termino']
    data = {
        'termino': termino,
        'usuario_id': session['usuario_id']
    }
    
    entradas = Entrada.search(data)
    return render_template('buscar.html', entradas=entradas, termino=termino)