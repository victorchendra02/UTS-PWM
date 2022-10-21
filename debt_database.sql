-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Oct 21, 2022 at 08:36 AM
-- Server version: 5.7.31
-- PHP Version: 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `debt_database`
--

-- --------------------------------------------------------

--
-- Table structure for table `customer_table`
--

DROP TABLE IF EXISTS `customer_table`;
CREATE TABLE IF NOT EXISTS `customer_table` (
  `id_customer` int(11) NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(255) DEFAULT NULL,
  `address` text,
  `phone_number` varchar(16) DEFAULT NULL,
  `debt_total` int(11) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id_customer`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer_table`
--

INSERT INTO `customer_table` (`id_customer`, `customer_name`, `address`, `phone_number`, `debt_total`, `is_active`) VALUES
(1, 'Victor Chendra Yah', 'Jl. Industri Raya BLOK B14, Kompleks RMCI', '-10084', 20000, 1),
(2, 'Filbert Thomas K.', 'Jl. Industri Raya BLOK B14, Kompleks RMCI', '0895-9211-1768', 680000, 1),
(3, 'Elbert Chandra', 'Jl. Industri Raya BLOK B14, Kompleks RMCI', '0895-9211-1768', 250000, 1),
(4, 'Jacob J. Warouw', 'Jl. Industri Raya BLOK B14, Kompleks RMCI', '0895-9211-1768', 900000, 1),
(6, 'Evan Christopher', 'Jl. Industri Raya BLOK B14, Kompleks RMCI', '0895-9211-1768', 400000, 1),
(7, 'Renata Tamara Teguh Karyadi', 'Jl. Industri Raya BLOK B14, Kompleks RMCI', '0895-9211-1768', 1000000, 1),
(8, 'Yudha Wira T.', 'Jl. Industri Raya BLOK B14, Kompleks RMCI', '0895-9211-1768', 0, 1),
(9, 'Elsa Nove Teresia', 'Jl. Industri Raya BLOK B14, Kompleks RMCI', '0895-9211-1768', 0, 1),
(10, 'Jason Caleb E. P.', 'Jl. Industri Raya BLOK B14, Kompleks RMCI', '0895-9211-1768', 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `transactions_table`
--

DROP TABLE IF EXISTS `transactions_table`;
CREATE TABLE IF NOT EXISTS `transactions_table` (
  `id_trns` int(11) NOT NULL AUTO_INCREMENT,
  `id_customer` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `debt_amount` int(11) DEFAULT NULL,
  `remark` text,
  `is_paid` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id_trns`),
  KEY `id_customer` (`id_customer`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `transactions_table`
--

INSERT INTO `transactions_table` (`id_trns`, `id_customer`, `date`, `debt_amount`, `remark`, `is_paid`) VALUES
(1, 1, '2022-10-21', 20000, 'Nasi goreng', 0),
(12, 6, '2022-10-21', 300000, 'Bayar', 0),
(4, 2, '2022-10-21', 250000, 'AOV', 0),
(5, 7, '2022-10-21', 1000000, 'Nyuknyang', 0),
(6, 4, '2022-10-21', 300000, 'Warteg', 0),
(7, 4, '2022-10-21', 300000, 'Warteg', 0),
(8, 4, '2022-10-21', 300000, 'Warteg', 0),
(9, 6, '2022-10-21', 100000, 'Legend of Mobile', 0),
(10, 2, '2022-10-21', 430000, 'Skin Valorant', 0),
(11, 3, '2022-10-21', 250000, 'Nasi padang', 0);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
