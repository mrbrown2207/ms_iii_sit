# MBPM Service Issue Tracker

## Table of Contents

- [Table of contents](#Table-of-Contents)
- [About](#About)
- [Functionality/UX](#UX-Functionality-and-Navigation)
  - [UX](#UX)
  - [Functionality/Navigation](#Functionality-and-Navigation)
- [Technologies](#Technologies)
  - [Languages/Libraries](#Languages-and-Libraries)
  - [Other Resources](#Other-Resources)
- [Testing](#Testing)
  - [Tools and Methods Used for Testing](#Tools-and-Methods-Used-for-Testing)
- [Potential Enhancements](#Potential-Enhancements)
- [Deployment](#Deployment)
  - [Local](#Local)
  - [Heroku](#Heroku)
- [Credits](#Credits)
  - [Content](#Content)
  - [Acknowledgements](#Acknowledgements)

## About

Milestone Project Three / Data Centric Development with Flask / Code Institute

This is a web application for a fictitious company called MB Property Management (MBPM). It runs on their web site and allows the tenants of
the properties they manage to be able log issues related to their property. They can also view issues related to other properties. 
The application is called MBPM Service Issue Tracker (SIT). It allows customers to:
- Log issues related to their property and track the progress of the resolution of the issue.
- Tenants may also edit their own issues.

This application is also used by administrators at MBPM:
- Viewing, acknowledging, editing and resolving issues
- Create new categories for tenants to choose from. The default issues that are loaded when the application is deployed are: Repair, Complaint, Suggestion, Question, and Comment.

## UX Functionality and Navigation

#### UX
- The web page is using two Google fonts:
1. **Archivo**
2. **Open Sans**

- The primary colours are:
1. ##203B4E - all body text,  h tags, panel frames, default icon state
2. #009AD1 - all add buttons, hover icon state, on icon state
4. #FFFFFF - button text

- Secondary colours:
1. #007BFF - (btn-primary) main page buttons
2. Red - denoting urgent issues

#### Functionality and Navigation

The site consists of the following pages that get be navigated to via the navbar:
1. Login
2. Registration (navigated to via the Login page)
3. Profile
4. How it Works - this goes into detailed explanation as to how the application/site works. To that end, I am not going to put too much in here.
5. Main/Landing - Welcome message and very brief overview of what the site does. The text and buttons change dynamically based on login status and authentication level. See the "How it Works" page on the site for a detailed explanation.
6. Issues Dashboard Page - You must have an account and be logged in to get to this page. Once here, in brief, you can:
- Log/Add an Issue
- Edit your own issues (Administrators can edit any issue)
- View summary and detail of any issue
- Filter the issues you see via a filter modal. Again, see "How it Works" page please.
- Search for issues where the subject or the description fields contain the critera you enter.
- Administrators can change the status of issues from this page, in the issue detail section of each issue.
7. Categories Dashboard Page - You must be an MBPM Administrator to be this page. An administrator is someone in the tblAccounts table with the column 
"maudindo" containing a value of 255. All normal users have a value of 1. Once here you can:
- Edit a category. As an administrator you can change the name, description, and state: active or non-active. Categories cannot be deleted.
- Add additional categories.

Other pages:
1. Add and Edit Categories
2. Add and Edit Issues

A note about a field I have in the user registration form. I have rolled my own anti-bot automated user registration by asking
a maths question such as "1 and 2 and 3 is...". The user has to answer this question correctly. If they fail 5 times, it goes back to 
the main page. There are 15 of these questions and each time the form is rendered, one of them randomly selected. I have also written
a unit test for it so in the case where a developer fat fingers the dictionary list or wants to add more, the unit test will ensure
that the answer is correct.

Please see the "How it Works" page for much greater detail.

You will notice that I have set this application up so you can load different configurations. I would like to make it a bit more dynamic. But hey, what I did isn't bad I don't think. The idea was to let me have a test config that gets loaded in my test/dev environment and then a production env configuration class. See ```config.py``` for the definition of the classes and ```__init__.py``` for the loading of the class upon the creation of the app.


## Technologies

#### Languages and Libraries

- [HTML5](https://www.w3.org/TR/html5/ "HTML5 Official Site")
- [CSS3](https://www.w3.org/Style/CSS/ "Cascading Style Sheets Official Site")
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/ "JavaScript Official Site")
- [Python 3.6](https://www.python.org "Python Official Site")
- [Flask 1.0.2](https://www.palletsprojects.com/p/flask/ "Flask Official Site")
- [Bootstrap - v4.4.1](https://getbootstrap.com/docs/4.1/getting-started/introduction/ "Bootstrap Official Site")
- [jQuery v3.4.1](http://jquery.com/ "jQuery Official Site")
- [Font Awesome - v4](https://fontawesome.com/ "Font Awesome Official Site")
- [MySQL 5.7.23](https://www.mysql.com "MySQL Official Site")


#### Other Resources

As always, for technical reference and help, I used the following sites.
- https://getbootstrap.com/
- https://www.w3schools.com/
- https://stackoverflow.com/
- https://https://docs.djangoproject.com/en/3.0/
- https://slack.com/
- A few videos on YouTube. One that was particularly amazing was one on the usage of Blueprints as well as setting up different configuraions in Flask. I cannot imagine writing a flask application without them to be honest. The url is: https://www.youtube.com/watch?v=Wfx4YBzg16s

## Testing

#### Tools and Methods Used for Testing

- [HTML Validation](https://validator.w3.org/ "W3C Markup Validation Service")
- [CSS Validation](http://jigsaw.w3.org/css-validator/ "CSS Validation Service") - A note about this. I receive a lot of warnings for my use of "var(--blah)"
- Chrome Developer Tools
- Flask/Python automated unit testing - I fall on my sword here. I could do more here, it is very minimal.
- Spreadsheet submitted with project was used as a checklist of all that was tested.


## Potential Enhancements

There is immense potential improvement of this site. Some that come to mind are:

- Sticky navbar.
- A dynamic widget that appears as you scroll down the page that when clicked, will take you to the top
- Filtering by urgent issues
- Filtering on "My Issues"
- Allowing people to post comments and maintain a thread for issues; mainly for the property management team to post comments and allow tenants to respond. I actually have the table created for that, but there just wasn't time to get to it.
- Attaching documents to an issue. For example, if something is damaged in your property, posting a photo for the property manager to view.
- A stats page showing number of issues closed etc.
- More administration -- namely user administration.
- Possibly a bit more imagery.
- So many more really. It has great potential. I am actually going to start on all of this as soon as I submit. I will fork the project of course.


## Deployment

### Local
1. Navigate to https://github.com/mrbrown2207/ms_iv_ua and click the green "Clone or download" button and choose "Open in Desktop" or "Download ZIP". If doing the latter, obviously, unpack.
2. From the terminal, change to the directory in which you will be work and want the cloned directory to be made.
3. Type in ```git clone https://github.com/mrbrown2207/ms_iii_sit```
4. You will need to install MySQL 5.7 locally. This document does not go into how to do that. You will need to create a user that has privileges to create databases and tables. That username and password will be used later if you use the MySQL CLI.
5. Once you have MySQL up and running, navigate to the ```msiiisit/static/sql/``` folder of the project. You can copy the script text to the clibboard that is in ```sitDbBootstrap_local.sql``` and paste into your favourite MySQL administration console to execute it. I use a couple of different consoles: https://www.phpmyadmin.net and https://www.mysql.com/products/workbench/. This will create a database called ```sitDb``` and four tables: ```tblAccounts, tblIssue, tblCat, and tblComments```. It will seed ```tblAccounts``` with a couple of users -- one being an admin. See the comments in the ```.sql``` file for the passwords. It will also generate the default issue categories as well as some test issues. The ```tblComments``` table is not used now and is there for future development.
6. If you don't want to bother with an administration console and rather do it from the MySQL CLI, then navigate to ```msiiisit/static/sql/``` and copy and paste the following command at the system prompt:
```mysql --host=localhost --user=[your user] --password=[your user pwd] < sitDbBootstrap_local.sql```.
7. You are done with MySQL and table creation. You now need to set up following environment variables:
    - ```DB``` - which should be set to ```sitDb``` assuming you don't change the sql script.
    - ```DB_HOST``` - and should either be ```localhost``` or ```127.0.0.1```
    - ```DB_USER``` - this should can be the same user as you used above.
    - ```DB_ABTRUSUS` - this is the password for the MySQL user. By the way, Abtrusus is the word for secret in Latin.
    - ```SIT_SECRET_KEY``` - this can be anything really -- especially for your local machine. However, if you want to be a bit more secret, then you could do the following from within python:
    ```>>> import secrets```
    ```>>> secrets.token_hex(16)```
    That will generate a token that you can use for your secret. Copy and paste where you are setting ```SIT_SECRET_KEY```
    - ```FLASK_APP_HOST``` - this should be set to the ip address of your local machine, so most likely ```127.0.0.1```
    - ```FLASK_APP_PORT``` - set this to ```5000```
8. You are just about there. Now navigate to your project directory and type in ```pip3 install -r requirements.txt```

You should be good to go.


### Heroku
- My final deployment of this project is on Heroku and is here: (https://ms-iii-ua.herokuapp.com/). If you want to deploy to Heroku, you will need to do the following:
1. Obviously you need a Heroku account. Once you have that, create an app with a unique name as you cannot use the same one that I did.
2. Once you do that, you will have to install heroku locally using this command: ```pip3 install heroku```
3. You will have to log into heroku from the command line: ```heroku login```. This will launch the browser and prompt you to log in via the browser. Once that is done, the browser window shuts and you are now logged in to heroku.
4. Once you are logged in, do the following:
```$ cd your-project``` (where you set up after cloning)
```$ git init```
```$ heroku git:remote -a your-app-name```
5. Once you have the basic app set up with heroku, you will need to do the following. As this is using MySQL and my Heroku doesn't run MySQL, you need a Heroku addon called ClearDB. Go to the Resources page of your heroku app, go to the Add-ons text field and start typing ClearDB. It will find ClearDB MySQL automatically. Select it and a modal dialog comes up asking you to provision. NOTE: you will have to enter a credit card here. However, you get 1000 free hours of the dyno so there is no risk of charges unless this is a production implementation.
6. Once you do this, ClearDB automatically provisions a database for you on a server some place. It also creates a MySQL user with a password. To get this information, go to the Settings page of your Heroku app and click on "Reveal Config Vars". You will see a config var called ```CLEARDB_DATABASE_URL```. It will look something like this: ```mysql://b939b5ef80249e:@eu-cdbr-west-02.cleardb.net/heroku_fe37d3484441663?reconnect=true```. 
    - The MySQL user is: ```b939b5ef80249e```
    - The MySQL user password is: ```fb3f61f8```
    - The host is: ```eu-cdbr-west-02.cleardb.net```
    - The MySQL db is: ```heroku_fe37d3484441663```
7. You now have to create the environment variables within Heroku that I listed above in the "Local Deployment" section in your app. This is done by clicking in the KEY field, adding a KEY, and then the VALUE field pasting or typing in the value, then clicking the Add button. So, your Heroku environment variables will look like this (YOUR VALUES WILL BE DIFFERENT -- THIS IS AN EXAMPLE)
    - ```DB``` - which should be set to ```heroku_fe37d3484441663```
    - ```DB_HOST``` - ```eu-cdbr-west-02.cleardb.net```
    - ```DB_USER``` - this would be ```b939b5ef80249e```.
    - ```DB_ABTRUSUS``` - set this to ```fb3f61f8```
    - ```SIT_SECRET_KEY``` - highly recommended you make this more secure by doing the following from within python:
    ```>>> import secrets```
    ```>>> secrets.token_hex(16)```
    That will generate a token that you can use for your secret. Copy and paste where you are setting ```SIT_SECRET_KEY```
    - ```FLASK_APP_HOST``` - this is different than a local implementation. Set this to ```0.0.0.0```
    - ```FLASK_APP_PORT``` - set this to ```5000```
8. Push your repo up and you should be good to go!


## Credits

#### Content

- All written content is bespoke and created by the code author (Michael Brown).
- Images that I purchased and have rights to use in any project.

#### Acknowledgements

- The Code Insititue! The tutors are always amazing, but were particularly helpful with this project. What 
made them really effective was there just would be some "chatting" between us and they would lead me to find 
the answer on my own. They acted like sounding boards.

- Another note: as this is my last project in this course, I want to say how much I have enjoyed the course! I am actually going to miss the tutors as they were absolutely amazing. I called him out before, but I will do it again: Tim Nelson in particular was brilliant. Thank you Tim!

I am also going to miss this journey through all these technologies. It has been an amazing experience. I feel like I have grown leaps and bounds as a developer...and I thought I was good before! :wink:

You stay classy Code Insititute! :thumbsup:

