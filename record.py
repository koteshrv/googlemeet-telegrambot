from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from dependencies import driver
import pyautogui, time

recordScreenXPath = '/html/body/div/button[4]'
stopCaptureXPath = '//*[@id="stop"]'
downloadButtonXPath = '//*[@id="download"]/button'

def startRecording():

	driver.switch_to.window(driver.window_handles[0])

	try:
		driver.find_element_by_xpath(recordScreenXPath).click()

	except Exception as e:
		print(str(e))

	pyautogui.keyDown('ctrl')
	pyautogui.press('\t')
	pyautogui.press('\t')
	pyautogui.keyUp('ctrl')
	pyautogui.press('\t')
	pyautogui.press('\t')
	pyautogui.press('down')
	pyautogui.press('down')
	pyautogui.press('\t')
	pyautogui.press('enter')
	pyautogui.press('\t')
	pyautogui.press('\t')
	pyautogui.press('enter')

	try:
		WebDriverWait(driver, 5).until(EC.alert_is_present())
		alert = driver.switch_to.alert
		alert.dismiss()

	except Exception as e:
		print(str(e))


def stopRecording():

	endButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, stopCaptureXPath)))
	endButton.click()
	time.sleep(2)

	downloadButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, downloadButtonXPath)))
	downloadButton.click()

	driver.switch_to.window(driver.window_handles[1])


