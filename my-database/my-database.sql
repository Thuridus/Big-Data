

CREATE Table `infects` (
    `date` date NOT NUll,
    `cases` int default NULL,
    `death` int default NULL,
    `country` varchar(64) default NULL,
    `continent` varchar(64) default NULL,
    `cases_prev` decimal(6,4) default NULL,
    `dead_prev` decimal(6,4) default NULL,
    `cases_rel_diff` decimal(6,4) default NULL,
    `deaths_rel_diff` decimal(6,4) default NULL,
PRIMARY KEY  (`date`) ) ENGINE=MyISAM DEFAULT CHARSET=latin1;

INSERT INTO `infects` (`date`,`cases`,`death`,`country`,`continent`, `cases_prev`, `dead_prev`, `cases_rel_diff`, `deaths_rel_diff`) VALUES ('02.05.2020','164','17000','Germany', 'Europe', NULL, NULL, NULL, NULL);

CREATE Table `dax` (
    `date` date NOT NUll,
    `open` decimal(6,4) default NULL,
    `close` decimal(6,4) default NULL,
    `diff` decimal(6,4) default NULL,
PRIMARY KEY  (`date`) ) ENGINE=MyISAM DEFAULT CHARSET=latin1;