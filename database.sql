CREATE USER 'odem'@'localhost' IDENTIFIED BY 'password';

CREATE DATABASE odem;

USE odem;

CREATE TABLE IF NOT EXISTS `users` (
`id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(25) NOT NULL,
  `mail` varchar(50) NOT NULL,
  `password` char(32) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `datasets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(25) NOT NULL,
  `content` text NOT NULL,
  `link` varchar(512) NOT NULL,
  `user` int(11) NOT NULL,
  `tags` varchar(512),
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

GRANT ALL PRIVILEGES ON odem.* TO 'odem'@'localhost' WITH GRANT OPTION;

FLUSH privileges;quit
