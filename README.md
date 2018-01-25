# Coursera Dump

Programm searches for courses on [coursera.org](https://www.coursera.org) and makes an excel file with list of courses and their common information(name, rating, amount of weeks, language)

# How to install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

# Quickstart

Programm takes path to folder and need of console output as arguments. For detailed information call -h (--help):

```bash
$ python coursera.py -h
usage: coursera.py [-h] [-d DISPLAY] [-o OUTPUT]

Programm searches for courses information on coursera.org, and outputs them
into Excel file

optional arguments:
  -h, --help            show this help message and exit
  -d DISPLAY, --display DISPLAY
                        input True to display parsing result
  -o OUTPUT, --output OUTPUT
                        path to result file
```

Example of programm output:
```bash
$ python coursera.py -o C:\devman -d True
https://www.coursera.org/learn/job-interview-capstone
name - How To Land the Job You Want (Capstone Project) | Coursera
average_grade - None
weeks required - 8 weeks of study, 3-4 hours/week
language - English
start - Starts Feb 05

https://www.coursera.org/learn/network-security-communications-sscp
name - Networks and Communications Security | Coursera
average_grade - None
weeks required - None
language - English
start - Starting 19 March
```

After the completion of the program you can find courses.xls file in specified folder(G:\courses).

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

