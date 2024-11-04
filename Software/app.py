from wtforms import StringField, IntegerField, SelectField, SubmitField
from flask import Flask, session, request, render_template, redirect, url_for, flash
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
import datetime

#pip install Flask Flask_SQLAlchemy mysql_connector Flask_WTF

app = Flask(__name__, static_folder="templates", static_url_path="")

app.config['SECRET_KEY'] = 'a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost/chimesubo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    contraseña = db.Column(db.String(250), nullable=False)
    rol = db.Column(db.String(50), nullable=False)

class LoginForm(FlaskForm):
    nombre = StringField('Nombre de Usuario', validators=[DataRequired()])
    contraseña = StringField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

@app.route('/login/<role>', methods=['GET', 'POST'])
def login(role):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Lógica de autenticación para Vendedor
        if role == 'vendedor':
            vendedor = Vendedor.query.filter_by(nombre=username).first()  # Busca el vendedor en la base de datos
            if vendedor and password == 'holaalumno':  # Si el vendedor existe y la contraseña es correcta
                session['role'] = 'vendedor'
                session['vendedor_id'] = vendedor.id  # Guarda el id del vendedor en la sesión
                session['vendedor_nombre'] = vendedor.nombre  # Guarda el nombre del vendedor en la sesión
                return redirect(url_for('vendedor_dashboard'))
        
        # Lógica de autenticación para Gerente (credenciales fijas)
        elif role == 'gerente' and username == 'gerente' and password == 'holaolaso':
            session['role'] = 'gerente'
            return redirect(url_for('gerente_dashboard'))

        # Mensaje de error si las credenciales son incorrectas
        flash('Credenciales incorrectas', 'danger')
    
    return render_template('login.html', role=role)

@app.route('/gerente_dashboard')
def gerente_dashboard():
    return render_template('gerente_dashboard.html')

@app.route('/vendedor_dashboard')
def vendedor_dashboard():
    return render_template('vendedor_dashboard.html')

@app.route('/logout')
def logout():
    # Limpiar la sesión
    session.clear()
    flash('Has cerrado sesión con éxito.', 'success')
    return redirect(url_for('index'))

class Vendedor(db.Model):
    __tablename__ = 'vendedor'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    ventas = db.relationship('Venta', backref='vend', lazy=True)
    inventarios = db.relationship('Inventario', backref='vendedor_autor', lazy=True)

class Inventario(db.Model):
    __tablename__ = 'inventario'
    id = db.Column(db.Integer, primary_key=True)
    autor = db.Column(db.Integer, db.ForeignKey('vendedor.id'), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    ventas = db.relationship('Venta', backref='invent', lazy=True)

class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer, primary_key=True)
    idA = db.Column(db.Integer, db.ForeignKey('inventario.id'), nullable=False)
    idV = db.Column(db.Integer, db.ForeignKey('vendedor.id'), nullable=False)
    nombreC = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.Integer, nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    marcaA = db.Column(db.String(50), nullable=False)
    modeloA = db.Column(db.String(50), nullable=False)
    precioA = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=datetime.date.today)

class VendedorForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[DataRequired()])
    submit = SubmitField('Registrar Vendedor')

class InventarioForm(FlaskForm):
    marca = StringField('Marca', validators=[DataRequired()])
    modelo = StringField('Modelo', validators=[DataRequired()])
    precio = IntegerField('Precio', validators=[DataRequired()])
    submit = SubmitField('Añadir al Inventario')

class VentaForm(FlaskForm):
    idA = SelectField('Inventario', coerce=int, validators=[DataRequired()])
    idV = SelectField('Vendedor', coerce=int, validators=[DataRequired()])
    nombreC = StringField('Nombre del Cliente', validators=[DataRequired()])
    dni = IntegerField('DNI', validators=[DataRequired()])
    telefono = IntegerField('Teléfono', validators=[DataRequired()])
    submit = SubmitField('Registrar Venta')

class EditVentaForm(FlaskForm):
    nombreC = StringField('Nombre del Cliente', validators=[DataRequired()])
    dni = IntegerField('DNI', validators=[DataRequired()])
    telefono = IntegerField('Teléfono', validators=[DataRequired()])
    fecha = StringField('Fecha', validators=[DataRequired()])  # Podrías usar un campo DateField si prefieres
    submit = SubmitField('Actualizar Venta')

