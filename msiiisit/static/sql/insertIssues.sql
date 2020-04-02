use sitDb;

insert into tblIssue (issueSubj, issueDesc, catId, urgent, acctId, dateAdded, dateModified)
values
("Toilet is leaking", "En-Suite toilet is leaking all over the floor. And it stinks!", 10, 1, 1, NOW(), NOW()),
("No hot water", "We have no hot water anywhere", 10, 1, 2, NOW(), NOW()),
("Concierge", "It would be good if the building had a concierge. They could accept packages on our behalf.", 12, 0, 2, NOW(), NOW()),
("Noisy neighbours", "The neighbours above us are extremely loud. They were singing on their balcony until 3:00 am yesterday!", 11, 0, 1, NOW(), NOW()),
("Thank you", "Appreciate that you dealt with the fly-tipping issue", 14, 0, 2, NOW(), NOW())
