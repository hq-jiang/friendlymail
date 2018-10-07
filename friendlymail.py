#!/usr/bin/python3

import os
import sys
import csv
import datetime
import subprocess
import tempfile
import argparse

def read_people_csv(filepath):
	people = []
	try:
		with open(filepath, mode='r') as f:
			f.readline()
			reader = csv.reader(f, delimiter=',')
			for line in reader:
				if line:
					person = {}
					person['name'] = line[0]
					person['email'] = line[1]
					person['birthday'] = parse_string2date(line[2])
					people.append(person)
	except:
		print('Could not read meta.dat')
		sys.exit()
	return people

def print_people(people):
	for person in people:
		print(person)

def read_meta_dat(filepath):
	if os.path.exists(filepath):
		print('Parsing meta.dat ...')
		try:
			with open(filepath, mode='r') as f:
				prev_date_dat = f.readline()
				prev_date = parse_string2date(prev_date_dat)
				print('Last run was', parse_date2string(prev_date))
		except:
			print('Could not read meta.dat')
			sys.exit()
	else:
		print('Could not find meta.dat, initializing with today')
		prev_date = datetime.date.today()
	return prev_date

def write_meta_dat(filepath, curr_date):
	print('Writing meta.dat ...')
	try:
		with open(filepath, 'w') as f:
			f.write('{}.{}.{}'.format(curr_date.day, 
									  curr_date.month, 
									  curr_date.year))
	except:
		print('Could not write meta.dat')
		sys.exit()

def write_log(filepath, text):
	try:
		with open(filepath, 'a') as f:
			f.write(text + '\n')
	except:
		print('Writing history.log failed')
		sys.exit()


def parse_string2date(date_string):
	date_list = date_string.split('.')
	date = datetime.date(year=int(date_list[2]), \
						 month=int(date_list[1]), \
						 day=int(date_list[0]))
	return date

def parse_date2string(date):
	return '{}.{}.{}'.format(date.day, date.month, date.year)

def send_mail(person, subject, filepath):
	with open(filepath, 'r') as file:
		filedata = file.read()
		first_name = person['name'].split()[0]
		filedata = filedata.replace('$NAME', first_name)
		filedata = filedata.replace('$AGE', str(datetime.date.today().year - person['birthday'].year))
		ps = subprocess.Popen(("echo", filedata), stdout=subprocess.PIPE)
		first_name = person['email']
		subprocess.call(["mail","-s", subject, person['email']] , stdin=ps.stdout)
		return filedata

def hash_ident(ident):
	# This function returns at max 117 which is almost 4 months
	return (37*(ident+7) % 293 ) % 118

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--debug", help="Run in debug mode", action="store_true")
	args = parser.parse_args()

	# Set paths to location of source file, so symlinks can be used
	os.chdir(os.path.expanduser('~/Desktop/friendlymail'))
	path = os.getcwd()
	log_path = os.path.join(path, 'history.log')
	meta_path = os.path.join(path, 'meta.dat')
	people_path = os.path.join(path, 'people.csv')
	
	birthday_template_path = os.path.join(path, 'birthday_template.txt')
	message_path = os.path.join(path, 'recon_template.txt')

	# Read data base of people, comma separated with no spaces at the end
	people = read_people_csv(people_path);
	print_people(people)

	# Meta data contains previous execution date
	prev_date = read_meta_dat(meta_path)
	curr_date = datetime.date.today()
	print('Today is', parse_date2string(curr_date))
	if not args.debug:
		write_log(log_path, 'Execution on ' + parse_date2string(curr_date))

	### Birthday
	print('Checking for birthdays ...')
	for person in people:
		birthday_this_year = datetime.date(year=datetime.date.today().year,
									  month=person['birthday'].month,
									  day=person['birthday'].day)
		if birthday_this_year > prev_date and birthday_this_year <= curr_date:
			if not args.debug:
				output_mail = send_mail(person, 'Geburtstaggrüße', birthday_template_path)
				print(output_mail)
				write_log(log_path, 'Email sent to ' + person['name'] + ' ' + person['email'])
			print('Birthday email sent to', person['name'],  person['email'])

	### Reconnection
	print('Checking for reconnection events ...')
	for ident, person in enumerate(people):
		which_third_of_year = (curr_date.month - 1) // 4
		start_date = datetime.date(year=datetime.date.today().year, \
								  month=which_third_of_year*4+1, \
								  day=1)
		recon_date = start_date + datetime.timedelta(hash_ident(ident))
		if recon_date > prev_date and recon_date <= curr_date:
			if not argparse.debug:
				output_mail = send_mail(person, 'Grüße', message_path)
				print(output_mail)
				write_log(log_path, 'Email sent to ' + person['name'] + ' ' + person['email'])
			print('Recon email sent to', person['name'],  person['email'])

	if not args.debug:
		write_meta_dat(meta_path, curr_date)

''' Todos:
- Fill in friends' data
- Multiple birthday mail template with random selection
- Text Generator
- Add unit tests
'''