@app.route('/')
def index():
    if 'role' in session:
        if session['role'] == 'gerente':
            return redirect(url_for('gerente_dashboard'))
        elif session['role'] == 'vendedor':
            return redirect(url_for('vendedor_dashboard'))
    return render_template('index.html')

@app.route('/registrar_vendedor', methods=['GET', 'POST'])
def registrar_vendedor():
    form = VendedorForm()
    if form.validate_on_submit():
        nuevoVendedor = Vendedor(nombre=form.nombre.data)
        db.session.add(nuevoVendedor)
        db.session.commit()
        
        # Guardar el vendedor en la sesión
        session['vendedor_id'] = nuevoVendedor.id
        session['vendedor_nombre'] = nuevoVendedor.nombre
        
        flash('Vendedor registrado exitosamente', 'success')
        return redirect(url_for('registrar_vendedor'))
    return render_template('registrar_vendedor.html', form=form)

@app.route('/ver_inventario')
def ver_inventario():
    inventario = Inventario.query.all()
    return render_template('ver_inventario.html', inventario=inventario)

# Ruta para editar un registro de inventario
@app.route('/editar_inventario/<int:id>', methods=['GET', 'POST'])
def editar_inventario(id):
    inventario = Inventario.query.get_or_404(id)
    form = InventarioForm(obj=inventario)
    if form.validate_on_submit():
        inventario.marca = form.marca.data
        inventario.modelo = form.modelo.data
        inventario.precio = form.precio.data
        db.session.commit()
        flash('Inventario actualizado correctamente', 'success')
        return redirect(url_for('ver_inventario'))
    return render_template('editar_inventario.html', form=form)

# Ruta para eliminar un registro de inventario
@app.route('/eliminar_inventario/<int:id>', methods=['POST'])
def eliminar_inventario(id):
    inventario = Inventario.query.get_or_404(id)
    db.session.delete(inventario)
    db.session.commit()
    flash('Inventario eliminado correctamente', 'success')
    return redirect(url_for('ver_inventario'))

@app.route('/stockear_inventario', methods=['GET', 'POST'])
def stockear_inventario():
    form = InventarioForm()
    if form.validate_on_submit():
        nuevoInventario = Inventario(
            autor=session.get('vendedor_id'),
            marca=form.marca.data,
            modelo=form.modelo.data,
            precio=form.precio.data,
        )
        db.session.add(nuevoInventario)
        db.session.commit()
        flash('Inventario añadido exitosamente', 'success')
        return redirect(url_for('stockear_inventario'))
    return render_template('stockear_inventario.html', form=form)

@app.route('/registrar_venta', methods=['GET', 'POST'])
def registrar_venta():
    form = VentaForm()
    form.idA.choices = [(i.id, f"{i.marca} {i.modelo}") for i in Inventario.query.all()]
    form.idV.choices = [(v.id, v.nombre) for v in Vendedor.query.all() if v.id == session.get('vendedor_id')]  # Solo muestra el vendedor actual
    
    if form.validate_on_submit():
        venta = Venta(
            idA=Inventario.query.get(form.idA.data).id,
            idV=session.get('vendedor_id'),
            nombreC=form.nombreC.data,
            dni=form.dni.data,
            telefono=form.telefono.data,
            marcaA=Inventario.query.get(form.idA.data).marca,
            modeloA=Inventario.query.get(form.idA.data).modelo,
            precioA=Inventario.query.get(form.idA.data).precio,
        )
        db.session.add(venta)

        # Eliminar el inventario correspondiente
        inventario = Inventario.query.get(form.idA.data)
        db.session.delete(inventario)

        db.session.commit()

        flash('Venta registrada y modelo eliminado del inventario exitosamente', 'success')
        return redirect(url_for('registrar_venta'))
    return render_template('registrar_venta.html', form=form)

