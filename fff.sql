-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Värd: 127.0.0.1
-- Tid vid skapande: 05 nov 2026 kl 13:08
-- Serverversion: 10.4.32-MariaDB
-- PHP-version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Databas: `fff`
--

-- --------------------------------------------------------

--
-- Tabellstruktur `anvandare`
--

CREATE TABLE `anvandare` (
  `id` int(11) NOT NULL,
  `epost` varchar(50) NOT NULL,
  `usern` varchar(50) NOT NULL,
  `pswrd` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumpning av Data i tabell `anvandare`
--

INSERT INTO `anvandare` (`id`, `epost`, `usern`, `pswrd`) VALUES
(1, 'luddest8@gmail.com', 'Ludvig', 'najs');

-- --------------------------------------------------------

--
-- Tabellstruktur `inlagg`
--

CREATE TABLE `inlagg` (
  `id` int(11) NOT NULL,
  `anvandare_id` int(11) NOT NULL,
  `topic_id` int(11) NOT NULL,
  `innehall` text NOT NULL,
  `skapad` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellstruktur `topic`
--

CREATE TABLE `topic` (
  `id` int(11) NOT NULL,
  `rubrik` varchar(50) NOT NULL,
  `tradskapare` int(11) NOT NULL,
  `skapad` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumpning av Data i tabell `topic`
--

INSERT INTO `topic` (`id`, `rubrik`, `tradskapare`, `skapad`) VALUES
(1, 'Jag la in en tråd i phpmyadmin', 1, '2026-11-05 11:58:11'),
(2, 'FUNGERAR?!', 1, '2026-11-05 12:00:42'),
(3, 'FUNGERAR?', 1, '2026-11-05 12:02:07'),
(4, 'test', 1, '2026-11-05 12:05:32');

--
-- Index för dumpade tabeller
--

--
-- Index för tabell `anvandare`
--
ALTER TABLE `anvandare`
  ADD PRIMARY KEY (`id`);

--
-- Index för tabell `inlagg`
--
ALTER TABLE `inlagg`
  ADD PRIMARY KEY (`id`),
  ADD KEY `anvandare_id` (`anvandare_id`),
  ADD KEY `topic_id` (`topic_id`);

--
-- Index för tabell `topic`
--
ALTER TABLE `topic`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `runrik` (`rubrik`),
  ADD KEY `tradskapare` (`tradskapare`);

--
-- AUTO_INCREMENT för dumpade tabeller
--

--
-- AUTO_INCREMENT för tabell `anvandare`
--
ALTER TABLE `anvandare`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT för tabell `inlagg`
--
ALTER TABLE `inlagg`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT för tabell `topic`
--
ALTER TABLE `topic`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restriktioner för dumpade tabeller
--

--
-- Restriktioner för tabell `inlagg`
--
ALTER TABLE `inlagg`
  ADD CONSTRAINT `inlagg_ibfk_1` FOREIGN KEY (`anvandare_id`) REFERENCES `anvandare` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `inlagg_ibfk_2` FOREIGN KEY (`topic_id`) REFERENCES `topic` (`id`) ON DELETE CASCADE;

--
-- Restriktioner för tabell `topic`
--
ALTER TABLE `topic`
  ADD CONSTRAINT `topic_ibfk_1` FOREIGN KEY (`tradskapare`) REFERENCES `anvandare` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
