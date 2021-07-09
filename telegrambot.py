from typing import Container
from dependencies.others import sendTimetable, sendToTelegram, takeScreenshot
from telegram.ext import CommandHandler, Job, run_async
from telegram import ChatAction
from os import execl
from sys import executable
from dependencies import discordAndPrint, dp, updater, driver
from dependencies.login import login
from dependencies.meetbot import meetbot
from meetschedule import dailySchedule
from dependencies.joinmeet import joinMeet, endButtonXPath
from dependencies.others import (setStatus, whichClass, loadTimeTable, fetchDataFromJSON,
                                classesToday, updateholidaysList, updateTimeTable,
                                sendDataToJSON, printLog)
import os, config, threading

@run_async
def joinnow(update, context):
	meetLink = update.message.text.split()[-1]
	if(meetLink[:24] == 'https://meet.google.com/' or meetLink[:23] == 'http://meet.google.com/'):
		joinMeet(context, URL = meetLink)
	else:
		sendToTelegram(context, 'OOPS! Invalid URL. Try again')

@run_async
def joinlater(update, context):
    arguments = update.message.text.split()
    meetLink, joinTime = arguments[-2], arguments[-1]
    if ((meetLink[:24] == 'https://meet.google.com/' or meetLink[:23] == 'http://meet.google.com/') 
        and (len(joinTime) == 5 and joinTime[2] == ':')):
        joinMeet(context, URL = meetLink, loginTime = joinTime)
    else:
        sendToTelegram(context, 'OOPS! Invalid arguments. Try again')

@run_async
def status(update, context):
    takeScreenshot(context)

@run_async
def restart(update, context):
    context.bot.send_message(chat_id = config.TELEGRAM_USER_ID, text = "Restarting, Please wait!")
    driver.quit()
    execl(executable, executable, "telegrambot.py")

@run_async
def exitmeet(update, context):
    setStatus("meetAlive", False)

@run_async
def whichclass(update, context):
    if whichClass() == None:
            sendToTelegram(context, 'No class is running at the moment!')
    else:
        sendToTelegram(context, whichClass())

@run_async
def timetable(update, context):
    sendToTelegram(context, sendTimetable())

@run_async
def classestoday(update, context):
    loadTimeTable()
    classesToday(printHoliday = False)
    log = fetchDataFromJSON('log.json')
    classes = log["todaysTimeTable"]
    s = 'Classes Today\n'
    spacesLen = 15
    for key, val in classes.items():
        keyLen = len(key)
        spacesLen = 15
        spaces = ' ' * (spacesLen - keyLen)
        s += key + spaces + val + '\n'
    sendToTelegram(context, s)

@run_async
def holidays(update, context):
    updateholidaysList()
    log = fetchDataFromJSON('log.json')
    holidays = log["holidaysList"]
    holidaysString = 'Holidays List\n'
    holidaysPresent = False
    for key, val in holidays.items():
        l = len(str(key))
        spaces = ' ' * (4 - l)
        holidaysString += (key + spaces + val + '\n')
        holidaysPresent = True
    if holidaysPresent:
        sendToTelegram(context, holidaysString) 
    else:
        sendToTelegram(context, "You don't have any holidays")

@run_async
def addholiday(update, context):
    arguments = update.message.text.split()
    date, occasion = arguments[-2], arguments[-1]
    if(date.isnumeric()):
        updateholidaysList(date, occasion)
        sendToTelegram(context, 'Added ' + str(date) + 'to the list successfully!')
        log = fetchDataFromJSON('log.json')
        holidays = log["holidaysList"]
        holidaysString = '__**Holidays List**__\n'
        holidaysPresent = False
        for key, val in holidays.items():
            l = len(str(key))
            spaces = ' ' * (4 - l)
            holidaysString += ('__**' + key + '**__ :' + spaces + val + '\n')
            holidaysPresent = True
        if holidaysPresent:
            sendToTelegram(context, holidaysString) 
        else:
            sendToTelegram(context, "You don't have any holidays")

