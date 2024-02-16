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
import pandas as pd




from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

# Try to import the configfile from different paths
try:
	from diskspace_report.pkg_helpers import config
except ImportError:
	pass
try:
	from pkg_helpers import config
except ImportError:
	pass

# Catch errors and check platform
def error_log():
	from pkg_helpers import config
	logging.basicConfig(filename=config.logfile, level=logging.DEBUG,
						format='%(asctime)s %(levelname)s %(name)s %(message)s')
	logger=logging.getLogger(__name__)
	return logger

def active_platform():
	running_platform = platform.system()
	return running_platform

# Main function that controls what should be done and the click parameter of the command line
@click.command()
@click.option("--editconfig", is_flag=True, help="Opens the config file for editing")
@click.option("--showinfo", is_flag=True,
			  help="Show the Package Information and some path information")
@click.option("--version", is_flag=True, help="Show the version number of the script")
@click.option("--showconfig", is_flag=True,
			  help="Show all the parameters configured in the configuration file")
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
		click.echo("Diskspace-Report Version: " + config.version)
		exit()

	elif (run is True):
		configuration()
	else:
		click.echo("Please make a valid choice or use --help")
		exit()

# Config the wanted output as of the configuration
def configuration():
	total_space, used_space, percent_usedspace, free_space, percent_freespace = calculate_space()

	# Check the printing parameter
	show_values(total_space, used_space, percent_usedspace, free_space, percent_freespace)

	# Check the export parameter
	if config.bool_export == True:
		write_csv(total_space, used_space, percent_usedspace, free_space, percent_freespace)

	# Check the email parameter
	if config.bool_email == True:
		mail_results()

# Show the configuration
def show_config():
	click.echo("Parameters of diskspace_report:")
	click.echo("__________________________")
	click.echo("Main Parameters:")
	click.echo("Print-Parameter: " + str(config.booL_print))
	click.echo("Report-Parameter: " + str(config.bool_export))
	click.echo("Email-Parameter: " + str(config.bool_email))
	click.echo("__________________________")
	click.echo("Report-Prameters:")
	click.echo("Filename / Path: " + config.csvfile)
	click.echo("Logfilename / Path: " + config.logfile)
	click.echo("Hostname: " + config.hostname)
	click.echo("__________________________")
	click.echo("Email-Parameters:")
	click.echo("Sender: " + str(config.sender))
	click.echo("Recipient: " + str(config.recipient))
	click.echo("MyUser: " + str(config.MY_USER))
	click.echo("MyPassword: xxxxxxxxxxx")
	click.echo("SMTP-Server: " + str(config.SMTP_SERVER))
	click.echo("SMTP_Port: " + str(config.SMTP_PORT))


# Calculate the values of the disk (free, used, total + percentage)
def calculate_space():
	total, used, free = shutil.disk_usage("/")

	total_space = total // config.disk_factor
	free_space = free // config.disk_factor
	used_space = total_space - free_space
	percent_freespace = round(((free_space / total_space) * 100), ndigits=2)
	percent_usedspace = round(((used_space / total_space) * 100), ndigits=2)
		
	return total_space, used_space, percent_usedspace, free_space, percent_freespace

# Set the number format for the exported values. Settings in the config file
def set_locale(number, digits=2):
	if number is None:
		return ""
	if not isinstance(number, int) and not isinstance(number, float):
		return ""
	else:
		format = '%.'+str(digits)+'f'
		return locale.format_string(format, number, 1)

