from bs4 import BeautifulSoup
from pymongo import Connection
import codecs
import locale
import sys
import os
import re

def extract_data(block):
	d = {}
	for field in ['focal', 'quote', 'author', 'title', 'year']:
		tag = block.find('div', class_=field)
		if field == 'quote': field = 'text'
		if tag != None:
			d[field] = tag.string
	return d

def inspect_file(file_name):

	global count

	raw_file = source_path + file_name
	raw_soup = BeautifulSoup(open(raw_file), from_encoding="utf-8")

	results = raw_soup.find_all('div', class_="citation")

	for citation in results:

		try:
			quote_dict = extract_data(citation)
			db.quotes.insert(quote_dict, safe=True)
			count += 1

		except: # Exception handler
			print ("Something wrong with: " + file_name)
			print ("Error message: ", sys.exc_info())
			continue

	return

def process_all(files_list):
	for i, file_name in enumerate(files_list):
		if i%5000 == 0: print ("Progress: " + str(int(i*100/len(files_list)))+"%")
		inspect_file(file_name)
	return

def connect_db():
	try:
		# Here the default parameters are specified explicitly
		db_connection = Connection(host="localhost", port=27017)
		print ("Connected to MongoDB successfully!")
	except:
		print("Could not connect to MongoDB!")
		sys.exit(0)
	return db_connection["deutsch"]

def load_directory(source_path):
	files_list = []
	for file_name in os.listdir(source_path):
		try:
			if file_name.endswith(".html"):
				files_list.append(file_name)
		except IndexError:
			sys.stderr.write("Something went wrong with " + file_name + ".")
			continue
	locale.setlocale(locale.LC_ALL, 'en_AU')
	number_of_files = locale.format("%d", len(files_list), grouping=True)
	print(number_of_files + " files loaded.")
	return files_list

if __name__ == '__main__':

	source_path = "Quotes/"
	
	print("Loading files...")
	files_list = load_directory(source_path)

	print("Connecting to database...")
	db = connect_db()

	count = 0
	print("Processing all files...")
	process_all(files_list)

	print(str(count) + " quotes found.")

	print("Valmis!")