@run_async
def removeholiday(update, context):
    date = update.message.text.split()[-1]
    if date.isnumeric():
        updateholidaysList(date, remove = True)
        sendToTelegram(context, 'Removed ' + str(date) + 'from the list successfully!')
        log = fetchDataFromJSON('log.json')
        holidays = log["holidaysList"]
        holidaysString = '__**Holidays List**__\n'
        holidaysPresent = False
        for key, val in holidays.items():
            l = len(str(key))
            spaces = ' ' * (4 - l)
            holidaysString += ('__**' + key + '**__ :' + spaces + val + '\n')
            holidaysPresent = True
        if holidaysPresent:
            sendToTelegram(context, holidaysString) 
        else:
            sendToTelegram(context, "You don't have any holidays")

@run_async
def updatetimetable(update, context):
    arguments = update.message.text.split()
    day, classTime, classToUpdate = arguments[-3], arguments[-2], arguments[-1]
    updateTimeTable(day, classTime, classToUpdate)
    loadTimeTable()
    sendToTelegram(context, 'Updated timetable successfully!')

@run_async
def tempupdatetimetable(update, context):
    arguments = update.message.text.split()
    day, classTime, classToUpdate = arguments[-3], arguments[-2], arguments[-1]

    log = fetchDataFromJSON('log.json')
    tempTimetableUpdateData = log["tempTimetableUpdate"]
    tempTimetableUpdateKeys = list(tempTimetableUpdateData.keys())
    previousClass = updateTimeTable(day, classTime, classToUpdate, previousClass = True)
    sendToTelegram(context, 'Temporarily updated ' + previousClass + ' in timetable successfully!')
    if len(tempTimetableUpdateKeys) == 0:
        tempTimetableUpdateData['0'] = {
            "day" : day,
            "period" : classTime,
            "classToUpdate" : classToUpdate,
            "previousClass" : previousClass
        }
    else :
        tempTimetableUpdateData[str(int(tempTimetableUpdateKeys[-1]) + 1)] = {
            "day" : day,
            "period" : classTime,
            "classToUpdate" : classToUpdate,
            "previousClass" : previousClass
        }
    log["tempTimetableUpdate"].update(tempTimetableUpdateData)
    sendDataToJSON('log.json', log)

@run_async
def sendlog(update, context):
    sendToTelegram(context, str(printLog()))

@run_async
def help(update, context):
    commands = ('meet - runs googlemeetbot\n'+
        'joinnow - takes meet link and joins the meet immediately\n'+
        'joinlater - takes meet link and schedules the meet\n'+
        'status - sends screenshot of driver instance\n'+
        'kill - kills the bot\n'+
        'whichclass - prints the present running class\n'+
        "classestoday - prints today's classes\n"+
        'timetable - prints timetable\n'+
        'updatetimetable - updates timetable\n'+
        'tempupdatetimetable - updates timetable temporarily\n'+
        'holidays - prints holidays list\n'+
        'addholiday - adds holiday to the list\n'+
        'removeholiday - removes holiday from the list\n'+
        'sendlog - prints log data'+
        'restart - restarts the bot'+
        'exitmeet - ends the meet immediately')
    sendToTelegram(context, commands)

def main():    
    dp.add_handler(CommandHandler("meet", meetbot))
    dp.add_handler(CommandHandler("restart", restart))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("login", login))
    dp.add_handler(CommandHandler("joinnow", joinnow))
    dp.add_handler(CommandHandler("joinlater", joinlater))
    dp.add_handler(CommandHandler("exitmeet", exitmeet))
    dp.add_handler(CommandHandler("whichclass", whichclass))
    dp.add_handler(CommandHandler("timetable", timetable))
    dp.add_handler(CommandHandler("classestoday", classestoday))
    dp.add_handler(CommandHandler("holidays", holidays))
    dp.add_handler(CommandHandler("addholiday", addholiday))
    dp.add_handler(CommandHandler("removeholiday", removeholiday))
    dp.add_handler(CommandHandler("updatetimetable", updatetimetable))
    dp.add_handler(CommandHandler("tempupdatetimetable", tempupdatetimetable))
    dp.add_handler(CommandHandler("sendlog", sendlog))
    dp.add_handler(CommandHandler("help", help))
    updater.start_polling()

    t1 = threading.Thread(target = dailySchedule)

    # starting thread 1
    t1.start()

if __name__ == '__main__':
    main()
