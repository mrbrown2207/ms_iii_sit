/*
	File name: 		issueTrackDbTableCreate.sql
	Purpose:		Create tables required for service issue tracking application database.
	Date Created:	02 May 2019
	Author:			Michael R. Brown
*/

/* Service Issue Tracking Database */
use sitDb;

/*
	Table for capturing users of the application: clients, management and administrators.
*/
select 'Creating tblAccounts table...' as 'Action';
create table if not exists tblAccounts
						(
						acctId 				    int(5) zerofill not null auto_increment primary key,
						email					varchar(128) not null unique,
						surname				    varchar(40) not null,
						firstName				varchar(40) not null,
						maudindo				tinyint(3) unsigned not null default '1',
						addrLine1	 			varchar(40) not null,
						addrLine2 				varchar(40),
                        addrLine3       		varchar(40),
						addrCity 				varchar(40) not null,
						addrCounty 				varchar(40),
                        postCode     			varchar(12) not null,
						addrCountryISO			char(2) not null default 'GB',
						phone					varchar(20), /*Either phone or mobile phone will have to exist*/
						mobilePhone				varchar(20), 
						abtrusus				varchar(40) not null,
						acctDisabled			tinyint unsigned not null default '0',
						lastTimeIn				datetime,
						dateAdded				datetime not null,
						dateModified			datetime not null
						) engine=InnoDB default charset=utf8;


/*
	Categories table. Every issue that is created is assigned a category. Upon initiation of development,
	the categories were as such: Something needs fixing, Complaint, Suggestion, Question, Comment.
*/
select 'Creating tblCat table...' as 'Action';
create table if not exists tblCat
						(
						catId 					tinyint(3) zerofill not null auto_increment primary key,
						catName					varchar(30),
						catDesc					varchar(60),
						dateAdded				datetime not null,
						dateModified			datetime not null
						) engine=InnoDB default charset=utf8;


/*
	Issues table. Table for capturing issues. At time of project start, the types of issues that
	could be logged by customers/clients were: Something needs fixing, complaint, suggestion, question or comment.
*/
select 'Creating tblIssue table...' as 'Action';
create table if not exists tblIssue
						(
						issueId 				int(6) zerofill not null auto_increment primary key,
						issueSubj				varchar(30),
						issueDesc				varchar(512),
						catId					tinyint(3) zerofill not null,
						urgent					tinyint(1) unsigned not null default '0',
						acctId				    int(5) zerofill not null, /* Person who submitted issue */
						issueStatus				tinyint(1) unsigned not null default '0' comment '0=entered, 1=viewed, 2=resolved',
						dateViewed			    datetime,
						dateResolved			datetime,
						markedResolvedBy		int(5) zerofill,
						resolutionDesc			varchar(512),
						dateAdded				datetime not null,
						dateModified			datetime not null,
						index (acctId),
						index (dateAdded),
						index (dateResolved),
						foreign key fk_catId(catId)
							references tblCat(catId)
							on update no action
							on delete cascade
						) engine=InnoDB default charset=utf8;


/*
	Comments table. Table for capturing comments to issues.
*/
select 'Creating tblComments table...' as 'Action';
create table if not exists tblComments
						(
						commId 					int(6) zerofill not null auto_increment primary key,
						comment					varchar(512),
						issueId					int(6) zerofill not null,
						acctId				    int(5) zerofill not null, /* Person who posted comment */
						dateAdded				datetime not null,
						dateModified			datetime not null,
						foreign key fk_issueId(issueId)
							references tblIssue(issueId)
							on update no action
							on delete cascade
						) engine=InnoDB default charset=utf8;

