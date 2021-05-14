from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from rich.console import Console
from selenium import webdriver
from datetime import datetime
from rich.table import Table
from art import *
import openpyxl, calendar, requests, json, time, sys, os, re


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


# fetch data from json and returns data
# argument: file name of json
def fetchDataFromJSON(fileName):
	with open('C:\\googlemeetbot\\' + fileName) as file:
		data = json.load(file)
	return data

# export data to json
# arguments: name of the file and data that we want to export
def sendDataToJSON(fileName, data):
	with open('C:\\googlemeetbot\\' + fileName, 'w') as file:
		json.dump(data, file, indent = 4)		

data = fetchDataFromJSON('data.json')
profilePath = data['dir']['profilePath']
windowsUser = data["otherData"]["windowsUser"]
if windowsUser:
    import winsound

# rich console
# https://github.com/willmcgugan/rich
console = Console()

# chrome options
chromeOptions = Options()
chromeOptions.add_argument("--disable-extensions")
chromeOptions.add_argument("--disable-popup-blocking")
chromeOptions.add_argument("--user-data-dir=" + profilePath)
#chromeOptions.add_argument("--profile-directory = Profile 1")
chromeOptions.add_experimental_option("prefs", { \
"profile.default_content_setting_values.media_stream_mic": 2,
"profile.default_content_setting_values.media_stream_camera": 2,
"profile.default_content_setting_values.geolocation": 2,
"profile.default_content_setting_values.notifications": 2
})

# classes and xpaths of google meet and google classroom elements
mailBoxXPath = '//*[@id="identifierId"]'
nextButtonXPath = '//*[@id="identifierNext"]/div/button'
enterPasswordBoxXPath = '//*[@id="password"]/div[1]/div/div[1]/input'
passwordNextButtonXPath = '//*[@id="passwordNext"]/div/button/div[2]'
meetLinkXPath = '//*[@id="yDmH0d"]/div[4]/div[3]/div/div[1]/div/div[2]/div[2]/div/span/a'
meetLinkInCommentsXPath = '//*[@id="ow43"]/div[2]/div/div[1]/div[2]/div[1]/html-blob/span/a[1]'
dateTimeInCommentsXPath = '//*[@id="ow43"]/div[2]/div[1]/div[1]/div[1]/div[1]/span/span[1]'
classroomPostClass = 'n8F6Jd'
meetLinkClass = 'qyN25' 
warningDismissButton = '//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div/span/span'
membersCountBeforeJoiningClass = 'Yi3Cfd'
messageAboveJoinButtonClass = 'JMAjle'
joinButtonXPath = '//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span/span'
captionsButtonXPath = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[9]/div[3]/div[2]/div/span/span/div/div[1]/i'
captionsXPath = 'VbkSUe'
membersCountXPath = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[1]/div[3]/div/div[2]/div[1]/span/span/div/div/span[2]'
chatBoxButtonXPath = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[1]/div[3]/div/div[2]/div[3]/span/span'
chatBoxXPath = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[4]/div/div[2]/div[2]/div[2]/span[2]/div/div[4]/div[1]/div[1]/div[2]/textarea'
chatSendButtonXPath = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[4]/div/div[2]/div[2]/div[2]/span[2]/div/div[4]/div[2]/span/span'
chatBoxCloseXPath = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[4]/div/div[2]/div[1]/div[2]/div/span/button/i'	


# custom output
def richStatus(text = 'Loading...', sleepTime = 10, spinnerType = 'dots', statusMessage = 'Done', color = "green"):
	with console.status("[bold white] " + text, spinner = spinnerType) as status:
		time.sleep(sleepTime)
	console.print(statusMessage, style = "bold " + color)

# custom output
def printInSameLine(str1 = 'Loading', str2 = '.', sleepTime = 10, isChar = True, newLine = False, seconds = False, color = "bold green", minutes = False):
	if newLine:
		print()
		return
	sec = sleepTime
	s = ' ' * 40
	for x in range (0, int(sleepTime) + 1): 
		minutesOrSeconds = ''
		if seconds:
			minutesOrSeconds = str(sec - x)
		if minutes:
			hours = (sec - x) // 60
			minutes = sec - x - (hours * 60)
			minutesOrSeconds = str(hours) + " hr : " + str(minutes) + " min"
		b = str1 + minutesOrSeconds +  str(str2) * (x if isChar else 1)
		print(s, end = '\r')
		console.print(b, end = '\r', style = color)
		if sleepTime > 0:
			time.sleep(1)
		
		if minutes:
			time.sleep(60)
		s = ' ' * len(b) 
	if isChar:
		print('')

