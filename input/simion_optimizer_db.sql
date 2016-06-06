-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 11, 2013 at 11:01 AM
-- Server version: 5.5.31
-- PHP Version: 5.3.10-1ubuntu3.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `simion_optimizer_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `best_values`
--

CREATE TABLE IF NOT EXISTS `best_values` (
  `geom_it_id` int(11) NOT NULL,
  `geom_part_id` int(11) NOT NULL,
  `best_value_global` float NOT NULL,
  `target_f_best` text NOT NULL,
  PRIMARY KEY (`geom_it_id`,`geom_part_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `jobs`
--

CREATE TABLE IF NOT EXISTS `jobs` (
  `job_id` int(11) NOT NULL AUTO_INCREMENT,
  `geom_it_id` int(11) NOT NULL,
  `geom_part_id` int(11) NOT NULL,
  `volt_it_id` int(11) NOT NULL,
  `part_volt_id` int(4) NOT NULL,
  `datetime` datetime NOT NULL,
  `status` int(1) NOT NULL COMMENT '0 offen,1 in arbeit, 2 done',
  `id_R` varchar(15) NOT NULL COMMENT 'welcher R dass rechnet',
  `zielfunktion` double NOT NULL,
  PRIMARY KEY (`job_id`),
  KEY `geom_it_id` (`geom_it_id`,`geom_part_id`,`volt_it_id`,`part_volt_id`),
  KEY `status` (`status`),
  KEY `zielfunktion` (`zielfunktion`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `jobs`
--

INSERT INTO `jobs` (`job_id`, `geom_it_id`, `geom_part_id`, `volt_it_id`, `part_volt_id`, `datetime`, `status`, `id_R`, `zielfunktion`) VALUES
(1, 0, 0, 1, 0, '2013-06-10 12:12:28', 0, '', 0),
(2, 0, 0, 1, 1, '2013-06-10 12:12:28', 0, '', 0),
(3, 0, 0, 1, 2, '2013-06-10 12:12:28', 0, '', 0),
(4, 0, 0, 1, 3, '2013-06-10 12:12:28', 0, '', 0);

-- --------------------------------------------------------

--
-- Table structure for table `optimierungs_parameter`
--

CREATE TABLE IF NOT EXISTS `optimierungs_parameter` (
  `anzahl_bad_news` int(11) NOT NULL,
  `max_diff_bad_news` float NOT NULL,
  `anzahl_geom_part` int(11) NOT NULL,
  `anzahl_volt_part` int(11) NOT NULL,
  `max_volt_iterations` int(11) NOT NULL,
  `anz_v_pro_pa` text NOT NULL,
  `fix_voltages` text NOT NULL,
  `fix_electrodes` text NOT NULL,
  `iob_filename` text NOT NULL,
  `PA_filenames` text NOT NULL,
  PRIMARY KEY (`iob_filename`(5))
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `optimierungs_parameter`
--

INSERT INTO `optimierungs_parameter` (`anzahl_bad_news`, `max_diff_bad_news`, `anzahl_geom_part`, `anzahl_volt_part`, `max_volt_iterations`, `anz_v_pro_pa`, `fix_voltages`, `fix_electrodes`, `iob_filename`, `PA_filenames`) VALUES
(1111, 0.0001, 0, 4, 25, '(lp0\nI3\naI0\naI0\na.', '(lp0\n(lp1\nF0.0\naF-70.0\naa(lp2\na(lp3\na.', '(lp0\n(lp1\nI1\naI2\naa(lp2\na(lp3\na.', 'einzel.iob', '(lp0\nS''einzel.pa#''\np1\na.');

-- --------------------------------------------------------

--
-- Table structure for table `status_of_gem_particle`
--

CREATE TABLE IF NOT EXISTS `status_of_gem_particle` (
  `id_R` int(11) NOT NULL,
  `geom_it_id` int(11) NOT NULL,
  `geom_part_id` int(11) NOT NULL,
  `status` int(1) NOT NULL DEFAULT '0' COMMENT '1-fertig',
  PRIMARY KEY (`geom_it_id`,`geom_part_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `status_r`
--

CREATE TABLE IF NOT EXISTS `status_r` (
  `R_id` int(11) NOT NULL,
  `status` int(1) NOT NULL COMMENT '0 idle,1 rechnen,5 read/write',
  `datetime` datetime NOT NULL,
  `geom_it_id` int(11) NOT NULL,
  `geom_part_id` int(11) NOT NULL,
  PRIMARY KEY (`R_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `voltages`
--

CREATE TABLE IF NOT EXISTS `voltages` (
  `job_id` int(11) NOT NULL,
  `geom_iteration_id` int(11) NOT NULL,
  `geom_particle_id` int(11) NOT NULL,
  `voltage_iteration_id` int(11) NOT NULL,
  `voltage_particle_id` int(11) NOT NULL,
  `volt_id` int(11) NOT NULL,
  `voltage` float NOT NULL,
  `v` float NOT NULL,
  PRIMARY KEY (`geom_iteration_id`,`geom_particle_id`,`voltage_iteration_id`,`voltage_particle_id`,`volt_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `voltages`
--

INSERT INTO `voltages` (`job_id`, `geom_iteration_id`, `geom_particle_id`, `voltage_iteration_id`, `voltage_particle_id`, `volt_id`, `voltage`, `v`) VALUES
(1, 0, 0, 1, 0, 0, 0, 0),
(1, 0, 0, 1, 0, 1, 0, 0),
(1, 0, 0, 1, 0, 2, 0, 0),
(2, 0, 0, 1, 1, 0, -4.05752, 0),
(2, 0, 0, 1, 1, 1, -70.5521, 0),
(2, 0, 0, 1, 1, 2, -77.2908, 0),
(3, 0, 0, 1, 2, 0, -64.159, 0),
(3, 0, 0, 1, 2, 1, 143.511, 0),
(3, 0, 0, 1, 2, 2, 184.121, 0),
(4, 0, 0, 1, 3, 0, -114.619, 0),
(4, 0, 0, 1, 3, 1, 145.546, 0),
(4, 0, 0, 1, 3, 2, 97.1988, 0);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
