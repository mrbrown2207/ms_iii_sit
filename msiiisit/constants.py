SQL_DT_FMT = '%Y-%m-%d %H:%M:%S'
DDMMYYYY_FMT = '%d/%m/%Y %H:%M:%S'

ISSUE_STATUS =  {
                    'notviewed':
                        {
                            "id":0,
                            "display":"Not Viewed",
                            "filter_status":"1",
                        },
                    'viewed':
                        {
                            "id":1,
                            "display":"Viewed",
                            "filter_status":"1",
                        },
                    'resolved':
                        {
                            "id":2,
                            "display":"Resolved",
                            "filter_status":"1",
                        },
}

# An alternative to captcha. Dictionary of questions. One will be chosen at random
# when a user registers or changes their password.
NO_BOTS = {
    '1 and 1 and 1':'3',
    '1 and 2 and 1':'4',
    '1 and 1 and 2':'4',
    '2 and 2 and 2':'6',
    '2 and 2 and 1':'5',
    '2 and 1 and 1':'4',
    '3 and 3 and 3':'9',
    '3 and 2 and 1':'6',
    '3 and 3 and 2':'8',
    '1 and 1 and 3':'5',
    '2 and 3 and 2':'7',
    '5 and 2 and 1':'8',
    '1 and 0 and 0':'1',
    '0 and 0 and 0':'0',
    '5 and 4 and 0':'9',
    '4 and 1 and 1':'6',
}

USER_LEVEL = {
                'plebe': 1,
                'superuser': 255, 
            }


# There was a few ways to do this. For example, I could have put in a table and selected it in
# country name order. I could have hard coded in the template in country name order. I could have
# created a list or a tuple which python provides ways of permanently sorting. I also could have
# created the dictionary already in country name order. However, I am purposely creating it NOT 
# in country name order to demonstrate my ability to dynamically sort a dictionary that results
# in a sorted representation thereof, which will be in a list of tuples.
COUNTRIES = {
                'GB':"United Kingdom",
                'IE':"Ireland",
                'US':"United States",
                'ES':"Spain",
                'DE':"Germany",
                'IT':"Italy",
                'FR':"France",
            }

