#!/usr/bin/python3
import locale, os, time
############ Start of Configuration ######################
##########################################################
version = "0.3.2"
# Parameters to configure the output
booL_print = True
bool_export = True
bool_email = True

# Control the path, filename and host
csvfile = "Diskusage_list.csv"
htmlfile = "Diskusage_list.html"
logfile = "Diskusage_log.txt"
hostname = "Macbook-Air"

# Format of the time and number format
actualtime = time.strftime("%d.%m.%Y,%H:%M:%S")
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

# Email-Parameters:
sender = 'mail@example.com'
recipient = 'reciepient@example.com'
MY_USER = 'Username'
MY_PASSWORD = 'Password'
SMTP_SERVER = 'Mailserver-Hostname'
SMTP_PORT = 587

# Report Parameters
SUBJECT = 'Disk Space Report'

# Body Text as HTML
body = ('Diskspace Report from: ' + str(hostname) + ' at the date of ' + str(actualtime) + "<br>"
			+ 'Attached will be the disk usage report as a csv-file, if you configured it in the config file' + "<br>")

# Calculation factor to meet the different disk form factors
disk_factor = (2**29.9)


############# End of Configuration ######################
#########################################################
