from telegram.ext import CommandHandler, Job, filters
from telegram import ChatAction
from os import execl
from sys import executable
from dependencies import Print, dp, updater, driver
from dependencies.login import login
from dependencies.meetbot import meetbot
from meetschedule import dailySchedule
from dependencies.joinmeet import joinMeet, endButtonXPath
from dependencies.others import (setStatus, whichClass, loadTimeTable, fetchDataFromJSON,
                                classesToday, updateholidaysList, updateTimeTable,
                                sendDataToJSON, printLog, sendMessageInChatBox,
                                sendTimetable, pageSource, sendToTelegram, takeScreenshot, 
                                checkStatus)
import os, config, threading, time, codecs
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext
)


def joinnow(update, context):
	sendToTelegram("Trying to join the meet now")
	meetLink = update.message.text.split()[-1]
	if(meetLink[:24] == 'https://meet.google.com/' or meetLink[:23] == 'http://meet.google.com/'):
		joinMeet(URL = meetLink)
	else:
		sendToTelegram(context, 'OOPS! Invalid URL. Try again')


def joinlater(update, context):
    arguments = update.message.text.split()
    meetLink, joinTime = arguments[-2], arguments[-1]
    sendToTelegram("Trying to schedule the meet at " + str(joinTime))

    if ((meetLink[:24] == 'https://meet.google.com/' or meetLink[:23] == 'http://meet.google.com/') 
        and (len(joinTime) == 5 and joinTime[2] == ':')):
        joinMeet(URL = meetLink, loginTime = joinTime)
    else:
        sendToTelegram('OOPS! Invalid arguments. Try again')


def status(update, context):
    takeScreenshot()


def restart(update, context):
    sendToTelegram("Restarting, Please wait!")
    driver.refresh()
    time.sleep(5)
    driver.quit()
    sendToTelegram("Restarted successfully!")
    execl(executable, executable, "telegrambot.py")
    


def exitmeet(update, context):
    if not checkStatus('meetAlive'):
        sendToTelegram('No meet is going on at the movement')
        Print('No meet is going on at the movement')

    setStatus("meetAlive", False)


def whichclass(update, context):
    if whichClass() == None:
            sendToTelegram('No class is running at the moment!')
    else:
        sendToTelegram(whichClass())


def timetable(update, context):
    sendToTelegram(sendTimetable())


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
    sendToTelegram(s)


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
        sendToTelegram(holidaysString) 
    else:
        sendToTelegram("You don't have any holidays")


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
            sendToTelegram(holidaysString) 
        else:
            sendToTelegram("You don't have any holidays")


def removeholiday(update, context):
    date = update.message.text.split()[-1]
    if date.isnumeric():
        updateholidaysList(date, remove = True)
        sendToTelegram('Removed ' + str(date) + 'from the list successfully!')
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
            sendToTelegram(holidaysString) 
        else:
            sendToTelegram("You don't have any holidays")


def updatetimetable(update, context):
    arguments = update.message.text.split()
    day, classTime, classToUpdate = arguments[-3], arguments[-2], arguments[-1]

    # updating time
    if classToUpdate[0].isnumeric():
        print(classToUpdate)
        classToUpdate = classToUpdate[:5] + ' - ' + classToUpdate[6:]

    updateTimeTable(day, classTime, classToUpdate)
    loadTimeTable()
    sendToTelegram('Updated timetable successfully!')


def tempupdatetimetable(update, context):
    arguments = update.message.text.split()
    day, classTime, classToUpdate = arguments[-3], arguments[-2], arguments[-1] 

    log = fetchDataFromJSON('log.json')
    tempTimetableUpdateData = log["tempTimetableUpdate"]
    tempTimetableUpdateKeys = list(tempTimetableUpdateData.keys())
    previousClass = updateTimeTable(day, classTime, classToUpdate, previousClass = True)
    sendToTelegram('Temporarily updated ' + previousClass + ' in timetable successfully!')
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


