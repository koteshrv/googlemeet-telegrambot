from telegram.ext.dispatcher import run_async
from art import *
import time
from datetime import datetime, timedelta
from dependencies.joinmeet import joinMeet, joinError
from dependencies.others import (checkStatus, fetchDataFromJSON, sendDataToJSON, updateholidaysList, loadTimeTable,
                           classesToday, classStatus, whichClass,
						   revertTimeTable, checklogin, Print, sendToTelegram, printLog)


def meetbot():
	# checks whether user account is already logged in or not
	if checklogin():
		return

	print(text2art("herokumeet", font = "small"))

	# Checking for previous day log
	# If previous day log is present then it's cleared
	dateAndTime = datetime.now()
	day = dateAndTime.day
	weekDay = dateAndTime.today().strftime('%A')
	jsonData = fetchDataFromJSON('log.json')
	if jsonData["log"]["day"] != weekDay:
		jsonData["log"]["day"] = weekDay
		jsonData["log"]["joiningLeavingTime"] = {}
		jsonData["log"]["classStatus"] = {}
	sendDataToJSON('log.json', jsonData)

	# checking for holiday
	dateAndTime = datetime.now()
	day = dateAndTime.day
	updateholidaysList()
	jsonData = fetchDataFromJSON('log.json')
	holidaysDict = jsonData["holidaysList"]
	for holidayDate in holidaysDict:
		if str(day) == holidayDate:
			Print('No classes today due to '+ holidaysDict[holidayDate])
			return

	loadTimeTable()
	classesToday()
	jsonData = fetchDataFromJSON('log.json')
	classesTodayData = jsonData["todaysTimeTable"]

	# todays class list from the present time
	# for suppose if we have classes from 9:00 to 4:00 and if we run this script at 10:00 
	# then it will consider classes from 10:00 into classList
	classesList = []
	
	for timings in classesTodayData:
		# if current time is less than class start time then we should add all periods to the list
		h, m, s = str(datetime.now().time()).split(':')
		presentTime = timedelta(hours = int(h), minutes = int(m), seconds = int(float(s)))
		startTime = timedelta(hours = int(timings[0:2]), minutes = int(timings[3:5]))
		endTime = timedelta(hours = int(timings[8:10]), minutes = int(timings[11:]))
		flag = False
		if presentTime < startTime: 
			flag = True
		# if we have a class in current time then we should add classes from now to the list
		if presentTime >= startTime and presentTime < endTime:
			flag = True
		if flag:
			classesList.append(timings + ' ' + classesTodayData[timings])

	completedClassesCount = len(classesTodayData) - len(classesList)

	# get status for class joining
	# if status is True: classwork is completed
	# if status is false: classwork is scheduled for today
	# if status if -1: classwork is going on at the moment
	status = classStatus()

	# if status is true: classwork is completed for today
	if status == True:
		Print('All classes attended for today')
		sendToTelegram('Print')
		return

	# if status will be false when current time is less than start time of college so we wait here until status becomes -1	
	if status == False:
		jsonData = fetchDataFromJSON('log.json')
		todaysTimeTable = jsonData["todaysTimeTable"]
		timings = list(todaysTimeTable.keys())
		start_h, start_m = map(int, timings[0][:5].split(':'))
		h, m, s = str(datetime.now().time()).split(':')
		timeToSleep = (timedelta(hours = start_h, minutes = start_m) - timedelta(hours = int(h), minutes = int(m), seconds = int(float(s)))).total_seconds()
		Print('You are early for the class. So I am sleeping for the next ' + str(timedelta(seconds = timeToSleep)))
		sendToTelegram('You are early for the class. So I am sleeping for the next ' + str(timedelta(seconds = timeToSleep)))
		time.sleep(timeToSleep)
		

	# if today is not a holiday and status is -1 that is classwork is going on 
	if status == -1 or status == False:
		classNow = whichClass()
		totalclassesTodayData = len(classesList)

		# joins all classes that are stored in classesList
		for i in range(totalclassesTodayData):
			classNow = whichClass()

			# if current class is "None" then it will wait until next class
			# current class returns "None" when we dont have any period or if we already attended the class
			if classNow == None:
				nextClass = whichClass(nextClass = True, nextClassTime = True)
				start_h, start_m = map(int, nextClass[0][:5].split(':'))
				h, m, s = str(datetime.now().time()).split(':')
				timeLeftForNextClass = (timedelta(hours = start_h, minutes = start_m) - timedelta(hours = int(h), minutes = int(m), seconds = int(float(s)))).total_seconds()
				Print('No class at the moment. Will try again in ' +  str(timedelta(seconds = timeLeftForNextClass)))
				sendToTelegram('No class at the moment. Will try again in ' +  str(timedelta(seconds = timeLeftForNextClass)))
				time.sleep(timeLeftForNextClass)

			# if current class returns "Lunch" then it sleeps until next class
			if classNow == "Lunch":
				nextClass = whichClass(nextClass = True, nextClassTime = True)
				start_h, start_m = map(int, nextClass[0][:5].split(':'))
				h, m, s = str(datetime.now().time()).split(':')
				timeLeftForNextClass = (timedelta(hours = start_h, minutes = start_m) - timedelta(hours = int(h), minutes = int(m), seconds = int(float(s)))).total_seconds()		
				Print('Lunch Time. Will join next class in ' + str(timedelta(seconds = timeLeftForNextClass)))
				sendToTelegram('Lunch Time. Will join next class in ' + str(timedelta(seconds = timeLeftForNextClass)))
				time.sleep(timeLeftForNextClass)

			# joins current class and updates the log
			classNow = whichClass()	
			while classNow == None or classNow == "Lunch":
				classNow = whichClass()
			Print(classNow + ' is going on at the moment')
			Print('Trying to join ' + classNow + ' class')
			joinMeet(subject = classNow)
			if joinError:
				sendToTelegram('Unexcepted error occured when trying to join the class\n So stopping the operation\n To try again send /meet')
				Print('Unexcepted error occured when trying to join the class\n So join again')
				return

			jsonData = fetchDataFromJSON('log.json')
			t = jsonData["todaysTimeTable"]
			classTime = list(t.keys())
			periods = {}
			if classTime[i + completedClassesCount] in periods:
				periods[classTime[i + completedClassesCount]].update(classNow)
			else :
				periods[classTime[i + completedClassesCount]] = classNow

			jsonData["log"]["classStatus"].update(periods)
			sendDataToJSON('log.json', jsonData)

		# reverting the classes if previously changed
		# if the timetable is temporarily changed then its reverted to original 
		revertTimeTable()

		Print("Attended all classes successfully!")
