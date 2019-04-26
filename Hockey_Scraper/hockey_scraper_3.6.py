__author__ = 'Nick Sarris (ngs5st)'

import pandas as pd
from bs4 import BeautifulSoup
import requests

def scrape_data():

    names = []
    teams = []
    positions = []

    cap_number_17_18 = []
    cap_number_18_19 = []

    salary_17_18 = []
    salary_18_19 = []
    salary_19_20 = []
    salary_20_21 = []
    salary_21_22 = []

    index = 0
    sessions = requests.session()

    while int(index/10) <= 1640:

        url = 'http://stats.nhlnumbers.com/players/index_griddle.json?year=2018&pageIndex=' + \
              str(int(index/10)) + '&perPage=10'
        response = sessions.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        table = list(soup.find_all('td'))

        if not table:
            index += 10

        for entry in table:
            if str(index)[-1] == '0':
                data = entry.find('a').contents
                data = str(data).replace('[', '')
                data = str(data).replace(']', '')
                data = str(data).replace("'", '')
                list.append(names, data)

            if str(index)[-1] == '1':
                data = entry.find('a').contents
                data = str(data).replace('[', '')
                data = str(data).replace(']', '')
                data = str(data).replace("'", '')
                list.append(teams, data)

            if str(index)[-1] == '2':
                data = entry.contents
                data = str(data).replace('[', '')
                data = str(data).replace(']', '')
                data = str(data).replace("'", '')
                list.append(positions, data)

            if str(index)[-1] == '3':
                data = entry.contents
                data = str(data).replace('[', '')
                data = str(data).replace(']', '')
                data = str(data).replace("'", '')
                list.append(cap_number_17_18, data)

            if str(index)[-1] == '4':
                data = entry.contents
                data = str(data).replace('[', '')
                data = str(data).replace(']', '')
                data = str(data).replace("'", '')
                list.append(cap_number_18_19, data)

            if str(index)[-1] == '5':
                data = entry.contents
                data = str(data).replace('[', '')
                data = str(data).replace(']', '')
                data = str(data).replace("\\\\n", '')
                data = str(data).replace("'", '')
                data = str(data).replace(' ', '')
                data = str(data).replace('\\xa0', '')
                list.append(salary_17_18, data)

            if str(index)[-1] == '6':
                data = entry.contents
                data = str(data).replace('[', '')
                data = str(data).replace(']', '')
                data = str(data).replace("\\\\n", '')
                data = str(data).replace("'", '')
                data = str(data).replace(' ', '')
                data = str(data).replace('\\xa0', '')
                list.append(salary_18_19, data)

            if str(index)[-1] == '7':
                data = entry.contents
                data = str(data).replace('[', '')
                data = str(data).replace(']', '')
                data = str(data).replace("\\\\n", '')
                data = str(data).replace("'", '')
                data = str(data).replace(' ', '')
                data = str(data).replace('\\xa0', '')
                list.append(salary_19_20, data)

            if str(index)[-1] == '8':
                data = entry.contents
                data = str(data).replace('[', '')
                data = str(data).replace(']', '')
                data = str(data).replace("\\\\n", '')
                data = str(data).replace("'", '')
                data = str(data).replace(' ', '')
                data = str(data).replace('\\xa0', '')
                list.append(salary_20_21, data)

            if str(index)[-1] == '9':
                data = entry.contents
                data = str(data).replace('[', '')
                data = str(data).replace(']', '')
                data = str(data).replace("\\\\n", '')
                data = str(data).replace("'", '')
                data = str(data).replace(' ', '')
                data = str(data).replace('\\xa0', '')
                list.append(salary_21_22, data)

            index += 1

    return names, teams, positions, cap_number_17_18, cap_number_18_19, \
           salary_17_18, salary_18_19, salary_19_20, salary_20_21, salary_21_22

def gen_output(names, teams, positions, cap_number_17_18, cap_number_18_19,
               salary_17_18, salary_18_19, salary_19_20, salary_20_21, salary_21_22):

    scraped_data = pd.DataFrame()
    scraped_data['name'] = names
    scraped_data['team'] = teams
    scraped_data['position'] = positions
    scraped_data['cap_number_17_18'] = cap_number_17_18
    scraped_data['cap_number_18_19'] = cap_number_18_19
    scraped_data['salary_17_18'] = salary_17_18
    scraped_data['salary_18_19'] = salary_18_19
    scraped_data['salary_19_20'] = salary_19_20
    scraped_data['salary_20_21'] = salary_20_21
    scraped_data['salary_21_22'] = salary_21_22
    scraped_data.to_csv('hockey_output_3.6.csv', index=False)

if __name__ == '__main__':

    names, teams, positions, cap_number_17_18, cap_number_18_19, \
    salary_17_18, salary_18_19, salary_19_20, salary_20_21, \
    salary_21_22 = scrape_data()

    gen_output(names, teams, positions, cap_number_17_18, cap_number_18_19,
    salary_17_18, salary_18_19, salary_19_20, salary_20_21,
    salary_21_22)