# compares time and returns true of false
# if twoValues is False, then it returns true when given time is greater than current time else returns False
# if twoValues is True, then it returns true when current time lies between both times else returns False
def compareTime(hours1 = 0, minutes1 = 0, hours2 = 0, minutes2 = 0, twoValues = False):
	temp1 = datetime.now()
	timeNow = datetime.now()
	if twoValues:
		temp2 = datetime.now()
		return (timeNow < temp2.replace(hour = hours2, minute = minutes2) and timeNow > temp1.replace(hour = hours1, minute = minutes1)) 
	return timeNow < temp1.replace(hour = hours1, minute = minutes1)

# returns current day with 0 index
# if current day is Monday then it returns 0, Tueday 1, Wednesday 2 ... and for Sunday 6
def findDay():
	dateAndTime = datetime.now()
	date = str(dateAndTime.day) + ' ' + str(dateAndTime.month) + ' ' + str(dateAndTime.year)
	weekDay = datetime.strptime(date, '%d %m %Y').weekday()
	return weekDay

# returns second saturday of present month
def isSecondSaturday():
	dateAndTime = datetime.now()
	month = dateAndTime.month
	year = dateAndTime.year
	day = dateAndTime.day
	monthCalendar = calendar.monthcalendar(year, month)
	if monthCalendar[0][calendar.SATURDAY]:
		secondSaturday = monthCalendar[1][calendar.SATURDAY]
	else:
		secondSaturday = monthCalendar[2][calendar.SATURDAY]
	return secondSaturday

# updates the holiday list
# when no key and value are given, then it checks for second saturday and sunday
# when key and value are given then it updates the holiday list with key and value and also check for second saturday and sunday
# when remove is true, then it removes the key and value from the holidays list
def updateholidaysList(key = None, value = None, remove = False):
	jsonData = fetchDataFromJSON('log.json')
	holidaysDict = jsonData["holidaysList"]
	if remove:
		del holidaysDict[key]
		console.print('Deleted '+ key + ' from holidays list successfully', style = "gold3")
	else :
		dateAndTime = datetime.now()
		day = dateAndTime.day
		secondSaturday = isSecondSaturday()
		if secondSaturday >= day:
			holidaysDict[str(secondSaturday)] = 'Second Saturday'
		if findDay() == 6:
			holidaysDict[str(day)] = 'Sunday'
		if not (key == None and value == None):
			holidaysDict[str(key)] = value
		for holidayDate in list(holidaysDict):
			if int(holidayDate) < day:
				holidaysDict.pop(holidayDate)

	jsonData["holidaysList"].update(holidaysDict)
	sendDataToJSON('log.json', jsonData)

# loads the time table from the excel sheet and then updates the classes today
def loadTimeTable():
	classTimeTableLocation = data['dir']['classTimeTableLocation']
	timetablewb = openpyxl.load_workbook(classTimeTableLocation) 
	sheet = timetablewb.active
	maxColumn = sheet.max_column
	maxRow = sheet.max_row
	completeTimeTable = {}
	for i in range(1, maxRow + 1):
		rowValues = []
		keyValue = sheet.cell(row = i, column = 1)
		for j in range(2, maxColumn + 1):
			cellValue = sheet.cell(row = i, column = j)
			if cellValue.value != None:
				rowValues.append(cellValue.value)
		completeTimeTable[keyValue.value] = rowValues
	jsonData = fetchDataFromJSON('log.json')
	jsonData["completeTimeTable"].update(completeTimeTable)
	sendDataToJSON('log.json', jsonData)
	classesToday(printHoliday = False)

