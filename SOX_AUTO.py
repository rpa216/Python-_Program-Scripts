#------------------------------------------------------------------------------------------------------------
# IMPORT LIBRARIES
import sys, re
sys.path.append("../Ops_Auto")

# Uncomment the below GUI_Auto section for Simulation functions 
from GUI_Auto import *
import GUI_Auto
GUI_Auto.sleep_factor = 1 # Default is 1
GUI_Auto.loop_count = 10 # Default is 10

from Ops_Auto import *
import Ops_Auto
Ops_Auto.log_level = 1 # Log level: 0=no logs, 1=imp logs, 2=alpyautogui.hotkey('win')
import sys, os, time, pyautogui

sys.path.append('../Simulate')
from Simulate import *
import Simulate
#-----------------------------------------------------------------------------------------------------
def tab_function():
	pyautogui.hotkey('alt','tab')
	sleep = sleepSecs(2)
	pyautogui.hotkey('alt','tab')
#------------------------------------------------------------------------------------------------------
def Opening_word():
	Piclocator = locatePic(r"D:\Python\Simulate\word_123.png",r"yes",5,5)
	if Piclocator == "ops_auto_error":
		exit(1)
		logMsg("Exiting... due to PIC not located","INFO")
		exit(0)
	sleep = sleepSecs(2)
	Piclocator = locatePic(r"D:\Python\Simulate\close.png",r"yes",5,5)
	if Piclocator == "ops_auto_error":
		exit(1)
		logMsg("Exiting... due to PIC not located","INFO")
		exit(0)
	pyautogui.press('enter')
	sleep = sleepSecs(2)
	pyautogui.press('enter')
	pyautogui.hotkey('alt','space','x')
	pyautogui.hotkey('ctrl','a')
	pyautogui.hotkey('del')
#------------------------------------------------------------------------------------------

def login_SAPGUI():

	#Client = input('Enter your client_info: ')
	#User_ID = input ('Enter the relevant User for client' Client)
	#Password = input('Enter the Password for' User_ID  )
	pyautogui.hotkey('win', 'd')
	pyautogui.hotkey('win')
	pyautogui.typewrite('sapgui 172.17.98.156 02', interval=0.10)
	pyautogui.hotkey('enter')
	spaceleep = sleepSecs(2)
	pyautogui.hotkey('alt','space','x')
	ret_value = locatePic(r"D:\Python\Simulate\sap_up.PNG",r"yes",1,2)
	if ret_value == "ops_auto_error":
		exit(1)
		logMsg("Exiting...","INFO")
		exit(0)
	sleep = sleepSecs(6)
	pyautogui.press('up')
	pyautogui.typewrite( '000', interval=0.17)
	pyautogui.press('tab')
	pyautogui.typewrite( 'rpa217', interval=0.10)
	pyautogui.press('tab')
	pyautogui.typewrite( 'Anant3bg', interval=0.10)
	pyautogui.press('enter')
	sleep = sleepSecs(2)
