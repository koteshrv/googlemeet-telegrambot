from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from rich.console import Console
from selenium import webdriver
from datetime import datetime
from art import *
import openpyxl
import calendar
import pandas
import cursor
import json
import time
import os
import re

def fetchDataFromJSON(fileName):
	with open(fileName) as file:
		data = json.load(file)
	return data

def sendDataToJSON(fileName, data):
	with open(fileName, 'w') as file:
		json.dump(data, file, indent = 4)

data = fetchDataFromJSON('data.json')
profilePath = data['dir']['profilePath']

console = Console()
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

mailBoxXPath = '//*[@id="identifierId"]'
nextButtonXPath = '//*[@id="identifierNext"]/div/button'
enterPasswordBoxXPath = '//*[@id="password"]/div[1]/div/div[1]/input'
passwordNextButtonXPath = '//*[@id="passwordNext"]/div/button/div[2]'
meetLinkXPath = '//*[@id="yDmH0d"]/div[4]/div[3]/div/div[1]/div/div[2]/div[2]/div/span/a'
meetLinkInCommentsXPath = '//*[@id="ow43"]/div[2]/div/div[1]/div[2]/div[1]/html-blob/span/a[1]'
classroomPostClass = 'n8F6Jd'
meetLinkClass = 'qyN25' 
warningDismissButton = '//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div/span/span'
membersCountBeforeJoiningClass = 'Yi3Cfd'
joinButtonXPath = '//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span/span'
captionsButtonXPath = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[9]/div[3]/div[2]/div/span/span/div/div[1]/i'
captionsXPath = 'VbkSUe'
membersCountXPath = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[1]/div[3]/div/div[2]/div[1]/span/span/div/div/span[2]'
chatBoxButtonXPath = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[1]/div[3]/div/div[2]/div[3]/span/span'
chatBoxXPath = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[4]/div/div[2]/div[2]/div[2]/span[2]/div/div[4]/div[1]/div[1]/div[2]/textarea'
chatSendButtonXPath = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[4]/div/div[2]/div[2]/div[2]/span[2]/div/div[4]/div[2]/span/span'
chatBoxCloseXPath = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[4]/div/div[2]/div[1]/div[2]/div/span/button/i'			


def toBold(str):
	boldedString = "\033[1m" + str + "\033[0m"
	return boldedString

def richStatus(text = 'Loading...', sleepTime = 10, spinnerType = 'dots', statusMessage = 'Done'):
	with console.status("[bold white] " + text, spinner = spinnerType) as status:
		time.sleep(sleepTime)
	console.print('[bold][green]' + statusMessage)

def printInSameLine(str1 = 'Loading', str2 = '.', sleepTime = 10, isChar = True, newLine = False, seconds = False):
	if newLine:
		print()
		return
	sec = sleepTime
	s = ' ' * 40
	for x in range (0, int(sleepTime) + 1): 
		b = str1 + (str(sec - x) if seconds else '') +  str(str2) * (x if isChar else 1)
		print(s, end = '\r')
		console.print(b, end = '\r', style = "bold green")
		if sleepTime > 0:
			time.sleep(1)
		s = ' ' * len(b) 
	if isChar:
		print('')

def findDay():
	dateAndTime = datetime.now()
	date = str(dateAndTime.day) + ' ' + str(dateAndTime.month) + ' ' + str(dateAndTime.year)
	date = datetime.strptime(date, '%d %m %Y').weekday()
	return date


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


def holidaysList(key = None, value = None):
	holidaysDict = {}
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
	jsonData = fetchDataFromJSON('log.json')
	jsonData["holidaysList"].update(holidaysDict)
	sendDataToJSON('log.json', jsonData)

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


def loadTodayClasses():
	loadTimeTable()
	date = findDay()
	classes = []
	holidaysList()
	jsonData = fetchDataFromJSON('log.json')
	holidays = jsonData["holidaysList"]
	dateAndTime = datetime.now()
	day = dateAndTime.day
	weekDay = dateAndTime.today().strftime('%A')
	weekDay = 'Monday'
	day = 11
	if str(day) in holidays:
		print("Today is a holiday due to ", holidays[str(day)])
	else:
		classesToday = jsonData["completeTimeTable"][weekDay]
		timings = jsonData["completeTimeTable"]["Timings"]
		timings = timings[:len(classesToday)]

		classes = []
		classtime = []

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
	jsonData["todaysTimeTable"] = t
	sendDataToJSON('log.json', jsonData)

	currentTime = dateAndTime.time()
	print('\t' + toBold('Current time: ') + toBold(str(time))[:12])
	time = str(time).split(":")

	for i in range(len(classtime)):
		if (time[0] >= classtime[i][0:2] and time[1] >= classtime[i][3:5]) and (time[0] < classtime[i][8:10] and time[1] <= '59'): #i[14:16]
			print('\n' + '\t' + toBold(classtime[i]) + ' ' + toBold(classes[i]))
		else:
			print('\n' + '\t' + classtime[i] + ' ' + classes[i])
	print('\n')