# returns the status of the classwork
# if no class is going on, then it returns False which means that classes are scheduled later
# if classwork is completed then it returns True which means all classes are already completed
# if classwork is going on, then it returns -1
def classStatus():
	jsonData = fetchDataFromJSON('log.json')
	todaysTimeTable = jsonData["todaysTimeTable"]
	timings = list(todaysTimeTable.keys())
	startTime = timings[0][:5]
	endTime = timings[-1][8:]
	time = datetime.now().time()
	time = str(time).split(":")
	if compareTime(int(startTime[:2]), int(startTime[3:]), int(endTime[:2]), int(endTime[3:]), True):
		return -1
	if compareTime(int(startTime[:2]), int(startTime[3:])):
		return False
	if not compareTime(int(endTime[:2]), int(endTime[3:])):
		return True

	
# subtracts the time (24 hour format)
def subtractTime(time1, time2):
	hour1, minutes1 = time1[:2], time1[3:]
	hour2, minutes2 = time2[:2], time2[3:]
	if minutes1 >= minutes2:
		return str(int(hour1) - int(hour2)) + ':' + str(int(minutes1) - int(minutes2))
	else :
		return str(int(hour1) - int(hour2) - 1) + ':' + str(60 - int(minutes2) + int(minutes1))

# makes a schedule  for classes today and prints  
def classesToday(printTable = False, printHoliday = True):
	date = findDay()
	classes = []
	updateholidaysList()
	jsonData = fetchDataFromJSON('log.json')
	holidays = jsonData["holidaysList"]
	dateAndTime = datetime.now()
	day = dateAndTime.day
	weekDay = dateAndTime.today().strftime('%A')
	if str(day) in holidays and printHoliday:
		console.print("\n\tToday is a holiday due to ", style = "bold cyan", end = '')
		console.print(holidays[str(day)] + '\n', style = "bold yellow")
	else:
		classes = []
		classtime = []
		classesToday = jsonData["completeTimeTable"][weekDay]
		timings = jsonData["completeTimeTable"]["Timings"]
		timings = timings[:len(classesToday)]
		prevClass = ''
		for i in range(len(classesToday)):
			if classesToday[i] == prevClass:
				classtime[-1] = classtime[-1][:8] + timings[i][8:]
			else :
				classes.append(classesToday[i])
				classtime.append(timings[i])
				prevClass = classesToday[i]
		t = {classtime[i]: classes[i] for i in range(len(classtime))}
		jsonData = fetchDataFromJSON('log.json')
		classLoginLog = jsonData["log"]["classStatus"]
		classesAlreadyAttended = list(classLoginLog.keys())
		jsonData["todaysTimeTable"] = t
		sendDataToJSON('log.json', jsonData)
		if printTable:
			currentTime = dateAndTime.time()
			time = str(currentTime).split(":")
			table = Table(show_lines=True)
			table.add_column("Timings", justify = "center", style = "cyan", no_wrap = True)
			table.add_column("Class", justify = "center", style = "green")
			table.add_column("Status", justify = "center", style = "magenta")
			classFlag = False
			for i in range(len(classtime)):
				if (not classFlag) and compareTime(int(classtime[i][0:2]), int(classtime[i][3:5])):
					table.add_row(classtime[i], classes[i], "[bold magenta] Scheduled [green]:hourglass:")
				elif compareTime(int(classtime[i][0:2]), int(classtime[i][3:5]), int(classtime[i][8:10]), int(classtime[i][11:]), True) and (not(classtime[i] in classesAlreadyAttended)):
					table.add_row(classtime[i], classes[i], "[bold magenta] ONGOING [green]:hourglass:")
					classFlag = True
				else:
					if classFlag == True:
						table.add_row(classtime[i], classes[i])
					else :
						table.add_row(classtime[i], classes[i], "[bold magenta]COMPLETED [green]:heavy_check_mark:")
			console.print(table)
			print()

