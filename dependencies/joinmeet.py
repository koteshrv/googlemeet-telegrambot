from logging import exception
#from record import startRecording, stopRecording
from sys import executable
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from os import execl, execv
from sys import executable
import config, time, re, string
from datetime import datetime, timedelta
from art import *
from dependencies import driver
from dependencies.others import checklogin, data, sendTimetable, sendToTelegram
from dependencies.others import (Print, membersAlreadyJoinedCount,
						whichClass, fetchDataFromJSON, sendDataToJSON, setStatus,
						updateMembersCount, takeScreenshot, checkStatus, sendMessageInChatBox)


#classes and xpath of elements
meetLinkXPath = '//*[@id="yDmH0d"]/div[4]/div[3]/div/div[1]/div/div[2]/div[2]/div/span/a'
meetLinkInCommentsXPath = '//*[@id="ow45"]/div[2]/div[1]/div[1]/div[2]'
dateTimeInCommentsXPath = '//*[@id="ow45"]/div[2]/div[1]/div[1]/div[1]/div[1]/span/span[2]'
classroomPostClass = 'n8F6Jd'
meetLinkClass = 'qyN25' 
warningDismissButton = '//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div'
membersCountBeforeJoiningClass = 'Yi3Cfd'
messageAboveJoinButtonClass = 'JMAjle'
joinButtonXPath = '//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[4]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/span'
captionsButtonXPath = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[10]/div[2]/div/div[3]/div/span/button/span[2]'
captions = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[7]/div/div[2]/div'
membersCountXPath = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[10]/div[3]/div[2]/div/div/div[2]/div/div'
muteButtonXPath = '//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[4]/div/div/div[1]/div[1]/div/div[4]/div[1]/div/div/div/span/span'
videoButtonXPath = '//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[4]/div/div/div[1]/div[1]/div/div[4]/div[2]/div/div/span/span'
endButtonXPath = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[10]/div[2]/div/div[7]'
justLeaveTheClassXPath = '//*[@id="yDmH0d"]/div[3]/div/div[2]/div[2]/div[1]/span/span'
askToJoinButtonXPath = "//span[@class='NPEfkd RveJvd snByac' and contains(text(), 'Ask to join')]"
joinNowButtonXPath = "//span[@class='NPEfkd RveJvd snByac' and contains(text(), 'Join now')]"
joinButtonXPath = '//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[4]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/span/span'
chatBoxButtonXPath = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[10]/div[3]/div[2]/div/div/div[3]/span/button/i[1]'

joinError = False

