-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 24-07-2026 a las 04:07:22
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
  `me_descripcion` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `medicamentos`
--

INSERT INTO `medicamentos` (`id_medicamentos`, `me_nombre_comercial`, `me_forma_farmaceutica`, `me_concentracion`, `me_fecha_caducidad`, `me_descripcion`) VALUES
(1, 'Paracetamol', 'Solidas', '500mg', '2027-12-31', 'Analgésico'),
(2, 'Amoxicilina', 'Liquidas', '250mg/5ml', '2026-06-30', 'Recomedable.');

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
  `id_enfermera_principal` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pacientes`
--

INSERT INTO `pacientes` (`id_pacientes`, `pa_nombre`, `pa_apellidos`, `pa_fecha_nacimiento`, `pa_nombre_contacto_emergencia`, `pa_tel_contacto_emergencia`, `id_enfermera_principal`) VALUES
(9, 'karla', 'sosa', '2026-07-16', 'sepa', 1122334455, 19),
(10, 'Monse', 'Campusano Juarez', '2019-07-18', 'sosa', 1122334455, 19);

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
  `tr_descripcion` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `us_especialidad` enum('Geriatría',',Médico General') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuarios`, `us_tipo_usuario`, `us_nombre`, `us_apellidos`, `us_fecha_nacimiento`, `us_contraseña`, `us_telefono`, `us_correo_electronico`, `us_direccion`, `us_especialidad`) VALUES
(1, 'Doctor', 'Juan', 'Morales Santiago', '2060-05-12', '12345', 1234567890, 'juan@gmail.com', 'Calle Falsa 123', 'Geriatría'),
(7, 'Enfermera', 'Camila', 'Santiago Juárez', '2091-07-17', '12345', 2147483647, 'camila@gmail.com', 'Calle 1 de enero', ''),
(15, 'Doctor', 'Camila', 'Camacho', '2026-07-15', '12345', 4455667788, 'camila', 'calle 1 de enero', 'Geriatría'),
(16, 'Administrador', 'Pedro', 'García', '2026-07-15', '12345', 4455667788, 'pedro@garcia', 'calle falsa', 'Geriatría'),
(17, 'Enfermera', 'Juan carlos', 'Lopez velazsquez', '2026-07-08', '12345', 1122334455, 'carlos@gamil.com', 'calle falsa', ''),
(18, 'Doctor', 'Paola', 'Montayo Nose', '2026-07-15', '12345', 5537196729, 'paola@montayo', 'calle falsa', 'Geriatría'),
(19, 'Enfermera', 'Manuel', 'Santiago Garcia', '2091-07-18', '12345', 1122334455, 'santi@gmail', 'calle 1 de enero ', ''),
(20, 'Doctor', 'a', 'a', '2026-07-16', 'a', 1, 'a', 'a1', ',Médico General'),
(22, 'Enfermera', 'e', 'e', '2026-07-16', 'e', 2, 'e', 'e1', ',Médico General'),
(23, 'Administrador', 'b', 'b', '2026-07-16', 'b', 1, 'b', 'b1', 'Geriatría');

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
  MODIFY `id_pacientes` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `receta`
--
ALTER TABLE `receta`
  MODIFY `id_recetas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `tratamientos`
--
ALTER TABLE `tratamientos`
  MODIFY `id_tratamientos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuarios` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

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
