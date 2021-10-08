CREATE DATABASE IF NOT EXISTS `pythonlogin_advanced` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `pythonlogin_advanced`;

CREATE TABLE IF NOT EXISTS `accounts` (
`id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `role` enum('Member','Admin') NOT NULL DEFAULT 'Member',
  `activation_code` varchar(255) NOT NULL DEFAULT '',
  `rememberme` varchar(255) NOT NULL DEFAULT '',
  `reset` varchar(255) NOT NULL DEFAULT '',
	`buydate` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

INSERT INTO `accounts` (`id`, `username`, `password`, `email`, `role`, `activation_code`, `rememberme`, `reset`, `buydate`) VALUES
(1, 'admin', '3962f2d53f180787c6f3ef9780eb0e6a976d1244', 'admin@codeshack.io', 'Admin', 'activated', '',  '', '2014-07-31 15:42:52'),
(2, 'member', 'f046926a90af0b97acbc451bcbde266878f5f963', 'member@codeshack.io', 'Member', 'activated', '',  '', '2014-07-31 15:42:52');
