from telegram.ext import Updater
from selenium import webdriver
import config, requests
from datetime import datetime

def sendToDiscord(message):
	webhook = config.DISCORD_WEBHOOK
	Message = {
		"content": '[' + str(datetime.now().strftime("%H:%M:%S")) + '] ' + message
	}
	requests.post(webhook, data = Message)

# prints text to terminal and discord
def discordAndPrint(text):
	sendToDiscord(text)
	print('[' + str(datetime.now().strftime("%H:%M:%S")) + '] ' + text)

updater = Updater(token = config.TELEGRAM_TOKEN, use_context = True)
dp = updater.dispatcher

options = webdriver.ChromeOptions()
options.add_argument("--disable-infobars")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent='User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'")
options.add_argument("--disable-popup-blocking")
options.add_experimental_option("prefs", { \
"profile.default_content_setting_values.media_stream_mic": 2,
"profile.default_content_setting_values.media_stream_camera": 2,
"profile.default_content_setting_values.geolocation": 2,
"profile.default_content_setting_values.notifications": 2
})

driver = webdriver.Chrome(chrome_options = options)
discordAndPrint('Driver loaded successfully')

