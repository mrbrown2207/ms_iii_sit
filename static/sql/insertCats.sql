use sitDb;

insert into tblCat (catName, catDesc, catActive, dateAdded, dateModified)
values
("Repair", "Repair or service request", 1, NOW(), NOW()),
("Complaint", "Complaint about service", 1, NOW(), NOW()),
("Suggestion", "Suggestion for improved service", 1, NOW(), NOW()),
("Question", "Question regarding service", 1, NOW(), NOW()),
("Comment", "Comment on service", 1, NOW(), NOW());
