import os


DEFAULT_LOCATION = '/app/dependencies/'
TIME_TABLE = DEFAULT_LOCATION + 'timetable.xlsx'
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
MAIL_ID = os.environ.get('MAIL_ID')
PASSWORD = os.environ.get('PASSWORD')
TELEGRAM_USER_ID = os.environ.get('TELEGRAM_USER_ID')

# If you want to run locally on your computer
# Place the chrome driver on path
# https://chromedriver.storage.googleapis.com/index.html?path=91.0.4472.101/
# Enter the location of dependencies in default location and add telegram token, mail id
# password and userid below in quotations

'''
DEFAULT_LOCATION = '/home/koteshrv/Desktop/heroku/herokumeet/dependencies/'
TIME_TABLE = DEFAULT_LOCATION + 'timetable.xlsx'
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
MAIL_ID = os.environ.get('MAIL_ID', '')
PASSWORD = os.environ.get('PASSWORD', '')
TELEGRAM_USER_ID = os.environ.get('TELEGRAM_USER_ID', '')
'''
