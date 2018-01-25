import requests
import openpyxl
from lxml import etree
from bs4 import BeautifulSoup
import sys
import os
import argparse


def get_courses_link_list(courses_number, http_response):
    etree_courses = etree.fromstring(http_response.content)
    courses_link_list = []
    for child in etree_courses.getchildren():
        courses_link_list.append(child.getchildren()[0].text)
    return courses_link_list[-courses_number:]


def get_course_info(course_attr_names, http_response):
    soup = BeautifulSoup(http_response.text, 'html.parser')
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
    for column, course_attr_name in enumerate(course_attr_names, start=2):
        work_sheet.cell(row=1, column=column).value = course_attr_name
    for row, course in enumerate(courses_info, start=2):
        for column, key in enumerate(course.keys(), start=2):
            work_sheet.cell(row=row, column=1).value = row
            work_sheet.cell(row=row, column=column).value = course[key]
    return courses_workbook


def get_http_response(link):
    return requests.get(link)


def create_parser():
    parser = argparse.ArgumentParser(
        description='Programm searches for courses '
                    'information on coursera.org, and '
                    'outputs them into Excel file')
    parser.add_argument('-d',
                        '--display',
                        type=bool,
                        default=False,
                        help='input True to display parsing result')
    parser.add_argument('-o',
                        '--output',
                        default='',
                        help='path to result file')
    return parser


def prettify_output(course_info):
    course_info_str = ''
    for course_attr in course_info:
        course_info_str += '{} - {}\n'.format(
            course_attr,
            course_info[course_attr])
    return course_info_str


if __name__ == '__main__':
    parser = create_parser()
    courses_number = 20
    course_attr_names = ['name',
                         'average grade',
                         'weeks required',
                         'language',
                         'start']
    http_response_links = get_http_response(
        'https://www.coursera.org/sitemap~www~courses.xml')
    courses_link_list = get_courses_link_list(
        courses_number,
        http_response_links)
    courses_info = []
    for course in courses_link_list:
        http_response_course_info = get_http_response(course)
        if parser.parse_args().output:
            print(course)
            print(
                prettify_output(
                    get_course_info(
                        course_attr_names,
                        http_response_course_info)))
        courses_info.append(
            get_course_info(course,
                            http_response_course_info))
    try:
        courses_book = output_courses_info_to_xls(
            courses_info,
            course_attr_names)
        courses_book.save(
            os.path.join(
                parser.parse_args().output,
                'courses.xls'))
    except IndexError:
        print('Error! Input path to folder.')
    except PermissionError:
        print('Error! Please, close target excel file')
