'''Run this file to create google.pkl file in the local machine
    So that you dont need to login every time you use the bot'''

import os, pickle, time, config
from dependencies import driver

def login():

    mail = config.MAIL_ID
    password = config.PASSWORD

    if os.path.exists("google.pkl"):
        print('Already logged in')

    else:
        driver.get('https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3Afad07e7074c3d678%2C10%3A1601127482%2C16%3A9619c3b16b4c5287%2Ca234368b2cab7ca310430ff80f5dd20b5a6a99a5b85681ce91ca34820cea05c6%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%22d18871cbc2a3450c8c4114690c129bde%22%7D&response_type=code&flowName=GeneralOAuthFlow')
        mailBox = driver.find_element_by_id('identifierId')
        print('Entering mail address')
        mailBox.send_keys(mail)
        nextButton = driver.find_element_by_id('identifierNext')
        print('Clicking next button')
        nextButton.click()
        time.sleep(7)

        passwordbox = driver.find_element_by_xpath("//input[@class='whsOnd zHQkBf']")
        print('Entering password')
        passwordbox.send_keys(password)
        signinButton = driver.find_element_by_id('passwordNext')
        print('Clicking sign in button')
        signinButton.click()
        time.sleep(7)

        if(driver.find_elements_by_xpath('//*[@id="authzenNext"]/div/button/div[2]')):
            print('Authentication found! Please verify')
            driver.find_element_by_xpath('//*[@id="authzenNext"]/div/button/div[2]').click()
            time.sleep(5)


        driver.get('https://apps.google.com/meet/')
        time.sleep(7)   

        pickle.dump(driver.get_cookies() , open("google.pkl","wb"))
        print('Successfully Logged into google account!')

login()