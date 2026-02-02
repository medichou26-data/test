-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : ven. 02 jan. 2026 à 17:02
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `librarydb`
--

-- --------------------------------------------------------

--
-- Structure de la table `authors`
--

CREATE TABLE `authors` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `bio` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `authors`
--

INSERT INTO `authors` (`id`, `name`, `bio`, `created_at`) VALUES
(1, 'Victor Hugo', 'Écrivain français du XIXe siècle, auteur des Misérables', '2026-01-01 21:48:41'),
(2, 'Albert Camus', 'Philosophe et écrivain français, prix Nobel de littérature', '2026-01-01 21:48:41'),
(3, 'Simone de Beauvoir', 'Écrivaine et philosophe française, figure du féminisme', '2026-01-01 21:48:41'),
(4, 'Antoine de Saint-Exupéry', 'Écrivain et aviateur français', '2026-01-01 21:48:41'),
(5, 'Marcel Proust', 'Écrivain français, auteur de À la recherche du temps perdu', '2026-01-01 21:48:41');

-- --------------------------------------------------------

--
-- Structure de la table `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `author_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `year` int(11) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `pdf_file` varchar(255) DEFAULT NULL,
  `cover_image` varchar(255) DEFAULT 'default-cover.jpg',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `books`
--

INSERT INTO `books` (`id`, `title`, `author_id`, `category_id`, `year`, `description`, `pdf_file`, `cover_image`, `created_at`, `updated_at`) VALUES
(3, 'Le Deuxième Sexe', 3, 5, 1949, 'Essai fondateur du féminisme moderne', 'SQL_for_Data_Analysis.pdf', 'rr.jpg', '2026-01-01 21:48:41', '2026-01-02 15:37:39'),
(4, 'Le Petit Prince', 4, 6, 1943, 'Conte philosophique et poétique', 'TP2_1Conteneurisation_Decembre_2020.pdf', 'r.png', '2026-01-01 21:48:41', '2026-01-02 15:37:04'),
(5, 'Du côté de chez Swann', 5, 1, 1913, 'Premier tome de À la recherche du temps perdu', 'lab4__Apache_kafka.pdf', 'O.jpg', '2026-01-01 21:48:41', '2026-01-02 15:36:28'),
(6, 'cv', 2, 5, 2011, 'MON CV', 'LAB_mongodbSPARK.pdf', 'book-41609_1.png', '2026-01-01 22:01:50', '2026-01-01 22:01:50'),
(7, 'test', 2, 6, 1999, 'hello word', 'LAB_mongodbSPARK.pdf', 'logo2.png', '2026-01-02 15:46:44', '2026-01-02 15:46:44');

-- --------------------------------------------------------

--
-- Structure de la table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `categories`
--

INSERT INTO `categories` (`id`, `name`, `description`, `created_at`) VALUES
(1, 'Roman', 'Œuvres de fiction narrative', '2026-01-01 21:48:41'),
(2, 'Philosophie', 'Ouvrages de réflexion philosophique', '2026-01-01 21:48:41'),
(3, 'Poésie', 'Recueils de poèmes', '2026-01-01 21:48:41'),
(4, 'Science-Fiction', 'Littérature d\'anticipation et de science-fiction', '2026-01-01 21:48:41'),
(5, 'Essai', 'Textes argumentatifs et analytiques', '2026-01-01 21:48:41'),
(6, 'Jeunesse', 'Littérature destinée aux jeunes lecteurs', '2026-01-01 21:48:41');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `authors`
--
ALTER TABLE `authors`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_name` (`name`);

--
-- Index pour la table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`),
  ADD KEY `author_id` (`author_id`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `idx_title` (`title`),
  ADD KEY `idx_year` (`year`);

--
-- Index pour la table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_name` (`name`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `authors`
--
ALTER TABLE `authors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT pour la table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `books`
--
ALTER TABLE `books`
  ADD CONSTRAINT `books_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `authors` (`id`),
  ADD CONSTRAINT `books_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