# returns current class 
# if no class is going on or if the current class is already attended then it will return None
def whichClass(nextClass = False, nextClassTime = False, currentClassTime = False) :
	loadTimeTable()
	jsonData = fetchDataFromJSON('log.json')
	subjects = jsonData["todaysTimeTable"]
	classLoginLog = jsonData["log"]["classStatus"]
	classesAlreadyAttended = list(classLoginLog.keys())
	classCount = len(subjects)
	nextClassFlag = False
	for i in subjects:
		if nextClassFlag and (not nextClassTime):
			return subjects[i]
		if nextClassFlag and nextClassTime:
			return (i, subjects[i])
		time = datetime.now().time()
		time = str(time).split(":")
		if nextClass:
			if compareTime(int(i[0:2]), int(i[3:5]), int(i[8:10]), int(i[11:]), True):
				nextClassFlag = True
				continue
		elif compareTime(int(i[0:2]), int(i[3:5]), int(i[8:10]), int(i[11:]), True) and (not(i in classesAlreadyAttended)):	
			if currentClassTime:
				return (i, subjects[i])
			return subjects[i]	
	if nextClassTime or currentClassTime:
		return (None, None)
	return None

# prints complete time table
def displayTimeTable():
	loadTimeTable()
	jsonData = fetchDataFromJSON('log.json')
	t = jsonData["completeTimeTable"]
	dateAndTime = datetime.now()
	weekDay = dateAndTime.today().strftime('%A')
	table = Table(show_lines=True)
	timetableKeys = list(t.keys())
	table.add_column(timetableKeys[0], justify = "center", style = "cyan", no_wrap = True)
	for i in range(len(t[timetableKeys[0]])):
		table.add_column(t[timetableKeys[0]][i], justify = "center", style = "yellow", no_wrap = True)
	for i in timetableKeys[1:]:
		tempList = [i] + t[i]
		if weekDay == i:
			table.add_row(*tempList, style = "bold")
		else:
			table.add_row(*tempList)
	console.print(table)

# displays holidays list
def displayHolidaysList():
	updateholidaysList()
	data = fetchDataFromJSON('log.json')
	holidayListKeys = list(data["holidaysList"].keys())
	table = Table(title = "[blink2 bold dodger_blue1]Holidays List", show_lines=True)
	table.add_column("[dark_orange]Date", justify = "center", style = "yellow3", no_wrap = True)
	table.add_column("[dark_orange]Occasion", justify = "center", style = "yellow3", no_wrap = True)
	holidaysFlag = False
	for key in holidayListKeys:
		value = data["holidaysList"][key]
		l = [key, value]
		table.add_row(*l)
		holidaysFlag = True
	if holidaysFlag:
		console.print(table)
	else :
		console.print("You dont have any holidays", style = "bold gold1")

# reverts to the original timetable
def revertTimeTable():
	jsonData = fetchDataFromJSON('log.json')
	totalUpdates = len(list(jsonData["tempTimetableUpdate"].keys()))
	if totalUpdates > 0:
		for i in range(totalUpdates):
			day = jsonData["tempTimetableUpdate"][str(i)]["day"]
			period = jsonData["tempTimetableUpdate"][str(i)]["period"]
			classToUpdate = jsonData["tempTimetableUpdate"][str(i)]["previousClass"]
			updateTimeTable(day, period, classToUpdate)
		jsonData["tempTimetableUpdate"] = {}
		sendDataToJSON('log.json', jsonData)

# updates the time table by taking day, period and class to update
# day should be string of any format. eg: "Monday", "monday", "MONday"
# period should be passed as stored in excel sheet
# class that you want to replace with
# if you want to remove a class then just pass the class with ''
def updateTimeTable(day, period, classToUpdate = None, previousClass = False):
	classTimeTableLocation = data['dir']['classTimeTableLocation']
	timetablewb = openpyxl.load_workbook(classTimeTableLocation) 
	sheet = timetablewb.active
	day = day.lower()
	log = fetchDataFromJSON('log.json')
	i, val, asciiVal = 1, 2, 66
	rowValues, colValues, colDict = {}, {}, {}
	for key in list(log['completeTimeTable'].keys())[1:] :
		key = key.lower()
		rowValues[key] = str(val)
		colValues[key] = chr(asciiVal)
		colDict[str(i)] = key
		i += 1
		asciiVal += 1	
		val += 1	
	
	prevClass =  sheet[colValues[colDict[period]] + str(rowValues[day])].value
	sheet[colValues[colDict[period]] + str(rowValues[day])] = classToUpdate
	timetablewb.save(classTimeTableLocation)
	if previousClass:
		return prevClass
	
