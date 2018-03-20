import urllib.request
import html2text
import re
from collections import Counter
import os
import sys
import math

def main():

	print("Welcome to tfid counter..!!!!")
	pathname = sys.argv[1]
	destination = sys.argv[2]
	stopword_path = sys.argv[3]
	stop_file = open(stopword_path, 'r')		#passing the stop word list from the stopword file
	stop_list = []
	for line in stop_file:
		w = line.split()
		for word in w:
			stop_list.append(word)
	R = Counter()
	#pathname = 'G:/Application_2016/Information_retreival/files_1/files/'
	#destination = 'G:/Application_2016/Information_retreival/output_result/'
	#Calculating the frequency count and finding the token frequency in all the document
	for i in range(1, 504):
		if i < 10:
			file_location = pathname+'00'+str(i)+'.html'
		if i >= 10 and i < 100:
			file_location = pathname+'0'+str(i)+'.html'
		if i >=100:
			file_location = pathname+str(i)+'.html'
		a = html_frequency_counter(file_location,stop_list)	
		#print(a)
		b = word_reduction(a)
		d = number_of_time_in_files(b)
		#print(d)
		R = R+d
	# calculation of final TFIDF score
	for i in range(1, 504):
		if i < 10:
			file_location = pathname+'00'+str(i)+'.html'
		if i >= 10 and i < 100:
			file_location = pathname+'0'+str(i)+'.html'
		if i >=100:
			file_location = pathname+str(i)+'.html'
		a = html_frequency_counter(file_location,stop_list)
		b = word_reduction(a)
		#print(b)
		c = tf_idf(b, R)
		#print(c)
		print(len(c))
		file_7 = open(destination+'output'+str(i)+'.txt', 'w+')
		for key, value in c.items():
			file_7.write(str(key)+':'+str(value)+'\n')
		file_7.close()
		print("The frequency count has been completed now ")
		print("NOw cleaning up the redundant file.....")
	os.remove("001.txt")
	os.remove("001_s.txt")
	os.remove("removing_hash_star.txt")
	print("Thank you for running the tfid counter..!!")
	print("have a Good day...!!")



def html_frequency_counter(file_location, stop_list):
	stop_list = stop_list
	frequency = Counter()
	f = urllib.request.urlopen('file:///' + file_location)
	page = f.read().decode('utf-8','replace')
	f.close()
	h = html2text.HTML2Text()
	h.ignore_links = False
	h.ignore_images = True
	h.escape_all = True
	h.image_to_alt = True
	text_1file = (h.handle(page))
	lines = [line.lower() for line in text_1file]
	with open("001.txt", 'w', encoding="utf-8") as text_file:
		for i in lines:
			text_file.write(i)
	
	text_file.close()



	# Removing special characters from the file

	file_2 = open('001.txt', 'r')
	file_3 = open('removing_hash_star.txt','w+')
	for line in file_2:
		line_1 = re.sub(r'[*|#|_|-|*|@|$|%|<|-|-|.|?|&|~|`|<|>|(|)|\|{|}|\\|,|:|;|//|=|+|,|<>]+',r'',line)
		file_3.write(line_1)

	file_3.close()
	text = []
	#Removing stopwords fromt he file
	file1 = open('removing_hash_star.txt', 'r').read().split()
	file2 = open('001_s.txt', 'w+')
	for word in file1:
		if word.lower() not in stop_list:
			file2.write(word + " ")
	file2.close()


	#counting the frequency of the words here
	final_reading = open('001_s.txt', 'r')
	for line in final_reading:
		frequency.update(line.split())

	final_reading.close()	
	return frequency

#Removinf the words which occur only once
def word_reduction(X):
	f = dict()
	#print(X)
	for key in set(X.elements()):
		if X[key] <= 1:
			del X[key]
	return(X)

#TFID score function
def tf_idf(f, R):
	f = dict(f)
	d = dict()
	for key, value in f.items():
		if key in R:
			d[key] = float((value/len(f))*(math.log(500/R.get(key))))
	return(d)

#Token frequency in files counter
def number_of_time_in_files(X):
	for key in set(X.elements()):
		X[key] = 1
	return(X)

if __name__ == '__main__':
	main()
