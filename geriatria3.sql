-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-07-2026 a las 17:30:51
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

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
-- Estructura de tabla para la tabla `medicamentos`
--

CREATE TABLE `medicamentos` (
  `id_me` int(11) NOT NULL,
  `me_nombre_comercial` varchar(50) NOT NULL,
  `me_tipo` enum('Jarabe','Tabletas','Inyecciones','Parches','Supositorios') NOT NULL DEFAULT 'Tabletas',
  `me_concentracion` varchar(50) NOT NULL,
  `me_fecha_caducidad` date NOT NULL,
  `me_descripcion` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `medicamentos`
--

INSERT INTO `medicamentos` (`id_me`, `me_nombre_comercial`, `me_tipo`, `me_concentracion`, `me_fecha_caducidad`, `me_descripcion`) VALUES
(1, 'Paracetamol', 'Tabletas', '500mg', '2027-12-31', 'Analgésico'),
(2, 'Amoxicilina', 'Jarabe', '250mg/5ml', '2026-06-30', 'Antibiótico');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pacientes`
--

CREATE TABLE `pacientes` (
  `id_pa` int(11) NOT NULL,
  `pa_nombre` varchar(50) NOT NULL,
  `pa_apellidos` varchar(50) NOT NULL,
  `pa_fecha_nacimiento` date NOT NULL,
  `pa_nombre_contacto_emergencia` varchar(50) NOT NULL,
  `pa_tel_contacto_emergencia` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pacientes`
--

INSERT INTO `pacientes` (`id_pa`, `pa_nombre`, `pa_apellidos`, `pa_fecha_nacimiento`, `pa_nombre_contacto_emergencia`, `pa_tel_contacto_emergencia`) VALUES
(1, 'Maria', 'Lopez', '1945-10-20', 'Pedro Lopez', 2147483647),
(2, '', '', '0000-00-00', '', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `receta`
--

CREATE TABLE `receta` (
  `id_receta` int(11) NOT NULL,
  `id_medicamento` int(11) NOT NULL,
  `id_tratamiento` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `receta`
--

INSERT INTO `receta` (`id_receta`, `id_medicamento`, `id_tratamiento`) VALUES
(1, 1, 1),
(2, 2, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tratamiento`
--

CREATE TABLE `tratamiento` (
  `id_tratamiento` int(11) NOT NULL,
  `tr_nombre` varchar(50) NOT NULL,
  `id_paciente` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `tr_fecha_inicio` date NOT NULL,
  `tr_fecha_final` date NOT NULL,
  `tr_descripcion` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tratamiento`
--

INSERT INTO `tratamiento` (`id_tratamiento`, `tr_nombre`, `id_paciente`, `id_usuario`, `tr_fecha_inicio`, `tr_fecha_final`, `tr_descripcion`) VALUES
(1, 'Tratamiento Resfriado', 1, 1, '2026-07-01', '2026-07-10', 'Tratamiento estándar');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuarios` int(11) NOT NULL,
  `us_tipo_usuario` enum('Doctor','Enfermera') DEFAULT NULL,
  `us_nombre` varchar(50) NOT NULL,
  `us_apellidos` varchar(50) NOT NULL,
  `us_fecha_nacimiento` date NOT NULL,
  `us_contraseña` varchar(255) NOT NULL,
  `us_telefono` int(10) NOT NULL,
  `us_correo_electronico` varchar(50) NOT NULL,
  `us_direccion` varchar(200) NOT NULL,
  `us_especialidad` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuarios`, `us_tipo_usuario`, `us_nombre`, `us_apellidos`, `us_fecha_nacimiento`, `us_contraseña`, `us_telefono`, `us_correo_electronico`, `us_direccion`, `us_especialidad`) VALUES
(1, 'Doctor', 'Juan', 'Perez', '1980-05-15', '12345', 1234567890, 'juan@mail.com', 'Calle Falsa 123', 'Geriatría'),
(2, 'Enfermera', 'Karla', 'lozno', '2000-06-22', '12345', 1344556633, 'karla@mail.com', 'calle 1 de enero', 'geriatria');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `medicamentos`
--
ALTER TABLE `medicamentos`
  ADD PRIMARY KEY (`id_me`);

--
-- Indices de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  ADD PRIMARY KEY (`id_pa`);

--
-- Indices de la tabla `receta`
--
ALTER TABLE `receta`
  ADD PRIMARY KEY (`id_receta`),
  ADD KEY `id_medicamento` (`id_medicamento`),
  ADD KEY `id_tratamiento` (`id_tratamiento`);

--
-- Indices de la tabla `tratamiento`
--
ALTER TABLE `tratamiento`
  ADD PRIMARY KEY (`id_tratamiento`),
  ADD KEY `id_paciente` (`id_paciente`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuarios`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `medicamentos`
--
ALTER TABLE `medicamentos`
  MODIFY `id_me` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  MODIFY `id_pa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `receta`
--
ALTER TABLE `receta`
  MODIFY `id_receta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `tratamiento`
--
ALTER TABLE `tratamiento`
  MODIFY `id_tratamiento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuarios` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `receta`
--
ALTER TABLE `receta`
  ADD CONSTRAINT `receta_ibfk_1` FOREIGN KEY (`id_medicamento`) REFERENCES `medicamentos` (`id_me`),
  ADD CONSTRAINT `receta_ibfk_2` FOREIGN KEY (`id_tratamiento`) REFERENCES `tratamiento` (`id_tratamiento`);

--
-- Filtros para la tabla `tratamiento`
--
ALTER TABLE `tratamiento`
  ADD CONSTRAINT `tratamiento_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id_pa`),
  ADD CONSTRAINT `tratamiento_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuarios`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
