
CREATE Table `infects` (
    `date` date NOT NUll,
    `cases` int(100) NOT Null,
    `death` integer(100) default NULL,
    `country` varchar(100) default NULL,
PRIMARY KEY  (`date`) ) ENGINE=MyISAM DEFAULT CHARSET=latin1;

INSERT INTO `infects` (`date`,`cases`,`death`,`country`) VALUES ('02.05.2020','164','17000','Germany');




CREATE Table `dax` (
    `daxvalue` decimal(6,2) default NULL,
    `date` date NOT NUll,
    `open` float(100) default NULL,
    `close` float(100) default NULL,
    `diff` float(100) default NULL,
PRIMARY KEY  (`date`) ) ENGINE=MyISAM DEFAULT CHARSET=latin1;

INSERT INTO `infects` ('daxvalue',`date`,`open`,`close`,`diff`) VALUE
