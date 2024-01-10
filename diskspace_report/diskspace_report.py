#!/usr/bin/python3

# Import libraries that are needed
import platform
import locale
import shutil
import sysconfig
from csv import DictWriter
import sys, os
import smtplib
import logging
import click
import subprocess

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

def error_log():
	logging.basicConfig(filename='diskspace_report.log', level=logging.DEBUG,
						format='%(asctime)s %(levelname)s %(name)s %(message)s')
	logger=logging.getLogger(__name__)
	return logger

try:
	from  diskspace_report.pkg_helpers import config_report
except ImportError:
	error_log()
try:
	from pkg_helpers import config_report
except ImportError:
	error_log()

def active_platform():
	running_platform = platform.system()
	return running_platform

# Main function that controls what should be done and the click parameter of the command line
@click.command()
@click.option("--editconfig", is_flag=True, help="Opens the config file for editing")
@click.option("--showinfo", is_flag=True, help="Show the Package Information and some path information")
@click.option("--version", is_flag=True, help="Show the version number of the script")
@click.option("--showconfig", is_flag=True, help="Show all the parameters configured in the configuration file")
@click.option("--run", default=True, help="Run the script. Defaults to True")
def main(run,editconfig,version,showinfo,showconfig):
	'''
	Diskspace_Report:
	A tool to analyse and print / email the available diskspace to a csv file
	'''

	if (run is True) and (showconfig is True):
		show_config()
		exit()

	elif (run is True) and (showinfo is True):
		show_info()
		exit()
	elif (run is True) and (editconfig is True):
		running_platform = active_platform()
		edit_config(running_platform)

	elif (run is True) and (version is True):
		click.echo("Diskspace-Report Version: " + config_report.version)
		exit()

	elif (run is True):
		configuration()
	else:
		click.echo("Please make a valid choise or use --help")
		exit()

# Check on which platform runs the script




# Config the wanted output as of the configuration
def configuration():
	total_space, used_space, percent_usedspace, free_space, percent_freespace = calculate_space()

	# Check the printing parameter
	if config_report.booL_print == True:
		show_values(total_space, used_space, percent_usedspace, free_space, percent_freespace)

	# Check the export parameter
	if config_report.bool_export == True:
		write_csv(total_space, used_space, percent_usedspace, free_space, percent_freespace)

	# Check the email parameter
	if config_report.bool_email == True:
		mail_results()

# Show the configuration
def show_config():
	click.echo("Parameters of diskspace_report:")
	click.echo("__________________________")
	click.echo("Main Parameters:")
	click.echo("Print-Parameter: " + str(config_report.booL_print))
	click.echo("Report-Parameter: " + str(config_report.bool_export))
	click.echo("Email-Parameter: " + str(config_report.bool_email))
	click.echo("__________________________")
	click.echo("Report-Prameters:")
	click.echo("Filename / Path: " + config_report.csvfile)
	click.echo("Hostname: " + config_report.hostname)
	click.echo("__________________________")
	click.echo("Email-Parameters:")
	click.echo("Sender: " + str(config_report.sender))
	click.echo("Recipient: " + str(config_report.recipient))
	click.echo("MyUser: " + str(config_report.MY_USER))
	click.echo("MyPassword: xxxxxxxxxxx")
	click.echo("SMTP-Server: " + str(config_report.SMTP_SERVER))
	click.echo("SMTP_Port: " + str(config_report.SMTP_PORT))


# Calculate the values of the disk (free, used, total + percentage)
def calculate_space():
	total, used, free = shutil.disk_usage("/")

	total_space = total // config_report.disk_factor
	free_space = free // config_report.disk_factor
	used_space = total_space - free_space
	percent_freespace = round(((free_space / total_space) * 100), ndigits=2)
	percent_usedspace = round(((used_space / total_space) * 100), ndigits=2)
		
	return total_space, used_space, percent_usedspace, free_space, percent_freespace

# Set the number format for the exported values. Settings in the config file
def set_locale(number, digits=2):
    if number is None:
        return ''
    if not isinstance(number, int) and not isinstance(number, float):
        return ''
    else:
        format = '%.'+str(digits)+'f'
        return locale.format_string(format, number, 1)

# Export the calculates values to a csv-file. Pathsettings above
def write_csv(total_space, used_space, percent_usedspace, free_space,  percent_freespace):
	# Format the sequence of the rows in the exported csv-file
	field_names = ['Date','Space Abs (GB)','Space Free (GB)','Percent Free', 'Space Used (GB)', 'Percent Used' ]
	dict = {'Date': config_report.actualtime, 'Space Abs (GB)': set_locale(total_space), 'Space Free (GB)': set_locale(free_space),
			'Percent Free': set_locale(percent_freespace), 'Space Used (GB)': set_locale(used_space),
			'Percent Used': set_locale(percent_usedspace)}
	
	# Check, if the file exists. Only write the header once
	if not os.path.exists(config_report.csvfile):
		with open(config_report.csvfile, 'w') as f_object:
			dictwriter_object = DictWriter(f_object, fieldnames=field_names, delimiter=';')
			dictwriter_object.writeheader()
			f_object.close()
	# Append new entries, at each run of the script
	with open(config_report.csvfile, 'a') as f_object:
		dictwriter_object = DictWriter(f_object, fieldnames=field_names, delimiter=';')
		dictwriter_object.writerow(dict)
		f_object.close()

# Print the calculated values to screen,
def show_values(total_space, used_space, percent_usedspace,free_space, percent_freespace):
	print("Disk Space Report from: " + str(config_report.actualtime))
	print("Total: %d GB" % total_space, " / 100 Percent")
	print("Used: %d GB" % used_space, " / %d Percent" % percent_usedspace)
	print("Free: %d GB" % free_space, " / %d Percent" % percent_freespace)


# Email the results
def mail_results():

	msg = MIMEMultipart('mixed')
	msg['From'] = config_report.sender
	msg['To'] = config_report.recipient
	msg['Subject'] = config_report.SUBJECT

	body = MIMEText(config_report.body)
	msg.attach(body)

	part = MIMEBase('application', "octet-stream")
	part.set_payload(open(config_report.csvfile, "rb", ).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % config_report.csvfile)
	msg.attach(part)

	smtpObj = smtplib.SMTP(config_report.SMTP_SERVER, config_report.SMTP_PORT)
	smtpObj.ehlo()
	smtpObj.starttls()
	smtpObj.login(config_report.MY_USER, config_report.MY_PASSWORD)
	smtpObj.sendmail(config_report.sender, config_report.recipient, msg.as_string())
	smtpObj.quit()


def show_info():
	print("Package-Information of diskspace_report")
	click.echo("__________________________")
	subprocess.run(["pip", "show", "diskspace_report"])
	click.echo("__________________________")
	print("Attached some general path information: ")
	print(sysconfig.get_path("purelib"))
	print(sys.path)
	click.echo("__________________________")

def edit_config(running_platform):
	config_file = os.path.join(os.path.dirname(__file__), 'pkg_helpers/config_report.py')

	if (running_platform == "Linux") or (running_platform == "Darwin"):
		print("Your config file path is: ")
		print(config_file)
		subprocess.run(["vim", config_file])
	if (running_platform == "Windows"):
		print("Your config file path is: ")
		print(config_file)
		subprocess.run(["notepad", config_file])



# Start the  programm
if __name__ == "__main__":
	main()
