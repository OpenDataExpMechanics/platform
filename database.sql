CREATE USER 'odem'@'localhost' IDENTIFIED BY 'password';

CREATE DATABASE odem;

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `name` varchar(25) NOT NULL,
  `mail` varchar(50) NOT NULL,
  `password` char(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
