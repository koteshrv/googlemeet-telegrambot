from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dependencies import *
from time import sleep
import time
import sys

argLen = len(sys.argv)

if argLen == 1:


	print(text2art("Google Meet Bot", font = "small"))

	dateAndTime = datetime.now()
	day = dateAndTime.day
	noClasses = False
	updateholidaysList()
	jsonData = fetchDataFromJSON('log.json')
	holidaysDict = jsonData["holidaysList"]
	classesToday = jsonData["todaysTimeTable"]
	for holidayDate in holidaysDict:
		if day == holidayDate:
			console.print('No classes today due to '+ holidaysDict[holidayDate], style = "bold red")
			console.print('[bold][green]' + 'Done\n')
			noClasses = True

	classesList = []
	for timings in classesToday:
		classesList.append(timings + ' '+ classesToday[timings])


	if not noClasses:

		classNow = whichClass()
		while classNow == None:
			printInSameLine(str1 = 'No class at the moment. Will trying again in ', str2 = ' seconds', isChar = False, seconds = True, sleepTime = 60, color = "bold red")
		
		driver = loadDriver()

		totalClassesToday = len(classesList)
		usedPrintInSameLine = False

		for i in range(totalClassesToday):
			if usedPrintInSameLine:
				printInSameLine(newLine = True)
			classNow = whichClass()
			if(classNow == None) :
				print('No ongoing classes at the moment')

			if classNow == "Lunch":
				TimeLeftForNextClass = 60 - int(str(datetime.now().time())[3:5]) # minutes
				printInSameLine(str1 = 'Lunch Time. Will trying again in ', str2 = ' seconds', isChar = False, seconds = True, sleepTime = TimeLeftForNextClass, color = "bold red", minutes = True)
		

			
			classAlreadyAttended = False
			classAlreadyAttendedFlag = True

			while True:
				log = fetchDataFromJSON('log.json')
				joiningLeavingTime = log["log"]["joiningLeavingTime"]
				if classNow in joiningLeavingTime and joiningLeavingTime[classNow]["joining time"][:2] == str(datetime.now().time())[:2]:
					classAlreadyAttended = True
				if classNow == None :
					printInSameLine(str1 = 'Waiting for Todays link. Trying again in ', str2 = ' seconds', isChar = False, seconds = True, sleepTime = 30)
					usedPrintInSameLine = True
					#time.sleep(30)
				elif classAlreadyAttended:
					if classAlreadyAttendedFlag:
						if usedPrintInSameLine:
							printInSameLine(newLine = True)
						print(classNow + ' class already joined!')
						print("Joining time: ", joiningLeavingTime[classNow]["joining time"][:8])
						print("Leaving time: ", joiningLeavingTime[classNow]["leaving time"][:8])
						classAlreadyAttendedFlag = False
					printInSameLine(str1 = "Trying again in ", str2 = ' seconds', isChar = False, seconds = True, sleepTime = 30)
					usedPrintInSameLine = True
				else :
					break
				classNow = whichClass()
			if usedPrintInSameLine:
				printInSameLine(newLine = True)
			print(classNow + ' is going on at the moment')
			print('Trying to join ' + classNow + ' class')
			joinClass(classNow, driver)
			print('Left ' + classNow + ' class')
		
		driver.quit()



elif argLen == 2:
	arg = sys.argv[1].lower()

	if arg == '--t':
		classesToday(printTable = True)

	elif arg == '--h':
		displayHolidaysList()

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

	else :
		if arg1 == '--h' or arg1 == '--t':
			print(arg2 + " is not a command. See main.py --help")	
		else :
			print("main.py " + arg1 + " " + arg2 + " is not a command. See main.py --help")		

	