@app.route('/ver_estadisticas')
def ver_estadisticas():
    # Obtener todas las ventas y el inventario
    ventas = Venta.query.all()
    inventario = Inventario.query.all()

    # Inicializar los contadores
    total_ventas_por_vendedor = {}
    stockeos_por_vendedor = {}
    venta_mas_cara = None

    # Contar las ventas y calcular la venta más cara
    for venta in ventas:
        vendedor_id = venta.idV
        total_ventas_por_vendedor[vendedor_id] = total_ventas_por_vendedor.get(vendedor_id, 0) + 1

        if venta_mas_cara is None or venta.precioA > venta_mas_cara.precioA:
            venta_mas_cara = venta

    # Contar los stockeos por vendedor
    for item in inventario:
        autor_id = item.autor  # Asegúrate de que este atributo esté definido en tu modelo
        stockeos_por_vendedor[autor_id] = stockeos_por_vendedor.get(autor_id, 0) + 1

    # Obtener los vendedores
    vendedores = Vendedor.query.all()

    # Obtener el vendedor que más ha vendido
    vendedor_mas_vendido_id = max(total_ventas_por_vendedor, key=total_ventas_por_vendedor.get, default=None)
    vendedor_mas_vendido = next((v for v in vendedores if v.id == vendedor_mas_vendido_id), None)

    return render_template('ver_estadisticas.html', 
                           total_ventas_por_vendedor=total_ventas_por_vendedor,
                           venta_mas_cara=venta_mas_cara,
                           stockeos_por_vendedor=stockeos_por_vendedor,
                           vendedor_mas_vendido=vendedor_mas_vendido,
                           vendedores=vendedores)

@app.route('/ver_ventas')
def ver_ventas():
    if 'role' not in session:
        flash('Debes iniciar sesión para acceder a esta página.', 'danger')
        return redirect(url_for('index'))
    ventas = Venta.query.all()
    return render_template('ver_ventas.html', ventas=ventas)

@app.route('/ver_ventas_ger')
def ver_ventas_ger():
    if 'role' not in session:
        flash('Debes iniciar sesión para acceder a esta página.', 'danger')
        return redirect(url_for('index'))
    ventas = Venta.query.all()
    return render_template('ver_ventas_ger.html', ventas=ventas)

@app.route('/editar_venta/<int:id>', methods=['GET', 'POST'])
def editar_venta(id):
    venta = Venta.query.get_or_404(id)
    form = EditVentaForm(obj=venta)

    if form.validate_on_submit():
        # Actualizar solo los campos permitidos
        venta.nombreC = form.nombreC.data
        venta.dni = form.dni.data
        venta.telefono = form.telefono.data
        venta.fecha = form.fecha.data
        db.session.commit()
        flash('Venta actualizada con éxito', 'success')
        return redirect(url_for('ver_ventas'))

    # Pasar los valores actuales a los campos del formulario
    form.nombreC.data = venta.nombreC
    form.dni.data = venta.dni
    form.telefono.data = venta.telefono
    form.fecha.data = venta.fecha.strftime('%Y-%m-%d')  # Si usas DateField, ajusta según sea necesario

    return render_template('editar_venta.html', form=form)

# Ruta para eliminar un registro de inventario
@app.route('/eliminar_venta/<int:id>', methods=['POST'])
def eliminar_venta(id):
    ventas = Venta.query.get_or_404(id)
    db.session.delete(ventas)
    db.session.commit()
    flash('Venta eliminada correctamente', 'success')
    return redirect(url_for('ver_ventas'))

@app.route('/ver_vendedores')
def ver_vendedores():
    vendedores = Vendedor.query.all()
    return render_template('ver_vendedores.html', vendedores=vendedores)

# Ruta para editar un registro de inventario
@app.route('/editar_vendedor/<int:id>', methods=['GET', 'POST'])
def editar_vendedor(id):
    vendedor = Vendedor.query.get_or_404(id)
    form = VendedorForm(obj=vendedor)
    if form.validate_on_submit():
        vendedor.nombre = form.nombre.data
        db.session.commit()
        flash('Vendedor actualizado correctamente', 'success')
        return redirect(url_for('ver_vendedores'))
    return render_template('editar_vendedor.html', form=form)

# Ruta para eliminar un registro de inventario
@app.route('/eliminar_vendedor/<int:id>', methods=['POST'])
def eliminar_vendedor(id):
    vendedor = Vendedor.query.get_or_404(id)
    db.session.delete(vendedor)
    db.session.commit()
    flash('Vendedor eliminado correctamente', 'success')
    return redirect(url_for('ver_vendedores'))

if __name__ == '__main__':
    app.run(host='www.phobos.net.ar', debug=True) 
