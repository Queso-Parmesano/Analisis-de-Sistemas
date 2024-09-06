CREATE DATABASE paintball;
USE paintball;

CREATE TABLE `promos` (
  `id` int(11) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `balas_extras` int(11) NOT NULL,
  `precio_agregado` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


INSERT INTO `promos` (`id`, `descripcion`, `balas_extras`, `precio_agregado`) VALUES
(1, 'Bla', 300, 1500.00),
(2, 'La mejor promo', 2000, 3000.00),
(3, 'zaza', 500, 200.00),
(4, 'albertinii', 10000, 5000.00);

CREATE TABLE `reservas` (
  `id` int(11) NOT NULL,
  `sucursal_id` int(11) DEFAULT NULL,
  `promo_id` int(11) DEFAULT NULL,
  `cancha` varchar(255) NOT NULL,
  `fecha` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_final` time NOT NULL,
  `balas_extras` int(11) DEFAULT NULL,
  `precio_total` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


INSERT INTO `reservas` (`id`, `sucursal_id`, `promo_id`, `cancha`, `fecha`, `hora_inicio`, `hora_final`, `balas_extras`, `precio_total`) VALUES
(3, 2, 2, '5', '2024-09-06', '12:00:00', '12:00:00', 0, 3100),
(4, 1, 3, '2', '2024-09-06', '13:00:00', '14:00:00', 100, 300);

CREATE TABLE `sucursales` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `direccion` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `sucursales` (`id`, `nombre`, `direccion`) VALUES
(1, '1', 'General Lavalle 6861'),
(2, '2', 'Teodoro Garcia 3899'),
(3, '3', 'Av. Chorroarin 200');

ALTER TABLE `promos`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `sucursales`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `promos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

ALTER TABLE `sucursales`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

ALTER TABLE `reservas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sucursal_id` (`sucursal_id`),
  ADD KEY `promo_id` (`promo_id`);

ALTER TABLE `reservas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

ALTER TABLE `reservas`
  ADD CONSTRAINT `reservas_ibfk_1` FOREIGN KEY (`sucursal_id`) REFERENCES `sucursales` (`id`),
  ADD CONSTRAINT `reservas_ibfk_2` FOREIGN KEY (`promo_id`) REFERENCES `promos` (`id`);

COMMIT;
