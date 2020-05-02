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



CREATE Table 'infects' ()
    'date' date(100) NOT NUll,
    'cases' int(100) NOT Null,
    `county` varchar(100) default NULL,
    `continent` varchar(100) default NULL,
PRIMARY KEY  (`date`) ) ENGINE=MyISAM DEFAULT CHARSET=latin1;

INSERT INTO `infects` (`date`,`cases`,`county`,`continent`) VALUES ('02.05.2020','164','Afghanistan','Asia');


CREATE TABLE `addresses` (
  `id` int(11) NOT NULL auto_increment,
  `location_id` int(11) NOT NULL,
  `language` varchar(100) default NULL,
  `suite` varchar(100) default NULL,
  `floor` varchar(100) default NULL,
  `building` varchar(100) default NULL,
  `street_number` varchar(100) default NULL,
  `street_prefix` varchar(100) default NULL,
  `street` varchar(100) default NULL,
  `street_suffix` varchar(100) default NULL,
  `neighborhood` varchar(100) default NULL,
  `district` varchar(100) default NULL,
  `locality` varchar(100) default NULL,
  `county` varchar(100) default NULL,
  `region` varchar(100) default NULL,
  `postal_code` varchar(100) default NULL,
  `country` varchar(100) default NULL,

  PRIMARY KEY  (`id`),
  KEY `IDX_addresses_1` (`locality`),
  KEY `IDX_addresses_2` (`region`),
  KEY `IDX_addresses_3` (`postal_code`),
  KEY `IDX_FK_add_loc_id__loc_id` (`location_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;



# Dump of table affiliation_phases
# ------------------------------------------------------------

CREATE TABLE `affiliation_phases` (
  `id` int(11) NOT NULL auto_increment,
  `affiliation_id` int(11) NOT NULL,
  `ancestor_affiliation_id` int(11) default NULL,
  `start_season_id` int(11) default NULL,
  `start_date_time` datetime default NULL,
  `end_season_id` int(11) default NULL,
  `end_date_time` datetime default NULL,
  PRIMARY KEY  (`id`),
  KEY `FK_seasons_affiliation_phases1` (`end_season_id`),
  KEY `FK_seasons_affiliation_phases` (`start_season_id`),
  KEY `FK_affiliations_affiliation_phases1` (`ancestor_affiliation_id`),
  KEY `FK_affiliations_affiliation_phases` (`affiliation_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;





# Dump of table affiliations
# ------------------------------------------------------------

CREATE TABLE `affiliations` (
  `id` int(11) NOT NULL auto_increment,
  `affiliation_key` varchar(100) NOT NULL,
  `affiliation_type` varchar(100) default NULL,
  `publisher_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `IDX_affiliations_1` (`affiliation_key`),
  KEY `IDX_affiliations_2` (`affiliation_type`),
  KEY `IDX_FK_aff_pub_id__pub_id` (`publisher_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

INSERT INTO `affiliations` (`id`,`affiliation_key`,`affiliation_type`,`publisher_id`) VALUES ('1','c.national','conference','1');
INSERT INTO `affiliations` (`id`,`affiliation_key`,`affiliation_type`,`publisher_id`) VALUES ('2','l.mlb.com','league','1');
INSERT INTO `affiliations` (`id`,`affiliation_key`,`affiliation_type`,`publisher_id`) VALUES ('3','15007000','sport','1');
INSERT INTO `affiliations` (`id`,`affiliation_key`,`affiliation_type`,`publisher_id`) VALUES ('4','c.american','conference','1');


# Dump of table affiliations_documents
# ------------------------------------------------------------

CREATE TABLE `affiliations_documents` (
  `affiliation_id` int(11) NOT NULL,
  `document_id` int(11) NOT NULL,
  KEY `FK_aff_doc_aff_id__aff_id` (`affiliation_id`),
  KEY `FK_aff_doc_doc_id__doc_id` (`document_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

INSERT INTO `affiliations_documents` (`affiliation_id`,`document_id`) VALUES ('1','1');
INSERT INTO `affiliations_documents` (`affiliation_id`,`document_id`) VALUES ('2','1');
INSERT INTO `affiliations_documents` (`affiliation_id`,`document_id`) VALUES ('3','1');
