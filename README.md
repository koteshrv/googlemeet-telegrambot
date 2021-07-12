# herokumeet
**herokumeet** is a telegram bot that attends your online classes. It can be easily deployed on heroku with in few minutes. It can be used to join all the classes of the day automatically. It has some features like **alert** when someone called, **auto respond**,joins and leaves the class according to the **members count**, **reply** and many more. For more details see features and usage.


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
- Send time to time updates to discord.
- Send log to telegram when required.

## Commands

```
/meet - runs joinmeet to join all classes today
/joinnow - takes meet link and joins the meet immediately
/joinlater - takes meet link and schedules the meet
/status - sends screenshot of driver instance
/kill - kills the bot
/whichclass - prints the present running class
/classestoday - prints today's classes
/timetable - prints timetable
/updatetimetable - updates timetable
/tempupdatetimetable - updates timetable temporarily
/holidays - prints holidays list
/addholiday - adds holiday to the list
/removeholiday - removes holiday from the list
/sendlog - prints log data
/help - displays all bot commands
/exitmeet - ends the current meet
/restart - restarts the bot 
/login - used to login google account
/reply - send a message to google meet chat. Needs confirmation 
/send - sends message to google meet chat that was received when reply is used
/logout - logs out google account
/pagesource - sends pagesource of the driver
```

## How to start using this

- First, you need to tell Telegram you want to register a Bot. To do this, send the [BotFather](https://t.me/botfather) a /newbot command. You get a token back.
- (Not mandatory) Now send /setcommands to change the list of commands. Select your bot and paste the commands list from [here](https://github.com/koteshrv/herokumeet#commands)
- Follow [this](https://stackoverflow.com/questions/32683992/find-out-my-own-user-id-for-sending-a-message-with-telegram-api#answers) procedure to get your telegram chat id.
- That's it! Now press the deploy to heroku button below and enter the bot token, user id, mail, password and deploy it into your heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

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

used to login google account
arguments: mail and password
this command is used to login using default mail and password
which are given at the time of heroku deployment
/login 
this command is used to login using custom mail and password
/login mail password

sends a message to google meet chat. Needs confirmation 
/reply Sending this message from telegram
now to send "Sending this message from telegram" to google meet chat you
should use /send

sends message to google meet chat that was received when reply is used
/send

logs out google account
/logout

sends pagesource of the driver
/pagesource 
```
