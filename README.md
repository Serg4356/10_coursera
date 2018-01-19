# Coursera Dump

Programm searches for courses on [coursera.org](https://www.coursera.org) and makes an excel file with list of courses and their common information(name, rating, amount of weeks, language)

# How to install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

# Quickstart

Programm takes path to folder as an argument. Like this:

```bash
$ python coursera.py G:\courses
```

Example of programm output:

```bash
https://www.coursera.org/learn/kennedy
{'name': 'The Kennedy Half Century | Coursera', 'average_grade': '4.6 stars', 'weeks_required': 'English', 'language': 'English', 'start': 'Starts Jan 29'}
```

Also you can find courses.xls file in specified folder(G:\courses\).

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
