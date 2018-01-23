import requests
import openpyxl
from lxml import etree
from bs4 import BeautifulSoup
import sys


def get_courses_list(courses_number):
    response = requests.get('https://www.coursera.org/sitemap~www~courses.xml')
    etree_courses = etree.fromstring(response.content)
    courses_list = []
    for child in etree_courses.getchildren():
        courses_list.append(child.getchildren()[0].text)
    return courses_list[-courses_number:]


def get_course_info(course_link, course_attr_names):
    response = requests.get(course_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    course_info = {}
    course_info[course_attr_names[0]] = soup.title.string
    try:
        course_info[course_attr_names[1]] = soup.find(
            'div',
            attrs={'class': 'ratings-text bt3-visible-xs'}
        ).find('span').text
    except AttributeError:
        course_info['average_grade'] = 'Course grade not found'
    course_info[course_attr_names[2]] = soup.find(
        'table',
        attrs={'class': 'basic-info-table bt3-table bt3-table-striped bt3-table-bordered bt3-table-responsive'
    }).find_all('td')[3].text,
    course_info[course_attr_names[3]] = soup.find(
        'table',
        attrs={'class': 'basic-info-table bt3-table bt3-table-striped bt3-table-bordered bt3-table-responsive'}
    ).find('div', attrs={'class': 'rc-Language'}).text,
    course_info[course_attr_names[4]] = soup.find('div', attrs='startdate rc-StartDateString caption-text').text

    return course_info


def output_courses_info_to_xlsx(courses_info, course_attr_names):
    courses_workbook = openpyxl.Workbook()
    work_sheet = courses_workbook.create_sheet('coursera_courses')
    row = 1
    for course_attr_name in course_attr_names:
        work_sheet.cell(row=1, column=column).value = course_attr_name
        column += 1
    for course in courses_info:
        row += 1
        column = 2
        for property_key, property_value in course.items():
            work_sheet.cell(row=row, column=1).value = row - 1
            work_sheet.cell(row=row, column=column).value = property_value
            column += 1
    return courses_workbook


if __name__ == '__main__':
    courses_number = 20
    course_attr_names = ['name', 'average grade', 'weeks required', 'language', 'start']
    courses_list = get_courses_list(courses_number)
    courses_info = []
    for course in courses_list:
        print(course)
        print(get_course_info(course))
        courses_info.append(get_course_info(course, course_attr_names))
    try:
        courses_book = output_courses_info_to_xlsx(courses_info)
        courses_book.save('{}\courses.xls'.format(sys.argv[1]))
    except IndexError:
        print('Error: Input path to folder.')
