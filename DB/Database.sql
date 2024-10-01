
create database galletas;
use galletas;

create table camioneros(
idCamionero int(11) auto_increment,
nombreCompleto varchar(250),
dni int(11),
modelo varchar(255),
patente varchar(75),
primary key (idCamionero)
);

create table clientes(
idCliente int(11) auto_increment,
nombre varchar(250),
apellido varchar(250),
dni int(11),
telefono varchar(25),
primary key (idCliente)
);

create table pedidos(
idPedido int(11) auto_increment,
idCamionero int(11),
idCliente int(11),
fechaRegistro date,
fechaEntrega date,
estado varchar(125),
peso varchar(125),
primary key (idPedido),
foreign key(idCamionero) references camioneros(idCamionero),
foreign key(idCliente) references clientes(idCliente)
);

create table pedidosEntregable(
idPedido int(11),
fechaRegistro date,
fechaEntrega date,
peso varchar(125)
)