# Export the calculates values to a csv-file. Pathsettings above
def write_csv(total_space, used_space, percent_usedspace, free_space,
			  percent_freespace):
	# Format the sequence of the rows in the exported csv-file
	field_names = ['Date', 'Space Abs (GB)', 'Space Free (GB)', 'Percent Free',
				   'Space Used (GB)', 'Percent Used']
	dict = {'Date': config.actualtime,
			'Space Abs (GB)': set_locale(total_space),
			'Space Free (GB)': set_locale(free_space),
			'Percent Free': set_locale(percent_freespace),
			'Space Used (GB)': set_locale(used_space),
			'Percent Used': set_locale(percent_usedspace)}

	# Check, if the file exists. Only write the header once
	if not os.path.exists(config.csvfile):
		with open(config.csvfile, 'w') as f_object:
			dictwriter_object = DictWriter(f_object, fieldnames=field_names, delimiter=';')
			dictwriter_object.writeheader()

			f_object.close()
	# Append new entries, at each run of the script
	with open(config.csvfile, 'a') as f_object:
		dictwriter_object = DictWriter(f_object, fieldnames=field_names, delimiter=';')
		dictwriter_object.writerow(dict)

		f_object.close()
	write_html()

def write_html():
	# Write the csv-Data into a html-File

	if os.path.exists(config.csvfile) is True:
		csv_file = pd.read_csv(config.csvfile, delimiter=";")
		csv_file.to_html(config.htmlfile , float_format='%s',  col_space = 20, max_rows=10, index=False,
						 columns= ["Date", "Space Used (GB)", "Space Free (GB)", "Percent Free"])
		print_html = pd.read_html(config.htmlfile, thousands=".")

		return print_html
	else:
		print("The first run does not contain any report data. Rerun the report again!")


# Print the calculated values to screen,
def show_values(total_space, used_space, percent_usedspace,free_space, percent_freespace):
	# Text and Variables to print.
	Text_ReportTitel = str("Disk Space Report from: " + str(config.actualtime))
	Text_SummeryDay = str("Summery:")
	Text_TotalSpace = str("Total Space: " + str(total_space) + " GB / 100 Percent")
	Text_UsedSpace = str("Used Space: " + str(used_space) + " GB / " + str(percent_usedspace) + " Percent")
	Text_FreeSpace = str("Free Space: " + str(free_space) + " GB / " + str(percent_freespace) + " Percent")
	Text_LastOverview = str("Overview of recent values:")

	# Format the Text for Console Output
	Report_Text = (
		  Text_ReportTitel + os.linesep + os.linesep +
		  Text_SummeryDay + os.linesep +
		  Text_TotalSpace + os.linesep +
		  Text_UsedSpace + os.linesep +
		  Text_FreeSpace + os.linesep)

	# Format the Output for HTML-Email
	global  Report_HTML
	newline_html = "<br>"

	Report_HTML = (
			Text_ReportTitel + newline_html + newline_html+
			Text_SummeryDay + newline_html +
			Text_TotalSpace + newline_html +
			Text_UsedSpace + newline_html +
			Text_FreeSpace + newline_html + newline_html)

	if config.booL_print == True:

		print(Report_Text)

		if config.bool_export == True:
			print(Text_LastOverview)
			print_html = write_html()
			print(print_html)

# Email the results
def mail_results():

	msg = MIMEMultipart('mixed')
	msg['From'] = config.sender
	msg['To'] = config.recipient
	msg['Subject'] = config.SUBJECT

	Report = MIMEText(Report_HTML, "html", "utf-8")
	msg.attach(Report)
	body = MIMEText(config.body, "html")
	msg.attach(body)

	if os.path.isfile(config.csvfile) is True:

		html_content = pd.read_csv(config.csvfile, delimiter=";")
		html_source = pd.DataFrame.to_html(html_content)
		msg.attach(MIMEText(html_source, "html"))

		part = MIMEBase('application', "octet-stream")
		part.set_payload(open(config.csvfile, "rb", ).read())

		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % config.csvfile)
		msg.attach(part)


	smtpObj = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
	smtpObj.ehlo()
	smtpObj.starttls()
	smtpObj.login(config.MY_USER, config.MY_PASSWORD)
	smtpObj.sendmail(config.sender, config.recipient, msg.as_string())
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
	config_file = os.path.join(os.path.dirname(__file__), 'pkg_helpers/config.py')

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
