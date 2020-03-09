use sitDb;

insert into tblCat (catName, catDesc, dateAdded, dateModified)
values
("Repair", "Repair or service request", NOW(), NOW()),
("Complaint", "Complaint about service", NOW(), NOW()),
("Suggestion", "Suggestion for improved service", NOW(), NOW()),
("Question", "Question regarding service", NOW(), NOW()),
("Comment", "Comment on service", NOW(), NOW());
