# Archivo principal de Flask con rutas
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import mysql.connector

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/jube_centro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELOS
class Profesional(db.Model):
    __tablename__ = 'profesionales'
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100))
    apellido_paterno = db.Column(db.String(100))
    apellido_materno = db.Column(db.String(100))
    dni = db.Column(db.String(8), unique=True)
    colegiatura = db.Column(db.String(20))
    area = db.Column(db.String(50))
    contrasena = db.Column(db.String(100))

class Estudiante(db.Model):
    __tablename__ = 'estudiantes'
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100))
    apellido_paterno = db.Column(db.String(100))
    apellido_materno = db.Column(db.String(100))
    dni = db.Column(db.String(8), unique=True)
    edad = db.Column(db.Integer)
    programa_estudios = db.Column(db.String(100))
    semestre = db.Column(db.String(10))
    turno = db.Column(db.String(10))

class Atencion(db.Model):
    __tablename__ = 'atenciones'
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100))
    apellido_paterno = db.Column(db.String(100))
    apellido_materno = db.Column(db.String(100))
    dni = db.Column(db.String(8))
    edad = db.Column(db.Integer)
    programa_estudios = db.Column(db.String(100))
    semestre = db.Column(db.String(10))
    turno = db.Column(db.String(10))
    motivo = db.Column(db.Text)
    tratamiento = db.Column(db.Text)
    fecha_atencion = db.Column(db.DateTime, default=datetime.now)
    nombre_profesional = db.Column(db.String(100))

# RUTA DE INICIO
@app.route('/')
def inicio():
    return render_template('login.html')

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    clave = request.form['clave']

    if usuario == 'admin' and clave == 'admin':
        session['tipo'] = 'admin'
        return redirect('/admin')
    else:
        profesional = Profesional.query.filter_by(dni=usuario).first()
        if profesional and profesional.contrasena == clave:
            session['tipo'] = 'profesional'
            session['nombre_profesional'] = f"{profesional.nombres} {profesional.apellido_paterno}"
            return redirect('/profesional')
        else:
            return "Usuario no válido"

# PANEL ADMIN
@app.route('/admin')
def panel_admin():
    if session.get('tipo') != 'admin':
        return redirect('/')
    profesionales = Profesional.query.all()
    return render_template('admin_panel.html', profesionales=profesionales)

