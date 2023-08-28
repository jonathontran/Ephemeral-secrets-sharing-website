create database ephemeralSecrets;
use ephemeralSecrets;

CREATE TABLE `secret` (
 `id` int(11) NOT NULL,
 `url` varchar(6) NOT NULL,
 `expiry` datetime NOT NULL,
 `password` varchar(256) NOT NULL,
 `secret` varchar(256) NOT NULL,
 `active` tinyint(1) NOT NULL,
 PRIMARY KEY (`id`)
);