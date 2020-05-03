# Source: http://sportsdb.org/sd/samples
# CocoaMySQL dump
# Version 0.7b5
# http://cocoamysql.sourceforge.net
#
# Host: localhost (MySQL 5.0.45)
# Database: sportsdb_qa
# Generation Time: 2009-03-18 14:20:27 -0700
# ************************************************************

# Dump of table addresses
# ------------------------------------------------------------



CREATE Table `infects` (
    `date` date NOT NUll,
    `cases` int(100) NOT Null,
    `county` varchar(100) default NULL,
    `continent` varchar(100) default NULL,
PRIMARY KEY  (`date`) ) ENGINE=MyISAM DEFAULT CHARSET=latin1;

INSERT INTO `infects` (`date`,`cases`,`county`,`continent`) VALUES ('02.05.2020','164','Afghanistan','Asia');

