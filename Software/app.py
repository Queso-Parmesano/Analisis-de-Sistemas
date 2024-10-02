from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField, TextAreaField
from flask import Flask, render_template, request, redirect, url_for, flash
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
import datetime

#pip install Flask Flask_SQLAlchemy Flask_WTF mysql-connector-python

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ss'
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
    peso = StringField('Peso', validators=[DataRequired()])
    submit = SubmitField('Tomar Pedido')

class ActualizarEstadoForm(FlaskForm):
    estado = SelectField('Estado del Pedido', choices=[
        ('Procesando', 'Procesando'),
        ('En Camino', 'En Camino'),
        ('Demorado', 'Demorado'),
        ('Entregado', 'Entregado')
    ], validators=[DataRequired()])
    submit = SubmitField('Actualizar Estado')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar_camionero', methods=['GET', 'POST'])
def registrar_camionero():
    form = CamioneroForm()
    if form.validate_on_submit():
        nuevo_camionero = Camionero(
            nombreCompleto=form.nombreCompleto.data,
            dni=form.dni.data,
            modelo=form.modelo.data,
            patente=form.patente.data
        )
        db.session.add(nuevo_camionero)
        db.session.commit()
        flash('Camionero registrado exitosamente', 'success')
        return redirect(url_for('index'))
    return render_template('registrar_camionero.html', form=form)

@app.route('/registrar_cliente', methods=['GET', 'POST'])
def registrar_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        nuevo_cliente = Cliente(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            dni=form.dni.data,
            telefono=form.telefono.data
        )
        db.session.add(nuevo_cliente)
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
        nuevo_pedido = Pedido(
            idCamionero=form.idCamionero.data,
            idCliente=form.idCliente.data,
            fechaEntrega=form.fechaEntrega.data,
            peso=form.peso.data,
            estado='Procesando'
        )
        db.session.add(nuevo_pedido)
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
    if form.validate_on_submit():
        pedido.estado = form.estado.data
        db.session.commit()
        flash('Estado del pedido actualizado exitosamente', 'success')
        return redirect(url_for('ver_pedidos'))
    return render_template('actualizar_estado.html', form=form, pedido=pedido)

if __name__ == '__main__':
    app.run(debug=True)