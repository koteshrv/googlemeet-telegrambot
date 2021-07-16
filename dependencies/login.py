from dependencies.others import checkStatus, pageSource, sendToTelegram, setStatus, takeScreenshot
from dependencies import Print, driver
from telegram.ext import run_async
from telegram import ChatAction
import os, pickle, time, config

run_async
def login(mail = None, password = None):

    if mail == None:
        mail = config.MAIL_ID
        password = config.PASSWORD

    if os.path.exists("google.pkl"):
        sendToTelegram("Already Logged into google account.")
        Print('Already Logged into google account.')
        return
    else:
        try:
            driver.get('https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3Afad07e7074c3d678%2C10%3A1601127482%2C16%3A9619c3b16b4c5287%2Ca234368b2cab7ca310430ff80f5dd20b5a6a99a5b85681ce91ca34820cea05c6%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%22d18871cbc2a3450c8c4114690c129bde%22%7D&response_type=code&flowName=GeneralOAuthFlow')
            mailBox = driver.find_element_by_id('identifierId')
            Print('Entering mail address')
            mailBox.send_keys(mail)
            time.sleep(5)
            nextButton = driver.find_element_by_id('identifierNext')
            Print('Clicking next button')
            nextButton.click()
            time.sleep(5)

            try: 
                captchaImg = driver.find_element_by_id('captchaimg')
                captcha = driver.find_element_by_id('ca')
                if captcha.text != 'Type the text you hear or see':
                    takeScreenshot()
                    setStatus('captcha', '')
                    sendToTelegram('Found captcha! Enter the captcha text with /captcha captchaText')
                    flag = 0
                    for i in range(60):
                        captchaText = checkStatus('captcha')
                        if captchaText != '':
                            Print('Entering captcha')
                            captcha.send_keys(captchaText)
                            nextButton = driver.find_element_by_id('identifierNext')
                            Print('Clicking next button')
                            nextButton.click()
                            flag = 1
                            time.sleep(10)
                            break
                        time.sleep(1)
                    
                    if not flag:
                        Print('Waited for 60 seconds. Try again with /login')
                        sendToTelegram('Waited for 60 seconds. Try again with /login')
                        return

            except Exception:
                pass

            passwordbox = driver.find_element_by_xpath("//input[@class='whsOnd zHQkBf']")
            Print('Entering password')
            passwordbox.send_keys(password)
            signinButton = driver.find_element_by_id('passwordNext')
            Print('Clicking sign in button')
            signinButton.click()
            time.sleep(10)

            if(driver.find_elements_by_xpath('//*[@id="authzenNext"]/div/button/div[2]')):
                Print('Authentication found! Please verify')
                sendToTelegram("Authentication found! Please verify")
                driver.find_element_by_xpath('//*[@id="authzenNext"]/div/button/div[2]').click()
                time.sleep(5)

                Print('Sending screenshot to telegram')
                takeScreenshot()

            driver.get('https://apps.google.com/meet/')
            time.sleep(7)   

            pickle.dump(driver.get_cookies() , open("google.pkl","wb"))
            sendToTelegram("Successfully Logged into google account!")
            Print('Successfully Logged into google account!')

        except Exception as e:
            pageSource()
            sendToTelegram('Unexpected error occured when trying to login to google account')
            sendToTelegram(str(e))
            Print('Unexpected error occured when trying to login to google account')
            Print(str(e))
