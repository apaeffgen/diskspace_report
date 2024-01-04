#!/usr/bin/python3

# Import libraries that are needed
import locale
import shutil
from csv import DictWriter
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

import config


# Main function that controls what should be done
def main():
	total_space, used_space,percent_usedspace, free_space, percent_freespace = calculate_space()

	# Check the printing parameter
	if config.booL_print == True:
		show_values(total_space, used_space,percent_usedspace, free_space, percent_freespace)

	# Check the export parameter
	if config.bool_export == True:
		write_csv(total_space, used_space,percent_usedspace, free_space, percent_freespace)

	# Check the email parameter
	if config.bool_email == True:
		mail_results()

# Calculate the values of the disk (free, used, total + percentage)
def calculate_space():
	total, used, free = shutil.disk_usage("/")

	total_space = total // config.disk_factor
	free_space = free // config.disk_factor
	used_space = total_space - free_space
	percent_freespace = round(((free_space / total_space) * 100), ndigits=2)
	percent_usedspace = round(((used_space / total_space) * 100), ndigits=2)
		
	return total_space, used_space, percent_usedspace, free_space, percent_freespace

# Set the number format for the exported values. Settings in the header
def int_num(number, digits=2):
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
	dict = {'Date': config.actualtime, 'Space Abs (GB)': int_num(total_space), 'Space Free (GB)': int_num(free_space),
			'Percent Free': int_num(percent_freespace), 'Space Used (GB)': int_num(used_space),
			'Percent Used': int_num(percent_usedspace)}
	
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

# Print the calculated values to screen,
def show_values(total_space, used_space, percent_usedspace,free_space, percent_freespace):
	print("Disk Space Report from: " + str(config.actualtime))
	print("Total: %d GB" % total_space, " / 100 Percent")
	print("Used: %d GB" % used_space, " / %d Percent" % percent_usedspace)
	print("Free: %d GB" % free_space, " / %d Percent" % percent_freespace)


# Email the results
def mail_results():

	msg = MIMEMultipart('mixed')
	msg['From'] = config.sender
	msg['To'] = config.recipient
	msg['Subject'] = config.SUBJECT

	body = MIMEText(config.body)
	msg.attach(body)

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

# Start the  programm
main()