SQL_DICT =  {
            "sel_recs": "select * from %s",
            "del_cat_rec": "delete from tblCat where catId=%s",
            "del_iss_rec": "delete from tblIssue where issueId=%s",
            "sel_cat_rec": "select * from tblCat where catId=%s",
            "sel_iss_rec": ("select i.issueId as issueId, i.issueSubj as issueSubj, i.issueDesc as issueDesc, i.catId as catId, " + 
                            "(case " +
                                "when i.urgent = 0 then 'No' " +
                                "when i.urgent = 1 then 'Yes' " + 
                            "end) as urgent, " +
                            "(case " + 
                                "when i.issueStatus = 0 then 'Not Viewed' " +
                                "when i.issueStatus = 1 then 'Viewed' " +
                                "when i.issueStatus = 2 then 'Resolved' " +
                                "else 'Unknown' " +
                            "end) as issueStatus, " + 
                            "i.issueStatus as issueStatusVal, i.dateViewed as dateViewed, i.acctId as acctId, " +
                            "i.markedResolvedBy as markedResolvedBy, i.dateResolved as dateResolved, i.resolutionDesc as resolutionDesc, " +
                            "i.dateAdded as dateAdded, " +
                            "concat(t.firstName, ' ', t.surname) as 'addedBy', " + 
                            "concat(t2.firstName, ' ', t2.surname) as 'resolvedBy' from tblIssue i " +
                                "left join tblCat c on c.catId = i.catId " +
                                "left join tblAccounts t on t.acctId = i.acctId " +
                                "left join tblAccounts t2 on t2.acctId = i.markedResolvedBy where i.issueId=%s"),
            "sel_all_isss": ("select i.issueId as issueId, i.issueSubj as issueSubj, i.issueDesc as issueDesc, i.catId as catId, " +
                            "(case " +
                                "when i.urgent = 0 then 'No' " +
                                "when i.urgent = 1 then 'Yes' " + 
                            "end) as urgent, " +
                            "(case " + 
                                "when i.issueStatus = 0 then 'Not Viewed' " +
                                "when i.issueStatus = 1 then 'Viewed' " +
                                "when i.issueStatus = 2 then 'Resolved' " +
                                "else 'Unknown' " +
                            "end) as issueStatus, i.issueStatus as issueStatusVal, i.dateViewed as dateViewed, " +
                            "i.markedResolvedBy as markedResolvedBy, i.dateResolved as dateResolved, i.resolutionDesc as resolutionDesc, " +
                            "i.dateAdded as dateAdded, c.catName as catName, " +
                            "concat(t.firstName, ' ', t.surname) as 'addedByName', " + 
                            "concat(t2.firstName, ' ', t2.surname) as 'resolvedByName' from tblIssue i " +
                                "left join tblCat c on c.catId = i.catId " +
                                "left join tblAccounts t on t.acctId = i.acctId " +
                                "left join tblAccounts t2 on t2.acctId = i.markedResolvedBy " + 
                                "order by i.dateAdded desc"),
            "sel_filtered_isss": ("select i.issueId as issueId, i.issueSubj as issueSubj, i.issueDesc as issueDesc, i.catId as catId, " +
                            "(case " +
                                "when i.urgent = 0 then 'No' " +
                                "when i.urgent = 1 then 'Yes' " + 
                            "end) as urgent, " +
                            "(case " + 
                                "when i.issueStatus = 0 then 'Not Viewed' " +
                                "when i.issueStatus = 1 then 'Viewed' " +
                                "when i.issueStatus = 2 then 'Resolved' " +
                                "else 'Unknown' " +
                            "end) as issueStatus, i.issueStatus as issueStatusVal, i.dateViewed as dateViewed, i.acctId as acctId, " +
                            "i.markedResolvedBy as markedResolvedBy, i.dateResolved as dateResolved, i.resolutionDesc as resolutionDesc, " +
                            "i.dateAdded as dateAdded, c.catName as catName, " +
                            "concat(t.firstName, ' ', t.surname) as 'addedByName', " + 
                            "concat(t2.firstName, ' ', t2.surname) as 'resolvedByName' from tblIssue i " +
                                "left join tblCat c on c.catId = i.catId " +
                                "left join tblAccounts t on t.acctId = i.acctId " +
                                "left join tblAccounts t2 on t2.acctId = i.markedResolvedBy " + 
                                "where %s " + 
                                "order by i.dateAdded desc"),
            "sel_all_cats": "select *,  "
                            "(case " +
                                "when catActive = 1 then 'Active' " +
                                "when catActive = 0 then 'Inactive' " +
                                "else 'Unknown' " +
                            "end) as catStatus from tblCat",
            "sel_all_cats_1": ("select concat('cat-', catId) as cat from tblCat order by catName"),
            "sel_active_cats": "select * from tblCat where catActive = 1",
            "sel_active_cats_1": ("select concat('cat-', catId) as cat from tblCat where catActive = 1 order by catName"),
            "sel_acct_rec": ("select firstName, surname, acctId, email, isActive, maudindo, abtrusus from tblAccounts where email = %s"),
            "sel_acct_rec_by_id": ("select firstName, surname, acctId, email, isActive, maudindo from tblAccounts where acctId = %s"),
            "upd_iss": ("update tblIssue set " +
                            "issueSubj=%s, " +
                            "issueDesc=%s, " +
                            "catId=%s, " +
                            "urgent=%s, " +
                            "dateModified=NOW() " +
                        "where issueId=%s"),
            "upd_iss_status": ("update tblIssue set issueStatus=%s where issueId=%s"),
            "upd_iss_reset": ("update tblIssue set issueStatus=0, dateResolved=NULL, resolutionDesc=NULL, markedResolvedBy=NULL where issueId=%s"),
            "upd_resolve_iss": ("update tblIssue set markedResolvedBy=%s, dateResolved=NOW(), resolutionDesc=%s, issueStatus=%s where issueId=%s"),
            "add_iss": ("insert into tblIssue (issueSubj, issueDesc, catId, urgent, acctId, dateAdded, dateModified) " +
                            "values " +
                        "(%s, %s, %s, %s, %s, NOW(), NOW())"),
            "upd_cat": ("update tblCat set " +
                            "catDesc=%s, " +
                            "catActive=%s, " +
                            "dateModified=NOW() " +
                        "where catId=%s"),
            "get_cats": ("select catId, catName, '1' as filter_status from tblCat where catActive = 1 order by catName"),
            "add_cat": ("insert into tblCat (catName, catDesc, catActive, dateAdded, dateModified) " +
                            "values " +
                        "(%s, %s, %s, NOW(), NOW())"),
            "add_account": ("insert into tblAccounts (email, surname, firstName, abtrusus, addrCountryISO, lastTimeIn, dateAdded, dateModified) " +
                            "values " +
                        "(%s, %s, %s, %s, %s, NOW(), NOW(), NOW())"),
            "sel_profile": ("select * from tblAccounts where acctId=%s"),
            "upd_profile": ("update tblAccounts set firstName=%s, surname=%s, addrLine1=%s, addrLine2=%s, addrCity=%s, " + 
                            "addrCounty=%s, addrCountryISO=%s, postcode=%s, mobilePhone=%s, phone=%s, dateModified=NOW() where acctId=%s"),
            "upd_profile_abtrusus": ("update tblAccounts set firstName=%s, surname=%s, addrLine1=%s, addrLine2=%s, addrCity=%s, " + 
                            "addrCounty=%s, addrCountryISO=%s, postcode=%s, mobilePhone=%s, phone=%s, abtrusus=%s, dateModified=NOW() where acctId=%s"),
            }

