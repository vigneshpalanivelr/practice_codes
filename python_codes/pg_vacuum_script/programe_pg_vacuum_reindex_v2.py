#!/usr/bin/env python
# -*- encoding: utf-8
'''
# Job Description:
	Clone the repo with input details
	Set crontab to run on every weekend for Vacuum
	Sending Mail notification

# Step 1 : Importing require modules
	module os				: to pass arguments from environment
	module sys				: to pass arguments from command line
	module psycopg2				: postgres client tool on python
	module HTML_py				: converting Nested list to HTML Table
	module smtplib				: sending email communication
	module argparse				: reading command line arguments
	module email.mime.multipart		:
	module email.mime.text			:
	module datetime				: to use time calculation on the script

# Step 2 : Defining Classes emailCommunication and vacuumFullReindex

# Step 3 : Class "vacuumFullReindex" with Methods
	Method sending_email_notification	: Will send the mail notofication
	
# Step 4 : Class "vacuumFullReindex" with Methods
	Method __init__				: contructor will connect to the database by default
	Method get_tables_query			: to define a query varies from whole (DB | schemas | table)
	Method get_table			: using above query will yield table one-by-one
	Method get_vaccum_query			: define a query according to our job (vacuum | vacuum full | reindex)
	Method executer				: execute the above job [the output will be saved to "self.conn.notices" list] 
	Method html_data_conversion		: converting nested list into HTML Data
	Method sending_email_notification	: sending HTML data in mail
'''

import os
import sys
import psycopg2
import HTML
import smtplib
import argparse		   
from   email.mime.multipart import MIMEMultipart
from   email.mime.text import MIMEText
from   datetime import datetime

# Defining Variables
vacuum_status = list()

class emailCommunication():
	def sending_email_notification(self,text_data,html_data=None):
		#Declare Class variables
		subject		= "Weekly Maintanence Job on Postgres RDS - "
		from_address	= "vignesh1650@gmail.com"
		to_address	= "vignesh1650@gmail.com"
		mail_password	= "p0$t9r3$"
		
		msg		= MIMEMultipart()
		msg['Subject']	= subject + database + '-' +job
		msg['From']	= from_address
		msg['To']	= to_address
		part1		= MIMEText(text_data, 'plain', 'utf-8')
		msg.attach(part1)
		if html_data:
			part2	= MIMEText(html_data, 'html', 'utf-8')
			msg.attach(part2)
		mail		= smtplib.SMTP('smtp.gmail.com', 587)
		mail.ehlo()
		mail.starttls()
		mail.login(from_address, mail_password)
		mail.sendmail(from_address, to_address, msg.as_string())
		mail.quit()


