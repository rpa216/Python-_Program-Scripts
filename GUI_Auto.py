#!/usr/bin/python
# ==========================================================================================
# NAME								VERSION 	DESCRIPTION
# GUI_Auto.py						1.0			Python Library for GUI Automation
# -------------------------------	----------	------------------------------------
# AUTHOR							DATE		MODIFICATIONS
# Vinay Babu Reddy N.				22 Jun 16	v1.0: First Draft
# ==========================================================================================
# Set Environment
# ------------------------------------------------------------------------------------------
import sys, os, time, pyautogui
sys.path.append('../Ops_Auto')
from Ops_Auto import *
import Ops_Auto
Ops_Auto.log_level = 1

# pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True
sleep_factor = 1
loop_count = 10
# ------------------------------------------------------------------------------------------
# Start of GUI Simulation Functions
# ------------------------------------------------------------------------------------------
def alertExit(msg_text,exit_code):
	logMsg('alertExit(msg_text,exit_code)')
	varValidate('string','msg_text',msg_text)
	varValidate('number','exit_code',exit_code)
	pyautogui.alert(msg_text)
	exit(exit_code)
# ------------------------------------------------------------------------------------------
def sleepSecs(sl_duration):
	logMsg('sleepSecs(sl_duration)')
	varValidate('number','sl_duration',sl_duration)
	sleep_dur = sl_duration * sleep_factor
	logMsg('Sleeping for '+str(sleep_dur)+'secs ...','INFO')
	time.sleep(sl_duration)
	return 'OK'
# ------------------------------------------------------------------------------------------
def enterText(full_text,enter_key='no'):
	logMsg('full_text,enter_key=\'no\'')
	varValidate('string','full_text',full_text)
	varValidate('string','enter_key',enter_key)
	pyautogui.typewrite(full_text,interval=0.05)
	pyautogui.press('delete')
	logMsg('Text entered: '+str(full_text),'INFO')
	if enter_key == 'yes':
		pyautogui.press('enter')
		logMsg('Enter!','INFO')
	return 'OK'
# ------------------------------------------------------------------------------------------
def readClipboard(dummy):
	logMsg('readClipboard()')
	from tkinter import Tk
	try:
		r = Tk()
		r.withdraw()
		return_text = r.selection_get(selection = "CLIPBOARD")
		r.destroy()
		logMsg('Clipboard data: '+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('Clipboard read failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def screenShot(file_path):
	logMsg('screenShot(file_path)')
	varValidate('string','file_path',file_path)
	try:
		img_scrn = pyautogui.screenshot(file_path)
		logMsg('Screenshot taken: '+str(file_path),'INFO')
		return 'OK'
	except Exception as e:
		logMsg('Screenshot failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def locatePic(pic_path,left_click='no',offset_x=0,offset_y=0):
	logMsg('locatePic(pic_path,left_click=\'no\',offset_x=0,offset_y=0)')
	varValidate('string','pic_path',pic_path)
	varValidate('string','left_click',left_click)
	varValidate('number','offset_x',offset_x)
	varValidate('number','offset_y',offset_y)
	try:
		if os.path.exists(pic_path):
			w_count = loop_count
			pic_location = None
			while pic_location is None and w_count > 0:
				time.sleep(sleep_factor)
				pic_location = pyautogui.locateOnScreen(pic_path,grayscale=True)
				w_count = w_count - 1
				logMsg('Loop: '+str(w_count),'DEBUG')
			if pic_location is None:
				logMsg('Could not locate: '+str(pic_path),'ERROR')
				return 'ops_auto_error'
			
			pic_x,pic_y = pyautogui.center(pic_location)
			if pic_x and pic_y:
				logMsg('Picture coordinate: '+str(pic_x)+','+str(pic_y),'DEBUG')
				pyautogui.moveTo(pic_x,pic_y)
				pyautogui.moveRel(offset_x,offset_y)
				logMsg('Pic located: '+str(pic_path),'INFO')
				if left_click == 'yes':
					pyautogui.click()
					logMsg('Click!','INFO')
				elif left_click == 'double':
					pyautogui.doubleClick()
					logMsg('Double click!','INFO')
				return str(pic_x)+','+str(pic_y)
			else:
				logMsg('Could not get coordinates: '+str(pic_path),'ERROR')
				return 'ops_auto_error'
		else:
			logMsg('Invalid path: '+str(pic_path),'ERROR')
			return 'ops_auto_error'
	except Exception as e:
		logMsg('Locate pic failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def openApp(app_path,win_pic,app_pic):
	logMsg('openApp(app_path,win_pic,app_pic)')
	varValidate('string','app_path',app_path)
	varValidate('string','win_pic',win_pic)
	varValidate('string','app_pic',app_pic)
	
	pyautogui.press('win')
	logMsg('Windows Start','INFO')
	bx = locatePic(win_pic)
	if bx == 'ops_auto_error':
		return 'ops_auto_error'
	
	r_msg = enterText(app_path,'yes')
	if r_msg == 'ops_auto_error':
		return 'ops_auto_error'
	
	bx = locatePic(app_pic)
	if bx == 'ops_auto_error':
		return 'ops_auto_error'
	logMsg('App opened: '+str(app_path),'INFO')
	return 'OK'
# ------------------------------------------------------------------------------------------
# Misc pyAutoGui commands
# ------------------------------------------------------------------------------------------
def keyPress(key_id):
	logMsg('keyPress(key_id)')
	varValidate('string','key_id',key_id)
	pyautogui.press(key_id)
	return 'OK'
# ------------------------------------------------------------------------------------------
def controlKey(key_id):
	logMsg('controlKey(key_id)')
	varValidate('string','key_id',key_id)
	pyautogui.hotkey('ctrl',key_id)
	return 'OK'
# ------------------------------------------------------------------------------------------
def mouseClick(click_type):
	logMsg('mouseClick(click_type)')
	varValidate('string','click_type',click_type)
	if click_type == 'single':
		pyautogui.click()
		r_msg = 'OK'
	elif click_type == 'double':
		pyautogui.doubleClick()
		r_msg = 'OK'
	elif click_type == 'right':
		pyautogui.rightClick()
		r_msg = 'OK'
	else:
		r_msg = 'ops_auto_error'
	return r_msg
# ------------------------------------------------------------------------------------------
def moveMouse(pos_x,pos_y,move_type='relative'):
	logMsg('moveMouse(pos_x,pos_y,move_type=\'relative\')')
	varValidate('number','pos_x',pos_x)
	varValidate('number','pos_y',pos_y)
	varValidate('string','move_type',move_type)
	if move_type == 'relative':
		pyautogui.moveRel(x,y)
	else:
		pyautogui.moveTo(x,y)
	return 'OK'
# ------------------------------------------------------------------------------------------
def scrollPage(offset_y):
	logMsg('scrollPage(offset_y)')
	varValidate('number','offset_y',offset_y)
	pyautogui.scroll(amount)
	return 'OK'
# ------------------------------------------------------------------------------------------
def dragSelect(offset_x,offset_y):
	logMsg('dragSelect(offset_x,offset_y)')
	varValidate('number','offset_x',offset_x)
	varValidate('number','offset_y',offset_y)
	pyautogui.dragRel(x,y,0.5,button='left')
	return 'OK'
# ------------------------------------------------------------------------------------------
# End of GUI Simulate
# ==========================================================================================