# prints log data
def printLog():
	logData = fetchDataFromJSON('log.json')
	print(json.dumps(logData, indent = 4))


# prints the arguments and their uses 
def helpFunction():
	table = Table(show_lines=True)
	table.add_column("Arguments", justify = "center", style = "yellow3", no_wrap = True)
	table.add_column("Details", justify = "center", style = "yellow3")
	table.add_row("no arguments", "runs the main program")
	table.add_row("--t", "displays todays timetable")
	table.add_row("--h", "displays holidays list")
	table.add_row("--c", "displays present class")
	table.add_row("--l", "uses class url to join the class immediately")
	table.add_row("--log", "displays log")
	table.add_row("--l 'time'", "uses class url to join the class and schedules at specified 'time'")
	table.add_row("--h -a", "add new holiday to the list and prints")
	table.add_row("--h -r", "removes holiday from the list and prints")
	table.add_row("--t -f", "displays complete timetable fetched from excel sheet")
	table.add_row("--t -u", "changes timetable and displays complete timetable fetched from excel sheet")
	table.add_row("--t -ut", "changes timetable temporarily and updates back the original timetable next time")
	console.print(table)

# returns the count of members joined before joining the class
def membersAlreadyJoinedCount(text):
	if text == 'No one else is here':
		return 0
	count = 0
	numberFromText = [int(i) for i in text.split() if i.isdigit()]
	commasCount = text.count(',')
	andCount = text.count('and')
	if len(numberFromText) > 0:
		count = numberFromText[0]
		andCount = 0
	count = count + commasCount + andCount + 1
	return count

