import requests
import openpyxl
from lxml import etree
from bs4 import BeautifulSoup
import sys


def get_courses_link_list(courses_number):
    response = get_http_response('https://www.coursera.org/sitemap~www~courses.xml')
    etree_courses = etree.fromstring(response.content)
    courses_link_list = []
    for child in etree_courses.getchildren():
        courses_link_list.append(child.getchildren()[0].text)
    return courses_link_list[-courses_number:]


def get_course_info(course_link, course_attr_names):
    response = get_http_response(course_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    course_info = {}
    course_info[course_attr_names[0]] = soup.title.string
    try:
        course_info[course_attr_names[1]] = soup.find(
            'div',
            attrs={'class': 'ratings-text bt3-visible-xs'}
        ).find('span').text
    except AttributeError:
        course_info['average_grade'] = None
    try:
        course_info[course_attr_names[2]] = soup.find(
            'table',
            attrs={'class': 'basic-info-table '
                            'bt3-table bt3-table-striped '
                            'bt3-table-bordered bt3-table-responsive'}).find(
            'i',
            attrs={'class': 'cif-clock'}).parent.parent.find(
            'td',
            attrs={'class': 'td-data'}).text
    except AttributeError:
        course_info[course_attr_names[2]] = None
    course_info[course_attr_names[3]] = soup.find(
        'table',
        attrs={'class': 'basic-info-table bt3-table bt3-table-striped '
                        'bt3-table-bordered bt3-table-responsive'}
    ).find('div', attrs={'class': 'rc-Language'}).text
    course_info[course_attr_names[4]] = soup.find(
        'div',
        attrs='startdate rc-StartDateString caption-text').text

    return course_info


def output_courses_info_to_xls(courses_info, course_attr_names):
    courses_workbook = openpyxl.Workbook()
    work_sheet = courses_workbook.create_sheet('coursera_courses')
    for column, course_attr_name in enumerate(course_attr_names):
        work_sheet.cell(row=1, column=column+2).value = course_attr_name
    for row, course in enumerate(courses_info):
        for column, key in enumerate(course.keys()):
            work_sheet.cell(row=row + 2, column=1).value = row
            work_sheet.cell(row=row + 2, column=column+2).value = course[key]
    return courses_workbook


def get_http_response(link):
    return requests.get(link)


if __name__ == '__main__':
    courses_number = 20
    course_attr_names = ['name',
                         'average grade',
                         'weeks required',
                         'language',
                         'start']
    courses_link_list = get_courses_link_list(courses_number)
    courses_info = []
    for course in courses_link_list:
        print(course)
        print(get_course_info(course, course_attr_names))
        courses_info.append(get_course_info(course, course_attr_names))
    try:
        courses_book = output_courses_info_to_xls(
            courses_info,
            course_attr_names)
        courses_book.save('{}\courses.xls'.format(sys.argv[1]))
    except IndexError:
        print('Error! Input path to folder.')
    except PermissionError:
        print('Error! Please, close target excel file')
