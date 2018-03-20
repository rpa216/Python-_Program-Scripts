#!/usr/bin/python
# ==========================================================================================
# NAME					VERSION 	DESCRIPTION
# Ops_Auto.py				1.0		Python Library for Operations Automation
# USAGE:
# - Import the library:
# 		from Ops_Auto import *
# - Set the log level (Optional) - default is 1:
# 		import Ops_Auto
#		Ops_Auto.log_level = 0
#		(0 = only errors, 1 = normal, 2 = debug)
# - Functions can be called as below. If the function fails, the return text is set to 'ops_auto_error'.
#		fn_results = executeCommand('ls -l')
#		if fn_results != 'ops_auto_error':
#			print(return_text)
# ==========================================================================================
# Start of Ops Automation Functions
# ------------------------------------------------------------------------------------------
# Default log level
log_level = 1
def logMsg(msg_to_log,msg_type='DEBUG'):
	if msg_to_log == '':
		return 'ops_auto_error'
	import time
	global log_level
	msg_type = msg_type.upper()
	if not(log_level == 0 and msg_type != 'ERROR') and not(log_level == 1 and msg_type == 'DEBUG'):
		formatted_msg = str(time.strftime('%Y-%m-%d %H:%M:%S'))+' - '+str(msg_type.rjust(5))+': '+str(msg_to_log)
		print(formatted_msg)
	return 'OK'
# ------------------------------------------------------------------------------------------
def readArguments(usage_msg):
	varValidate('string','usage_msg',usage_msg)
	import sys
	return_text=sys.argv[1:]
	if return_text == [] or return_text == '':
		logMsg('Usage: '+str(sys.argv[0])+' "'+str(usage_msg)+'"','ERROR')
		exit(1)
	else:
		return_text = '|'.join(return_text)
		return_text = return_text.strip()
		logMsg('Arguments provided: '+str(return_text),'INFO')
		return return_text
# ------------------------------------------------------------------------------------------
def varValidate(variable_type,variable_name,variable_value):
	if variable_type == 'number' and not isinstance(variable_value,int):
		logMsg('Expected number in: '+str(variable_name),'ERROR')
		exit(1)
	elif variable_type == 'string' and not isinstance(variable_value,str):
		logMsg('Expected string in: '+str(variable_name),'ERROR')
		exit(1)
	elif variable_type == 'list' and not isinstance(variable_value,list):
		logMsg('Expected list in: '+str(variable_name),'ERROR')
		exit(1)
	elif variable_type == 'dict' and not isinstance(variable_value,dict):
		logMsg('Expected dictionary in: '+str(variable_name),'ERROR')
		exit(1)
	if (isinstance(variable_value,list) and (variable_value == [] or variable_value == [''])) or variable_value == '':
		logMsg('Found null value in: '+str(variable_name),'ERROR')
		exit(1)
	if variable_name == 'connection_strings':
		local_value = variable_value[:]
		local_value[2] = 'xxxxxxxx'
	else:
		local_value = variable_value
	logMsg(str(variable_name)+' = '+str(local_value))
	return 'OK'