class vacuumFullReindex(object):
    
	def __init__(self):
		"""
		Connect to Postgre database.
		"""
		self.vacuum_status = list()
		try:
			self.conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (database, user, host, password))
			self.text_data  = "Connected to Instance \t\t\t: %s \n" % (host)
			self.text_data += "Connected to Database \t\t\t: %s \n" % (database)
			self.text_data += "Connected as Username \t\t\t: %s \n" % (database)
		except Exception as e:
			self.text_data = "Error : Unable to connect to PostgreSQL Instance : %s" % (host)
			m.sending_email_notification(self.text_data)
			sys.exit (100)

	def get_tables_query(self):
		"""
		Get the correct query to do the job against database
		"""
		if schema and table:
			query = """
				SELECT nsp.nspname ||'.'||relname
				FROM pg_class c
				INNER JOIN pg_namespace nsp ON relnamespace = nsp.oid
				WHERE 
					c.relkind in ('r','m') 
					AND nsp.nspname = '{schema}' AND relname = '{table}'
					AND nsp.nspname NOT LIKE 'pg\_%' 
					AND nsp.nspname NOT IN ('information_schema')""".format(schema=schema,table=table)
			self.text_data += "Starting "+ job + " on the Table "+ table + "\n\n"
			
		elif schema:
			query = """
				SELECT nsp.nspname ||'.'||relname
				FROM pg_class c
				INNER JOIN pg_namespace nsp ON relnamespace = nsp.oid
				WHERE 
					c.relkind in ('r','m') 
					AND nsp.nspname = '{schema}'
					AND nsp.nspname NOT LIKE 'pg\_%' 
					AND nsp.nspname NOT IN ('information_schema')""".format(schema=schema)
			self.text_data += "Starting "+ job + " on the Schema : " + schema + "\n\n"
			
		else:
			query = """
				SELECT nsp.nspname ||'.'||relname
				FROM pg_class c
				INNER JOIN pg_namespace nsp ON relnamespace = nsp.oid
				WHERE 
					c.relkind in ('r','m')
					AND nsp.nspname NOT LIKE 'pg\_%' 
					AND nsp.nspname NOT IN ('information_schema')"""
			self.text_data += "Starting "+ job + " on the Database : " + database + "\n\n"
		#return query
		return v.get_table(query)

	def get_table(self,query):
		"""
		Get all tables and return the value using generator function gives set
		"""
		try:
			cursor = self.conn.cursor()
			cursor.execute(query)
		except psycopg2.Error:
			m.sending_email_notification(self.text_data)
		
		for i in cursor.fetchall():
			yield(i[0])

	def get_vaccum_query(self, table):
		"""
		Run Vacuum on a given table.
		"""
		if job == 'VACUUM':
			query = "VACUUM VERBOSE ANALYZE %s;" % (table)
		elif job == "VACUUM-FULL":
			query = "VACUUM FULL VERBOSE ANALYZE %s;" % (table)
		if job == "REINDEX":
			query = "REINDEX TABLE %s;" % table
		#return query,table
		v.executer(query,table)

	def executer(self,query,table):
		"""
		VACUUM can not run in a transaction block, which psycopg2 uses by default.
		http://bit.ly/1OUbYB3
		Then Setting isolation_level back to normal
		"""
		
		message = ['%s' %(datetime.now().strftime('%a %b %d %H:%M:%S')), job ,table]
		
		isolation_level = self.conn.isolation_level
		self.conn.set_isolation_level(0)
		
		try:
			cursor = self.conn.cursor()
			cursor.execute(query)
			message.append('Success')
		except psycopg2.Error as e:
			#message.append('Failed ! {}'.format(str(sys.exc_info())))
			message.append('Failure! - Error : {}'.format(e))
		
		self.conn.set_isolation_level(isolation_level)
		
		self.vacuum_status.append(message)
		 
		#This block is to recursively provide the notices from database
		#for element in self.conn.notices:
			#yield (element)

	def html_data_conversion(self):
		resultant_colors = {
			'Success': '#3CB371',
			'Failure': '#FFA07A'
		}

		htmlcode = HTML.Table(
			header_row=['Time','Job','Table','Status'],
			style="border: 3px solid #000000; border-collapse: collapse;",
			cellpadding="8"
		)
		for i in self.vacuum_status:
			for j in resultant_colors:
				if i[3].find(j) > -1:
					coloured_row	= HTML.TableRow(i,attribs={'bgcolor': j})
			htmlcode.rows.append(coloured_row)
		return self.text_data,htmlcode

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description = 'DB status & Weekly Maintanence Job for Postgres RDS')
	parser.add_argument('host',	action='store',	help='R53 Host Address')
	parser.add_argument('database',	action='store',	help='Database')
	parser.add_argument('user',	action='store',	help='Username')
	parser.add_argument('password',	action='store',	help='Password')
	parser.add_argument('--job',	action='store',	dest='job',	help='Default Value = "VACUUM" ;;',default='VACUUM',choices=["VACUUM","VACUUM-FULL","REINDEX"])
	parser.add_argument('--schema',	action='store',	dest='schema',	help='Provide Schema Name ;; If no Schema Provided, then Job will run in All the Schemas and Tables')
	parser.add_argument('--table',	action='store',	dest='table',	help='Provide Table Name ;; If no Table Provided, then Job will run in All the Tables')
	
	#Argument Testing
	#args		= parser.parse_args(['postgres.clsd7wqaeoew.ap-south-1.rds.amazonaws.com','postgres','postgres','postgres','--job','REINDEX'])
	#Argument Passing
	args		= parser.parse_args()
	#parser.print_help()
	host		= args.host
	database	= args.database
	user		= args.user
	password	= args.password
	job		= args.job
	schema		= None if args.schema == "None" else args.schema
	table		= None if args.table == "None" else args.table
	#print host,database,user,password,job,schema,table
	#creating class object
	m		= emailCommunication()
	v		= vacuumFullReindex()
 
	"""
	Get the one-by-one table name by SQL query using yield generator with one element set
	Passing the table create vacuum or vacuum-full or reindex query
	Execute the query against the database
	"""

	for j in v.get_tables_query():
		v.get_vaccum_query(j)
		#for notice in v.executer(vacuum_query,vacuum_table):
		#	print (notice)
		
	text_data, htmlcode = v.html_data_conversion()
	m.sending_email_notification(text_data,str(htmlcode))