def whichClass() :
	jsonData = fetchDataFromJSON('log.json')
	subjects = jsonData["todaysTimeTable"]
	for i in subjects:
		time = datetime.now().time()
		time = str(time).split(":")
		if (time[0] >= i[0:2] and time[1] >= i[3:5]) and (time[0] < i[8:10] and time[1] <= '59'):
			return i[17:]		

	return None

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


def joinClass(subject, driver):
	subject = subject.upper()
	url = data['classroomLinks'][subject]
	print('Opening ' + subject + ' classroom in new tab' )
	driver.execute_script("window.open('');")
	driver.switch_to.window(driver.window_handles[1])
	driver.get(url)
	#printInSameLine(sleepTime = 5) #prints loading line by default
	richStatus(sleepTime = 5)
	print('Waiting for Google Meet link for ' + subject + ' class')

	usedPrintInSameLine = False
	linkPostedSeperatelyInAnnouncementTab = data['otherData']['linkPostedSeperatelyInAnnouncementTab']

	if subject in linkPostedSeperatelyInAnnouncementTab:	
		previousPostData = None
		while True:
			#From the below fetched data check the date is matching before joining
			announcementTabData = str(driver.find_element_by_class_name(classroomPostClass).text)
			if previousPostData != announcementTabData :
				print('Fetched Data \n')
				print(toBold(announcementTabData) + '\n')

			previousPostData = announcementTabData
			
			classURL = driver.find_element_by_xpath(meetLinkInCommentsXPath).text

			current_time = datetime.now() 

			# checking for date and month posted in announcementTabData
			if announcementTabData[9:11].lstrip('0') == str(current_time.day) and announcementTabData[12:14].lstrip('0') == str(current_time.month):
				if usedPrintInSameLine == True:
					printInSameLine(newLine = True)
				if (classURL[:24] == 'https://meet.google.com/') :
					print('Fetched ', classURL, 'from the google classroom')
					print('Opening ', classURL)
					driver.get(classURL)
					#printInSameLine(sleepTime = 5)
					richStatus(sleepTime = 5)
					break

				else:
					print('Fetching Link failed')
				
			else :
				driver.refresh()
				printInSameLine(str1 = 'Waiting for Todays link. Trying again in ', str2 = ' seconds', isChar = False, seconds = True)
				usedPrintInSameLine = True

	else :
		
		while True:
			try:
				if usedPrintInSameLine == True:
					printInSameLine(newLine = True)
				classData = driver.find_element_by_class_name(meetLinkClass).text
				classURL = re.search("(?P<url>https?://[^\s]+)", classData).group("url")
				print('classURL ', str(classURL))
				if classURL[:24] == 'https://meet.google.com/':
					print('Fetched ', classURL, 'from the google classroom')
					print('Opening ', classURL)
					driver.get(classURL)
					printInSameLine(sleepTime = 5)
					print('Opened meet link')
					#printInSameLine(str1 = 'Loading', sleepTime = 5)
					richStatus(sleepTime = 5)
					break
			except AttributeError:
				print('Meet link not available to fetch.')
				driver.refresh()
				printInSameLine(str1 = 'Trying again in ', str2 = ' seconds', isChar = False, seconds = True)
				usedPrintInSameLine = True


	print('Pressing dismiss button')
	warningDismiss = driver.find_element_by_xpath(warningDismissButton).click()
	time.sleep(3)

	membersCountBeforeJoiningData = driver.find_element_by_class_name(membersCountBeforeJoiningClass).text
	print('Members Joined\n')
	print(str(membersCountBeforeJoiningData), '\n')

	joinedMembers = membersAlreadyJoinedCount(membersCountBeforeJoiningData)

	usedPrintInSameLine = False
	minCountToJoin = data['otherData']['minCountToJoin']

	while True:
		if usedPrintInSameLine == True:
			printInSameLine(newLine = True)
		if joinedMembers >= minCountToJoin: 
			print('More than ' + str(minCountToJoin) + ' members already joined')
			print('Joining the class now')
			break
		else :
			if joinedMembers == 0:
				printInSameLine(str1 = 'No one joined. Trying again in ', str2 = ' seconds', isChar = False, seconds = True)
				usedPrintInSameLine = True
			else :
				print('Only ' + str(joinedMembers) + ' joined')
				print('Waiting for ' + str(minCountToJoin - joinedMembers) + ' more students to join the class')
				printInSameLine(str1 = 'Trying again in ', str2 = ' seconds', isChar = False, seconds = True)
				usedPrintInSameLine = True
				membersCountBeforeJoiningData = driver.find_element_by_class_name(membersCountBeforeJoiningClass).text
				joinedMembers = membersAlreadyJoinedCount(membersCountBeforeJoiningData)


	# clicks join button
	print('Pressing join button')
	join=driver.find_element_by_xpath(joinButtonXPath).click()
	time.sleep(3)


	# turn on captions
	print('Turning on captions')
	driver.find_element_by_xpath(captionsButtonXPath).click()
	time.sleep(4)

	# counting number of students joined 
	count = driver.find_element_by_xpath(membersCountXPath).text

	flag = False
	minCountToLeave = data['otherData']['minCountToLeave']
	alertWords = data['otherData']['alertWords']

	# Reads the text from captions str(count) > '30':
	while True:
		count = driver.find_element_by_xpath(membersCountXPath).text
		printInSameLine('Members Count: ', count, sleepTime = 0, isChar = False)
		try:
			if count > str(minCountToLeave):
				flag = True
			elems = driver.find_element_by_class_name(captionsXPath)
			captionTextLower = str(elems.text).lower()

			for word in alertWords:
				if word in captionTextLower:
					printInSameLine(newLine = True)
					print(text2art("ALERT", font = "small")) 
					alertSound() # alert sound for soundCount times
					#responseMessage = data['otherData']['responseMessage']
					#sendMessageInChatBox(driver, responseMessage)
					
			if count < str(minCountToLeave) and flag :
				print('\nExiting Class')
				driver.close()
				break


		except (NoSuchElementException, StaleElementReferenceException):
			if count > str(minCountToLeave):
				flag = True
			if count < str(minCountToLeave) and flag :
				console.print('\nExiting Class', style = "bold red")
				driver.close()
				#printInSameLine(sleepTime = 10)
				richStatus(sleepTime = 5, statusMessage = 'Left the class')
				break


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
	print('Responded to the class by sending ', toBold(responseMessage))
	richStatus(text = 'Message sent successfully', sleepTime = 10, spinnerType = 'point') 

	

