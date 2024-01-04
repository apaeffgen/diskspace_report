# Project Diskspace-Report
A platform independent reporting tool for diskspace usage in time. Every time the script runs, it adds an entry of the actual diskspace to a csv file.
Over time you can analye, where your diskspace goes.

The report csv-file can be emailed via your email account. The file can be set up as a service as well, so you will get automated reports via email.

## Installation
### Via PyPi.org

pip install diskspace-report

### Via Source-Code on Github

1. Download and unpack the source-code (whereever you want)
2. Make sure python3 is installed
3. Install the requirements:
```pip install -r requirements.txt ```

## Supported Platforms (tested)

1. Windows
2. MacOS
3. Linux

## Configuration

1. There is a config.py file to adjust the settings.
2. Email ist turned off by default
3. You have to fill all required fields for the email to work and to switch on email

### Testing the funcitonality

1. Test the script without email on the command line
2. When everything works, test it with email on the command line

## Installing as a service

Coming soon
