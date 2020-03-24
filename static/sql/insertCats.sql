use sitDb;

insert into tblCat (catId, catName, catDesc, catActive, dateAdded, dateModified)
values
(10, "Repair", "Repair or service request", 1, NOW(), NOW()),
(11, "Complaint", "Complaint about service", 1, NOW(), NOW()),
(12, "Suggestion", "Suggestion for improved service", 1, NOW(), NOW()),
(13, "Question", "Question regarding service", 1, NOW(), NOW()),
(14, "Comment", "Comment on service", 1, NOW(), NOW());
