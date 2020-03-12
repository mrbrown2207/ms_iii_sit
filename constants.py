"""Some constants"""
SQL_DT_FMT = '%Y-%m-%d %H:%M:%S'
DDMMYYYY_FMT = '%d/%m/%Y %H:%M:%S'

SQL_DICT =  {
            "sel_recs": "select * from %s",
            "del_cat_rec": "delete from tblCat where catId=%s",
            "del_iss_rec": "delete from tblIssue where issueId=%s",
            "sel_cat_rec": "select * from tblCat where catId=%s",
            "sel_iss_rec": ("select i.issueSubj as issueSubj, i.issueDesc as issueDesc, i.catId as catId, i.urgent as urgent, " +
                            "case " + 
                                "when i.issueStatus = 0 then 'New' " +
                                "when i.issueStatus = 1 then 'Viewed' " +
                                "when i.issueStatus = 2 then 'Resolved' " +
                                "else 'Unknown' " +
                            "end as issueStatus, i.dateViewed as dateViewed, " +
                            "i.markedResolvedBy as markedResolvedBy, i.dateResolved as dateResolved, i.resolutionDesc as resolutionDesc, " +
                            "i.dateAdded as dateAdded, " +
                            "concat(t.firstName, ' ', t.surname) as 'addedBy', " + 
                            "concat(t2.firstName, ' ', t2.surname) as 'resolvedBy' from tblIssue i " +
                                "left join tblCat c on c.catId = i.catId " +
                                "left join tblAccounts t on t.acctId = i.acctId " +
                                "left join tblAccounts t2 on t2.acctId = i.markedResolvedBy where i.issueId=%s"),
            "sel_all_isss": ("select i.issueId as issueId, i.issueSubj as issueSubj, i.issueDesc as issueDesc, i.catId as catId, i.urgent as urgent, " +
                            "case " + 
                                "when i.issueStatus = 0 then 'New' " +
                                "when i.issueStatus = 1 then 'Viewed' " +
                                "when i.issueStatus = 2 then 'Resolved' " +
                                "else 'Unknown' " +
                            "end as issueStatus, i.dateViewed as dateViewed, " +
                            "i.markedResolvedBy as markedResolvedBy, i.dateResolved as dateResolved, i.resolutionDesc as resolutionDesc, " +
                            "i.dateAdded as dateAdded, c.catName as catName, " +
                            "concat(t.firstName, ' ', t.surname) as 'addedByName', " + 
                            "concat(t2.firstName, ' ', t2.surname) as 'resolvedByName' from tblIssue i " +
                                "left join tblCat c on c.catId = i.catId " +
                                "left join tblAccounts t on t.acctId = i.acctId " +
                                "left join tblAccounts t2 on t2.acctId = i.markedResolvedBy"),
            "sel_all_cats": "select * from tblCat",
            "sel_int_rec": "select * from tblAccounts where acctId=%s",
            "upd_iss": ("update tblIssue set " +
                            "issueSubj=%s, " +
                            "issueDesc=%s, " +
                            "catId=%s, " +
                            "urgent=%s, " +
                            "issueStatus=%s, " +
                            "markedResolvedBy=%s, " +
                            "dateResolved=%s, " +
                            "resolutionDesc=%s, " +
                            "dateModified=NOW() " +
                        "where issueId=%s"),
            "add_iss": ("insert into tblIssue (issueSubj, issueDesc, catId, urgent, acctId, dateAdded, dateModified) " +
                            "values " +
                        "(%s, %s, %s, %s, %s, NOW(), NOW())"),
            "upd_cat": ("update tblCat set " +
                            "catName=%s, " +
                            "catDesc=%s, " +
                            "dateModified=NOW() " +
                        "where catId=%s"),
            "add_cat": ("insert into tblCat (catName, catDesc, dateAdded, dateModified) " +
                            "values " +
                        "(%s, %s, NOW(), NOW())")
            }
DEL = 1
SEL = 2
SEL_ALL = 3

CATS = {
    'repair':1,
    'complaint':2,
    'suggestion':3,
    'question':4,
    'comment':5
}


"""""<<<---->>>"""""