# ------------------------------------------------------------------------------------------
def sendMail(mail_from,mail_to,mail_subject,mail_body,smtpserver='localhost'):
	logMsg('sendMail(mail_from,mail_to,mail_subject,mail_body,smtpserver=\'localhost\')')
	varValidate('string','mail_from',mail_from)
	varValidate('list','mail_to',mail_to)
	varValidate('string','mail_subject',mail_subject)
	varValidate('string','mail_body',mail_body)
	varValidate('string','smtpserver',smtpserver)
	import smtplib
	try:
		mail_content = 'From: '+mail_from+'\nTo: '+str(mail_to)+'\nSubject: '+mail_subject+'\n\n'+mail_body
		mail = smtplib.SMTP(smtpserver)
		mail.sendmail(mail_from,mail_to,mail_content)
		mail.quit()
		logMsg('Mail sent to: '+str(mail_to),'INFO')
		return 'OK'
	except Exception as e:
		logMsg('Send mail failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def httpRequest(http_url,data_values={'NA':'NA'},cookie_values=['NA','NA']):
	logMsg('httpRequest(http_url,data_values={\'NA\':\'NA\'},cookie_values=[\'NA\',\'NA\'])')
	varValidate('string','http_url',http_url)
	varValidate('dict','data_values',data_values)
	varValidate('list','cookie_values',cookie_values)
	import urllib.request, http.cookiejar
	try:
		return_text = ''
		cookie_jar = http.cookiejar.CookieJar()
		http_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar),urllib.request.HTTPHandler(),urllib.request.HTTPSHandler())
		http_opener.addheaders = [('User-Agent','Mozilla/5.0')]
		if cookie_values != ['NA','NA']:
			for cookie_value in cookie_values:
				http_opener.addheaders.append(('Cookie',cookie_value))
		if data_values != {'NA':'NA'}:
			data_values_encoded = urllib.urlencode(data_values)
			data_values_encoded = data_values_encoded.encode('utf-8')
			http_request = http_opener.open(http_url,data_values_encoded)
		else:
			http_request = http_opener.open(http_url)
		return_text = http_request.read()
		if return_text:
			return_text = return_text.decode()
		return_text = return_text + '\n'.join(cj for cj in cookie_jar)
		return_text = return_text.strip()
		logMsg('Content of webpage '+str(http_url)+':\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('HTTP request failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def executeCommand(command_to_execute,cli_options=['NA']):
	logMsg('executeCommand(command_to_execute,cli_options=[\'NA\'])')
	varValidate('string','command_to_execute',command_to_execute)
	varValidate('list','cli_options',cli_options)
	import subprocess, time
	try:
		return_text = ''
		sub = subprocess.Popen(command_to_execute,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,universal_newlines=True)
		if cli_options != ['NA']:
			for cli_option in cli_options:
				logMsg('Entering option: '+str(cli_option))
				sub.stdin.write(str(cli_option)+'\n')
				sub.stdin.flush()
				time.sleep(1)
		sub_out, sub_err = sub.communicate()
		if sub_err:
			logMsg('Popen execution failed:\n'+str(sub_err),'ERROR')
			return 'ops_auto_error'
		return_text = str(sub_out)
		return_text = return_text.strip()
		logMsg('Output of '+str(command_to_execute)+':\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('Command execution failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def connectSSH(server_name,connection_strings):
	logMsg('connectSSH(server_name,connection_strings)')
	varValidate('string','server_name',server_name)
	varValidate('list','connection_strings',connection_strings)
	import paramiko
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
		ssh.connect(connection_strings[0],username=connection_strings[1],password=connection_strings[2])
		# ssh.close()
		logMsg('SSH connection made to: '+str(connection_strings[0]),'INFO')
		return ssh
	except Exception as e:
		logMsg('SSH connection failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
def executeSSH(ssh_connection,command_to_execute):
	logMsg('executeSSH(ssh_connection,command_to_execute)')
	varValidate('string','command_to_execute',command_to_execute)
	try:
		return_text = ''
		ssh_in, ssh_out, ssh_err = ssh_connection.exec_command(command_to_execute)
		ssh_errs = ssh_err.readlines()
		ssh_err_lines = ''.join(err_line for err_line in ssh_errs)
		if ssh_err_lines:
			logMsg('SSH execution failed:\n'+str(ssh_err_lines),'ERROR')
			return 'ops_auto_error'
		ssh_outs = ssh_out.readlines()
		return_text = ''.join(out_line for out_line in ssh_outs)
		return_text = return_text.strip()
		logMsg('Output of '+str(command_to_execute)+':\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('SSH execution failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def connectWRM(server_name,connection_strings):
	logMsg('connectWRM(server_name,connection_strings)')
	varValidate('string','server_name',server_name)
	varValidate('list','connection_strings',connection_strings)
	import winrm
	try:
		wrm = winrm.Session(connection_strings[0],auth=(connection_strings[1],connection_strings[2]))
		logMsg('WinRM connection made to: '+str(connection_strings[0]),'INFO')
		return wrm
	except Exception as e:
		logMsg('WRM connection failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
def executeWRM(winrm_connection,command_to_execute):
	logMsg('executeWRM(winrm_connection,command_to_execute)')
	varValidate('string','command_to_execute',command_to_execute)
	try:
		return_text = ''
		wrm_r = winrm_connection.run_cmd(command_to_execute)
		if wrm_r.std_err:
			logMsg('WRM execution failed:\n'+str(wrm_r.std_err),'ERROR')
			return 'ops_auto_error'
		return_text = wrm_r.std_out
		return_text = return_text.strip()
		logMsg('Output of '+str(command_to_execute)+':\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('WRM execution failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def connectDB(db_type,db_name,connection_strings=['NA','NA','NA']):
	logMsg('connectDB(db_type,db_name,connection_strings=[\'NA\'])')
	varValidate('string','db_type',db_type)
	varValidate('string','db_name',db_name)
	varValidate('list','connection_strings',connection_strings)
	try:
		db_type = db_type.lower()
		if db_type == 'mysql':
			import MySQLdb
			db = MySQLdb.connect(host=connection_strings[0],user=connection_strings[1],password=connection_strings[2],database=db_name)
		elif db_type == 'sybase':
			import sybpydb
			db = sybpydb.connect(host=connection_strings[0],user=connection_strings[1],password=connection_strings[2],database=db_name)
		elif db_type == 'oracle':
			import cx_Oracle
			db = cx_Oracle.connect(connection_strings[1],connection_strings[2],db_name)
		elif db_type == 'msaccess':
			import pypyodbc
			db = pypyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+db_name)
		else:
			logMsg('Invalid DB type: '+str(db_type),'ERROR')
			return 'ops_auto_error'
		# db.close()
		logMsg('DB connection made to: '+str(connection_strings[0]),'INFO')
		return db
	except Exception as e:
		logMsg('DB connection failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
def executeDB(db_connection,sql_to_execute):
	logMsg('executeDB(sql_to_execute)')
	varValidate('string','sql_to_execute',sql_to_execute)
	try:
		db_cursor = db_connection.cursor()
		db_cursor.execute(sql_to_execute)
		sql_lower = sql_to_execute.lower()
		if sql_lower.startswith('select'):
			sql_output = db_cursor.fetchall()
		else:
			sql_output = db_cursor.commit()
		if sql_output:
			return_text = '\n'.join(str(line_in_sql).lstrip('(').rstrip(')') for line_in_sql in sql_output if line_in_sql)
		return_text = return_text.strip()
		logMsg('Output of '+str(sql_to_execute)+':\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('DB execution failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def readFile(source_file_path):
	logMsg('readFile(source_file_path)')
	varValidate('string','source_file_path',source_file_path)
	import os
	try:
		return_text = ''
		if os.path.exists(source_file_path):
			file = open(source_file_path,'r')
			return_text = file.read()
			file.close()
		else:
			logMsg('Invalid path: '+str(source_file_path),'ERROR')
			return 'ops_auto_error'
		return_text = return_text.strip()
		logMsg('Content of '+str(source_file_path)+':\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('Read file failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def writeFile(text_to_write,source_file_path):
	logMsg('writeFile(text_to_write,source_file_path)')
	varValidate('string','source_file_path',source_file_path)
	varValidate('string','text_to_write',text_to_write)
	import os
	try:
		return_text = ''
		file = open(source_file_path,'a')
		file.write(text_to_write)
		file.close()
		return_text = return_text.strip()
		logMsg('File '+str(source_file_path)+' written with content:\n'+str(text_to_write),'INFO')
		return_text = 'OK'
		return return_text
	except Exception as e:
		logMsg('Read file failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def zipFiles(source_dir,source_files,target_dir,target_file):
	logMsg('zipFiles(source_dir,source_files,target_dir,target_file)')
	varValidate('string','source_dir',source_dir)
	varValidate('list','source_files',source_files)
	varValidate('string','target_dir',target_dir)
	varValidate('string','target_file',target_file)
	import os, zipfile
	try:
		return_text = ''
		target_file_path = os.path.join(target_dir,target_file)
		if os.path.exists(target_file_path):
			os.remove(target_file_path)
			logMsg('Existing file removed: '+str(target_file_path),'WARN')
		zf = zipfile.ZipFile(target_file_path,'a')
		for source_file in source_files:
			if source_file:
				source_file_path = os.path.join(source_dir,source_file)
				if os.path.exists(source_file_path):
					zf.write(source_file_path,source_file)
				else:
					logMsg('Invalid path: '+str(source_file_path),'ERROR')
					return 'ops_auto_error'
		return_text = '\n'.join(os.listdir(target_dir))
		zf.close()
		return_text = return_text.strip()
		logMsg('Dir list, after Zip:\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('Zip files failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def ftpFiles(ftp_type,local_dir,ftp_files,connection_strings,remote_dir='NA'):
	logMsg('ftpFiles(ftp_type,local_dir,ftp_files,connection_strings,remote_dir=\'NA\')')
	varValidate('string','ftp_type',ftp_type)
	varValidate('string','local_dir',local_dir)
	varValidate('list','ftp_files',ftp_files)
	varValidate('list','connection_strings',connection_strings)
	varValidate('string','remote_dir',remote_dir)
	import os, ftplib
	try:
		return_text = ''
		ftp_type = ftp_type.upper()
		ftp = ftplib.FTP(connection_strings[0],connection_strings[1],connection_strings[2])
		if remote_dir != 'NA':
			ftp.cwd(remote_dir)
		if ftp_type == 'RETR': # Download
			for ftp_file in ftp_files:
				if ftp_file and os.path.isdir(local_dir):
					ftp.retrbinary('RETR '+str(ftp_file),open(os.path.join(local_dir,ftp_file),'wb').write)
				else:
					logMsg('Invalid path: '+str(local_dir),'ERROR')
					return 'ops_auto_error'
			return_text = '\n'.join(os.listdir(local_dir))
		elif ftp_type == 'STOR': # Upload
			for ftp_file in ftp_files:
				if ftp_file:
					ftp_file_path = os.path.join(local_dir,ftp_file)
					if os.path.exists(ftp_file_path):
						ftp.storbinary('STOR '+str(ftp_file),open(ftp_file_path,'rb'))
					else:
						logMsg('Invalid path: '+str(ftp_file_path),'ERROR')
						return 'ops_auto_error'
			return_text = '\n'.join(ftp.retrlines('LIST'))
		else:
			logMsg('Invalid FTP type: '+str(ftp_type),'ERROR')
			return 'ops_auto_error'
		ftp.quit()
		return_text = return_text.strip()
		logMsg('Dir list, after FTP:\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('FTP files failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def archiveFiles(source_dir,older_than_days):
	logMsg('archiveFiles(source_dir,older_than_days)')
	varValidate('string','source_dir',source_dir)
	varValidate('number','older_than_days',older_than_days)
	import os, datetime
	try:
		return_text = ''
		today = datetime.datetime.now()
		if os.path.isdir(source_dir):
			for dirpath, dirnames, filenames in os.walk(source_dir):
				for filename in filenames:
					file_full_path = os.path.join(dirpath,filename)
					file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file_full_path))
					if today - file_modified > datetime.timedelta(days=older_than_days):
						os.remove(file_full_path)
						logMsg('File removed: '+str(filename),'INFO')
			return_text = '\n'.join(os.listdir(source_dir))
		else:
			logMsg('Invalid path: '+str(source_dir),'ERROR')
			return 'ops_auto_error'
		return_text = return_text.strip()
		logMsg('Dir list, after archive:\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('Archive files failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def fileInfo(source_file_path,time_format='%Y-%m-%d %H:%M:%S'):
	logMsg('fileInfo(source_file_path,time_format=\'%Y-%m-%d %H:%M:%S\')')
	varValidate('string','source_file_path',source_file_path)
	varValidate('string','time_format',time_format)
	import os, datetime
	try:
		return_text = ''
		if os.path.exists(source_file_path):
			file_stats = os.stat(source_file_path)
			if file_stats:
				file_mtime = datetime.datetime.fromtimestamp(file_stats.st_mtime)
				file_mtime = file_mtime.strftime(time_format)
				return_text = str(file_mtime)+' '+str(file_stats.st_size)
			else:
				logMsg('Stats failed: '+str(source_file),'ERROR')
		else:
			logMsg('Invalid path: '+str(source_file_path),'ERROR')
			return 'ops_auto_error'
		return_text = return_text.strip()
		logMsg('Info of '+str(source_file_path)+':\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('File info failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def convertToDict(input_text,de_limiter,block_seperator='NA'):
	logMsg('converToDict(input_text,de_limiter,block_seperator=\'NA\')')
	varValidate('string','input_text',input_text)
	varValidate('string','de_limiter',de_limiter)
	varValidate('string','block_seperator',block_seperator)
	try:
		return_dict = []
		if block_seperator == 'NA':
			text_blocks = [input_text]
		else:
			text_blocks = input_text.split(block_seperator)
		for text_block in text_blocks:
			if text_block:
				inner_dict = {}
				lines_in_block = text_block.splitlines()
				for line_in_block in lines_in_block:
					line_in_block = line_in_block.strip()
					if line_in_block:
						key,val = line_in_block.split(de_limiter)
						key = key.strip()
						if key in inner_dict:
							inner_dict[key] = inner_dict[key]+","+val.strip()
						else:
							inner_dict[key] = val.strip()
				return_dict.append(inner_dict)
		logMsg('Converted dictionary object:\n'+str(return_dict),'INFO')
		return return_dict
	except Exception as e:
		logMsg('Convert to dictionary failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def formatText(input_text,chars_to_replace=['NA'],replace_with_char='NA'):
	logMsg('formatText(input_text,chars_to_replace=[\'NA\'],char_to_replace=\'NA\')')
	varValidate('string','input_text',input_text)
	varValidate('list','chars_to_replace',chars_to_replace)
	varValidate('string','replace_with_char',replace_with_char)
	import re
	try:
		return_text = input_text
		return_text = re.sub('[ \t]+',' ',return_text)
		return_text = re.sub('\n+','\n',return_text)
		if chars_to_replace != ['NA']:
			for char_to_replace in chars_to_replace:
				if char_to_replace:
					if replace_with_char == 'NA':
						return_text = return_text.replace(char_to_replace,'')
					else:
						return_text = return_text.replace(char_to_replace,replace_with_char)
		return_text = return_text.strip()
		logMsg('Formatted text:\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('Format text failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def findPatterns(input_text,patterns_to_find,starts_with_pattern='no'):
	logMsg('findPatterns(input_text,patterns_to_find,starts_with_pattern=\'no\')')
	varValidate('string','input_text',input_text)
	varValidate('list','patterns_to_find',patterns_to_find)
	varValidate('string','starts_with_pattern',starts_with_pattern)
	try:
		return_text = ''
		lines_in_text = input_text.splitlines()
		for pattern_to_find in patterns_to_find:
			if pattern_to_find:
				for line_in_text in lines_in_text:
					if line_in_text:
						line_in_text = line_in_text.strip()
						if (starts_with_pattern == 'no' and pattern_to_find in line_in_text) or (starts_with_pattern != 'no' and line_in_text.startswith(pattern_to_find)):
							return_text = return_text+str(line_in_text)+'\n'
		return_text = return_text.strip()
		logMsg('Lines with '+str(patterns_to_find)+':\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('Find pattern failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def removePatterns(input_text,patterns_to_remove,starts_with_pattern='no'):
	logMsg('removePatterns(input_text,patterns_to_remove,starts_with_pattern=\'no\')')
	varValidate('string','input_text',input_text)
	varValidate('list','patterns_to_remove',patterns_to_remove)
	varValidate('string','starts_with_pattern',starts_with_pattern)
	try:
		return_text = input_text
		for pattern_to_remove in patterns_to_remove:
			if pattern_to_remove:
				lines_in_text = return_text.splitlines()
				return_text = ''
				for line_in_text in lines_in_text:
					if line_in_text:
						line_in_text = line_in_text.strip()
						if (starts_with_pattern == 'no' and pattern_to_remove not in line_in_text) or (starts_with_pattern != 'no' and not line_in_text.startswith(pattern_to_remove)):
							return_text = return_text+str(line_in_text)+'\n'
		return_text = return_text.strip()
		logMsg('Lines without '+str(patterns_to_remove)+':\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('Remove pattern failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def countUnique(input_text):
	logMsg('countUnique(input_text)')
	varValidate('string','input_text',input_text)
	import operator
	try:
		return_text = ''
		lines_in_text = input_text.splitlines()
		unique_dict = {}
		for line_in_text in lines_in_text:
			if line_in_text:
				line_in_text = line_in_text.strip()
				if line_in_text in unique_dict:
					unique_dict[line_in_text] += 1
				else:
					unique_dict[line_in_text] = 1
		if unique_dict:
			logMsg('After adding to dict: '+str(unique_dict))
			sorted_dict = sorted(unique_dict.items(),key=operator.itemgetter(1))
			return_text = '\n'.join('{}: {}'.format(val,key) for key,val in sorted_dict)
		return_text = return_text.strip()
		logMsg('Count unique:\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('Count unique failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def sortColumn(input_text,column_number,reverse_order='no'):
	logMsg('sortColumn(input_text,column_number)')
	varValidate('string','input_text',input_text)
	varValidate('number','column_number',column_number)
	varValidate('string','reverse_order',reverse_order)
	import operator
	try:
		return_text = ''
		lines_in_text = input_text.splitlines()
		lines_dict = []
		for line_in_text in lines_in_text:
			if line_in_text:
				line_in_text = line_in_text.strip()
				words_in_text = line_in_text.split(' ')
				i = 0
				for word_in_text in words_in_text:
					if word_in_text.isdigit():
						words_in_text[i] = word_in_text.rjust(16,'0')
					i = i + 1
				if words_in_text and column_number < len(words_in_text):
					lines_dict.append(words_in_text)
				else:
					logMsg('Column num '+str(column_number)+' out of boundary in: '+str(words_in_text),'WARN')
		if lines_dict:
			logMsg('After adding to dict: '+str(lines_dict))
			if reverse_order == 'no':
				sorted_dict = sorted(lines_dict,key=operator.itemgetter(column_number))
			else:
				sorted_dict = sorted(lines_dict,key=operator.itemgetter(column_number),reverse=True)
			for line_in_dict in sorted_dict:
				i = 0
				for word_in_dict in line_in_dict:
					if word_in_dict.isdigit():
						line_in_dict[i] = word_in_dict.lstrip('0')
					i = i + 1
				return_text = return_text+' '.join(line_in_dict)+'\n'
		return_text = return_text.strip()
		logMsg('Sorted on column '+str(column_number)+':\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('Sort columns failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def stringBetween(input_text,preceding_string,succeeding_string):
	logMsg('stringBetween(input_text,preceding_string,succeeding_string)')
	varValidate('string','input_text',input_text)
	varValidate('string','preceding_string',preceding_string)
	varValidate('string','succeeding_string',succeeding_string)
	import re
	try:
		return_text = ''
		return_text = re.search(preceding_string+'(.*)'+succeeding_string,input_text,re.DOTALL)
		if return_text:
			return_text = return_text.group(1)
		return_text = return_text.strip()
		logMsg('String between '+str(preceding_string)+' and '+str(succeeding_string)+':\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('Split failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def getColumns(input_text,column_numbers,de_limiter='NA'):
	logMsg('getColumns(input_text,column_numbers,de_limiter=\'NA\')')
	varValidate('string','input_text',input_text)
	varValidate('list','column_numbers',column_numbers)
	varValidate('string','de_limiter',de_limiter)
	try:
		return_text = ''
		lines_in_text = input_text.splitlines()
		for line_in_text in lines_in_text:
			if line_in_text:
				line_in_text = line_in_text.strip()
				if de_limiter == 'NA':
					words_in_text = list(line_in_text)
				else:
					words_in_text = line_in_text.split(de_limiter)
				if words_in_text:
					logMsg('After delimiting: '+str(words_in_text))
					column_text = ''
					for column_number in column_numbers:
						column_number = int(column_number)
						if column_number != '' and column_number < len(words_in_text):
							column_text = column_text+words_in_text[column_number]+' '
						else:
							logMsg('Column num '+str(column_number)+' out of boundary in: '+str(words_in_text),'WARN')
					return_text = return_text+str(column_text.strip())+'\n'
		return_text = return_text.strip()
		logMsg('Columns '+str(column_numbers)+':\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('Get columns failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def getRows(input_text,from_line,to_line=0):
	logMsg('getRows(input_text,from_line,to_line=0)')
	varValidate('string','input_text',input_text)
	varValidate('number','from_line',from_line)
	varValidate('number','to_line',to_line)
	try:
		return_text = ''
		lines_in_text = input_text.splitlines()
		if to_line == 0:
			return_text = lines_in_text[from_line:]
		else:
			return_text = lines_in_text[from_line:to_line]
		return_text = '\n'.join(return_text)
		return_text = return_text.strip()
		logMsg('Rows '+str(from_line)+' to '+str(to_line)+':\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('Get rows failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def compareText(file1_text,file2_text,sort_lines='no'):
	logMsg('compareText(file1_text,file2_text,sort_lines=\'no\')')
	varValidate('string','file1_text',file1_text)
	varValidate('string','file2_text',file2_text)
	varValidate('string','sort_lines',sort_lines)
	import os, difflib
	try:
		return_text = ''
		file1_lines = file1_text.splitlines()
		file2_lines = file2_text.splitlines()
		if sort_lines != 'no':
			file1_lines.sort()
			file2_lines.sort()
		diff_instance = difflib.Differ()
		diff_lines = list(diff_instance.compare(file1_lines,file2_lines))
		if diff_lines:
			return_text = '\n'.join(diff_line for diff_line in diff_lines if diff_line[0] == '-' or diff_line[0] == '+')
			return_text = return_text.replace('\n\n','\n')
		return_text = return_text.strip()
		logMsg('Difference between the 2 texts:\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('Compare files failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def compareTime(timestamp1,timestamp2,time_format='%Y-%m-%d %H:%M:%S'):
	logMsg('compareTime(timestamp1,timestamp2,time_format=\'%Y-%m-%d %H:%M:%S\')')
	varValidate('string','timestamp1',timestamp1)
	varValidate('string','timestamp2',timestamp2)
	varValidate('string','time_format',time_format)
	from datetime import datetime
	try:
		return_text = ''
		t1 = datetime.strptime(timestamp1,time_format)
		t2 = datetime.strptime(timestamp2,time_format)
		diff = t1 - t2
		return_text = (diff.days * 1440) + (diff.hours * 60) + (diff.minutes) + (diff.seconds / 60)
		logMsg('Difference between the 2 time stamps:\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('Compare times failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
def addMinutes(date_string,minutes_to_add,time_format='%Y-%m-%d %H:%M:%S'):
	logMsg('addMinutes(date_string,minutes_to_add,time_format=\'%Y-%m-%d %H:%M:%S\')')
	varValidate('string','date_string',date_string)
	varValidate('number','minutes_to_add',minutes_to_add)
	varValidate('string','time_format',time_format)
	import datetime
	try:
		return_text = ''
		input_datetime = datetime.datetime.strptime(date_string,time_format)
		if input_datetime:
			return_text = input_datetime + datetime.timedelta(minutes=minutes_to_add)
			return_text = return_text.strftime(time_format)
		return_text = return_text.strip()
		logMsg('Datetime after adding '+str(minutes_to_add)+':\n'+str(return_text),'INFO')
		return return_text
	except Exception as e:
		logMsg('Add time failed:\n'+str(e),'ERROR')
		return 'ops_auto_error'
# ------------------------------------------------------------------------------------------
#Modules imported
import uuid, hashlib
# module to get encrypted string
def hashString(string_to_hash):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + string_to_hash.encode()).hexdigest() + ':' + salt 
def checkString(hashed_string,user_string):
    new_str,salt = hashed_string.split(':')
    return new_str == hashlib.sha256(salt.encode() + user_string.encode()).hexdigest()
# ------------------------------------------------------------------------------------------
# End of Ops_Auto
# ==========================================================================================
# os.rename(source_file_path,target_file_path)
# os.remove(source_file_path)
# os.rmdir(source_dir)
# shutil.move(source_file_path,target_file_path)
# shutil.copy2(source_file_path,target_file_path)
# shutil.rmtree(source_dir)
# os.mkdir(target_dir)
# $(Get-Item file.txt).lastwritetime=$(Get-Date "30/03/2015 01:00 am")
# re.sub('[^A-Za-z0-9]+','',input_text)
# datetime.datetime.today().strftime(time_format)
# datetime.datetime.strptime(date_string,time_format)
# import sys
# sys.path.append('/full/path/')
# import module
# ------------------------------------------------------------------------------------------