# joins the class of given subject
def joinClass(driver, subject = None, URL = None, loginTime = None):
	wait = WebDriverWait(driver, 1800)
	if URL == None:
		# used when we want to implicitly wait 
		# time = 1800/60 = 30 minutes
		log = {}
		subject = subject.upper()
		url = data['classroomLinks'][subject]
		print('Opening ' + subject + ' classroom in new tab' )
		driver.get(url)
		richStatus(sleepTime = 5)
		print('Waiting for Google Meet link for ' + subject + ' class')
		usedPrintInSameLine = False
		linkPostedSeperatelyInAnnouncementTab = data['otherData']['linkPostedSeperatelyInAnnouncementTab']
		# if subject link is posted seperately in announcement tab
		if subject in linkPostedSeperatelyInAnnouncementTab:	
			print(subject + ' class Link is posted in announcement tab')
			print('So trying to fetch data from announcement tab')
			previousPostData = None
			while True:
				# from the below fetched data
				# check the date is matching before joining
				# if the link is posted today, then the element stores the time for eg: "12.06 AM"
				# if the link is not posted today, then element stores the day for eg: "May 11"
				announcementTabData = str(driver.find_element_by_class_name(classroomPostClass).text)
				announcementTabpostedDateTime = str(driver.find_element_by_xpath(dateTimeInCommentsXPath).text)
				if previousPostData != announcementTabData :
					print('\n' + color.BOLD +'Fetched Data' + color.END + '\n')
					print(color.BOLD + color.YELLOW + announcementTabData + color.END + '\n')
				previousPostData = announcementTabData
				# fetching url from annoucement tab data
				# until url is fetched, the page loads for every 10 seconds
				classURL = re.search("(?P<url>https?://[^\s]+)", announcementTabData).group("url")
				if not announcementTabpostedDateTime[8].isalpha():
					if (classURL[:24] == 'https://meet.google.com/') :
						print('Fetched class link from the google classroom')
						print('Opening ', classURL)
						driver.get(classURL)
						richStatus(sleepTime = 5)
						break
					else:
						print('Fetching link failed or link not posted')
				else :
					driver.refresh()
					printInSameLine(str1 = 'Waiting for Todays link. Trying again in ', str2 = ' seconds', isChar = False, seconds = True)
					usedPrintInSameLine = True
		# fetches data from link posted in google classroom
		# if link is not available and it loads and check for every 10 seconds
		else :
			while True:
				try:
					classData = driver.find_element_by_class_name(meetLinkClass).text
					classURL = re.search("(?P<url>https?://[^\s]+)", classData).group("url")
					if classURL[:24] == 'https://meet.google.com/':
						if usedPrintInSameLine == True:
							printInSameLine(newLine = True)
						print('Fetched class link from the google classroom')
						print('Opening ', classURL)
						driver.get(classURL)
						print('Opened meet link')
						richStatus(sleepTime = 5)
						break
				except AttributeError:
					print('Meet link not available to fetch.')
					driver.refresh()
					printInSameLine(str1 = 'Trying again in ', str2 = ' seconds', isChar = False, seconds = True)
					usedPrintInSameLine = True
	else:
		if loginTime == None:
			print('Opening ', URL)
			driver.get(URL)
			print('Opened meet link')
			richStatus(sleepTime = 5)
		else:
			dateAndTime = datetime.now()
			currentTime = dateAndTime.time()
			currentTime = str(currentTime)[:5]
			timeLeftForNextClass = subtractTime(loginTime, currentTime)
			hours, minutes = timeLeftForNextClass.split(':')
			sleepTimeForNextClass = int(hours) * 60 + int(minutes)
			printInSameLine(str1 = 'Class is scheduled successfully. Will join the class in ', str2 = ' seconds', isChar = False, seconds = True, sleepTime = sleepTimeForNextClass, color = "bold red", minutes = True)
			print(' ' * 100)
			print('Opening ', URL)
			driver.get(URL)
			print('Opened meet link')
			richStatus(sleepTime = 5)


	print('Pressing dismiss button')
	warningDismiss = driver.find_element_by_xpath(warningDismissButton).click()
	time.sleep(3)
	# fetching count of members already joined
	# if members count is not available then is sets the  minCountToJoinConsidered to False
	try :
		membersCountBeforeJoiningData = driver.find_element_by_class_name(membersCountBeforeJoiningClass).text
		print('\n' + color.BOLD + color.YELLOW + str(membersCountBeforeJoiningData) + color.END + '\n')
		joinedMembers = membersAlreadyJoinedCount(membersCountBeforeJoiningData)
		minCountToJoinConsidered = True
		minCountToJoin = data['otherData']['minCountToJoin']
	except NoSuchElementException:
		#messageAboveJoinButtonData = driver.find_element_by_class_name(messageAboveJoinButtonClass).text
		print("Members count not available! So joining the class without considering 'minCountToJoin'")
		minCountToJoinConsidered = False
	usedPrintInSameLine = False
	# checking for minCountToJoin to join the class
	while True:
		if not minCountToJoinConsidered:
			break
		if joinedMembers >= minCountToJoin: 
			if usedPrintInSameLine == True:
				printInSameLine(newLine = True)
			print('More than ' + str(minCountToJoin) + ' members already joined')
			print('Joining the class now')
			break
		else :
			if joinedMembers == 0:
				printInSameLine(str1 = 'No one joined. Trying again in ', str2 = ' seconds', isChar = False, seconds = True)
				usedPrintInSameLine = True
			else :
				if usedPrintInSameLine == True:
					printInSameLine(newLine = True)
				print('Only ' + str(joinedMembers) + ' joined')
				print('Waiting for ' + str(minCountToJoin - joinedMembers) + ' more students to join the class')
				printInSameLine(str1 = 'Trying again in ', str2 = ' seconds', isChar = False, seconds = True)
				usedPrintInSameLine = True
				membersCountBeforeJoiningData = driver.find_element_by_class_name(membersCountBeforeJoiningClass).text
				joinedMembers = membersAlreadyJoinedCount(membersCountBeforeJoiningData)
	# waits until join button is clickable
	element = wait.until(EC.element_to_be_clickable((By.XPATH, joinButtonXPath)))
	element.click()
	print('Pressing join button')
	# waits until caption button is clickable and turn on captions
	element = wait.until(EC.element_to_be_clickable((By.XPATH, captionsButtonXPath)))
	element.click()
	print('Turning on captions')
	alertSound(frequency = False)
	if URL == None:
		# sending class joining time to discord
		discord("Joined " + subject + " class at " + str(datetime.now().time())[:8])
		classTime = whichClass(currentClassTime = True)[0]
		joiningLeavingTimeDict = {}
		joiningLeavingTimeDict["joining time"] = str(datetime.now().time())
		if classTime in log:
			log[classTime].update(joiningLeavingTimeDict)
		else :
			log[classTime] = joiningLeavingTimeDict
		logData = fetchDataFromJSON('log.json')
		logData["log"]["joiningLeavingTime"].update(log)
		sendDataToJSON('log.json', logData)
		time.sleep(3)

	else :
		# sending class joining time to discord
		discord('Joined the class with ' + URL + ' successfully at ' + str(datetime.now().time())[:8])
	# counting number of students joined 
	count = driver.find_element_by_xpath(membersCountXPath).text
	flag = False
	minCountToLeave = data['otherData']['minCountToLeave']
	alertWords = data['otherData']['alertWords']
	autoReply = data['otherData']['autoReply']
	logData = fetchDataFromJSON('log.json')
	# Reads the text from captions until str(count) > minCountToLeave:
	while True:
		wait.until(EC.visibility_of_element_located((By.XPATH, membersCountXPath)))
		count = driver.find_element_by_xpath(membersCountXPath).text
		printInSameLine('Members Count: ', count, sleepTime = 0, isChar = False)
		try:
			# flag is used to check when class count reaches above minCountToLeave
			# when it is set to true it implies that it is waiting to leave the class when count reaches below minCountToLeave
			if count > str(minCountToLeave):
				flag = True
			elems = driver.find_element_by_class_name(captionsXPath)
			captionTextLower = str(elems.text).lower()
			# if alert word is found in captions then it plays an alert sound for soundFrequency times and then sends alert message to discord
			# if you want to enable auto replay when this triggers then uncomment the line below. This sends the response message that is given in data.json file
			for word in alertWords:
				if word in captionTextLower:
					discord("ALERT! Some one called you at " + str(datetime.now().time())[:8])
					discord(captionTextLower)
					discord("Triggered word: " + word)
					print("Triggered word: " + word)
					printInSameLine(newLine = True)
					print(text2art("ALERT", font = "small")) 
					alertSound() # alert sound for soundCount times
					if autoReply:
						responseMessage = data['otherData']['responseMessage']
						sendMessageInChatBox(driver, responseMessage)	
			# leaves the class when class count is less than minCountToLeave
			if count < str(minCountToLeave) and flag :
				alertSound(frequency = False)
				if URL == None:
					discord("Left the " + subject + " class at " + str(datetime.now().time())[:8])
					joiningLeavingTimeDict["leaving time"] = str(datetime.now().time())
					log[classTime].update(joiningLeavingTimeDict)
					logData = fetchDataFromJSON('log.json')
					logData["log"]["joiningLeavingTime"].update(log)
					sendDataToJSON('log.json', logData)
					driver.close()
					richStatus(sleepTime = 5, statusMessage = 'Left '+ subject + ' class', color = "bright_yellow")
					console.print('\nLeft the class successfully', style = "bold red", end = '\r')	
					break
				else :
					discord('Left the class of url ' + URL + ' successfully at ' + str(datetime.now().time())[:8])
					driver.close()
					console.print('\nLeft the class successfully', style = "bold red")	
					break
				
					
		except (NoSuchElementException, StaleElementReferenceException):
			# flag is used to check when class count reaches above minCountToLeave
			# when it is set to true it implies that it is waiting to leave the class when count reaches below minCountToLeave
			if count > str(minCountToLeave):
				flag = True
			# leaves the class when class count is less than minCountToLeave
			if count < str(minCountToLeave) and flag :
				alertSound(frequency = False)
				if URL == None:
					discord("Left the " + subject + " class at " + str(datetime.now().time())[:8])
					joiningLeavingTimeDict["leaving time"] = str(datetime.now().time())
					log[classTime].update(joiningLeavingTimeDict)
					logData = fetchDataFromJSON('log.json')
					logData["log"]["joiningLeavingTime"].update(log)
					sendDataToJSON('log.json', logData)
					driver.close()
					richStatus(sleepTime = 5, statusMessage = 'Left '+ subject + ' class', color = "bright_yellow")
					console.print('\nLeft the class successfully', style = "bold red", end = '\r')
					break
				else :
					discord('Left the class of url ' + URL + ' successfully at ' + str(datetime.now().time())[:8])
					driver.close()
					console.print('\nLeft the class successfully', style = "blink2 bold red")
					break
				
				