def sendlog(update, context):
    sendToTelegram(str(printLog()))


def help(update, context):
    commands = ('/meet - runs googlemeetbot\n'+
        '/joinnow - takes meet link and joins the meet immediately\n'+
        '/joinlater - takes meet link and schedules the meet\n'+
        '/status - sends screenshot of driver instance\n'+
        '/whichclass - prints the present running class\n'+
        "/classestoday - prints today's classes\n"+
        "/timetable - prints timetable\n"+
        '/updatetimetable - updates timetable\n'+
        '/tempupdatetimetable - updates timetable temporarily\n'+
        '/login - used to login to google account\n'
        '/holidays - prints holidays list\n'+
        '/addholiday - adds holiday to the list\n'+
        '/removeholiday - removes holiday from the list\n'+
        '/sendlog - prints log data\n'+
        '/restart - restarts the bot\n'+
        '/exitmeet - ends the meet immediately\n'+
        '/reply - send a message to google meet chat. Needs confirmation\n'+
        '/send - sends message to google meet chat that was received when /reply is used')
    sendToTelegram(commands)

def meet(update, context):
    sendToTelegram("Trying to call meetbot")
    meetbot()

def unknown(update, context):
    user = str(update.effective_chat.id)
    if user == config.TELEGRAM_USER_ID:
        context.bot.send_message(chat_id = user, text="Sorry, I didn't understand that command.")
    else:
        context.bot.send_message(chat_id = user, text="Hey! This bot is not for you :( \nIf you want to make a similar one, then go to https://github.com/koteshrv/herokumeet :)")

def reply(update, context):
    msg = ' '.join(update.message.text.split()[1:])
    if len(msg) > 0:
        setStatus('messageFromTelegram', msg)
        sendToTelegram('Message received successfully!\n If you want to send this to google meet chat then press /send')
    else:
        sendToTelegram('OOPS! No message received! Send the message along with /reply\n Eg: /reply Hello from telegram')

def send(update, context):
    message = checkStatus('messageFromTelegram')
    sendMessageInChatBox(message)
   
def googleLogin(update, context):
    if len(update.message.text.split()) > 1:
        mail, password = update.message.text.split()[1:]
        login(mail, password)
    else :
        login()

def logout(update, context):
    try:
        os.remove('google.pkl')
        sendToTelegram('Logged out successfully')
        Print('Logged out successfully')
    except Exception:
        sendToTelegram('No account found to logout')
        Print('No account found to logout')


def sendPageSource(update, context):
    try:
        pageSource()
        sendToTelegram('Sent page source successfully!')
        Print('Sent page source successfully!')
    except Exception:
        sendToTelegram('Page source not found!')
        Print('Page source not found!')


def main():    
    dp.add_handler(CommandHandler("meet", meet, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("restart", restart, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("status", status, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("login", googleLogin, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("joinnow", joinnow, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("joinlater", joinlater, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("exitmeet", exitmeet, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("whichclass", whichclass, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("timetable", timetable, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("classestoday", classestoday, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("holidays", holidays, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("addholiday", addholiday, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("removeholiday", removeholiday, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("updatetimetable", updatetimetable, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("tempupdatetimetable", tempupdatetimetable, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("sendlog", sendlog, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("help", help, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("reply", reply, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("send", send, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("logout", logout, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))
    dp.add_handler(CommandHandler("pagesource", sendPageSource, run_async = True, filters = Filters.user(user_id = int(config.TELEGRAM_USER_ID))))


    unknown_handler = MessageHandler(Filters.command, unknown)
    dp.add_handler(unknown_handler)

    updater.start_polling(timeout=15, read_latency=4)

if __name__ == '__main__':

    try:

        t1 = threading.Thread(target = dailySchedule)

        # starting thread 1
        t1.start()
    
    except Exception as e:
        Print(str(e))


    main()
