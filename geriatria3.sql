-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-08-2026 a las 09:47:39
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `geriatria3`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tratamientos`
--

CREATE TABLE `tratamientos` (
  `id_tratamientos` int(11) NOT NULL,
  `tr_nombre` varchar(50) NOT NULL,
  `id_paciente` int(11) NOT NULL,
  `id_doctor` int(11) NOT NULL,
  `tr_fecha_inicio` date NOT NULL,
  `tr_fecha_final` date NOT NULL,
  `tr_descripcion` varchar(100) NOT NULL,
  `tr_activo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tratamientos`
--

INSERT INTO `tratamientos` (`id_tratamientos`, `tr_nombre`, `id_paciente`, `id_doctor`, `tr_fecha_inicio`, `tr_fecha_final`, `tr_descripcion`, `tr_activo`) VALUES
(6, 'Alzheimer', 10, 18, '2026-07-25', '2026-07-30', 'Precaución ', 1),
(7, 'Diabetes', 11, 20, '2026-07-28', '2026-07-31', '...', 0),
(8, 'Epilepsia', 10, 15, '2026-07-29', '2026-08-05', '...', 1),
(9, 'Cinesiterapia', 10, 18, '2026-07-29', '2026-08-04', 'Tome sus debidas precauciones', 1),
(10, 'prueba', 10, 18, '2026-07-31', '2026-07-16', 'ffgbg', 1),
(11, 'Rehabilitación', 9, 20, '2026-07-31', '2026-08-05', 'Tomar el paracetamol para el dolor', 0),
(12, 'Optometria', 12, 15, '2026-08-03', '2026-08-20', 'Acudir con los estudios realizados previamente.', 0),
(13, 'Anemia3', 12, 24, '2026-08-04', '2026-08-20', 'Toma tus mediacamentos', 1),
(14, 'Quimioterapia', 12, 24, '2026-08-02', '2026-09-08', 'Tomar los fármacos correspondientes', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `tratamientos`
--
ALTER TABLE `tratamientos`
  ADD PRIMARY KEY (`id_tratamientos`),
  ADD KEY `tratamientos_ibfk_1` (`id_paciente`),
  ADD KEY `tratamientos_ibfk_2` (`id_doctor`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `tratamientos`
--
ALTER TABLE `tratamientos`
  MODIFY `id_tratamientos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `tratamientos`
--
ALTER TABLE `tratamientos`
  ADD CONSTRAINT `tratamientos_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id_pacientes`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tratamientos_ibfk_2` FOREIGN KEY (`id_doctor`) REFERENCES `usuarios` (`id_usuarios`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
