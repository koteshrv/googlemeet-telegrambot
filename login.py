from dependencies import login
from os import environ

# used to login to gmail 
# we use this only once while setting chrome profile
mail = environ['MAIL_ID']
password = environ['PASSWORD']
login(mail, password)