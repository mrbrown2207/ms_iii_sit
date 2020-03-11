use sitDb;

insert into tblIssue (issueId, issueSubj, issueDesc, catId, urgent, acctId, dateAdded, dateModified)
values
(10000, "Toilet is leaking", "En-Suite toilet is leaking all over the floor. And it stinks!", 1, 1, 1, NOW(), NOW()),
(10001, "No hot water", "We have no hot water anywhere", 1, 1, 2, NOW(), NOW()),
(10002, "Concierge", "It would be good if the building had a concierge. They could accept packages on our behalf.", 3, 0, 2, NOW(), NOW()),
(10003, "Noisy neighbours", "The neighbours above us are extremely loud. They were singing on their balcony until 3:00 am yesterday!", 2, 0, 1, NOW(), NOW()),
(10004, "Thank you", "Appreciate that you dealt with the fly-tipping issue", 5, 0, 2, NOW(), NOW())
