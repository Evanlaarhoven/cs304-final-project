#!/usr/local/bin/python2.7
'''Author: Emily Van Laarhoven Marissa Okoli
   CS 304 OddJobs Beta
   showJobs.py
Helper module for flask application to retrieve listed jobs from database
Contains functions for connecting to the database port:7332	
'''

import sys
import MySQLdb
import dbconn2
import db_curs
from oddjobs_dsn import DSN

def getJobs(cursor,zipcode):
	'''Returns a list of jobs, optional filter by location (zip code)'''
	if zipcode == None:
		cursor.execute('select jid,title,dt,location,pay from job where available=1')
	else:
		cursor.execute('select jid,title,dt,location,pay from job where available=1 and location=%s;',[zipcode])
	lines = []
	while True:
		row = cursor.fetchone()
		if row == None:
			return lines
		lines.append('{jid} {title} {dt} {location} ${pay}'.format(**row))
	
#def main():
	'''Checks if actor is in database, if not inserts actor and returns success message,
#    else returns message saying actor is already in the database'''
#    return getJobs(db_curs.cursor()) ##Emily commented out Marissa code - don't need
	
if __name__ == '__main__':
	print main()