# sends the message in chat box when alert word is triggered in captions
def sendMessageInChatBox(driver, message):
	driver.find_element_by_xpath(chatBoxButtonXPath).click()
	driver.implicitly_wait(10)
	time.sleep(1)
	chatBox = driver.find_element_by_xpath(chatBoxXPath)
	chatBox.send_keys(message)
	time.sleep(1)
	driver.find_element_by_xpath(chatSendButtonXPath).click()
	driver.implicitly_wait(10)
	time.sleep(1)
	driver.find_element_by_xpath(chatBoxCloseXPath).click()
	driver.implicitly_wait(10)
	print('Responded to the class by sending ', color.BOLD + message + color.END)
	richStatus(text = 'Message sent successfully', sleepTime = 10, spinnerType = 'point') 
	

# plays alert sound for soundFrequency times where soundFrequency is stored in data.json
def alertSound(frequency = True):
	if not windowsUser:
		beep = lambda x: os.system("echo -n '\a'; sleep 0.2;" * x)
		if frequency:
			soundFrequency = data['otherData']['soundFrequency']
			beep(soundFrequency)
			richStatus(text = 'Played alert sound successfully', sleepTime = 10, spinnerType = 'point') 	
		else:
			beep(2)

	else:
		if frequency:
			soundFrequency = data['otherData']['soundFrequency']
			for i in range(soundFrequency):
				winsound.Beep(1000, 1000)
				time.sleep(0.5)
			richStatus(text = 'Played alert sound successfully', sleepTime = 10, spinnerType = 'point') 	
		else:
			for i in range(2):
				winsound.Beep(1000, 1000)
				time.sleep(0.5)
	

