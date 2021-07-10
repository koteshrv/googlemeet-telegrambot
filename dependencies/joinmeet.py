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
from dependencies.others import (discordAndPrint, membersAlreadyJoinedCount,
						whichClass, fetchDataFromJSON, sendDataToJSON, setStatus,
						updateMembersCount, takeScreenshot, checkStatus, sendMessageInChatBox)


#classes and xpath of elements
meetLinkXPath = '//*[@id="yDmH0d"]/div[4]/div[3]/div/div[1]/div/div[2]/div[2]/div/span/a'
meetLinkInCommentsXPath = '//*[@id="ow43"]/div[2]/div/div[1]/div[2]/div[1]/html-blob/span/a[1]'
dateTimeInCommentsXPath = '//*[@id="ow46"]/div[2]/div[1]/div[1]/div[1]/div[1]/span/span[2]'
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

# joins the class of given subject
def joinMeet(context, subject = None, URL = None, loginTime = None):
	checklogin(context)
	try:
		# url or subject is given to joinClass
		if URL == None:
			log = {}
			subject = subject.upper()
			url = data['classroomLinks'][subject]
			discordAndPrint('Opening ' + subject + ' classroom in new tab')
			driver.get(url)
			time.sleep(5)
			discordAndPrint('Waiting for Google Meet link for ' + subject + ' class')
			linkPostedSeperatelyInAnnouncementTab = data['otherData']['linkPostedSeperatelyInAnnouncementTab']
			# checking if the subject link is posted seperately in announcement tab
			if subject in linkPostedSeperatelyInAnnouncementTab:	
				discordAndPrint(subject + ' class Link is posted in announcement tab')
				discordAndPrint('So trying to fetch data from announcement tab')
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
							discordAndPrint('Exception occured when trying to fetch data. So trying again in 30 seconds')
							discordAndPrint(str(e))
							time.sleep(30)
					if previousPostData != announcementTabData :
						discordAndPrint('Fetched Data')
						discordAndPrint(announcementTabData)
						discordAndPrint(announcementTabpostedDateTime)
					previousPostData = announcementTabData
					# fetching url from annoucement tab data
					# until url is fetched, the page loads for every 10 seconds
					classURL = re.search("(?P<url>https?://[^\s]+)", announcementTabData).group("url")
					# if the link is posted today it will contain time when posted
					if not announcementTabpostedDateTime[0].isalpha():
						if (classURL[:24] == 'https://meet.google.com/') :
							discordAndPrint('Fetched class link from the google classroom')
							discordAndPrint('Opening ' + classURL)
							driver.get(classURL)
							time.sleep(5)
							break
						else:
							discordAndPrint('Fetching link failed or link not posted')
							return
					else :
						driver.refresh()
						discordAndPrint('Waiting for Todays link. Trying again in 10 seconds')
						time.sleep(10)

			# fetches data from link posted in google classroom
			# if link is not available and it loads and check for every 10 seconds
			else :
				try:
					classData = driver.find_element_by_class_name(meetLinkClass).text
					classURL = re.search("(?P<url>https?://[^\s]+)", classData).group("url")
					if classURL[:24] == 'https://meet.google.com/':
						discordAndPrint('Fetched class link from the google classroom')
						discordAndPrint('Opening ' + classURL)
						driver.get(classURL)
						discordAndPrint('Opened meet link')
						time.sleep(5)
				except AttributeError:
					discordAndPrint('Meet link not available to fetch. Trying again in 10 seconds')
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
				discordAndPrint('Class is scheduled successfully. Will join the class in ' + str(timedelta(seconds = timeLeftForNextClass)))
				time.sleep(timeLeftForNextClass)
				discordAndPrint('Opening ' + URL)
				driver.get(URL)
				discordAndPrint('Opened meet link')
				time.sleep(5)
		
		dismissButtonPressed = False
		try:
			# pressing dismiss missing of permissions warning
			discordAndPrint('Pressing dismiss button')
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
				sendToTelegram(context, e)
				sendToTelegram(context, 'Unable to turn off audio and video')
				discordAndPrint('Unable to turn off audio and video')
		
		# fetching count of members already joined
		# if members count is not available then is sets the  minCountToJoinConsidered to False
		try :
			membersCountBeforeJoiningData = driver.find_element_by_class_name(membersCountBeforeJoiningClass).text
			discordAndPrint(str(membersCountBeforeJoiningData))
			joinedMembers = membersAlreadyJoinedCount(membersCountBeforeJoiningData)
			minCountToJoinConsidered = True
			minCountToJoin = data['otherData']['minCountToJoin']

		except NoSuchElementException:
			discordAndPrint("Members count not available! So joining the class without considering 'minCountToJoin'")
			minCountToJoinConsidered = False

		# checking for minCountToJoin to join the class
		while True:
			if not minCountToJoinConsidered:
				break
			if joinedMembers >= minCountToJoin: 
				discordAndPrint('More than ' + str(minCountToJoin) + ' members already joined')
				discordAndPrint('Joining the class now')
				break
			else :
				if joinedMembers == 0:
					discordAndPrint('No one joined. Will try for every 10 seconds')
					time.sleep(10)

				else :
					discordAndPrint('Only ' + str(joinedMembers) + ' joined')
					discordAndPrint('Waiting for ' + str(minCountToJoin - joinedMembers) + ' more students to join the class')
					discordAndPrint('Trying again in 10 seconds')
					time.sleep(10)
					membersCountBeforeJoiningData = driver.find_element_by_class_name(membersCountBeforeJoiningClass).text
					joinedMembers = membersAlreadyJoinedCount(membersCountBeforeJoiningData)

		try:
			askToJoinButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, askToJoinButtonXPath)))
			askToJoinButton.click()
		except:
			joinNowButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, joinNowButtonXPath)))
			joinNowButton.click()		
		time.sleep(10)
		discordAndPrint('Pressing join button')

		try:
			# waits until caption button is clickable and turn on captions
			captionsButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, captionsButtonXPath)))
			captionsButton.click()
			discordAndPrint('Turning on captions')
		except:
			discordAndPrint('Unable to turn on captions')
			sendToTelegram(context, 'Unable to turn on captions')

		if URL == None:
			# sending class joining time to discord
			discordAndPrint("Joined " + subject + " class at " + str(datetime.now().time())[:8])
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
			discordAndPrint('Joined the class with ' + URL + ' successfully')
		
		# counting number of students joined 
		count = driver.find_element_by_xpath(membersCountXPath).text
		flag = False
		minCountToLeave = data['otherData']['minCountToLeave']
		alertWords = data['otherData']['alertWords']
		logData = fetchDataFromJSON('log.json')

		setStatus("meetAlive")
		meetAlive = checkStatus("meetAlive")
		autoReply = data['otherData']['autoReply']

		#startRecording()
		#discordAndPrint('Started recording successfully!')
		#time.sleep(10)

		# Reads the text from captions until str(count) > minCountToLeave:
		while True:
			
			meetAlive = checkStatus("meetAlive")

			try:
				count = driver.find_element_by_xpath(membersCountXPath).text
				updateMembersCount(count)

			except Exception as e:
				discordAndPrint(str(e))
			
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
						sendToTelegram(context, "ALERT! Some one called you at " + str(datetime.now().time())[:8])
						sendToTelegram(context, captionTextLower)
						sendToTelegram(context, "Triggered word: " + word)
						takeScreenshot(context)
						discordAndPrint("ALERT! Some one called you at " + str(datetime.now().time())[:8])
						discordAndPrint(captionTextLower)
						discordAndPrint("Triggered word: " + word)
						if autoReply:
							responseMessage = data['otherData']['responseMessage']
							sendMessageInChatBox(responseMessage)
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
								#stopRecording()
								break
							except Exception as e:
								discordAndPrint(str(e))
								sendToTelegram(context, 'Failed to leave the class')
								discordAndPrint('Failed to leave the class')
						updateMembersCount(None)
						time.sleep(5)
						print('Left '+ subject + ' class')
						discordAndPrint('Left the class successfully')	
						sendToTelegram(context, 'Left the class successfully')
					else :
						while True:
							try:
								endButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, endButtonXPath)))
								endButton.click()
								try:
									driver.find_element_by_xpath(justLeaveTheClassXPath).click()
								except:
									pass
								#stopRecording()
								break
							except Exception as e:
								discordAndPrint(str(e))
								sendToTelegram(context, 'Failed to leave the class')
								discordAndPrint('Failed to leave the class')
						updateMembersCount(None)
						discordAndPrint('Left the class successfully')	
						sendToTelegram(context, 'Left the class successfully')
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
								#stopRecording()
								break
							except Exception as e:
								discordAndPrint(str(e))
								sendToTelegram(context, 'Failed to leave the class')
								discordAndPrint('Failed to leave the class')
						updateMembersCount(None)
						time.sleep(5)
						print('Left '+ subject + ' class')
						discordAndPrint('Left the class successfully')	
						sendToTelegram(context, 'Left the class successfully')
					else :
						while True:
							try:
								endButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, endButtonXPath)))
								endButton.click()
								try:
									driver.find_element_by_xpath(justLeaveTheClassXPath).click()
								except:
									pass
								#stopRecording()
								break
							except Exception as e:
								discordAndPrint(str(e))
								sendToTelegram(context, 'Failed to leave the class')
								discordAndPrint('Failed to leave the class')
						updateMembersCount(None)
						discordAndPrint('Left the class successfully')	
						sendToTelegram(context, 'Left the class successfully')
					setStatus("membersCount", None)
					break

					

	except Exception as e:

		driver.quit()
		discordAndPrint('Unexpected error occurred! Fix the error ASAP and try again!')
		discordAndPrint(str(e))

		context.bot.send_message(chat_id = config.TELEGRAM_USER_ID, text = "Unexpected error occurred! Fix the error ASAP and try again!")
		context.bot.send_message(chat_id = config.TELEGRAM_USER_ID, text = str(e))
		execl(executable, executable, "telegrambot.py")
