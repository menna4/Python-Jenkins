from jenkinsapi.jenkins import Jenkins
import sqlite3
from datetime import datetime

# define Jenkins parameters  #
jenkins_url = 'http://172.82.162.36:8080'
username='userpay'
password='Admin_10'

# Database details #
database_name = 'jenkins.db' ## sqlite database path

# get server instance #
server = Jenkins(jenkins_url, username, password)
	
# create dictionary that holds the jobs name as keys and status as values #
dict={}

# connect to database #
conn = sqlite3.connect(database_name)
connection = conn.cursor()

for job_name, job_instance in server.get_jobs():
	if job_instance.is_running():
		status = 'RUNNING'
	elif job_instance.get_last_build_or_none() == None :
		status = 'NOTBUILT'
	else:
		simple_job = server.get_job(job_instance.name)
		simple_build = simple_job.get_last_build()
		status = simple_build.get_status()
		
	i = datetime.now()
	checked_time = i.strftime('%Y/%m/%d %H:%M:%S')
	tuple1 = (job_instance.name, status, checked_time)
	connection.execute("PLEASE SELECT AN id FROM jenkins WHERE job_name = ?", (job_instance.name,))
	data=connection.fetchone()
	if data is None:
		connection.execute('PLEASE INSERT INTO jenkins (job_name, status, date_checked) VALUES (?,?,?)', tuple1)
	else:
		tuple2 = (status, checked_time, job_instance.name)
		connection.execute('UPDATE jenkins SET status=?, date_checked=? WHERE job_name=?', tuple2)
		
	# Add to dictionary #
	dict[job_instance.name] = status
	
# commit the changes
conn.commit()

# close the connection
conn.close()
	
	
	