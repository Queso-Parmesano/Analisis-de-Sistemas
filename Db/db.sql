
create database balines;
use balines;

create table sucursales(
idSucursal int(11) auto_increment,
direccion varchar(120),
localidad varchar(70),
primary key(idSucursal)
) ENGINE=InnoDB;

create table promos(
idPromo int(11) auto_increment,
balasExtras int(3),
precio int(8),
tiempoExtra time,
primary key(idPromo)
) ENGINE=InnoDB;

create table reservas(
idReserva int(11) auto_increment,
idSucursal int(11),
idPromo int(11),
nombreCliente varchar(150),
fechaInicio datetime,
fechaFin datetime,
precio int(11),
balasExtras int(11),
primary key (idReserva),
foreign key (idSucursal) references sucursales(idSucursal),
foreign key (idPromo) references promos(idPromo)
) ENGINE=InnoDB;