# launches the chrome driver and opens google classroom if needed with loaded profile
def loadDriver(classroom = False):
	pathToChromeDriver = data['dir']['pathToChromeDriver']
	driver = webdriver.Chrome(options = chromeOptions, executable_path = pathToChromeDriver)
	driver.maximize_window()
	print('Disabled extensions')
	print('Turned off Location')
	console.print('Turned off Camera', style = "bold red")
	console.print('Turned off Microphone', style = "bold red")
	print('Turned off Pop-up')
	if classroom:
		driver.get('https://classroom.google.com')
		print('Opening Google Classroom')
		richStatus(sleepTime = 5)
	return driver

# used to login to gmail 
# not used here as we used chrome profile
def login():
	pathToChromeDriver = data['dir']['pathToChromeDriver']
	driver = webdriver.Chrome(options = chromeOptions, executable_path = pathToChromeDriver)
	driver.maximize_window()
	print('Disabled extensions')
	print('Turned off Location')
	console.print('Turned off Camera', style = "bold red")
	console.print('Turned off Microphone', style = "bold red")
	print('Turned off Pop-up')
	print('Logging into ' + color.BOLD + 'Google account' + color.END)
	driver.get('https://classroom.google.com/?emr=0')
	time.sleep(3)
	mailAddress = data['credentials']['mailAddress']
	password = data['credentials']['password']
	print('Entering mail address')
	mailBox = driver.find_element_by_xpath(mailBoxXPath)
	driver.implicitly_wait(10)
	mailBox.send_keys(mailAddress)
	driver.find_element_by_xpath(nextButtonXPath).click()
	driver.implicitly_wait(10)
	time.sleep(2)
	print(color.BOLD + 'Entering password' + color.END)
	passwordBox = driver.find_element_by_xpath(enterPasswordBoxXPath)
	driver.implicitly_wait(10)
	passwordBox.send_keys(password)
	driver.find_element_by_xpath(passwordNextButtonXPath).click()
	driver.implicitly_wait(10)
	time.sleep(2)
	printInSameLine(sleepTime = 10)
	print('Login Successful')
	return driver

# sends message to discord
def discord(message):
	url = data['credentials']['discordURL']
	Message = {
		"content": message
	}
	requests.post(url, data = Message)
