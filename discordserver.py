from dependencies import *
import discord, asyncio, traceback

open(config.PATH + 'discordserverlog.txt', 'w').close()
client = discord.Client()
data = fetchDataFromJSON('data.json')
token = data["credentials"]["token"]

def updatelog():
	f = open(config.PATH + 'discordserverlog.txt', 'a')
	traceback.print_exc(file = f)
	f.close()

def timetable():
	log = fetchDataFromJSON('log.json')
	timetableData = log["completeTimeTable"]
	timings = timetableData['Timings']
	s = '__**Time Table**__\n'
	for key in timetableData:
		if key != 'Timings':
			datalist = timetableData[key]
			period = 0
			s += '__**' + key + '**__' + ':' + '\n'
			for i in range(len(datalist)):
				s += timings[period] + ' : ' + datalist[period] + '\n'
				period += 1
			s += '\n'
	return s


@client.event
async def on_ready():
	dateAndTime = datetime.now()
	currentTime = dateAndTime.time()
	print('Discord server started successfully at ' + str(currentTime))


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.lower() == 'googlemeetbot':
		setStatus("discordServer")
		googlemeetbotThread()
		await message.channel.send('Started googlemeetbot successfully')

	if message.content.lower() == 'join meet':
		try:
			setStatus("discordServer")
			await message.channel.send('Enter meet link below')
			def checkURL(m):
				classURL = m.content
				if classURL[:24] == 'https://meet.google.com/' or classURL[:23] == 'http://meet.google.com/':
					return 1
				return 0 
			try:
				classLink = await client.wait_for('message', timeout = 30.0, check = checkURL)
				classLink = classLink.content
				await message.channel.send('Joining the meet now!') 
				joinClassThread(classLink)	
			except asyncio.TimeoutError:
				await message.channel.send('Timeout! Try again')  
		except Exception:
			updatelog()

	if message.content.lower() == 'schedule meet':
		setStatus("discordServer")
		await message.channel.send('Enter meet link below')
		def checkURL(m):
			classURL = m.content
			if classURL[:24] == 'https://meet.google.com/' :
				return 1
			return 0 
		def checkTime(t):
			time = t.content
			if len(time) == 5 and time[2] == ':':
				return 1
			return 0
		try:
			classLink = await client.wait_for('message', timeout = 30.0, check = checkURL)
			await message.channel.send('Enter the time you want to schedule the meet')
			scheduleTime = await client.wait_for('message', timeout = 30.0, check = checkTime)
			classLink = classLink.content
			scheduleTime = scheduleTime.content
			joinClassThread(classLink, schedule = scheduleTime)
			await message.channel.send('Meet scheduled successfully!') 
		except asyncio.TimeoutError:
			await message.channel.send('Timeout! Try again')

	if message.content.lower() == 'status':
		if checkStatus('status'):
			await message.channel.send("Google meet bot is __**running**__ at the moment!\nMember's count: " + str(checkStatus('membersCount')))
		else :
			await message.channel.send('Google meet bot is __**not running**__ at the moment!')

	if message.content.lower() == 'killbot':
		setStatus("stop")

	if message.content.lower() == 'which class':
		if whichClass() == None:
			await message.channel.send('No class is running at the moment!')
		else:
			await message.channel.send(whichClass())	
	
	if message.content.lower() == '/reply':
		logdata = fetchDataFromJSON('log.json')
		await message.channel.send('Enter the message you want to send')
		def checkmsg(m):
			msg = m.content
			if msg[:5] != 'Enter' :
				return 1
			return 0 
		def checkstatus(m):
			msg = m.content.lower()
			if msg == 'y' :
				return 1
			return 0 
		try:
			msg = await client.wait_for('message', timeout = 30.0, check = checkmsg)
			msg = msg.content
			await message.channel.send('Do you want to send this message? [Y/N]')
			await message.channel.send('```' + msg +'```')  
			status = await client.wait_for('message', timeout = 30.0, check = checkstatus)
			status = status.content
			if status.lower() == 'y':
				setStatus("sendMessageRequest")
				logdata["log"]["messageToSendFromDiscordToMeet"] = msg
				sendDataToJSON('log.json', logdata)
				for i in range(10):
					time.sleep(1)
					if checkStatus("messageSentFromDiscordToMeet"):
						break
				if not checkStatus("messageSentFromDiscordToMeet"):
					await message.channel.send('Unexpected error occured. So message not sent successfully!')
				else:
					await message.channel.send('Message sent successfully!') 
					setStatus("sendMessageRequest", False)
					setStatus("messageSentFromDiscordToMeet", False)
					logdata["log"]["messageToSendFromDiscordToMeet"] = ""
					sendDataToJSON('log.json', logdata)
			else:
				await message.channel.send('Reply command aborted!') 
		except asyncio.TimeoutError:
			await message.channel.send('Timeout! Try again')

	if message.content.lower() == 'classes today':
		loadTimeTable()
		classesToday(printHoliday = False)
		log = fetchDataFromJSON('log.json')
		classes = log["todaysTimeTable"]
		s = '__**Classes Today**__\n'
		spacesLen = 15
		for key, val in classes.items():
			keyLen = len(key)
			spacesLen = 15
			spaces = ' ' * (spacesLen - keyLen)
			s += key + spaces + val + '\n'
		await message.channel.send(s)

	if message.content.lower() == 'timetable':
		await message.channel.send(timetable())

	if message.content.lower() == 'holidays':
		updateholidaysList()
		log = fetchDataFromJSON('log.json')
		holidays = log["holidaysList"]
		holidaysString = '__**Holidays List**__\n'
		holidaysPresent = False
		for key, val in holidays.items():
			l = len(str(key))
			spaces = ' ' * (4 - l)
			holidaysString += ('__**' + key + '**__ :' + spaces + val + '\n')
			holidaysPresent = True
		if holidaysPresent:
			await message.channel.send(holidaysString) 
		else:
			await message.channel.send("You don't have any holidays")  

	if message.content.lower() == 'add holiday':
		await message.channel.send('Enter day and occasion separated with space')
		def details(data):
			data = data.content
			date, occasion = data.split()
			if date.isnumeric():
				return 1
			return 0 
		data = await client.wait_for('message', timeout = 30.0, check = details)
		data = data.content
		date, occasion = data.split()
		updateholidaysList(date, occasion)
		await message.channel.send('Added ' + str(date) + 'to the list successfully!')
		log = fetchDataFromJSON('log.json')
		holidays = log["holidaysList"]
		holidaysString = '__**Holidays List**__\n'
		holidaysPresent = False
		for key, val in holidays.items():
			l = len(str(key))
			spaces = ' ' * (4 - l)
			holidaysString += ('__**' + key + '**__ :' + spaces + val + '\n')
			holidaysPresent = True
		if holidaysPresent:
			await message.channel.send(holidaysString) 
		else:
			await message.channel.send("You don't have any holidays")

	if message.content.lower() == 'remove holiday':
		await message.channel.send('Enter day you want to remove')
		def details(data):
			date = data.content
			if date.isnumeric():
				return 1
			return 0 
		date = await client.wait_for('message', timeout = 30.0, check = details)
		date = date.content
		updateholidaysList(date, remove = True)
		await message.channel.send('Removed ' + str(date) + 'from the list successfully!')
		log = fetchDataFromJSON('log.json')
		holidays = log["holidaysList"]
		holidaysString = '__**Holidays List**__\n'
		holidaysPresent = False
		for key, val in holidays.items():
			l = len(str(key))
			spaces = ' ' * (4 - l)
			holidaysString += ('__**' + key + '**__ :' + spaces + val + '\n')
			holidaysPresent = True
		if holidaysPresent:
			await message.channel.send(holidaysString) 
		else:
			await message.channel.send("You don't have any holidays")

		
	if message.content.lower() == 'update timetable':
		await message.channel.send('Enter day and period you want to change')
		def details(data):
			try:
				data = data.content
				day, period = data.split()
				if day[-3:].lower() == 'day':
					return 1
				return 0 
			except ValueError:
				return 0
		def classdetails(data):
			data = data.content
			if len(data) < 8:
				return 1
			return 0 
		data = await client.wait_for('message', timeout = 30.0, check = details)
		data = data.content
		day, classTime = data.split()
		await message.channel.send('Enter the class name you want to change')
		classToUpdate = await client.wait_for('message', timeout = 30.0, check = classdetails)
		classToUpdate = classToUpdate.content
		updateTimeTable(day, classTime, classToUpdate)
		loadTimeTable()
		await message.channel.send('Updated timetable successfully!')


	if message.content.lower() == 'temp update timetable':
		log = fetchDataFromJSON('log.json')
		tempTimetableUpdateData = log["tempTimetableUpdate"]
		tempTimetableUpdateKeys = list(tempTimetableUpdateData.keys())
		await message.channel.send('Enter day and period you want to change')
		def details(data):
			try:
				data = data.content
				day, period = data.split()
				if day[-3:].lower() == 'day':
					return 1
				return 0 
			except ValueError:
				return 0
		def classdetails(data):
			data = data.content
			if len(data) < 8:
				return 1
			return 0 
		data = await client.wait_for('message', timeout = 30.0, check = details)
		data = data.content
		day, classTime = data.split()
		await message.channel.send('Enter the class name you want to change')
		classToUpdate = await client.wait_for('message', timeout = 30.0, check = classdetails)
		classToUpdate = classToUpdate.content
		previousClass = updateTimeTable(day, classTime, classToUpdate, previousClass = True)
		await message.channel.send('Temporarily updated ' + previousClass + ' in timetable successfully!')
		if len(tempTimetableUpdateKeys) == 0:
			tempTimetableUpdateData['0'] = {
				"day" : day,
				"period" : classTime,
				"classToUpdate" : classToUpdate,
				"previousClass" : previousClass
			}
		else :
			tempTimetableUpdateData[str(int(tempTimetableUpdateKeys[-1]) + 1)] = {
				"day" : day,
				"period" : classTime,
				"classToUpdate" : classToUpdate,
				"previousClass" : previousClass
			}
		log["tempTimetableUpdate"].update(tempTimetableUpdateData)
		sendDataToJSON('log.json', log)
		
	if message.content.lower() == 'log':
		await message.channel.send(str(printLog(discordServer = True)))

	if message.content.lower() == 'serverlog':
		await message.channel.send(file = discord.File('/home/koteshrv/Desktop/googlemeetbot/discordserverlog.txt'))

	if message.content.lower() == 'help':
		helpstr = '__**googlemeetbot discord server commands**__\n'
		helpstr += '**googlemeetbot**: runs googlemeetbot\n'
		helpstr += '**join meet** : takes meet link and joins the meet immediately\n'
		helpstr += '**schedule meet** : takes meet link and schedules the meet\n'
		helpstr += '**status** : prints the current bot status\n'
		helpstr += '**killbot**: kills the bot\n'
		helpstr += '**which class** : prints the present running class\n'
		helpstr += "**classes today** : prints today's classes\n"
		helpstr += '**timetable** : prints timetable\n'
		helpstr += '**update timetable** : updates timetable\n'
		helpstr += '**update timetable** : updates timetable\n'
		helpstr += '**temp update timetable** : updates timetable temporarily\n'
		helpstr += '**holidays** : prints holidays list\n'
		helpstr += '**add holiday** : adds holiday to the list\n'
		helpstr += '**remove holiday** : removes holiday from the list\n'
		helpstr += '**log** : prints log data'
		await message.channel.send(helpstr)


client.run(token)



