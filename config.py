import os


DEFAULT_LOCATION = '/app/dependencies/'
TIME_TABLE = DEFAULT_LOCATION + 'timetable.xlsx'
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
DISCORD_WEBHOOK = os.environ.get('DISCORD_WEBHOOK')
MAIL_ID = os.environ.get('MAIL_ID')
PASSWORD = os.environ.get('PASSWORD')
TELEGRAM_USER_ID = os.environ.get('TELEGRAM_USER_ID')


