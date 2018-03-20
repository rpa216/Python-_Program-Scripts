#----------------------------------------------------------------
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
import xlrd
import xlwt
#-----------------------------------------------------------------------------------------------------
def login_SAPGUI():

	#Client = input('Enter your client_info: ')
	#User_ID = input ('Enter the relevant User for client' Client)
	#Password = input('Enter the Password for' User_ID  )
	IP_Address = input("Please enter the IP Address of the Server: ")
	Instance_Number = input("PLease enter the Instance Number: ")
	pyautogui.hotkey('win', 'd')
	pyautogui.hotkey('win')
	pyautogui.typewrite('sapgui' +' ' + IP_Address + ' ' + Instance_Number, interval=0.10)
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
	pyautogui.hotkey('ctrl','a')
	pyautogui.typewrite( '000', interval=0.17)
	pyautogui.press('tab')
	pyautogui.typewrite( 'rpa217', interval=0.10)
	pyautogui.press('tab')
	pyautogui.typewrite( 'Anant3bg', interval=0.10)
	pyautogui.press('enter')
	sleep = sleepSecs(2)

#--------------------------------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------------------------------
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
#----------------------------------------------------------------------------------------------------------
def transaction_RSWBO040():
	FromDate = input("Please enter from date: ")
	To_Date = input(" PLease Current Date: ")
	bx,by = locatePic(r"D:\Python\Simulate\NextTab.png",r"yes",5,5)
	pyautogui.typewrite('/nRSWBO040', interval=0.10)
	pyautogui.press('enter')
	ret_value = locatePic(r"D:\Python\Simulate\CA01_RSWBO040\Date.png",r"yes",7,7)
	pyautogui.press('tab')
	pyautogui.typewrite(FromDate, interval=0.10)
	pyautogui.press('tab')
	pyautogui.typewrite(To_Date, interval=0.10)
	ret_value = locatePic(r"D:\Python\Simulate\Execute.PNG",r"yes",9,11)
	sleep = sleepSecs(2)
	pyautogui.press('printscreen')
	tab_function()
	bx,by = locatePic(r"D:\Python\Simulate\word_blank.PNG",r"yes",5,5)
	pyautogui.typewrite('Client Check for client '+ ' ' + a[i], interval=0.10)
	pyautogui.press('enter')
	pyautogui.hotkey('ctrl','v')
	pyautogui.press('enter')
	tab_function()
	ret_value = locatePic(r"D:\Python\Simulate\back.PNG",r"yes",5,5)
	if ret_value == "ops_auto_error":
		exit(1)
		logMsg("Exiting...","INFO")
		exit(0)
#-----------------------------------------------------------------------------------------------------------------
def Table_SE16():
	ret_value = locatePic(r"D:\Python\Simulate\NextTab.png",r"yes",5,5)
	if ret_value == "ops_auto_error":
			exit(1)
			logMsg("Exiting...","INFO")
			exit(0)
	pyautogui.typewrite('SE16', interval=0.17)
	pyautogui.press('enter')
	ret_value = locatePic(r"D:\Python\Simulate\Confirm_SE16.PNG",r"no",5,5)
	if ret_value == "ops_auto_error":
			exit(1)
			logMsg("Exiting...","INFO")
			exit(0)
	ret_value = locatePic(r"D:\Python\Simulate\Text_area_SE16.PNG",r"no",5,5)
	if ret_value == "ops_auto_error":
			exit(1)
			logMsg("Exiting...","INFO")
			exit(0)
	ret_value = enterText("USR02",r"yes")
	ret_value = locatePic(r"D:\Python\Simulate\USR02_CLASS.PNG",r"yes",45,9)
	if ret_value == "ops_auto_error":
			exit(1)
			logMsg("Exiting...","INFO")
			exit(0)
	pyautogui.press('tab')
	pyautogui.press('tab')
	pyautogui.press('tab')
	pyautogui.press('enter')
	a = ["BACKGROUND","CPIC","SUPER","SAP-SUPPORT" ]
	for i in range(0,4):
		pyautogui.typewrite(a[i], interval=0.17)
		pyautogui.press('tab')
		pyautogui.press('tab')
	ret_value = locatePic(r"D:\Python\Simulate\USR02_Execute_entry.PNG",r"yes",9,8)
	if ret_value == "ops_auto_error":
			exit(1)
			logMsg("Exiting...","INFO")
			exit(0)
	#ret_value = locatePic(r"D:\Python\Simulate\USR02_ERDAT.PNG",r"yes",40,9)
	#if ret_value == "ops_auto_error":
	#		exit(1)
	#		logMsg("Exiting...","INFO")
	#		exit(0)	
	pyautogui.press('tab')
	pyautogui.press('tab')
	date = ["01.01.2016","31.07.2016"] # add the variable here for the current date and the date to specified.
	#pyautogui.press('down')
	for j in range(0,2):
		pyautogui.typewrite(date[j], interval=0.17) 	
		pyautogui.press('tab')
	ret_value = locatePic(r"D:\Python\Simulate\USR02_MaxHit.PNG",r"double",8,2)
	if ret_value == "ops_auto_error":
			exit(1)
			logMsg("Exiting...","INFO")
			exit(0)	
	#pyautogui.press('tab')
	pyautogui.hotkey('ctrl','a')
	pyautogui.press('del')	
	ret_value = locatePic(r"D:\Python\Simulate\Execute.PNG",r"yes",9,11)
	if ret_value == "ops_auto_error":
			exit(1)
	sleep = sleepSecs(4)
#------------------------------------------------------------------------------------------------------------------------
