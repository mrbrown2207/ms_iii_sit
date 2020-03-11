use sitDb;

insert into tblCat (catId, catName, catDesc, dateAdded, dateModified)
values
(10, "Repair", "Repair or service request", NOW(), NOW()),
(11, "Complaint", "Complaint about service", NOW(), NOW()),
(12, "Suggestion", "Suggestion for improved service", NOW(), NOW()),
(13, "Question", "Question regarding service", NOW(), NOW()),
(14, "Comment", "Comment on service", NOW(), NOW());
