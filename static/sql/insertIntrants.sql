use sitDb;

insert into tblAccounts (email, surname, firstName, maudindo, addrLine, addrCity, postCode, mobilePhone, abtrusus, dateAdded, dateModified)
values
("mb@mb.com", "Brown", "Michael", 255, "Flat 23", "London", "W3 0RG", "+44 (0) 7777 878787", "pbkdf2:sha256:150000$vabZ3a7F$619e1453737c19428febcc4650b780522ff3aa15f701a742ae468d1cd135e7f5", NOW(), NOW()),
("kb@kb.com", "Brown", "Kelly", 1, "Flat 23", "London", "W3 0RG", "+44 (0) 8888 878787", "pbkdf2:sha256:150000$vabZ3a7F$619e1453737c19428febcc4650b780522ff3aa15f701a742ae468d1cd135e7f5", NOW(), NOW());
