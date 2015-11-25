-- phpMyAdmin SQL Dump
-- version 4.2.12deb2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Erstellungszeit: 13. Nov 2015 um 15:48
-- Server Version: 5.6.27-0ubuntu0.15.04.1
-- PHP-Version: 5.6.4-4ubuntu6.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Datenbank: `eschaton`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `articles`
--

CREATE TABLE IF NOT EXISTS `articles` (
`id` int(100) NOT NULL COMMENT 'ID des Artikels.',
  `EAN` int(100) NOT NULL COMMENT 'EAN des Artikels.',
  `set_number` int(100) NOT NULL COMMENT 'Setnummer des Artikels.',
  `name` varchar(100) NOT NULL COMMENT 'Name des Artikels.',
  `unit` int(3) NOT NULL COMMENT 'Sekundäreinheit des Artikels.',
  `packaging_unit` int(3) NOT NULL COMMENT 'Primäreinheit des Artikels.',
  `sell_prince_1` int(100) NOT NULL COMMENT 'Verkafspreis 1.',
  `sell_prince_2` int(100) NOT NULL COMMENT 'Verkafspreis 2.',
  `sell_prince_3` int(100) NOT NULL COMMENT 'Verkafspreis 3.',
  `buy_price_1` int(100) NOT NULL COMMENT 'Einkaufspreis 1.',
  `buy_price_2` int(100) NOT NULL COMMENT 'Einkaufspreis 2.',
  `buy_price_3` int(100) NOT NULL COMMENT 'Einkaufspreis 3.',
  `should_be_min` int(255) NOT NULL COMMENT 'So viel sollte von dem Produkt mindestens auf Lager sein.',
  `should_be_max` int(255) NOT NULL COMMENT 'So viel darf maximal von dem Produkt auf Lager sein.',
  `category` int(3) NOT NULL COMMENT 'Kategorie, der das Produkt angehört.',
  `amount` int(255) NOT NULL COMMENT 'Menge, die von dem Produkt auf Lager ist.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `articles_deleted`
--

CREATE TABLE IF NOT EXISTS `articles_deleted` (
  `id` int(100) NOT NULL COMMENT 'ID des Artikels.',
  `EAN` int(100) NOT NULL COMMENT 'EAN des Artikels.',
  `set_number` int(100) NOT NULL COMMENT 'Setnummer des Artikels.',
  `name` varchar(100) NOT NULL COMMENT 'Name des Artikels.',
  `unit` int(3) NOT NULL COMMENT 'SekundÃ¤reinheit des Artikels.',
  `packaging_unit` int(3) NOT NULL COMMENT 'PrimÃ¤reinheit des Artikels.',
  `sell_prince_1` int(100) NOT NULL COMMENT 'Verkafspreis 1.',
  `sell_prince_2` int(100) NOT NULL COMMENT 'Verkafspreis 2.',
  `sell_prince_3` int(100) NOT NULL COMMENT 'Verkafspreis 3.',
  `buy_price_1` int(100) NOT NULL COMMENT 'Einkaufspreis 1.',
  `buy_price_2` int(100) NOT NULL COMMENT 'Einkaufspreis 2.',
  `buy_price_3` int(100) NOT NULL COMMENT 'Einkaufspreis 3.',
  `should_be_min` int(255) NOT NULL COMMENT 'So viel sollte von dem Produkt mindestens auf Lager sein.',
  `should_be_max` int(255) NOT NULL COMMENT 'So viel darf maximal von dem Produkt auf Lager sein.',
  `category` int(3) NOT NULL COMMENT 'Kategorie, der das Produkt angehÃ¶rt.',
  `amount` int(255) NOT NULL COMMENT 'Menge, die von dem Produkt auf Lager ist.',
  `deleted` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitpunkt der Löschung.',
  `deleted_by` int(3) NOT NULL COMMENT 'ID des Benutzers, der die Löschung vorgenommen hat.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `categories`
--

CREATE TABLE IF NOT EXISTS `categories` (
`id` int(3) NOT NULL COMMENT 'ID der Kategorie.',
  `name` varchar(100) NOT NULL COMMENT 'Name der Kategorie.',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitstempel von der Erstellung der Kategorie.',
  `created_by` int(3) NOT NULL COMMENT 'ID des Benutzers, der die Kategorie erstellt hat.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `categories_deleted`
--

CREATE TABLE IF NOT EXISTS `categories_deleted` (
  `id` int(3) NOT NULL COMMENT 'ID der Kategorie.',
  `name` varchar(100) NOT NULL COMMENT 'Name der Kategorie.',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitstempel von der Erstellung der Kategorie.',
  `created_by` int(3) NOT NULL COMMENT 'ID des Benutzers, der die Kategorie erstellt hat.',
  `deleted` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitpunkt der Löschung.',
  `deleted_by` int(3) NOT NULL COMMENT 'ID des Benutzers, der die Löschung vorgenommen hat.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `jobs`
--

CREATE TABLE IF NOT EXISTS `jobs` (
`ID` int(3) NOT NULL COMMENT 'ID des Auftrags.',
  `name` varchar(30) NOT NULL COMMENT 'Name des Auftrags.',
  `description` varchar(30) NOT NULL COMMENT 'Beschreibung des Auftrags.',
  `priority` int(11) NOT NULL COMMENT 'Priorität des Auftrags, höhere Zahlen sind wichtigere Aufträge.',
  `for_ID` int(3) NOT NULL COMMENT 'ID der Rolle, für die der Auftrag ist.',
  `done` int(1) NOT NULL COMMENT 'Gibt an, ob der Auftrag erledigt wurde.',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitpunkt der Erstellung des Auftrags.',
  `created_by` int(3) NOT NULL COMMENT 'ID des Benutzers, welcher diesen Auftrag erstellt hat.'
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

--
-- Daten für Tabelle `jobs`
--

INSERT INTO `jobs` (`ID`, `name`, `description`, `priority`, `for_ID`, `done`, `created`, `created_by`) VALUES
(1, 'Todo', 'Todos erledigen', 1, 1, 0, '2015-10-01 15:02:06', 1),
(2, 'Bla', 'BlaBlaBlaBlaBlaBlaBlaBlaBlaBla', 1, 1, 1, '2015-10-01 15:47:45', 1),
(3, 'huhu', 'huhuhuhuhuhuhuhh', 1, 6, 1, '2015-10-01 15:47:45', 1),
(5, 'test', 'erfghgfd\n', 1, 1, 1, '2015-11-13 10:23:17', 1),
(6, 'fefehfhefhF', 'ewgwge\n', 1, 1, 1, '2015-11-13 10:25:15', 1),
(7, 'gvc', 'sdvfbg\n', 1, 2, 0, '2015-11-13 10:25:52', 1),
(8, 'sdfghb', 'sdfg\n', 2, 0, 0, '2015-11-13 10:26:32', 1),
(9, 'sdfv', 'dfg\n', 2, 1, 0, '2015-11-13 10:27:17', 1);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `jobs_deleted`
--

CREATE TABLE IF NOT EXISTS `jobs_deleted` (
  `ID` int(3) NOT NULL COMMENT 'ID des Auftrags.',
  `name` varchar(30) NOT NULL COMMENT 'Name des Auftrags.',
  `description` varchar(30) NOT NULL COMMENT 'Beschreibung des Auftrags.',
  `priority` int(11) NOT NULL COMMENT 'PrioritÃ¤t des Auftrags, hÃ¶here Zahlen sind wichtigere AuftrÃ¤ge.',
  `for_ID` int(3) NOT NULL COMMENT 'ID des Benutzers oder der Rolle, fÃ¼r die der Auftrag ist.',
  `done` int(1) NOT NULL COMMENT 'Gibt an, ob der Auftrag erledigt wurde.',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitpunkt der Erstellung des Auftrags.',
  `created_by` int(3) NOT NULL COMMENT 'ID des Benutzers, welcher diesen Auftrag erstellt hat.',
  `deleted` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitpunkt der Löschung.',
  `deleted_by` int(3) NOT NULL COMMENT 'ID des Benutzers, der die Löschung vorgenommen hat.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Daten für Tabelle `jobs_deleted`
--

INSERT INTO `jobs_deleted` (`ID`, `name`, `description`, `priority`, `for_ID`, `done`, `created`, `created_by`, `deleted`, `deleted_by`) VALUES
(10, 'iegi', 'ieneiihgfne\n', 4, 1, 0, '2015-11-13 12:33:12', 1, '2015-11-13 13:04:08', 1),
(4, '{name}', '{desc}', 1, 1, 0, '2015-11-13 09:52:30', 1, '2015-11-13 13:35:39', 1);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `nodes`
--

CREATE TABLE IF NOT EXISTS `nodes` (
`id` int(3) NOT NULL COMMENT 'ID des Standortes.',
  `name` varchar(100) NOT NULL COMMENT 'Name des Standortes',
  `adress` varchar(100) NOT NULL COMMENT 'Adresse des Standortes.',
  `image` blob NOT NULL COMMENT 'Bild oder Logo des Standortes.',
  `imagetype` varchar(10) NOT NULL COMMENT 'Typ des Bildes.',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitstempel der Erstellung des Standortes.',
  `created_by` int(3) NOT NULL COMMENT 'ID des Benutzers, der den Standort erstellt hat.'
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Daten für Tabelle `nodes`
--

INSERT INTO `nodes` (`id`, `name`, `adress`, `image`, `imagetype`, `created`, `created_by`) VALUES
(1, 'Standort 1', 'Data Nova', '', '', '2015-10-09 08:46:12', 1);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `nodes_deleted`
--

CREATE TABLE IF NOT EXISTS `nodes_deleted` (
  `id` int(3) NOT NULL COMMENT 'ID des Standortes.',
  `name` varchar(100) NOT NULL COMMENT 'Name des Standortes',
  `adress` varchar(100) NOT NULL COMMENT 'Adresse des Standortes.',
  `image` blob NOT NULL COMMENT 'Bild oder Logo des Standortes.',
  `imagetype` varchar(10) NOT NULL COMMENT 'Typ des Bildes.',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitstempel der Erstellung des Standortes.',
  `created_by` int(3) NOT NULL COMMENT 'ID des Benutzers, der den Standort erstellt hat.',
  `deleted` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitpunkt der Löschung.',
  `deleted_by` int(3) NOT NULL COMMENT 'ID des Benutzers, der die Löschung vorgenommen hat.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `roles`
--

CREATE TABLE IF NOT EXISTS `roles` (
`ID` int(3) NOT NULL COMMENT 'ID der Rolle.',
  `rolename` varchar(100) NOT NULL COMMENT 'Name der Rolle.',
  `shortname` varchar(3) NOT NULL COMMENT 'Systemname der Rolle, 3-stellig.',
  `permissions` varchar(10000) NOT NULL COMMENT 'Rechte dieser Rolle, getrennt durch '','' (Komma) oder '' '' (Leerzeichen).',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitstempel an dem diese Rolle erstellt wurde.',
  `created_by` int(3) NOT NULL COMMENT 'ID des Benutzers, der diese Rolle erstellt hat.'
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Daten für Tabelle `roles`
--

INSERT INTO `roles` (`ID`, `rolename`, `shortname`, `permissions`, `created`, `created_by`) VALUES
(1, 'Betatester', 'BET', 'tab.open.*\r\naccount.login\r\nconfig.exit', '2015-10-01 13:08:16', 1),
(2, 'Standortmanager', 'SOM', '', '2015-10-08 09:23:36', 1),
(3, 'usergroup_1', 'USR', '', '2015-11-11 14:51:40', 1);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `roles_deleted`
--

CREATE TABLE IF NOT EXISTS `roles_deleted` (
  `ID` int(3) NOT NULL COMMENT 'ID der Rolle.',
  `rolename` varchar(100) NOT NULL COMMENT 'Name der Rolle.',
  `shortname` varchar(3) NOT NULL COMMENT 'Systemname der Rolle, 3-stellig.',
  `permissions` varchar(10000) NOT NULL COMMENT 'Rechte dieser Rolle, getrennt durch '','' (Komma) oder '' '' (Leerzeichen).',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitstempel an dem diese Rolle erstellt wurde.',
  `created_by` int(3) NOT NULL COMMENT 'ID des Benutzers, der diese Rolle erstellt hat.',
  `deleted` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitpunkt der Löschung.',
  `deleted_by` int(3) NOT NULL COMMENT 'ID des Benutzers, der die Löschung vorgenommen hat.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `settings`
--

CREATE TABLE IF NOT EXISTS `settings` (
  `setting` varchar(100) NOT NULL COMMENT 'Name der Einstellung',
  `value` varchar(100) NOT NULL COMMENT 'Wert der Einstellung'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Daten für Tabelle `settings`
--

INSERT INTO `settings` (`setting`, `value`) VALUES
('sql_log_DELETE', '1'),
('sql_log_INSERT', '1'),
('sql_log_SHOW', '0'),
('sql_log_UPDATE', '1');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `units`
--

CREATE TABLE IF NOT EXISTS `units` (
`id` int(3) NOT NULL COMMENT 'ID der VPE.',
  `is_primary` tinyint(1) NOT NULL COMMENT 'Gibt an, ob diese eine Einheit ist, die aus anderen bestehen kann. z.B.: Ein Karton, der aus Flaschen bestehen kann.',
  `name_single` varchar(100) NOT NULL COMMENT 'Name der Einheit für ein Stück. Z.B.: Karton.',
  `name_multiple` varchar(100) NOT NULL COMMENT 'Name der Einheit für mehrere Stück. Z.B.: Kartons.',
  `so_much` int(100) NOT NULL COMMENT 'Nur bei Sekundäreinheiten! So viele ergeben eine Primäreinheit.',
  `is_one_of` int(3) NOT NULL COMMENT 'ID der Primäreinheit, welche diese Sekndäreinheit ergibt.',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitstempel, wann die Einheit erstellt wurde.',
  `created_by` int(3) NOT NULL COMMENT 'ID des Benutzers, der diese Einheit erstellt hat.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `units_deleted`
--

CREATE TABLE IF NOT EXISTS `units_deleted` (
  `id` int(3) NOT NULL COMMENT 'ID der VPE.',
  `is_primary` tinyint(1) NOT NULL COMMENT 'Gibt an, ob diese eine Einheit ist, die aus anderen bestehen kann. z.B.: Ein Karton, der aus Flaschen bestehen kann.',
  `name_single` varchar(100) NOT NULL COMMENT 'Name der Einheit fÃ¼r ein StÃ¼ck. Z.B.: Karton.',
  `name_multiple` varchar(100) NOT NULL COMMENT 'Name der Einheit fÃ¼r mehrere StÃ¼ck. Z.B.: Kartons.',
  `so_much` int(100) NOT NULL COMMENT 'Nur bei SekundÃ¤reinheiten! So viele ergeben eine PrimÃ¤reinheit.',
  `is_one_of` int(3) NOT NULL COMMENT 'ID der PrimÃ¤reinheit, welche diese SekndÃ¤reinheit ergibt.',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitstempel, wann die Einheit erstellt wurde.',
  `created_by` int(3) NOT NULL COMMENT 'ID des Benutzers, der diese Einheit erstellt hat.',
  `deleted` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitpunkt der Löschung.',
  `deleted_by` int(3) NOT NULL COMMENT 'ID des Benutzers, der die Löschung vorgenommen hat.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `user`
--

CREATE TABLE IF NOT EXISTS `user` (
`ID` int(3) NOT NULL COMMENT 'ID des Benutzers.',
  `username` varchar(100) NOT NULL COMMENT 'Benutzername.',
  `password` varchar(100) NOT NULL COMMENT 'Passwort des Benutzers.',
  `name` varchar(100) NOT NULL COMMENT 'Vollständiger Name.',
  `image` longblob COMMENT 'Profilbild.',
  `imagefilename` varchar(100) NOT NULL COMMENT 'Typ des Bildes.',
  `roles` varchar(100) NOT NULL COMMENT 'Rollen des Benutzers, durch '','' (Koma) oder '' '' (Leerzeichen) getrennt.',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitstempel der Erstellung des Benutzers.',
  `created_by` int(3) NOT NULL COMMENT 'ID des Benutzers, der diesen erstellt hat.',
  `usergroup` int(3) NOT NULL COMMENT 'Benutzergruppe des Benutzers.'
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Daten für Tabelle `user`
--

INSERT INTO `user` (`ID`, `username`, `password`, `name`, `image`, `imagefilename`, `roles`, `created`, `created_by`, `usergroup`) VALUES
(1, 'admin', '123', 'Administrator', NULL, '', '1, 2', '2015-10-01 13:08:26', 1, 3);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `user_deleted`
--

CREATE TABLE IF NOT EXISTS `user_deleted` (
  `ID` int(3) NOT NULL COMMENT 'ID des Benutzers.',
  `username` varchar(100) NOT NULL COMMENT 'Benutzername.',
  `password` varchar(100) NOT NULL COMMENT 'Passwort des Benutzers.',
  `name` varchar(100) NOT NULL COMMENT 'VollstÃ¤ndiger Name.',
  `image` longblob COMMENT 'Profilbild.',
  `imagefilename` varchar(100) NOT NULL COMMENT 'Typ des Bildes.',
  `roles` varchar(100) NOT NULL COMMENT 'Rollen des Benutzers, durch '','' (Koma) oder '' '' (Leerzeichen) getrennt.',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitstempel der Erstellung des Benutzers.',
  `created_by` int(3) NOT NULL COMMENT 'ID des Benutzers, der diesen erstellt hat.',
  `deleted` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Zeitpunkt der Löschung.',
  `deleted_by` int(3) NOT NULL COMMENT 'ID des Benutzers, der die Löschung vorgenommen hat.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Daten für Tabelle `user_deleted`
--

INSERT INTO `user_deleted` (`ID`, `username`, `password`, `name`, `image`, `imagefilename`, `roles`, `created`, `created_by`, `deleted`, `deleted_by`) VALUES
(388, '52061910', 'random', '7421305072327647', NULL, '', '1', '2015-10-02 14:37:33', 1, '2015-11-05 16:26:23', 1),
(387, '337786449', 'random', '7236818248675303', NULL, '', '1', '2015-10-02 14:37:33', 1, '2015-11-05 16:33:18', 1),
(385, '132847', 'random', '9752722865119803', NULL, '', '1', '2015-10-02 14:37:33', 1, '2015-11-05 16:36:48', 385),
(390, 'a', 'a', '', NULL, '', '', '2015-11-05 16:39:49', 1, '2015-11-05 16:39:59', 390),
(386, '367030248', 'random', '2509918357217403', NULL, '', '1', '2015-10-02 14:37:33', 1, '2015-11-11 14:49:00', 1),
(384, '163567330', 'random', '5276071969246087', NULL, '', '1', '2015-10-02 14:37:33', 1, '2015-11-11 14:49:01', 1),
(383, '432430192', 'random', '1498941869806065', NULL, '', '1', '2015-10-02 14:37:33', 1, '2015-11-11 14:49:02', 1),
(382, '929984222', 'random', '2906723543372794', NULL, '', '1', '2015-10-02 14:37:33', 1, '2015-11-11 14:49:03', 1),
(381, '556561862', 'random', '292327507542180', NULL, '', '1', '2015-10-02 14:37:33', 1, '2015-11-11 14:49:04', 1),
(380, '855153595', 'random', '6806141910702189', NULL, '', '1', '2015-10-02 14:37:33', 1, '2015-11-11 14:49:04', 1),
(379, '702394246', 'random', '604451193396823', NULL, '', '1', '2015-10-02 14:37:33', 1, '2015-11-11 14:49:05', 1),
(378, '131964516', 'random', '6117937206441406', NULL, '', '1', '2015-10-02 14:37:33', 1, '2015-11-11 14:49:05', 1),
(377, '677867872', 'random', '8615658066341917', NULL, '', '1', '2015-10-02 14:37:33', 1, '2015-11-11 14:49:06', 1),
(376, '141617648', 'random', '3488576651266402', NULL, '', '1', '2015-10-02 14:37:33', 1, '2015-11-11 14:49:06', 1),
(375, '506953946', 'random', '7769910105890101', NULL, '', '1', '2015-10-02 14:37:33', 1, '2015-11-11 14:49:07', 1),
(374, '60209174', 'g', '1603509142078062', NULL, '', '1', '2015-10-02 14:37:33', 1, '2015-11-11 14:49:07', 1),
(373, '962794459', 'random', '6052631603162180', NULL, '', '1', '2015-10-02 14:37:33', 1, '2015-11-11 14:49:08', 1),
(372, '730933594', 'sdfghjdsasdfg', '6207744807217208', NULL, '', '1', '2015-10-02 14:37:33', 1, '2015-11-11 14:49:09', 1),
(371, '710527901', 'dfg', '5', NULL, '', '1', '2015-10-02 14:37:32', 1, '2015-11-11 14:49:09', 1),
(3, 'random', 'fr', 'Random Guy', NULL, '', '1', '2015-10-02 14:26:01', 1, '2015-11-11 14:49:10', 1),
(2, 'hans', '123', 'Hans Peter', NULL, '', '1, 2', '2015-10-01 15:10:20', 1, '2015-11-11 14:49:10', 1);

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `articles`
--
ALTER TABLE `articles`
 ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `categories`
--
ALTER TABLE `categories`
 ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `jobs`
--
ALTER TABLE `jobs`
 ADD PRIMARY KEY (`ID`), ADD UNIQUE KEY `ID` (`ID`);

--
-- Indizes für die Tabelle `nodes`
--
ALTER TABLE `nodes`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `id` (`id`);

--
-- Indizes für die Tabelle `roles`
--
ALTER TABLE `roles`
 ADD PRIMARY KEY (`ID`);

--
-- Indizes für die Tabelle `settings`
--
ALTER TABLE `settings`
 ADD PRIMARY KEY (`setting`), ADD UNIQUE KEY `setting` (`setting`);

--
-- Indizes für die Tabelle `units`
--
ALTER TABLE `units`
 ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `user`
--
ALTER TABLE `user`
 ADD PRIMARY KEY (`ID`), ADD UNIQUE KEY `username` (`username`), ADD UNIQUE KEY `ID` (`ID`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `articles`
--
ALTER TABLE `articles`
MODIFY `id` int(100) NOT NULL AUTO_INCREMENT COMMENT 'ID des Artikels.';
--
-- AUTO_INCREMENT für Tabelle `categories`
--
ALTER TABLE `categories`
MODIFY `id` int(3) NOT NULL AUTO_INCREMENT COMMENT 'ID der Kategorie.';
--
-- AUTO_INCREMENT für Tabelle `jobs`
--
ALTER TABLE `jobs`
MODIFY `ID` int(3) NOT NULL AUTO_INCREMENT COMMENT 'ID des Auftrags.',AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT für Tabelle `nodes`
--
ALTER TABLE `nodes`
MODIFY `id` int(3) NOT NULL AUTO_INCREMENT COMMENT 'ID des Standortes.',AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT für Tabelle `roles`
--
ALTER TABLE `roles`
MODIFY `ID` int(3) NOT NULL AUTO_INCREMENT COMMENT 'ID der Rolle.',AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT für Tabelle `units`
--
ALTER TABLE `units`
MODIFY `id` int(3) NOT NULL AUTO_INCREMENT COMMENT 'ID der VPE.';
--
-- AUTO_INCREMENT für Tabelle `user`
--
ALTER TABLE `user`
MODIFY `ID` int(3) NOT NULL AUTO_INCREMENT COMMENT 'ID des Benutzers.',AUTO_INCREMENT=2;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