# joins the class of given subject
def joinMeet(subject = None, URL = None, loginTime = None):
	if checklogin():
		return
	try:
		# url or subject is given to joinClass
		if URL == None:
			log = {}
			subject = subject.upper()
			url = data['classroomLinks'][subject]
			Print('Opening ' + subject + ' classroom in new tab')
			driver.get(url)
			time.sleep(5)
			Print('Waiting for Google Meet link for ' + subject + ' class')
			linkPostedSeperatelyInAnnouncementTab = data['otherData']['linkPostedSeperatelyInAnnouncementTab']
			# checking if the subject link is posted seperately in announcement tab
			if subject in linkPostedSeperatelyInAnnouncementTab:	
				Print(subject + ' class Link is posted in announcement tab')
				Print('So trying to fetch data from announcement tab')
				previousPostData = None
				while True:
					# from the below fetched data
					# check the date is matching before joining
					# if the link is posted today, then the element stores the time for eg: "12.06 AM"
					# if the link is not posted today, then element stores the day for eg: "May 11"
					while True:
						try:
							announcementTabData = str(driver.find_element_by_class_name(classroomPostClass).text)
							announcementTabpostedDateTime = str(driver.find_element_by_xpath(dateTimeInCommentsXPath).text)
							break
						except Exception as e:
							Print('Exception occured when trying to fetch data. So trying again in 30 seconds')
							Print(str(e))
							time.sleep(30)
					if previousPostData != announcementTabData :
						Print('Fetched Data')
						Print(announcementTabData)
						Print(announcementTabpostedDateTime)
					previousPostData = announcementTabData
					# fetching url from annoucement tab data
					# until url is fetched, the page loads for every 10 seconds
					classURL = re.search("(?P<url>https?://[^\s]+)", announcementTabData).group("url")
					# if the link is posted today it will contain time when posted
					if not announcementTabpostedDateTime[0].isalpha():
						if (classURL[:24] == 'https://meet.google.com/') :
							Print('Fetched class link from the google classroom')
							Print('Opening ' + classURL)
							driver.get(classURL)
							time.sleep(5)
							break
						else:
							Print('Fetching link failed or link not posted in announcement section')
							sendToTelegram('Fetching link failed or link not posted in announcement section')
							return
					else :
						driver.refresh()
						Print('Waiting for Todays link. Trying again in 10 seconds')
						time.sleep(10)

			# fetches data from link posted in google classroom
			# if link is not available and it loads and check for every 10 seconds
			else :
				try:
					classData = driver.find_element_by_class_name(meetLinkClass).text
					classURL = re.search("(?P<url>https?://[^\s]+)", classData).group("url")
					if classURL[:24] == 'https://meet.google.com/':
						Print('Fetched class link from the google classroom')
						Print('Opening ' + classURL)
						driver.get(classURL)
						Print('Opened meet link')
						time.sleep(5)
				except AttributeError:
					sendToTelegram('Meet link not available to fetch. Trying again in 10 seconds')
					Print('Meet link not available to fetch. Trying again in 10 seconds')
					driver.refresh()
					time.sleep(10)

		else:
			# if loginTime is None then it joins immediately else it waits till that time
			if loginTime == None:
				print('[' + str(datetime.now().strftime("%H:%M:%S")) + '] ' + 'Opening ', URL)
				driver.get(URL)
				time.sleep(5)
				
			else:
				h, m, s = str(datetime.now().time()).split(':')
				presentTime = timedelta(hours = int(h), minutes = int(m), seconds = int(float(s)))
				timeLeftForNextClass = (timedelta(hours = int(loginTime[:2]), minutes = int(loginTime[-2:])) - presentTime).total_seconds()
				Print('Class is scheduled successfully. Will join the class in ' + str(timedelta(seconds = timeLeftForNextClass)))
				sendToTelegram('Class is scheduled successfully. Will join the class in ' + str(timedelta(seconds = timeLeftForNextClass)))
				time.sleep(timeLeftForNextClass)
				Print('Opening ' + URL)
				driver.get(URL)
				Print('Opened meet link')
				time.sleep(5)
		
		dismissButtonPressed = False
		try:
			# pressing dismiss missing of permissions warning
			Print('Pressing dismiss button')
			dismissButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, warningDismissButton)))
			dismissButton.click()
			time.sleep(3)
			dismissButtonPressed = True
		except:
			pass

		if not dismissButtonPressed:
			try:
				muteButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, muteButtonXPath)))
				muteButton.click()
				videoButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, videoButtonXPath)))
				videoButton.click()

			except Exception as e:
				sendToTelegram(e)
				sendToTelegram('Unable to turn off audio and video')
				Print('Unable to turn off audio and video')
				return
		
		# fetching count of members already joined
		# if members count is not available then is sets the  minCountToJoinConsidered to False
		try :
			membersCountBeforeJoiningData = driver.find_element_by_class_name(membersCountBeforeJoiningClass).text
			Print(str(membersCountBeforeJoiningData))
			joinedMembers = membersAlreadyJoinedCount(membersCountBeforeJoiningData)
			minCountToJoinConsidered = True
			minCountToJoin = data['otherData']['minCountToJoin']

		except NoSuchElementException:
			Print("Members count not available! So joining the class without considering 'minCountToJoin'")
			minCountToJoinConsidered = False

		# checking for minCountToJoin to join the class
		while True:
			if not minCountToJoinConsidered:
				break
			if joinedMembers >= minCountToJoin: 
				Print('More than ' + str(minCountToJoin) + ' members already joined')
				Print('Joining the class now')
				break
			else :
				if joinedMembers == 0:
					Print('No one joined. Will try for every 10 seconds')
					sendToTelegram('No one joined. Will try for every 10 seconds')
					time.sleep(10)

				else :
					Print('Only ' + str(joinedMembers) + ' joined')
					Print('Waiting for ' + str(minCountToJoin - joinedMembers) + ' more students to join the class')
					Print('Trying again in 10 seconds')
					sendToTelegram('Only ' + str(joinedMembers) + ' joined')
					sendToTelegram('Waiting for ' + str(minCountToJoin - joinedMembers) + ' more students to join the class')
					sendToTelegram('Trying again in 10 seconds')
					time.sleep(10)
					membersCountBeforeJoiningData = driver.find_element_by_class_name(membersCountBeforeJoiningClass).text
					joinedMembers = membersAlreadyJoinedCount(membersCountBeforeJoiningData)
		

		try:
			#try:
			#	askToJoinButton = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, askToJoinButtonXPath)))
			#	askToJoinButton.click()
			#except:
			joinNowButton = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, joinButtonXPath)))
			joinNowButton.click()	
		except Exception as e:
			sendToTelegram(str(e))
			sendToTelegram('Unexcepted error occured when trying to join the class\n So join again')
			Print(str(e))
			Print('Unexcepted error occured when trying to join the class\n So join again')
			if URL == None:
				joinError = True
			return

		time.sleep(10)
		Print('Pressing join button')

		try:
			# waits until caption button is clickable and turn on captions
			captionsButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, captionsButtonXPath)))
			captionsButton.click()
			Print('Turning on captions')
		except:
			Print('Unable to turn on captions. So alert will not work :/')
			sendToTelegram('Unable to turn on captions. So alert will not work :/')

		if URL == None:
			# sending class joining time to discord
			Print("Joined " + subject + " class at " + str(datetime.now().time())[:8])
			sendToTelegram("Joined " + subject + " class at " + str(datetime.now().time())[:8])
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
			Print('Joined the class with ' + URL + ' successfully')
			sendToTelegram('Joined the class with ' + URL + ' successfully')
		
		# counting number of students joined 
		count = driver.find_element_by_xpath(membersCountXPath).text
		flag = False
		minCountToLeave = data['otherData']['minCountToLeave']
		alertWords = data['otherData']['alertWords']
		autoReply = data['otherData']['autoReply']
		logData = fetchDataFromJSON('log.json')

		setStatus("meetAlive")
		meetAlive = checkStatus("meetAlive")

		driver.find_element_by_xpath(chatBoxButtonXPath).click()
		driver.implicitly_wait(10)
		time.sleep(1)

		# Reads the text from captions until str(count) > minCountToLeave:
		while True:
			
			meetAlive = checkStatus("meetAlive")

			try:
				count = driver.find_element_by_xpath(membersCountXPath).text
				updateMembersCount(count)

			except Exception as e:
				Print(str(e))
				Print('So auto exit will not work :/')
				sendToTelegram(str(e))
				sendToTelegram('So auto exit will not work :/')
			
			try:
				# flag is used to check when class count reaches above minCountToLeave
				# when it is set to true it implies that it is waiting to leave the class when count reaches below minCountToLeave
				if count > str(minCountToLeave):
					flag = True

				elems = driver.find_element_by_xpath(captions)
				captionTextLower = str(elems.text).translate(str.maketrans('', '', string.punctuation)).lower()
				# if alert word is found in captions then it plays an alert sound for soundFrequency times and then sends alert message to discord
				# if you want to enable auto replay when this triggers then uncomment the line below. This sends the response message that is given in data.json file
				for word in alertWords:
					if word in captionTextLower:
						print(text2art("ALERT", font = "small")) 
						sendToTelegram("ALERT! Some one called you at " + str(datetime.now().time())[:8])
						sendToTelegram(captionTextLower)
						sendToTelegram("Triggered word: " + word)
						takeScreenshot()
						Print("ALERT! Some one called you at " + str(datetime.now().time())[:8])
						Print(captionTextLower)
						Print("Triggered word: " + word)
						if autoReply:
							responseMessage = data['otherData']['responseMessage']
							sendMessageInChatBox(driver, responseMessage)	
						time.sleep(10)	

				if (count < str(minCountToLeave) and flag) or (not meetAlive):

					#if url is none then update log
					if URL == None:
						joiningLeavingTimeDict["leaving time"] = str(datetime.now().time())
						log[classTime].update(joiningLeavingTimeDict)
						logData = fetchDataFromJSON('log.json')
						logData["log"]["joiningLeavingTime"].update(log)
						sendDataToJSON('log.json', logData)
						while True:
							try:
								endButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, endButtonXPath)))
								endButton.click()
								try:
									driver.find_element_by_xpath(justLeaveTheClassXPath).click()
								except:
									pass
								break
							except Exception as e:
								Print(str(e))
								sendToTelegram('Failed to leave the class. Help me ASAP')
								Print('Failed to leave the class. Help me ASAP')
						updateMembersCount(None)
						time.sleep(5)
						print('Left '+ subject + ' class')
						Print('Left the class successfully')	
						sendToTelegram('Left the class successfully')
					else :
						while True:
							try:
								endButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, endButtonXPath)))
								endButton.click()
								try:
									driver.find_element_by_xpath(justLeaveTheClassXPath).click()
								except:
									pass
								break
							except Exception as e:
								Print(str(e))
								Print('Failed to leave the class. Help me ASAP')
								sendToTelegram(str(e))
								sendToTelegram('Failed to leave the class. Help me ASAP')
						updateMembersCount(None)
						Print('Left the class successfully')	
						sendToTelegram('Left the class successfully')
					setStatus("membersCount", None)
					break
					
						
			except (NoSuchElementException, StaleElementReferenceException):
				# flag is used to check when class count reaches above minCountToLeave
				# when it is set to true it implies that it is waiting to leave the class when count reaches below minCountToLeave
				if count > str(minCountToLeave):
					flag = True

				if (count < str(minCountToLeave) and flag) or (not meetAlive):

					#if url is none then update log
					if URL == None:
						joiningLeavingTimeDict["leaving time"] = str(datetime.now().time())
						log[classTime].update(joiningLeavingTimeDict)
						logData = fetchDataFromJSON('log.json')
						logData["log"]["joiningLeavingTime"].update(log)
						sendDataToJSON('log.json', logData)
						while True:
							try:
								endButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, endButtonXPath)))
								endButton.click()
								try:
									driver.find_element_by_xpath(justLeaveTheClassXPath).click()
								except:
									pass
								break
							except Exception as e:
								Print(str(e))
								Print('Failed to leave the class. Help me ASAP')
								sendToTelegram(str(e))
								sendToTelegram('Failed to leave the class. Help me ASAP')
						updateMembersCount(None)
						time.sleep(5)
						print('Left '+ subject + ' class')
						Print('Left the class successfully')	
						sendToTelegram('Left the class successfully')
					else :
						while True:
							try:
								endButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, endButtonXPath)))
								endButton.click()
								try:
									driver.find_element_by_xpath(justLeaveTheClassXPath).click()
								except:
									pass
								break
							except Exception as e:
								Print(str(e))
								Print('Failed to leave the class. Help me ASAP')
								sendToTelegram(str(e))
								sendToTelegram('Failed to leave the class. Help me ASAP')
						updateMembersCount(None)
						Print('Left the class successfully')	
						sendToTelegram('Left the class successfully')
					setStatus("membersCount", None)
					break

					

	except Exception as e:

		try:
			endButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, endButtonXPath)))
			endButton.click()
			driver.find_element_by_xpath(justLeaveTheClassXPath).click()
		except:
			pass

		driver.quit()
		takeScreenshot()
		Print('Unexpected error occurred! Fix the error ASAP and try again!')
		Print(str(e))
		sendToTelegram("Unexpected error occurred! Fix the error ASAP and try again!")
		sendToTelegram(str(e))

		execl(executable, executable, "telegrambot.py")
