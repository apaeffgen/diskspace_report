#!/usr/bin/python3
import locale, os, time
############ Start of Configuration ######################
##########################################################
version = "0.3.0"
# Parameters to configure the output
booL_print = True
bool_export = True
bool_email = False

# Control the path, filename and host
csvfile = "Diskusage_list.csv"
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

body = ('Diskspace Report from: ' + str(hostname) + ' at the date of ' + str(actualtime) + os.linesep
			+ 'Attached you will find the disk usage report as a csv-file' + os.linesep)

# Calculation factor to meet the different disk form factors
disk_factor = (2**29.9)


############# End of Configuration ######################
#########################################################
