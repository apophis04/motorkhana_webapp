-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Oct 10, 2023 at 10:50 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `motorkhana`
--

-- --------------------------------------------------------

--
-- Table structure for table `car`
--

CREATE TABLE `car` (
  `car_num` int(11) NOT NULL,
  `model` varchar(20) NOT NULL,
  `drive_class` varchar(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `car`
--

INSERT INTO `car` (`car_num`, `model`, `drive_class`) VALUES
(11, 'Mini', 'FWD'),
(17, 'GR Yaris', '4WD'),
(18, 'MX-5', 'RWD'),
(20, 'Camaro', 'RWD'),
(22, 'MX-5', 'RWD'),
(31, 'Charade', 'FWD'),
(36, 'Swift', 'FWD'),
(44, 'BRZ', 'RWD');

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE `course` (
  `course_id` varchar(1) NOT NULL,
  `name` varchar(30) NOT NULL,
  `image` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `course`
--

INSERT INTO `course` (`course_id`, `name`, `image`) VALUES
('A', 'Going Loopy', 'loopy.gif'),
('B', 'Mums Favourite', 'mums.gif'),
('C', 'Walnut', 'walnut.gif'),
('D', 'Hamburger', 'hamburger.gif'),
('E', 'Shoulders Back', 'upright.gif'),
('F', 'Cracked Fluorescent', 'fluoro.gif');

-- --------------------------------------------------------

--
-- Table structure for table `driver`
--

CREATE TABLE `driver` (
  `driver_id` int(11) NOT NULL,
  `first_name` varchar(25) NOT NULL,
  `surname` varchar(25) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `caregiver` int(11) DEFAULT NULL,
  `car` int(11) NOT NULL,
  `is_junior` int(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `driver`
--

INSERT INTO `driver` (`driver_id`, `first_name`, `surname`, `date_of_birth`, `age`, `caregiver`, `car`, `is_junior`) VALUES
(120, 'Tina', 'Zheng', '2005-05-05', 18, NULL, 22, NULL),
(121, 'Li', 'Bao', NULL, NULL, NULL, 22, NULL),
(124, 'Dora', 'Watson', NULL, NULL, NULL, 31, NULL),
(128, 'Alan', 'Montgomery', NULL, NULL, NULL, 36, NULL),
(129, 'Jack', 'Atwood', '2011-08-18', 12, 135, 18, 0),
(132, 'Lucas', 'Morales', NULL, NULL, NULL, 17, NULL),
(133, 'Oliver', 'Ngatai', NULL, NULL, NULL, 44, NULL),
(135, 'Maggie', 'Atwood', NULL, NULL, NULL, 18, NULL),
(137, 'Daniel', 'Celeste', NULL, NULL, NULL, 20, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `run`
--

CREATE TABLE `run` (
  `dr_id` int(11) NOT NULL,
  `crs_id` varchar(1) NOT NULL,
  `run_num` int(11) NOT NULL,
  `seconds` float DEFAULT NULL,
  `cones` int(11) DEFAULT NULL,
  `wd` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `run`
--

INSERT INTO `run` (`dr_id`, `crs_id`, `run_num`, `seconds`, `cones`, `wd`) VALUES
(120, 'A', 1, 60.61, NULL, 0),
(120, 'A', 2, 56, NULL, 0),
(120, 'B', 1, 36.84, NULL, 0),
(120, 'B', 2, 45.24, NULL, 0),
(120, 'C', 1, 50.03, NULL, 0),
(120, 'C', 2, 64.78, NULL, 0),
(120, 'D', 1, 59.89, NULL, 0),
(120, 'D', 2, 64.89, NULL, 0),
(120, 'E', 1, 22.4, NULL, 0),
(120, 'E', 2, 34.51, NULL, 0),
(120, 'F', 1, 40.14, NULL, 0),
(120, 'F', 2, 38.68, NULL, 0),
(121, 'A', 1, NULL, NULL, 0),
(121, 'A', 2, 69.7, NULL, 0),
(121, 'B', 1, 42.18, NULL, 0),
(121, 'B', 2, 45.58, NULL, 0),
(121, 'C', 1, 61.68, NULL, 0),
(121, 'C', 2, 58.48, NULL, 0),
(121, 'D', 1, 50.29, NULL, 0),
(121, 'D', 2, 64.69, NULL, 0),
(121, 'E', 1, 25.14, NULL, 0),
(121, 'E', 2, 28.56, NULL, 0),
(121, 'F', 1, 45.92, NULL, 0),
(121, 'F', 2, 42.7, NULL, 0),
(124, 'A', 1, 76.94, 1, 0),
(124, 'A', 2, 45.41, NULL, 0),
(124, 'B', 1, 52.78, NULL, 0),
(124, 'B', 2, 41.64, NULL, 0),
(124, 'C', 1, 45.92, NULL, 0),
(124, 'C', 2, 54.46, NULL, 0),
(124, 'D', 1, 54.92, NULL, 0),
(124, 'D', 2, 56.37, NULL, 0),
(124, 'E', 1, 24.89, NULL, 0),
(124, 'E', 2, 35.8, NULL, 0),
(124, 'F', 1, 45.62, NULL, 0),
(124, 'F', 2, 49.46, NULL, 0),
(128, 'A', 1, 70.32, NULL, 0),
(128, 'A', 2, 65.38, NULL, 0),
(128, 'B', 1, 36.26, NULL, 0),
(128, 'B', 2, 47.6, NULL, 0),
(128, 'C', 1, 71.62, NULL, 0),
(128, 'C', 2, 59.84, NULL, 0),
(128, 'D', 1, 63.7, NULL, 0),
(128, 'D', 2, 54.83, NULL, 0),
(128, 'E', 1, 37.38, NULL, 0),
(128, 'E', 2, NULL, NULL, 0),
(128, 'F', 1, NULL, NULL, 0),
(128, 'F', 2, NULL, NULL, 0),
(129, 'A', 1, 58.72, 7, 1),
(129, 'A', 2, 54.37, 1, 1),
(129, 'B', 1, 51.2, NULL, 0),
(129, 'B', 2, 38.9, NULL, 1),
(129, 'C', 1, 77.43, NULL, 0),
(129, 'C', 2, 44.99, NULL, 0),
(129, 'D', 1, 40.08, NULL, 0),
(129, 'D', 2, 42.49, NULL, 0),
(129, 'E', 1, 33.53, NULL, 0),
(129, 'E', 2, 31.91, NULL, 0),
(129, 'F', 1, NULL, NULL, 0),
(129, 'F', 2, NULL, NULL, 0),
(132, 'A', 1, 60.38, NULL, 0),
(132, 'A', 2, NULL, NULL, 0),
(132, 'B', 1, 39.9, NULL, 0),
(132, 'B', 2, 38.36, NULL, 0),
(132, 'C', 1, 45.76, NULL, 0),
(132, 'C', 2, 61.99, NULL, 0),
(132, 'D', 1, 59.82, NULL, 0),
(132, 'D', 2, 55.91, NULL, 0),
(132, 'E', 1, 23.71, NULL, 0),
(132, 'E', 2, 27.33, NULL, 0),
(132, 'F', 1, 48.13, NULL, 0),
(132, 'F', 2, 37.6, NULL, 0),
(133, 'A', 1, 65.12, NULL, 0),
(133, 'A', 2, 72.27, 2, 0),
(133, 'B', 1, 51.42, NULL, 0),
(133, 'B', 2, 52.53, NULL, 0),
(133, 'C', 1, 76.32, 2, 0),
(133, 'C', 2, 61.31, NULL, 0),
(133, 'D', 1, 39.4, NULL, 0),
(133, 'D', 2, 39.97, NULL, 0),
(133, 'E', 1, 32.41, NULL, 0),
(133, 'E', 2, 36.64, NULL, 0),
(133, 'F', 1, 49.48, NULL, 0),
(133, 'F', 2, 42.93, NULL, 0),
(135, 'A', 1, 41.64, NULL, 0),
(135, 'A', 2, 61.89, NULL, 1),
(135, 'B', 1, NULL, NULL, 0),
(135, 'B', 2, 44.07, NULL, 0),
(135, 'C', 1, 61.93, NULL, 0),
(135, 'C', 2, 55.92, NULL, 0),
(135, 'D', 1, 43.02, NULL, 0),
(135, 'D', 2, 60.33, NULL, 0),
(135, 'E', 1, 26.49, NULL, 0),
(135, 'E', 2, 22, NULL, 0),
(135, 'F', 1, 42.31, NULL, 0),
(135, 'F', 2, 50.42, NULL, 0),
(137, 'A', 1, NULL, NULL, 0),
(137, 'A', 2, 49.16, NULL, 0),
(137, 'B', 1, 44.98, NULL, 1),
(137, 'B', 2, 39.09, NULL, 0),
(137, 'C', 1, 68.98, NULL, 0),
(137, 'C', 2, 63.47, NULL, 0),
(137, 'D', 1, 55.7, NULL, 0),
(137, 'D', 2, 46.37, NULL, 0),
(137, 'E', 1, 37.44, NULL, 0),
(137, 'E', 2, 26.5, NULL, 1),
(137, 'F', 1, 49.47, NULL, 0),
(137, 'F', 2, 50.32, NULL, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `car`
--
ALTER TABLE `car`
  ADD PRIMARY KEY (`car_num`);

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`course_id`);

--
-- Indexes for table `driver`
--
ALTER TABLE `driver`
  ADD PRIMARY KEY (`driver_id`),
  ADD KEY `caregiver` (`caregiver`),
  ADD KEY `car` (`car`);

--
-- Indexes for table `run`
--
ALTER TABLE `run`
  ADD PRIMARY KEY (`dr_id`,`crs_id`,`run_num`),
  ADD KEY `crs_id` (`crs_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `driver`
--
ALTER TABLE `driver`
  MODIFY `driver_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=153;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `driver`
--
ALTER TABLE `driver`
  ADD CONSTRAINT `driver_ibfk_1` FOREIGN KEY (`caregiver`) REFERENCES `driver` (`driver_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `driver_ibfk_2` FOREIGN KEY (`car`) REFERENCES `car` (`car_num`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `run`
--
ALTER TABLE `run`
  ADD CONSTRAINT `run_ibfk_1` FOREIGN KEY (`dr_id`) REFERENCES `driver` (`driver_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `run_ibfk_2` FOREIGN KEY (`crs_id`) REFERENCES `course` (`course_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
