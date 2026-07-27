-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 27-07-2026 a las 07:17:04
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
  `id_medicamentos` int(11) NOT NULL,
  `me_nombre_comercial` varchar(50) NOT NULL,
  `me_forma_farmaceutica` enum('Solidas','Semisolidas','Liquidas','Inhalables') DEFAULT NULL,
  `me_concentracion` varchar(50) NOT NULL,
  `me_fecha_caducidad` date NOT NULL,
  `me_descripcion` varchar(100) DEFAULT NULL,
  `me_activo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `medicamentos`
--

INSERT INTO `medicamentos` (`id_medicamentos`, `me_nombre_comercial`, `me_forma_farmaceutica`, `me_concentracion`, `me_fecha_caducidad`, `me_descripcion`, `me_activo`) VALUES
(1, 'Paracetamol', 'Solidas', '500mg', '2027-12-31', 'Analgésico', 1),
(2, 'Amoxicilina', 'Liquidas', '250mg/5ml', '2026-06-30', 'Recomedable.', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pacientes`
--

CREATE TABLE `pacientes` (
  `id_pacientes` int(11) NOT NULL,
  `pa_nombre` varchar(50) NOT NULL,
  `pa_apellidos` varchar(50) NOT NULL,
  `pa_fecha_nacimiento` date NOT NULL,
  `pa_nombre_contacto_emergencia` varchar(50) NOT NULL,
  `pa_tel_contacto_emergencia` bigint(10) NOT NULL,
  `id_enfermera_principal` int(11) NOT NULL,
  `pa_activo` tinyint(4) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pacientes`
--

INSERT INTO `pacientes` (`id_pacientes`, `pa_nombre`, `pa_apellidos`, `pa_fecha_nacimiento`, `pa_nombre_contacto_emergencia`, `pa_tel_contacto_emergencia`, `id_enfermera_principal`, `pa_activo`) VALUES
(9, 'karla', 'Medina', '2026-07-24', 'Eli', 1122334455, 17, 1),
(10, 'Monse', 'Campusano Juarez', '2026-07-24', 'Juan', 1122334455, 19, 0),
(11, 'Emili', 'Garcia Lopes', '2026-07-01', 'Paloma juarez', 2233445566, 17, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `receta`
--

CREATE TABLE `receta` (
  `id_recetas` int(11) NOT NULL,
  `id_medicamento` int(11) NOT NULL,
  `id_tratamiento` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(6, 'Alzheimer', 10, 18, '2026-07-25', '2026-07-30', 'Precaución ', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuarios` int(11) NOT NULL,
  `us_tipo_usuario` enum('Doctor','Enfermera','Administrador') DEFAULT NULL,
  `us_nombre` varchar(50) NOT NULL,
  `us_apellidos` varchar(50) NOT NULL,
  `us_fecha_nacimiento` date NOT NULL,
  `us_contraseña` varchar(255) NOT NULL,
  `us_telefono` bigint(10) NOT NULL,
  `us_correo_electronico` varchar(50) NOT NULL,
  `us_direccion` varchar(200) NOT NULL,
  `us_especialidad` enum('Geriatría',',Médico General') DEFAULT NULL,
  `us_activo` tinyint(4) NOT NULL DEFAULT 1,
  `us_cedula` int(11) NOT NULL DEFAULT 10000000
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuarios`, `us_tipo_usuario`, `us_nombre`, `us_apellidos`, `us_fecha_nacimiento`, `us_contraseña`, `us_telefono`, `us_correo_electronico`, `us_direccion`, `us_especialidad`, `us_activo`, `us_cedula`) VALUES
(7, 'Enfermera', 'Camila', 'Santiago Juárez', '2091-07-17', '12345', 2147483647, 'camila@gmail.com', 'Calle 1 de enero', '', 1, 10000000),
(15, 'Doctor', 'Camila', 'Camacho', '2026-07-15', '12345', 4455667788, 'camila', 'calle 1 de enero', 'Geriatría', 1, 10000000),
(16, 'Administrador', 'Pedro', 'García', '2026-07-15', '12345', 4455667788, 'pedro@garcia', 'calle falsa', 'Geriatría', 1, 10000000),
(17, 'Enfermera', 'Juan carlos', 'Lopez velazsquez', '2026-07-08', '12345', 1122334455, 'carlos@gamil.com', 'calle falsa', '', 1, 10000000),
(18, 'Doctor', 'Paola', 'Montayo Nose', '2026-07-15', '12345', 5537196729, 'paola@montayo', 'calle falsa', 'Geriatría', 1, 10000000),
(19, 'Enfermera', 'Manuel', 'Santiago Garcia', '2091-07-18', '12345', 1122334455, 'santi@gmail', 'calle 1 de enero ', '', 1, 10000000),
(20, 'Doctor', 'Juan', 'camacho', '2000-12-02', '12345', 1122334455, 'juan@camacho', '2 de octubre', '', 1, 10000000);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `medicamentos`
--
ALTER TABLE `medicamentos`
  ADD PRIMARY KEY (`id_medicamentos`);

--
-- Indices de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  ADD PRIMARY KEY (`id_pacientes`),
  ADD KEY `id_enfermera_principal` (`id_enfermera_principal`);

--
-- Indices de la tabla `receta`
--
ALTER TABLE `receta`
  ADD PRIMARY KEY (`id_recetas`),
  ADD KEY `receta_ibfk_1` (`id_medicamento`),
  ADD KEY `receta_ibfk_2` (`id_tratamiento`);

--
-- Indices de la tabla `tratamientos`
--
ALTER TABLE `tratamientos`
  ADD PRIMARY KEY (`id_tratamientos`),
  ADD KEY `tratamientos_ibfk_1` (`id_paciente`),
  ADD KEY `tratamientos_ibfk_2` (`id_doctor`);

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
  MODIFY `id_medicamentos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  MODIFY `id_pacientes` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `receta`
--
ALTER TABLE `receta`
  MODIFY `id_recetas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `tratamientos`
--
ALTER TABLE `tratamientos`
  MODIFY `id_tratamientos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuarios` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `pacientes`
--
ALTER TABLE `pacientes`
  ADD CONSTRAINT `pacientes_ibfk_1` FOREIGN KEY (`id_enfermera_principal`) REFERENCES `usuarios` (`id_usuarios`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `receta`
--
ALTER TABLE `receta`
  ADD CONSTRAINT `receta_ibfk_1` FOREIGN KEY (`id_medicamento`) REFERENCES `medicamentos` (`id_medicamentos`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `receta_ibfk_2` FOREIGN KEY (`id_tratamiento`) REFERENCES `tratamientos` (`id_tratamientos`) ON DELETE CASCADE ON UPDATE CASCADE;

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