# CRUD PROFESIONALES
@app.route('/admin/profesionales/agregar', methods=['POST'])
def agregar_profesional():
    nuevo = Profesional(
        nombres=request.form['nombres'],
        apellido_paterno=request.form['apellido_paterno'],
        apellido_materno=request.form['apellido_materno'],
        dni=request.form['dni'],
        colegiatura=request.form['colegiatura'],
        area=request.form['area'],
        contrasena=request.form['contrasena']
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect('/admin')

@app.route('/admin/profesionales/eliminar/<int:id>')
def eliminar_profesional(id):
    profesional = Profesional.query.get_or_404(id)
    db.session.delete(profesional)
    db.session.commit()
    return redirect('/admin')

# CRUD ESTUDIANTES

@app.route('/admin/estudiantes')
def estudiantes():
    if session.get('tipo') != 'admin':
        return redirect('/')

    busqueda = request.args.get('buscar', '')
    query = Estudiante.query
    if busqueda:
        query = query.filter(
            (Estudiante.nombres.ilike(f"%{busqueda}%")) |
            (Estudiante.apellido_paterno.ilike(f"%{busqueda}%")) |
            (Estudiante.apellido_materno.ilike(f"%{busqueda}%")) |
            (Estudiante.dni.like(f"%{busqueda}%"))
        )
    lista = query.all()
    return render_template('estudiantes.html', estudiantes=lista)


@app.route('/admin/estudiantes/agregar', methods=['POST'])
def agregar_estudiante():
    nuevo = Estudiante(
        nombres=request.form['nombres'],
        apellido_paterno=request.form['apellido_paterno'],
        apellido_materno=request.form['apellido_materno'],
        dni=request.form['dni'],
        edad=request.form['edad'],
        programa_estudios=request.form['programa_estudios'],
        semestre=request.form['semestre'],
        turno=request.form['turno']
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect('/admin/estudiantes')

@app.route('/admin/estudiantes/eliminar/<int:id>')
def eliminar_estudiante(id):
    est = Estudiante.query.get_or_404(id)
    db.session.delete(est)
    db.session.commit()
    return redirect('/admin/estudiantes')

# PANEL PROFESIONAL
@app.route('/profesional')
def panel_profesional():
    if session.get('tipo') != 'profesional':
        return redirect('/')
    atenciones = Atencion.query.all()
    return render_template('profesional_panel.html', atenciones=atenciones)

@app.route('/profesional/atencion', methods=['POST'])
def registrar_atencion():
    # Verifica si el estudiante ya existe por DNI
    estudiante = Estudiante.query.filter_by(dni=request.form['dni']).first()
    if not estudiante:
        estudiante = Estudiante(
            nombres=request.form['nombres'],
            apellido_paterno=request.form['apellido_paterno'],
            apellido_materno=request.form['apellido_materno'],
            dni=request.form['dni'],
            edad=request.form['edad'],
            programa_estudios=request.form['programa_estudios'],
            semestre=request.form['semestre'],
            turno=request.form['turno']
        )
        db.session.add(estudiante)

    nueva = Atencion(
        nombres=request.form['nombres'],
        apellido_paterno=request.form['apellido_paterno'],
        apellido_materno=request.form['apellido_materno'],
        dni=request.form['dni'],
        edad=request.form['edad'],
        programa_estudios=request.form['programa_estudios'],
        semestre=request.form['semestre'],
        turno=request.form['turno'],
        motivo=request.form['motivo'],
        tratamiento=request.form['tratamiento'],
        nombre_profesional=session['nombre_profesional']
    )
    db.session.add(nueva)
    db.session.commit()
    return redirect('/profesional')


# CERRAR SESIÓN
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/admin/profesionales/editar/<int:id>', methods=['GET'])
def formulario_editar_profesional(id):
    if session.get('tipo') != 'admin':
        return redirect('/')
    profesional = Profesional.query.get_or_404(id)
    return render_template('editar_profesional.html', profesional=profesional)


@app.route('/admin/profesionales/editar/<int:id>', methods=['POST'])
def editar_profesional(id):
    if session.get('tipo') != 'admin':
        return redirect('/')
    profesional = Profesional.query.get_or_404(id)
    profesional.nombres = request.form['nombres']
    profesional.apellido_paterno = request.form['apellido_paterno']
    profesional.apellido_materno = request.form['apellido_materno']
    profesional.dni = request.form['dni']
    profesional.colegiatura = request.form['colegiatura']
    profesional.area = request.form['area']

    nueva_contra = request.form['contrasena']
    if nueva_contra.strip():
        profesional.contrasena = nueva_contra  # Solo si se escribe una nueva

    db.session.commit()
    return redirect('/admin')

@app.route('/profesional/atencion/editar/<int:id>', methods=['GET'])
def formulario_editar_atencion(id):
    if session.get('tipo') != 'profesional':
        return redirect('/')
    atencion = Atencion.query.get_or_404(id)
    return render_template('editar_atencion.html', atencion=atencion)

@app.route('/profesional/atencion/editar/<int:id>', methods=['POST'])
def editar_atencion(id):
    if session.get('tipo') != 'profesional':
        return redirect('/')
    atencion = Atencion.query.get_or_404(id)
    atencion.nombres = request.form['nombres']
    atencion.apellido_paterno = request.form['apellido_paterno']
    atencion.apellido_materno = request.form['apellido_materno']
    atencion.dni = request.form['dni']
    atencion.edad = request.form['edad']
    atencion.programa_estudios = request.form['programa_estudios']
    atencion.semestre = request.form['semestre']
    atencion.turno = request.form['turno']
    atencion.motivo = request.form['motivo']
    atencion.tratamiento = request.form['tratamiento']
    db.session.commit()
    return redirect('/profesional')

@app.route('/profesional/atencion/eliminar/<int:id>')
def eliminar_atencion(id):
    if session.get('tipo') != 'profesional':
        return redirect('/')
    atencion = Atencion.query.get_or_404(id)
    db.session.delete(atencion)
    db.session.commit()
    return redirect('/profesional')

# Ruta: Mostrar formulario de cambio de contraseña
@app.route('/profesional/cambiar_contrasena')
def formulario_cambiar_contrasena():
    if session.get('tipo') != 'profesional':
        return redirect('/')
    return render_template('cambiar_contrasena.html')

# Ruta: Procesar cambio de contraseña
@app.route('/profesional/cambiar_contrasena', methods=['POST'])
def cambiar_contrasena():
    if session.get('tipo') != 'profesional':
        return redirect('/')

    # Busca al profesional en sesión
    profesional = Profesional.query.filter(
        Profesional.nombres + " " + Profesional.apellido_paterno == session['nombre_profesional']
    ).first()

    if profesional:
        nueva = request.form['nueva_contrasena']
        profesional.contrasena = nueva
        db.session.commit()
        return redirect('/profesional')
    else:
        return "Error: Usuario no encontrado"

@app.route('/constancia/<int:atencion_id>')
def constancia_publica(atencion_id):
    atencion = Atencion.query.get_or_404(atencion_id)

    import qrcode, io, base64
    data = f"{request.url_root}constancia/{atencion.id}"
    qr = qrcode.make(data)
    buf = io.BytesIO()
    qr.save(buf, format='PNG')
    qr_base64 = base64.b64encode(buf.getvalue()).decode('ascii')

    return render_template('constancia_publica.html',
                           atencion=atencion,
                           qr_code=qr_base64,
                           link=data)



@app.route('/profesional/filtrar')
def filtrar_atenciones():
    if session.get('tipo') != 'profesional':
        return redirect('/')

    nombre = request.args.get('nombre', '').strip()
    dni = request.args.get('dni', '').strip()
    fecha = request.args.get('fecha', '').strip()

    query = Atencion.query

    if nombre:
        query = query.filter(
            (Atencion.nombres.ilike(f"%{nombre}%")) |
            (Atencion.apellido_paterno.ilike(f"%{nombre}%")) |
            (Atencion.apellido_materno.ilike(f"%{nombre}%"))
        )
    if dni:
        query = query.filter(Atencion.dni.like(f"%{dni}%"))
    if fecha:
        query = query.filter(db.func.date(Atencion.fecha_atencion) == fecha)

    resultados = query.all()
    return render_template('tabla_atenciones.html', atenciones=resultados)


# INICIALIZAR
if __name__ == '__main__':
    app.run(debug=True)
