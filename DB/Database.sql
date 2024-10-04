CREATE DATABASE gestion_pedidos;
USE gestion_pedidos;

CREATE TABLE `camioneros` (
  `idCamionero` int(11) NOT NULL,
  `nombreCompleto` varchar(250) DEFAULT NULL,
  `dni` int(11) DEFAULT NULL,
  `modelo` varchar(255) DEFAULT NULL,
  `patente` varchar(75) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `clientes` (
  `idCliente` int(11) NOT NULL,
  `nombre` varchar(250) DEFAULT NULL,
  `apellido` varchar(250) DEFAULT NULL,
  `dni` int(11) DEFAULT NULL,
  `telefono` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `pedidos` (
  `idPedido` int(11) NOT NULL,
  `idCamionero` int(11) DEFAULT NULL,
  `idCliente` int(11) DEFAULT NULL,
  `fechaRegistro` date DEFAULT NULL,
  `fechaEntrega` date DEFAULT NULL,
  `estado` varchar(125) DEFAULT NULL,
  `cantPalets` int(11) DEFAULT NULL,
  `paletsDañados` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE `camioneros`
  ADD PRIMARY KEY (`idCamionero`);

ALTER TABLE `clientes`
  ADD PRIMARY KEY (`idCliente`);

ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`idPedido`),
  ADD KEY `idCamionero` (`idCamionero`),
  ADD KEY `idCliente` (`idCliente`);

ALTER TABLE `camioneros`
  MODIFY `idCamionero` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

ALTER TABLE `clientes`
  MODIFY `idCliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

ALTER TABLE `pedidos`
  MODIFY `idPedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

ALTER TABLE `pedidos`
  ADD CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`idCamionero`) REFERENCES `camioneros` (`idCamionero`) ON DELETE CASCADE,
  ADD CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`idCliente`) REFERENCES `clientes` (`idCliente`) ON DELETE CASCADE;
  
COMMIT;
