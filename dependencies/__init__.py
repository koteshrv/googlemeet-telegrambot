from telegram.ext import Updater
from selenium import webdriver
import config, requests, logging, telegram
from datetime import datetime
from telegram import ChatAction

telegramBot = telegram.Bot(token = config.TELEGRAM_TOKEN)


def sendToDiscord(message):
	webhook = config.DISCORD_WEBHOOK
	Message = {
		"content": '[' + str(datetime.now().strftime("%H:%M:%S")) + '] ' + message
	}
	requests.post(webhook, data = Message)

def sendToTelegram(message):
	telegramBot.send_chat_action(chat_id = config.TELEGRAM_USER_ID, action = ChatAction.TYPING)
	telegramBot.send_message(chat_id = config.TELEGRAM_USER_ID, text = message)
	discordAndPrint('Sent a message successfully!')

# prints text to terminal and discord
def discordAndPrint(text):
	sendToDiscord(text)
	print('[' + str(datetime.now().strftime("%H:%M:%S")) + '] ' + text)
	

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


updater = Updater(token = config.TELEGRAM_TOKEN, use_context = True, workers = 32, request_kwargs={'read_timeout': 6, 'connect_timeout': 10})
dp = updater.dispatcher


options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
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

sendToTelegram("Hey! I'm alive :)")
sendToTelegram('Driver loaded successfully')
discordAndPrint('Telegram bot is alive :)')
discordAndPrint('Driver loaded successfully')


