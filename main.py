#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from rich.console import Console
from dependencies import *
from time import sleep
import time
import sys

argLen = len(sys.argv)

# rich console
# https://github.com/willmcgugan/rich
console = Console()

if argLen == 1:

	print(text2art("Google Meet Bot", font = "small"))

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
	noClasses = False
	updateholidaysList()
	loadTimeTable()
	jsonData = fetchDataFromJSON('log.json')
	holidaysDict = jsonData["holidaysList"]
	classesTodayData = jsonData["todaysTimeTable"]
	for holidayDate in holidaysDict:
		if day == holidayDate:
			console.print('No classes today due to '+ holidaysDict[holidayDate], style = "bold red")
			console.print('[bold][green]' + 'Done\n')
			noClasses = True

	# todays class list from the present time
	# for suppose if we have classes from 9:00 to 4:00 and if we run this script at 10:00 
	# then it will consider classes from 10:00 into classList
	classesList = []
	flag = False
	for timings in classesTodayData:
		# if current time is less than class start time then we should add all periods to the list
		if compareTime(int(timings[0:2]), int(timings[3:5])): 
			flag = True
		# if we have a class in current time then we should add classes from now to the list
		if compareTime(int(timings[0:2]), int(timings[3:5]), int(timings[8:10]), int(timings[11:]), True):
			flag = True
		if flag:
			classesList.append(timings + ' '+ classesTodayData[timings])

	completedClassesCount = len(classesTodayData) - len(classesList)

	# classesList
	'''['23:45 - 23:50 TEST', '22:50 - 22:55 TEST2', '22:55 - 23:00 TEST', '23:00 - 23:05 TEST2', '23:05 - 23:10 TEST', '23:10 - 23:15 TEST2', '23:50 - 23:55 TEST']'''

	print()
	classesToday(printTable = True)

	# get status for class joining
	# if status is True: classwork is completed
	# if status is false: classwork is scheduled for today
	# if status if -1: classwork is going on at the moment
	status = classStatus()

	# if status is true: classwork is completed for today
	if status == True:
		console.print('All classes attended for today', style = "blink2 bold red")

	# if status will be false when current time is less than start time of college so we wait here until status becomes -1	
	if status == False:
		jsonData = fetchDataFromJSON('log.json')
		todaysTimeTable = jsonData["todaysTimeTable"]
		timings = list(todaysTimeTable.keys())
		startTime = timings[0][:5]
		dateAndTime = datetime.now()
		currentTime = dateAndTime.time()
		time = str(currentTime)[:5]
		timeForClass = subtractTime(startTime, time)
		l = timeForClass.split(':')
		timeToSleep = ((int(l[0]) * 60) + int(l[1]))
		printInSameLine(str1 = 'You are early for the class. So I am sleeping for the next ', str2 = '', isChar = False, seconds = True, sleepTime = timeToSleep, color = "bold bright_yellow", minutes = True)
		print(' ' * 80, end = '\r')

	# if today is not a holiday and status is -1 that is classwork is going on 
	if (not noClasses) and (status == -1 or status == False):
		classNow = whichClass()
		driver = loadDriver()
		totalclassesTodayData = len(classesList)
		usedPrintInSameLine = False

		# joins all classes that are stored in classesList
		for i in range(totalclassesTodayData):
			if usedPrintInSameLine:
				printInSameLine(newLine = True)
			classNow = whichClass()

			# if current class returns "Lunch" then it sleeps until next class
			if classNow == "Lunch":
				nextClass = whichClass(nextClass = True, nextClassTime = True)
				nextClassStartTime = nextClass[0][:5]
				dateAndTime = datetime.now()
				currentTime = dateAndTime.time()
				time = str(currentTime)[:5]
				timeLeftForNextClass = subtractTime(nextClassStartTime, time)
				hours, minutes = timeLeftForNextClass.split(':')
				sleepTimeForNextClass = int(hours) * 60 + int(minutes)
				printInSameLine(str1 = 'Lunch Time. Will trying again in ', str2 = ' seconds', isChar = False, seconds = True, sleepTime = sleepTimeForNextClass, color = "bold red", minutes = True)
			classAlreadyAttended = False
			classAlreadyAttendedFlag = True

			# if current class is "None" then it will wait until next class
			# current class returns "None" when we dont have any period or if we already attended the class
			if classNow == None:
				nextClass = whichClass(nextClass = True, nextClassTime = True)
				nextClassStartTime = nextClass[0][:5]
				dateAndTime = datetime.now()
				currentTime = dateAndTime.time()
				time = str(currentTime)[:5]
				timeLeftForNextClass = subtractTime(nextClassStartTime, time)
				hours, minutes = timeLeftForNextClass.split(':')
				sleepTimeForNextClass = int(hours) * 60 + int(minutes)
				printInSameLine(str1 = "No class to join at the moment! Trying again in ", str2 = '', isChar = False, seconds = True, sleepTime = sleepTimeForNextClass, minutes = True)
				print(' ' * 80, end = '\r')

			# joins current class and updates the log	
			classNow = whichClass()
			if usedPrintInSameLine:
				printInSameLine(newLine = True)
			console.print('\n' + classNow, style = "bold bright_yellow", end = '')
			console.print(' class is going on at the moment\n', style = "bold")
			print('Trying to join ' + classNow + ' class')
			joinClass(classNow, driver)
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

		console.print("Attened all classes successfully!", style = "BLINK2 bold red")
		driver.quit()


elif argLen == 2:
	arg = sys.argv[1].lower()

	# loads the timetable and prints todays timetable
	if arg == '--t':
		loadTimeTable()
		classesToday(printTable = True)

	# prints the holidays list
	elif arg == '--h':
		displayHolidaysList()

	# loads the timetable and prints the current class
	# if there is no class at the moment, then it returns "None"
	elif arg == '--c':
		loadTimeTable()
		print(color.CYAN + str(whichClass()) + color.END)

	# prints all arguments and their uses
	elif arg == '--help':
		helpFunction()

	else :
		print(arg + " is not a command. See main.py --help")

elif argLen == 3:
	arg1 = sys.argv[1].lower()
	arg2 = sys.argv[2].lower()

	# add holiday to the holiday list
	if arg1 == '--h' and arg2 == '-a':
		date, occasion = input("Enter holiday and occasion: ").split()
		updateholidaysList(date, occasion)
		data = fetchDataFromJSON('log.json')
		displayHolidaysList()

	# remove holiday from the holiday list
	elif arg1 == '--h' and arg2 == '-r':
		date = input("Enter the date you wanted to remove: ")
		updateholidaysList(date, remove = True)
		data = fetchDataFromJSON('log.json')
		displayHolidaysList()

	# prints complete timetable
	elif arg1 == '--t' and arg2 == '-f':
		displayTimeTable()

	# updates timetable
	elif arg1 == '--t' and arg2 == '-u':
		displayTimeTable()
		count = input("Enter number of classes you want to update: ")
		for i in range(int(count)):
			day, classTime = input("Enter day and period you want to change: ").split()
			classToUpdate = input("Enter the class name you want to change: ")
			updateTimeTable(day, classTime, classToUpdate)
		displayTimeTable()

	else :
		print("main.py " + arg1 + " " + arg2 + " is not a command. See main.py --help")		

	