def alertSound():
	beep = lambda x: os.system("echo -n '\a'; sleep 0.2;" * x)
	soundFrequency = data['otherData']['soundFrequency']
	beep(soundFrequency)
	print('Played alert sound successfully')
	richStatus(text = 'Played alert sound successfully', sleepTime = 10, spinnerType = 'point') 

def loadDriver():
	pathToChromeDriver = data['dir']['pathToChromeDriver']
	driver = webdriver.Chrome(options = chromeOptions, executable_path = pathToChromeDriver)

	print('Disabled extensions')
	print('Turned off Location')
	console.print('Turned off Camera', style = "bold red")
	console.print('Turned off Microphone', style = "bold red")
	print('Turned off Pop-up')

	driver.maximize_window()

	driver.get('https://classroom.google.com')
	#printInSameLine(sleepTime = 5)
	print('Opening Google Classroom')
	richStatus(sleepTime = 5)

	return driver

	
def login():
	pathToChromeDriver = data['dir']['pathToChromeDriver']
	driver = webdriver.Chrome(options = chromeOptions, executable_path = pathToChromeDriver)

	print('Disabled extensions')
	print('Turned off Location')
	console.print('Turned off Camera', style = "bold red")
	console.print('Turned off Microphone', style = "bold red")
	print('Turned off Pop-up')

	driver.maximize_window()

	print('Logging into ' + toBold('Google account'))
	
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

	print(toBold('Entering password'))
	passwordBox = driver.find_element_by_xpath(enterPasswordBoxXPath)
	driver.implicitly_wait(10)
	passwordBox.send_keys(password)
	driver.find_element_by_xpath(passwordNextButtonXPath).click()
	driver.implicitly_wait(10)
	time.sleep(2)

	printInSameLine(sleepTime = 10)
	print('Login Successful')

	return driver