#!/usr/bin/python
# ==========================================================================================
# NAME					VERSION 	DESCRIPTION
# Simulate.py				1.0		Python Library for GUI Automation
# -------------------------------	----------	------------------------------------
# AUTHOR					DATE		MODIFICATIONS
# Vinay Babu Reddy N.			13 May 16	v1.0: First Draft
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
# Start of Simulate Functions
# ------------------------------------------------------------------------------------------
def alertExit(msg_text,exit_code):
	varValidate('string','msg_text',msg_text)
	varValidate('number','exit_code',exit_code)
	pyautogui.alert(msg_text)
	exit(exit_code)
# ------------------------------------------------------------------------------------------
def sleepSecs(sl_duration):
	varValidate('number','sl_duration',sl_duration)
	sleep_dur = sl_duration * sleep_factor
	logMsg('Sleeping for '+str(sleep_dur)+'secs ...','INFO')
	time.sleep(sl_duration)
	return 'OK'
# ------------------------------------------------------------------------------------------
def selectDelete():
	pyautogui.hotkey('ctrl','a')
	pyautogui.press('backspace')
	logMsg('Text deleted','INFO')
	return 'OK'
# ------------------------------------------------------------------------------------------
def selectCopy():
	pyautogui.hotkey('ctrl','a')
	pyautogui.hotkey('ctrl','c')
	logMsg('Text copied','INFO')
	return 'OK'
# ------------------------------------------------------------------------------------------
def selectPaste():
	pyautogui.hotkey('ctrl','v')
	logMsg('Text pasted','INFO')
	return 'OK'
# ------------------------------------------------------------------------------------------
def enterText(full_text,enter_key='no'):
	varValidate('string','full_text',full_text)
	varValidate('string','enter_key',enter_key)
	pyautogui.typewrite(full_text,interval=0.10)
	pyautogui.press('delete')
	logMsg('Text entered: '+str(full_text),'INFO')
	if enter_key == 'yes':
		pyautogui.press('enter')
		logMsg('Enter!','INFO')
	return 'OK'
# ------------------------------------------------------------------------------------------
def readClipboard():
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
	varValidate('string','file_path',file_path)
	try:
		img_scrn = pyautogui.screenshot(file_path)
		logMsg('Screenshot taken: '+str(file_path),'INFO')
		return 'OK'
	except Exception as e:
		logMsg('Screenshot failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def locatePic(pic_path,left_click='no',offsetx=0,offsety=0):
	varValidate('string','pic_path',pic_path)
	varValidate('string','left_click',left_click)
	varValidate('number','offsetx',offsetx)
	varValidate('number','offsety',offsety)
	try:
		if os.path.exists(pic_path):
			w_count = loop_count
			pic_location = None
			while pic_location is None and w_count > 0:
				time.sleep(sleep_factor)
				pic_location = pyautogui.locateOnScreen(pic_path)
				w_count = w_count - 1
				logMsg('Loop: '+str(w_count),'DEBUG')
			if pic_location is None:
				logMsg('Could not locate: '+str(pic_path),'ERROR')
				return 'ops_auto_error','0'
			
			picx,picy = pyautogui.center(pic_location)
			if picx and picy:
				logMsg('Picture coordinate: '+str(picx)+','+str(picy),'DEBUG')
				pyautogui.moveTo(picx,picy)
				pyautogui.moveRel(offsetx,offsety)
				logMsg('Pic located: '+str(pic_path),'INFO')
				if left_click == 'yes':
					pyautogui.click()
					logMsg('Click!','INFO')
				elif left_click == 'double':
					pyautogui.doubleClick()
					logMsg('Double click!','INFO')
				return picx,picy
			else:
				logMsg('Could not get coordinates: '+str(pic_path),'ERROR')
				return 'ops_auto_error','0'
		else:
			logMsg('Invalid path: '+str(pic_path),'ERROR')
			return 'ops_auto_error','0'
	except Exception as e:
		logMsg('Locate pic failed:\n'+str(e),'ERROR')
		return 'ops_auto_error','0'
# ------------------------------------------------------------------------------------------
def openApp(app_path,win_pic,app_pic):
	varValidate('string','app_path',app_path)
	varValidate('string','win_pic',win_pic)
	varValidate('string','app_pic',app_pic)
	
	pyautogui.press('win')
	logMsg('Windows Start','INFO')
	bx,by = locatePic(win_pic)
	if bx == 'ops_auto_error':
		return 'ops_auto_error'
	
	r_code = enterText(app_path,'yes')
	if r_code == 'ops_auto_error':
		return 'ops_auto_error'
	
	bx,by = locatePic(app_pic)
	if bx == 'ops_auto_error':
		return 'ops_auto_error'
	logMsg('App opened: '+str(app_path),'INFO')
	return 'OK'
# ------------------------------------------------------------------------------------------
# End of Simulate
# ==========================================================================================