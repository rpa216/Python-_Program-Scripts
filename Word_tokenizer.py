import urllib.request
import html2text
import re
from collections import Counter
import os
import sys

def main():

	print("Welcome to word counters..!!!!")
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
	#file_location = 'G:/Application_2016/Information_retreival/files_1/files/'+str(i)+'.html'
	for i in range(1, 504):
		if i < 10:
			file_location = pathname+'00'+str(i)+'.html'
		if i >= 10 and i < 100:
			file_location = pathname+'0'+str(i)+'.html'
		if i >=100:
			file_location = pathname+str(i)+'.html'
		a = html_frequency_counter(file_location,stop_list)
		file_6 = open(destination+str(i)+'output.txt', 'w+')
		for line1 in set(a.elements()):
			file_6.write(line1+':'+str(a[line1])+'\n')
		file_6.close()
		R = R+a
	c = dict(R)
	b  = set(R.most_common(len(R)-1))
	b = sorted(b)
		#print(b)
	file_7 = open(destination+'output_sorted_alphabetically.txt', 'w+')
	for j in b:
		file_7.write(str(j)+'\n')
	file_7.close()
	d = (sorted(c.items(), key=lambda x:x[1]))
	file_8 = open(destination+'output_sorted_frequency.txt', 'w+')
	for line2 in d:
		file_8.write(str(line2)+'\n')
	file_8.close()

	os.remove("001.txt")
	os.remove("001_s.txt")
	os.remove("removing_hash_star.txt")







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

	#Removing stopwords fromt he file
	file1 = open('removing_hash_star.txt', 'r')
	file2 = open('001_s.txt', 'w+')
	for line in file1:
		w = line.split(' ')
		for word in w:
			if word in stop_list:
				continue
			else:
				file2.write(word + " ")
	file2.close()


	#counting the frequency of the words here
	final_reading = open('001_s.txt', 'r')
	for line in final_reading:
		frequency.update(line.split())

	final_reading.close()
	print("The frequency count has been completed now ")
	print("NOw cleaning up the redundant file.....")	
	return frequency

main()