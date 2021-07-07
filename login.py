from dependencies import login
import os

# used to login to gmail 
# we use this only once while setting chrome profile
mail = os.environ.get('MAIL_ID')
password = os.environ.get('PASSWORD')
login(mail, password)