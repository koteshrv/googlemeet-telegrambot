#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from rich.console import Console
from dependencies import *
from time import sleep
import time
import sys

argLen = len(sys.argv)
console = Console()

if argLen == 1:

	print(text2art("Google Meet Bot", font = "small"))

	# checks for holiday
	dateAndTime = datetime.now()
	day = dateAndTime.day
	noClasses = False
	updateholidaysList()
	loadTimeTable()
	jsonData = fetchDataFromJSON('log.json')
	holidaysDict = jsonData["holidaysList"]
	classesToday = jsonData["todaysTimeTable"]
	for holidayDate in holidaysDict:
		if day == holidayDate:
			console.print('No classes today due to '+ holidaysDict[holidayDate], style = "bold red")
			console.print('[bold][green]' + 'Done\n')
			noClasses = True

	# todays class list
	classesList = []
	for timings in classesToday:
		classesList.append(timings + ' '+ classesToday[timings])

	# classesList
	'''['23:45 - 23:50 TEST', '22:50 - 22:55 TEST2', '22:55 - 23:00 TEST', '23:00 - 23:05 TEST2', '23:05 - 23:10 TEST', '23:10 - 23:15 TEST2', '23:50 - 23:55 TEST']'''

	#get status for class joining
	# if status is True: classwork is completed
	# if status is false: classwork is scheduled for today in coming hours
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
		printInSameLine(str1 = 'You are early for the class. So I am sleeping for the next ', str2 = '', isChar = False, seconds = True, sleepTime = timeToSleep, color = "bold red", minutes = True)
		print()


	# if today is not a holiday and status is -1 that is when current time is between and start and end time of college classword
	if (not noClasses) and (status == -1 or status == False):

		print('currently in main code')
		
		classNow = whichClass()
		print(classNow)
		driver = loadDriver()
		totalClassesToday = len(classesList)
		usedPrintInSameLine = False

		for i in range(totalClassesToday):
			if usedPrintInSameLine:
				printInSameLine(newLine = True)
			classNow = whichClass()
			# this case occurs when someone joins the class late
			# that is when start time is 10:00 and when you try to join in 11:30 then you should skip the first class
			if(classNow == None) :
				continue

			if classNow == "Lunch":
				TimeLeftForNextClass = 60 - int(str(datetime.now().time())[3:5]) # minutes
				printInSameLine(str1 = 'Lunch Time. Will trying again in ', str2 = ' seconds', isChar = False, seconds = True, sleepTime = TimeLeftForNextClass, color = "bold red", minutes = True)
		
			classAlreadyAttended = False
			classAlreadyAttendedFlag = True

			while True:
				log = fetchDataFromJSON('log.json')
				joiningLeavingTime = log["log"]["joiningLeavingTime"]
				print(classNow)
				if classNow in joiningLeavingTime:
					if joiningLeavingTime[classNow]["joining time"][:2] == str(datetime.now().time())[:2] and "leaving time" in joiningLeavingTime[classNow]:
						classAlreadyAttended = True
						prevClass = classNow
				if classAlreadyAttended:
					if classAlreadyAttendedFlag:
						if usedPrintInSameLine:
							printInSameLine(newLine = True)
						print(classNow + ' class already joined!')
						print("Joining time: ", joiningLeavingTime[classNow]["joining time"][:8])
						print("Leaving time: ", joiningLeavingTime[classNow]["leaving time"][:8])
						classAlreadyAttendedFlag = False
					printInSameLine(str1 = "Trying again in ", str2 = ' seconds', isChar = False, seconds = True, sleepTime = 30)
					usedPrintInSameLine = True
				elif classNow == None:
					while classNow == None:
						print(classNow)
						printInSameLine(str1 = "No class to join at the moment! Trying again in ", str2 = ' seconds', isChar = False, seconds = True, sleepTime = 30)
						usedPrintInSameLine = True
					break
				else :
					break
				classNow = whichClass()
			if usedPrintInSameLine:
				printInSameLine(newLine = True)
			print(classNow + ' is going on at the moment')
			print('Trying to join ' + classNow + ' class')
			joinClass(classNow, driver)
			jsonData = fetchDataFromJSON('log.json')
			t = jsonData["todaysTimeTable"]
			classTime = list(t.keys())
			periods = {}
			if classTime[i] in periods:
				periods[classTime[i]].update("Attended")
			else :
				periods[classTime[i]] = "Attended"

			jsonData["log"]["classStatus"].update(periods)
			sendDataToJSON('log.json', jsonData)


			print('Left ' + classNow + ' class')
		
		driver.quit()

		


elif argLen == 2:
	arg = sys.argv[1].lower()

	if arg == '--t':
		loadTimeTable()
		classesToday(printTable = True)

	elif arg == '--h':
		displayHolidaysList()

	elif arg == '--c':
		loadTimeTable()
		print(color.CYAN + str(whichClass()) + color.END)

	elif arg == '--help':
		helpFunction()

	else :
		print(arg + " is not a command. See main.py --help")

elif argLen == 3:
	arg1 = sys.argv[1].lower()
	arg2 = sys.argv[2].lower()

	if arg1 == '--h' and arg2 == '-a':
		date, occasion = input("Enter holiday and occasion: ").split()
		updateholidaysList(date, occasion)
		data = fetchDataFromJSON('log.json')
		displayHolidaysList()

	elif arg1 == '--h' and arg2 == '-r':
		date = input("Enter the date you wanted to remove: ")
		updateholidaysList(date, remove = True)
		data = fetchDataFromJSON('log.json')
		displayHolidaysList()

	elif arg1 == '--t' and arg2 == '-f':
		displayTimeTable()

	elif arg1 == '--t' and arg2 == '-u':
		displayTimeTable()
		count = input("Enter number of classes you want to update: ")
		for i in range(count):
			day, classTime = input("Enter day and period you want to change: ").split()
			classToUpdate = input("Enter the class name you want to change: ")
			updateTimeTable(day, classTime, classToUpdate)
		displayTimeTable()

	else :
		if arg1 == '--h' or arg1 == '--t':
			print(arg2 + " is not a command. See main.py --help")	
		else :
			print("main.py " + arg1 + " " + arg2 + " is not a command. See main.py --help")		

	