# ------------------------------------------------------------------------------------------
def transaction_SM51():
	autoVar_Server1 = ["Win2k8StdR2_POX_02", "augfgwfgqifwigf", "gagoqwqgiq"]
	for i in range(0,3):
		ret_value = locatePic(r"D:\Python\Simulate\sap_on.png",r"yes",5,5)
		if ret_value == "ops_auto_error":
			exit(1)
			logMsg("Exiting...","INFO")
			exit(0)
		Piclocator = locatePic(r"D:\Python\Simulate\NextTab.png",r"yes",5,5)
		if Piclocator == "ops_auto_error":
			exit(1)
			logMsg("Exiting...","INFO")
			exit(0)
		pyautogui.typewrite('/nsm51', interval=0.17)
		pyautogui.press('enter')
		sleep = sleepSecs(2)
		sleep = sleepSecs(2)
		pyautogui.hotkey('ctrl','f')
		# locate pic 1
		textenter = enterText(autoVar_Server1[i],r"yes")
		ret_value = locatePic(r"D:\Python\Simulate\Hit_displayed.png")	
		# if pic 1 is not found or any error in finding pic 1
		if ret_value == "ops_auto_error":
			# locate pic 2
			ret_value = locatePic(r"D:\Python\Simulate\NoHit_display.PNG.png")
			if ret_value == "ops_auto_error":
				exit(1)
				logMsg("Exiting...","INFO")
				exit(0)
			pyautogui.press('printscreen')
			pyautogui.hotkey('esc')
			tab_function()
			bx,by = locatePic(r"D:\Python\Simulate\word_blank.PNG",r"yes",5,5)
			pyautogui.typewrite('Screenshots of SM51 with Instance given not found', interval=0.17)
			pyautogui.press('enter')
			pyautogui.hotkey('ctrl','v')
			pyautogui.press('enter')
			tab_function()
		pyautogui.press('printscreen')
		pyautogui.hotkey('esc')
		tab_function()
		bx,by = locatePic(r"D:\Python\Simulate\word_blank.PNG",r"yes",5,5)
		pyautogui.typewrite('Screenshots of SM51 the Instance given found', interval=0.17)
		pyautogui.press('enter')
		pyautogui.hotkey('ctrl','v')
		pyautogui.press('enter')
		tab_function()
#---------------------------------------------------------------------------------------------------------------------------------------------
def transaction_SU01():
	User_list = ["rpa216", "sap*"]
	Client = ["000", "100"]
	j = 0
	for i in range (0, 2):
		ret_value = locatePic(r"D:\Python\Simulate\NextTab.png",r"yes",5,5)
		if ret_value == "ops_auto_error":
			exit(1)
			logMsg("Exiting...","INFO")
			exit(0)
		pyautogui.typewrite('/nsu01', interval=0.10)
		pyautogui.press('enter')
		pyautogui.hotkey('ctrl','a')
		ret_value = enterText(User_list[i],r"no")
		if ret_value == "ops_auto_error":
			exit(1)
			logMsg("Exiting...","INFO")
			exit(0)
		pyautogui.hotkey('f7')
		sleep = sleepSecs(1)
		bx,by = locatePic(r"D:\Python\Simulate\LogonData.png",r"yes",5,5)
		sleep = sleepSecs(2)
		pyautogui.press('printscreen')
		tab_function()
		ret_value = locatePic(r"D:\Python\Simulate\word_blank.PNG",r"yes",5,5)
		if ret_value == "ops_auto_error":
			exit(1)
			logMsg("Exiting...","INFO")
			exit(0)
		pyautogui.typewrite('USER CHECK FOR  ' + ' ' + User_list[i] + 'in ' +  ' ' + Client [j], interval=0.10)
		pyautogui.press('enter')
		pyautogui.hotkey('ctrl','v')
		pyautogui.press('enter')
		tab_function()

#----------------------------------------------------------------------------------------------------------------------------
def transaction_SCC4():
	ret_value = locatePic(r"D:\Python\Simulate\NextTab.png",r"yes",5,5)
	if ret_value == "ops_auto_error":
			exit(1)
			logMsg("Exiting...","INFO")
			exit(0)
	pyautogui.typewrite('/nscc4', interval=0.17)
	pyautogui.press('enter')
	sleep = sleepSecs(2)
	pyautogui.press('printscreen')
	tab_function()
	ret_value = locatePic(r"D:\Python\Simulate\word_blank.PNG",r"yes",5,5)
	if ret_value == "ops_auto_error":
			exit(1)
			logMsg("Exiting...","INFO")
			exit(0)
	pyautogui.typewrite('Client overview in the system', interval=0.10)
	pyautogui.press('enter')
	pyautogui.hotkey('ctrl','v')
	pyautogui.press('enter')
	tab_function()
#--------------------------------------------------------------------------------------------------------------------------

login_SAPGUI()
Opening_word()
tab_function()
transaction_SM51()
transaction_SU01()
transaction_SCC4()