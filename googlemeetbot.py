from rich.console import Console
from dependencies import *
import sys

argLen = len(sys.argv)

# rich console
console = Console()

try:
	if argLen == 1:
		googlemeetbotThread()

	elif argLen == 2:
		arg = sys.argv[1].lower()
		# loads the timetable and prints todays timetable
		if arg == '--t':
			loadTimeTable()
			classesToday(printTable = True)

		# uses class url to join the class immediately
		elif arg == '--l':
			print(text2art("googlemeetbot", font = "small"))
			classLink = input(color.BOLD + color.YELLOW + 'Enter the class link: ' + color.END)
			print('Trying to join the class from the link')
			joinClassThread(classLink)

		# prints the holidays list
		elif arg == '--h':
			displayHolidaysList()

		# loads the timetable and prints the current class
		# if there is no class at the moment, then it returns "None"
		elif arg == '--c':
			print(color.CYAN + str(whichClass()) + color.END)

		# prints all arguments and their uses
		elif arg == '--help':
			helpFunction()

		# prints the log data(data in log.json)
		elif arg == '--log':
			printLog()

		else :
			print(arg + " is not a command. See googlemeetbot --help")

	elif argLen == 3:
		arg1 = sys.argv[1].lower()
		arg2 = sys.argv[2].lower()
		# uses class url to join the class and schedules at specified 'time'
		if arg1 == '--l':
			print(text2art("googlemeetbot", font = "small"))
			hours, minutes = arg2.split(':')
			print(color.YELLOW + 'If you want to schedule the class at ' + color.END + color.BOLD + color.GREEN +  hours + ' hr ' + minutes + ' min' + color.END)
			decision = input(color.GREEN + 'Do you want to schedule[Y/n]: ' + color.END)
			if decision == 'Y' or decision == 'y':
				classLink = input(color.BOLD + color.YELLOW + 'Enter the class link: ' + color.END)
				joinClassThread(classLink, arg2)
			else :
				print(color.BOLD + color.RED + 'Aborted' + color.END)

			

		# add holiday to the holiday list
		elif arg1 == '--h' and arg2 == '-a':
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

		elif arg1 == '--t' and arg2 == '-ut':
			data = fetchDataFromJSON('log.json')
			tempTimetableUpdateData = data["tempTimetableUpdate"]
			tempTimetableUpdateKeys = list(tempTimetableUpdateData.keys())
			displayTimeTable()
			count = input("Enter number of classes you want to update: ")
			for i in range(int(count)):
				day, classTime = input("Enter day and period you want to change: ").split()
				classToUpdate = input("Enter the class name you want to change: ")
				previousClass = updateTimeTable(day, classTime, classToUpdate, previousClass = True)
				if len(tempTimetableUpdateKeys) == 0:
					tempTimetableUpdateData[str(i)] = {
						"day" : day,
						"period" : classTime,
						"classToUpdate" : classToUpdate,
						"previousClass" : previousClass
					}
				else :
					tempTimetableUpdateData[str(int(tempTimetableUpdateKeys[-1]) + i + 1)] = {
						"day" : day,
						"period" : classTime,
						"classToUpdate" : classToUpdate,
						"previousClass" : previousClass
					}
				data["tempTimetableUpdate"].update(tempTimetableUpdateData)
			sendDataToJSON('log.json', data)
			displayTimeTable()

		else :
			print("googlemeetbot " + arg1 + " " + arg2 + " is not a command. See googlemeetbot --help")		

	

except KeyboardInterrupt:
	print(' ' * 150)
	print('Interrupted')
	try:
		sys.exit(0)
	except SystemExit:
		os._exit(0)



