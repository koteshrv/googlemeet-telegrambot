# telegram-meet-bot

Telegram meet bot uses selenium to attend google meet classes. It can be easily deployed to heroku or local machine. You can schedule all the classes and it will join automatically. It has some features like alert when someone called, auto respond when alert triggers ,joins and leaves the class according to the members count, reply and many more.

![Demo](files/demo.gif)

## Features

- Fetches class link from the google classroom from default position and from the announcement section.
- Sends an alert message when someone calls you.
- Auto responds in the chat section. (can be turned off if not required).
- Joins and leaves the meet according to the members count.
- Scheduled to attend classes everyday.
- Will not join classes on holidays. Second Saturdays and Sundays are automatically calculated.
- Add or remove holidays from telegram.
- Fetches the class schedule from timetable.xlsx.
- Timetable can be updated from telegram.
- Change todays schedule in advance temporarily from telegram.
- Schedule or joins a class immediately from telegram with class link.
- Sends a screenshot of driver instance to telegram.
- Leaves the class when message is triggered from telegram.
- Send log to telegram when required.

## Commands

```
meet - runs joinmeet to join all classes today
joinnow - takes meet link and joins the meet immediately
joinlater - takes meet link and schedules the meet
status - sends screenshot of driver instance
whichclass - prints the present running class
classestoday - prints today's classes
timetable - prints timetable
updatetimetable - updates timetable
tempupdatetimetable - updates timetable temporarily
holidays - prints holidays list
addholiday - adds holiday to the list
removeholiday - removes holiday from the list
sendlog - prints log data
help - displays all bot commands
exitmeet - ends the current meet
restart - restarts the bot 
reply - send a message to google meet chat. Needs confirmation 
send - sends message to google meet chat that was received when reply is used
pagesource - sends pagesource of the driver
load - loads the url sent by the user
files - returns files present in the repository
```

## How to start using this

**Prerequisites**

> You need to have Python3 installed.
> You need Heroku-CLI installed on your system. [Installation Guide Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
> You need to have Google Chrome installed and [Chromedriver](https://chromedriver.storage.googleapis.com/index.html?path=91.0.4472.101/) in path.

- You need to tell Telegram you want to register a Bot. To do this, send the [BotFather](https://t.me/botfather) a /newbot command. You get a token back.
- (Not mandatory) Now send /setcommands to change the list of commands. Select your bot and paste the commands list from [here](https://github.com/koteshrv/herokumeet#commands)
- Follow [this](https://stackoverflow.com/questions/32683992/find-out-my-own-user-id-for-sending-a-message-with-telegram-api#answers) procedure to get your telegram chat id.
- That's it! Now press the deploy to heroku button below and enter the bot token, user id, mail, password and deploy it into your heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

- Now go to app settings get the heroku git link. Url will be in the following format "https://git.heroku.com/appname.git"
- Now clone this repo locally.
- In dependencies/data.json add classroom links of your subjects, change alertWords,  minCountToJoin, minCountToLeave.
- Add subjects to linkPostedSeperatelyInAnnouncementTab if your class link is posted in announcement section.
- Change startupTime in data.json to the time when your classes are about to start. If your classwork starts at 09:00 then set startupTime to 08:55.
- Set auto reply to 1, if you need and change the responseMessage to your choice.
- Change timetable.xlsx and set time format as 'HH:MM - HH:MM' and subject names in timetable and subject keys in data.json should be same.
- Fill telegram token, id, gmail and password in config.py and run googleLogin.py. This will create a google.pkl file. This is used to login to your account.
- Now delete .gitignore file and push the repo
- Now you can start using this telegram bot.

## If you want to deploy locally

- Run telegrambot.py and you can start using the bot.

## Usage

```
joins all classes for today 
/meet 

takes meet link and joins the meet immediately
arguments: meet link
/joinnow https://meet.google.com/tkj-kdxp-cjs 

takes meet link and schedules the meet
arguments: meet link, time
/joinlater https://meet.google.com/tkj-kdxp-cjs 18:35

sends screenshot of driver instance
/status

returns present running class and None if no class is going on
/whichclass 

prints today's classes
/classestoday

prints timetable
/timetable

updates timetable
arguments: day, period, class name
/updatetimetable monday 2 DBMS
the above command changes second period on monday to dbms
we can also use updatetimetable to update timings
/updatetimetable timings 2 10:00-10:50
the above command changes second period timing to 10:00 - 10:50

updates timetable temporarily and reverts to original timetable after the class ends
arguments are same as updatetimetable command
/tempupdatetimetable monday 2 DBMS 

prints holidays list
/holidays

adds holiday to the list
arguments: day and occasion(without spaces)
/addholiday 15 Independence_day

removes holiday from the list
arguments: day
/removeholiday 15 

prints log data
/sendlog

displays all bot commands with description
/help

ends the current meet if meet is going on
/exitmeet

restarts the bot 
/restart

sends a message to google meet chat. Needs confirmation 
/reply Sending this message from telegram
now to send "Sending this message from telegram" to google meet chat you
should use /send

sends message to google meet chat that was received when reply is used
/send

sends pagesource of the driver
/pagesource 

loads the url sent by the user
/load url

returns files present in the repository
/files
```

## Credits

- [Aditya](https://github.com/1337w0rm) (His [repo](https://github.com/1337w0rm/YeetMeet) helped me to understand how to deploy this on heroku)

## Task List

- [X] Fetch link from google classroom
- [X] Send alert message when someone called
- [X] Auto reply
- [ ] Screen record with audio
- [ ] Upload recording to google drive
