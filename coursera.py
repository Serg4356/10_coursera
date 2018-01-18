import requests
import openpyxl
from lxml import etree
from bs4 import BeautifulSoup


def get_courses_list():

    response = requests.get('https://www.coursera.org/sitemap~www~courses.xml')
    etree_courses = etree.fromstring(response.content)
    courses_list = []
    for child in etree_courses.getchildren():
        courses_list.append(child.getchildren()[0].text)
    return courses_list[-20:]


'''
# name
# language
# date of start
# weeks needed 
# average grade
'''


def get_course_info(course_link):
    response = requests.get(course_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    print()
    course_info = {'name': soup.title.string,
                   'average grade': soup.find('div', attrs={'class': 'ratings-text bt3-visible-xs'}).find('span').text,
                   'weeks_required': soup.find('table', attrs={
                       'class': 'basic-info-table bt3-table bt3-table-striped bt3-table-bordered bt3-table-responsive'
                   }).find_all('td')[3].text,
                   'language': soup.find('table', attrs={
                       'class': 'basic-info-table bt3-table bt3-table-striped bt3-table-bordered bt3-table-responsive'
                   }).find('div', attrs={'class': 'rc-Language'}).text,
                   'start': soup.find('div', attrs='startdate rc-StartDateString caption-text').text
                   }
    return course_info


def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    courses_list = get_courses_list()
    print(courses_list[0])
    print(get_course_info(courses_list[0]))
