
CREATE Table `infects` (
    `date` date NOT NUll,
    `cases` int(100) NOT Null,
    `death` integer(100) default NULL,
    `country` varchar(100) default NULL,
PRIMARY KEY  (`date`) ) ENGINE=MyISAM DEFAULT CHARSET=latin1;

INSERT INTO `infects` (`date`,`cases`,`death`,`country`) VALUES ('02.05.2020','164','17000','Germany');




CREATE Table `dax` (
    `date` date NOT NUll,
    `open` decimal(6,4) default NULL,
    `close` decimal(6,4) default NULL,
    `diff` decimal(6,4) default NULL,
PRIMARY KEY  (`date`) ) ENGINE=MyISAM DEFAULT CHARSET=latin1;

