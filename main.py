from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dependencies import *
from time import sleep
import time
import sys


arg = sys.argv[1].lower()
#option = sys.argv[2].lower()

if arg == '--t':
	print(text2art("Time Table", font = "small"))
	classes_today()
	

elif arg == '--h':
	if option == '-d':
		holidaysList()
		data = fetchDataFromJSON('log.json')
		print(data["holidaysList"])
	elif option == '-u':
		date, occasion = input("Enter holiday and occasion: ").split()
		holidaysList(date, occasion)
		data = fetchDataFromJSON('log.json')
		print(data["holidaysList"])

	else :
		print('Wrong argument ', option)

	

elif input == '--auto':
	print(text2art("Google Meet Bot", font = "small"))
	classNow = 'TEST'
	driver = loadDriver()
	joinClass(classNow, driver)
	print('Left ' + classNow + ' class')

	'''
	dateAndTime = datetime.now()
	day = dateAndTime.day
	noClasses = False
	for holidayDate in holidayList:
		if day == holidayDate:
			console.print('No classes today due to '+ holidaysDict[holidayDate], style = "bold red")
			console.print('[bold][green]' + 'Done\n')
			noClasses = True


	if not noClasses:

		classNow = whichClass()

		if(classNow == None) :
			print('No ongoing classes at the moment')
		else :
			driver = loadDriver()
			totalClassesToday = len(findClasses())
			print('class count ', totalClassesToday)

			for i in range(totalClassesToday):
				classNow = whichClass()
				while True:
					if(classNow == None) :
						print('No ongoing classes at the moment')
						time.sleep(30)
					else :
						break
					classNow = whichClass()
				print(classNow + ' is going on at the moment')
				print('Trying to join ' + classNow + ' class')
				joinClass(classNow, driver)
				print('Left ' + classNow + ' class')

	'''