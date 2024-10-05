from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField
from flask import Flask, render_template, redirect, url_for, flash
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
import datetime

#pip install Flask Flask_SQLAlchemy Flask_WTF 

app = Flask(__name__, static_folder="templates", static_url_path="")

app.config['SECRET_KEY'] = 'zaza'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost/gestion_pedidos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Camionero(db.Model):
    __tablename__ = 'camioneros'
    idCamionero = db.Column(db.Integer, primary_key=True)
    nombreCompleto = db.Column(db.String(250), nullable=False)
    dni = db.Column(db.Integer, nullable=False)
    modelo = db.Column(db.String(255), nullable=False)
    patente = db.Column(db.String(75), nullable=False)
    pedidos = db.relationship('Pedido', backref='camionero', lazy=True)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    idCliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    apellido = db.Column(db.String(250), nullable=False)
    dni = db.Column(db.Integer, nullable=False)
    telefono = db.Column(db.String(25), nullable=False)
    pedidos = db.relationship('Pedido', backref='cliente', lazy=True)

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    idPedido = db.Column(db.Integer, primary_key=True)
    idCamionero = db.Column(db.Integer, db.ForeignKey('camioneros.idCamionero'), nullable=False)
    idCliente = db.Column(db.Integer, db.ForeignKey('clientes.idCliente'), nullable=False)
    fechaRegistro = db.Column(db.Date, nullable=False, default=datetime.date.today)
    fechaEntrega = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(125), nullable=False, default='procesando')
    cantPalets = db.Column(db.String(125), nullable=False)
    paletsDañados = db.Column(db.String(125), nullable=False)

class CamioneroForm(FlaskForm):
    nombreCompleto = StringField('Nombre Completo', validators=[DataRequired()])
    dni = IntegerField('DNI', validators=[DataRequired()])
    modelo = StringField('Modelo del Camión', validators=[DataRequired()])
    patente = StringField('Patente', validators=[DataRequired()])
    submit = SubmitField('Registrar Camionero')

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    dni = IntegerField('DNI', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    submit = SubmitField('Registrar Cliente')

class PedidoForm(FlaskForm):
    idCamionero = SelectField('Camionero', coerce=int, validators=[DataRequired()])
    idCliente = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    fechaEntrega = DateField('Fecha de Entrega', format='%Y-%m-%d', validators=[DataRequired()])
    palets = StringField('Palets', validators=[DataRequired()])
    submit = SubmitField('Tomar Pedido')

class ActualizarEstadoForm(FlaskForm):
    estado = SelectField('Estado del Pedido', choices=[
        ('Procesando', 'Procesando'),
        ('En Camino', 'En Camino'),
        ('Demorado', 'Demorado'),
        ('Entregado', 'Entregado'),
        ('Rechazado', 'Rechazado')
    ], validators=[DataRequired()])
    submit = SubmitField('Actualizar Estado')

class ReportarPedido(FlaskForm):
    cantPaq = IntegerField('Cantidad de palets en mal estado', validators=[DataRequired()])
    submit = SubmitField('Reportar pedido')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar_camionero', methods=['GET', 'POST'])
def registrar_camionero():
    form = CamioneroForm()
    if form.validate_on_submit():
        nuevoCamionero = Camionero(
            nombreCompleto=form.nombreCompleto.data,
            dni=form.dni.data,
            modelo=form.modelo.data,
            patente=form.patente.data
        )
        db.session.add(nuevoCamionero)
        db.session.commit()
        flash('Camionero registrado exitosamente', 'success')
        return redirect(url_for('index'))
    return render_template('registrar_camionero.html', form=form)

@app.route('/registrar_cliente', methods=['GET', 'POST'])
def registrar_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        nuevoCliente = Cliente(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            dni=form.dni.data,
            telefono=form.telefono.data
        )
        db.session.add(nuevoCliente)
        db.session.commit()
        flash('Cliente registrado exitosamente', 'success')
        return redirect(url_for('index'))
    return render_template('registrar_cliente.html', form=form)

@app.route('/tomar_pedido', methods=['GET', 'POST'])
def tomar_pedido():
    form = PedidoForm()
    form.idCamionero.choices = [(c.idCamionero, c.nombreCompleto) for c in Camionero.query.all()]
    form.idCliente.choices = [(c.idCliente, f"{c.nombre} {c.apellido}") for c in Cliente.query.all()]
    if form.validate_on_submit():
        nuevoPedido = Pedido(
            idCamionero = form.idCamionero.data,
            idCliente = form.idCliente.data,
            fechaEntrega = form.fechaEntrega.data,
            cantPalets = form.palets.data,
            estado ='Procesando',
            paletsDañados = 0
        )
        db.session.add(nuevoPedido)
        db.session.commit()
        flash('Pedido tomado exitosamente', 'success')
        return redirect(url_for('index'))
    return render_template('tomar_pedido.html', form=form)

@app.route('/ver_pedidos')
def ver_pedidos():
    pedidos = Pedido.query.all()
    return render_template('ver_pedidos.html', pedidos=pedidos)

@app.route('/actualizar_estado/<int:idPedido>', methods=['GET', 'POST'])
def actualizar_estado(idPedido):
    pedido = Pedido.query.get_or_404(idPedido)
    form = ActualizarEstadoForm(obj=pedido)
    if pedido.estado == 'Entregado':
        flash('El pedido ya fue entregado, no se puede actualizar.', 'info')
        return redirect(url_for('ver_pedidos'))
    
    if pedido.estado == 'Rechazado':
        flash('El pedido fue Rechazado, no se puede actualizar.', 'info')
        return redirect(url_for('ver_pedidos'))
    
    if form.validate_on_submit():
        pedido.estado = form.estado.data
        db.session.commit()
        flash('Estado del pedido actualizado con exito.', 'success')
        return redirect(url_for('ver_pedidos'))
    return render_template('actualizar_estado.html', form=form, pedido=pedido)

@app.route('/reportar_pedido/<int:idPedido>', methods=['GET','POST'])
def reportar_pedido(idPedido):
    pedido = Pedido.query.get_or_404(idPedido)
    form = ReportarPedido(obj=pedido)
    
    if type(form.cantPaq.data) == int: 
        if form.cantPaq.data <= 0 or form.cantPaq.data > pedido.cantPalets:
            flash('Ingrese un valor valido', 'info')
            return render_template('reportar_pedido.html', form=form, pedido=pedido)

    
    if form.validate_on_submit() and form.cantPaq.data >= 0:
        pedido.paletsDañados = pedido.paletsDañados + form.cantPaq.data
        pedido.cantPalets = pedido.cantPalets - form.cantPaq.data
        db.session.commit()
        flash('Se reporto el pedido con exito.', 'info')
        return redirect(url_for('ver_pedidos'))
        
    return render_template('reportar_pedido.html', form=form, pedido=pedido)

if __name__ == '__main__':
    app.run(host= 'www.phobos.net.ar', debug= True)
