# Project Diskspace-Report
A platform independent reporting tool for diskspace usage in time. Every time the script runs, it adds an entry of the actual diskspace to a specified csv file.
Over time you can analyse, where your diskspace goes.

The report csv-file can be emailed via your email account. The file can be set up as a service as well, so you will get automated reports via email.

## Installation
### Via PyPi.org

`pip install diskspace_report`

`pip show diskspace_report`

Afterwords, when no error occurred, diskspace_report binary is in your path and you can use it by invoking:
`diskspace_report --help`

### Via Source-Code on Github

1. Download and unpack the source-code (whereever you want)
2. Make sure python3 is installed and all relevant paths are in your path environment
3. Install the requirements:
```pip install -r requirements.txt ```

## Tested Platforms

1. Windows
2. MacOS
3. Linux
4. The script may run on every platform which supports python3. Some functionality like --editconfig may fail.

## Configuration

1. There is a config.py file to adjust the settings. You can edit the config with `diskspace_report --editconfig`
2. Email ist turned off by default. Parameters can be shown with `diskspace_report --showconfig`
3. You have to fill all required fields for the email to work and to switch on email report

### Testing the functionality

1. Test the script without email on the command line
2. When everything works, test it with email on the command line
3. Afterwords you can add it as a service and run it on a automated basis

### Menu functionality
```
Usage: diskspace_report [OPTIONS]

  Diskspace_Report: A tool to analyse and print / email the available
  diskspace to a csv file

Options:

--editconfig   Opens the config file for editing
--showinfo     Show the Package Information and some path information
--version      Show the version number of the script
--showconfig   Show all the parameters configured in the configuration file
--run BOOLEAN  Run the script. Defaults to True
--help         Show this message and exit.
```


