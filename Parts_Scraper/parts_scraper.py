__author__ = 'Nick Sarris (ngs5st)'

import re
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

def _save(fname, data):
    with open(fname, "w") as f:
        for s in data:
            f.write(str(s) + "\n")


def _load(fname):
    data = []
    with open(fname, "r") as f:
        for line in f:
            data.append(line.strip())
    return data

def scrape_data(scraper, make, model, engine, year, data, identifiers):

    car_url = 'http://www.mpdonline.co.uk/ajax.php?x=setVehicle'
    parts_url = 'http://www.mpdonline.co.uk/car-parts'

    headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US,en;q=0.8',
        'Connection':'keep-alive',
        'Content-Length':'53',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':'PHPSESSID=4jdc6siog2jueoealhusfm0je0; '
                 '__utmt=1; '
                 '__utma=240008415.2137967596.1501708623.1501708623.1501712459.2; '
                 '__utmb=240008415.6.10.1501712459; '
                 '__utmc=240008415; '
                 '__utmz=240008415.1501708623.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        'Host':'www.mpdonline.co.uk',
        'Origin':'http://www.mpdonline.co.uk',
        'Referer':'http://www.mpdonline.co.uk/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/59.0.3071.115 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
    }

    payload = {
        'make': make,
        'model': model,
        'submodel': '',
        'engine': engine,
        'year': year
    }

    response = scraper.post(car_url, data=payload, headers=headers)

    headers = {
        'Accept': 'text/html,application/xhtml+xml,'
                  'application/xml;q=0.9,image/webp,'
                  'image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=4jdc6siog2jueoealhusfm0je0; '
                  '__utmt=1; '
                  '__utma=240008415.2137967596.1501708623.1501708623.1501712459.2; '
                  '__utmb=240008415.6.10.1501712459; '
                  '__utmc=240008415; '
                  '__utmz=240008415.1501708623.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        'Host': 'www.mpdonline.co.uk',
        'Referer': 'http://www.mpdonline.co.uk/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/59.0.3071.115 Safari/537.36',
    }

    response = scraper.get(parts_url, headers=headers)
    parts_list = ['air-filters','oil-filters','fuel-filters','brake-pads','spark-plugs-and-glow-plugs',
                  'wiper-blades','cabin-filters','engine-oil','fan-belts','brake-discs','brake-drums',
                  'brake-shoes','brake-pads','brake-drums','brake-shoes','pad-warning-wires',
                  'fitting-kits','brake-calipers','brake-fluid','brake-hoses','wheel-cylinders',
                  'master-cylinders','cables','air-filters','cabin-filters','fuel-filters','oil-filters',
                  'distributor','distributor-cap','glow-plugs','ignition-coil','ignition-leads',
                  'ignition-modules','rotor-arm','spark-plugs','air-conditioning-parts','fan-belts',
                  'radiator-caps-thermostats','radiators-heaters-coolers','switches-and-sensors',
                  'water-pumps','belts-chains','bushes-mountings','engine-gaskets-seals','engine-parts',
                  'engines-and-gearboxes','idlers-pulleys-tensioners','steering-boxes','steering-pump',
                  'steering-rack-gaiters','steering-racks','track-rods','track-rod-ends','ball-joints',
                  'coil-springs','shock-absorbers','stabiliser-links','top-suspension-mount',
                  'track-control-arms','cables','clutch-hydraulics','clutches','cv-boots','cv-joints',
                  'drive-shafts','gear-boxes','wheel-bearings-kits-and-hubs','alternators-dynamos',
                  'batteries','distributor-caps','ignition-coils','lead-sets','starter-motors',
                  'switches-sensors','window-regulator','brake-light-switches','bulbs','light-units',
                  'reverse-light-switches','cables','mirrors-and-mirror-glasses','tow-bars','exhaust-systems',
                  'wiper-blades','washer-pumps','brake-fluids','coolant-fluids','engine-oils','steering-fluids',
                  'suspension-fluids','transmission-oils']

    parts_list = list(set(parts_list))
    for type in parts_list:

        print('Scraping Part:', ' '.join([x.capitalize() for x in type.split('-')]))

        part_url = 'http://www.mpdonline.co.uk/' + type
        response = scraper.get(part_url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        specific_url = soup.find_all('div', {'class':'link'})
        part_numbers = soup.find_all('div', {'class':'productCode'})
        parts = [part.contents[2] for part in part_numbers]

        for url in specific_url:
            if parts[specific_url.index(url)] not in identifiers:
                ending = url.a['href']
                data_url = 'http://www.mpdonline.co.uk' + ending
                response = scraper.get(data_url, headers=headers)
                soup = BeautifulSoup(response.text, 'lxml')

                try:
                    name = soup.find_all('div', {'class':'subcatholder'})[0].h2.contents[0]
                    brand = soup.find_all('a', href=re.compile('^/brand/'))[0]['href'].split('/')[2].replace('%20',' ')
                    part = soup.find_all('div', {'class':'subcatholder'})[0].h2.contents[1].text
                    price = soup.find_all('div', {'class':'priceHolder'})[0].label.contents[0].replace('£','')
                    store = soup.find_all('div', {'class':'branchname'})[0].text
                    category = ' '.join([x.capitalize() for x in type.split('-')])

                    try:
                        desc_1 = str(soup.find_all('div', {'class':'technicalholder'})[0].h2.text).rstrip()
                        desc_2 = BeautifulSoup(str(soup.find_all('div', {'class':'technicalholder'})[0]), 'lxml')

                        desc_2_columns = desc_2.find_all('th')
                        desc_2_values = desc_2.find_all('td')

                        desc_2 = []
                        for val in zip(desc_2_columns, desc_2_values):
                            column = str(val[0]).lstrip('<th>').rstrip('</th>')
                            value = str(val[1]).lstrip('<td>').rstrip('</td>')
                            list.append(desc_2, column + ': ' + value)

                        desc_2 = ', '.join(desc_2)
                        description = desc_1 + '. ' + desc_2
                    except:
                        description = "No Description Available"

                    try:
                        stock = soup.find_all('div', {'class': 'instockbig'})[0].text.lstrip().rstrip()
                    except IndexError:
                        stock = 'Not in Stock'

                    try:
                        image = soup.find_all('a', {'class': 'imageLightBox'})[0]['href']
                    except:
                        image = 'No Image'

                    final_part = [name, brand, part, price,
                        stock, store, image, category, description]

                    list.append(data, final_part)
                    list.append(identifiers, parts[specific_url.index(url)])

                except:
                    continue
            else:
                continue

    return data, identifiers

def get_data(make, data, urls):

    final_data = []
    url_data = []
    scraper = requests.Session()

    payload = {
        'option':'models',
        'make': make,
    }

    url = 'http://www.mpdonline.co.uk/ajax.php?x=getVehicleOptions'
    response = BeautifulSoup(scraper.post(url, data=payload).text, 'lxml')
    options = response.find_all('option')

    for var in options:
        model = var.contents[0]

        payload = {
            'option': 'hasSubModels',
            'make': make,
            'model': model,
        }

        url = 'http://www.mpdonline.co.uk/ajax.php?x=getVehicleOptions'
        response = BeautifulSoup(scraper.post(url, data=payload).text, 'lxml')

        payload = {
            'option': 'engines',
            'make': make,
            'model': model,
        }

        url = 'http://www.mpdonline.co.uk/ajax.php?x=getVehicleOptions'
        response = BeautifulSoup(scraper.post(url, data=payload).text, 'lxml')
        options = response.find_all('option')

        for var in options:
            engine = var.contents[0]

            payload = {
                'option': 'years',
                'make': make,
                'model': model,
                'submodel': '',
                'engine': engine + '00',
            }

            url = 'http://www.mpdonline.co.uk/ajax.php?x=getVehicleOptions'
            response = BeautifulSoup(scraper.post(url, data=payload).text, 'lxml')
            options = response.find_all('option')

            for var in options:
                year = var.contents[0]

                print('')
                print(make, model, engine, year)
                data, parts = scrape_data(scraper, make, model,
                                engine, year, final_data, url_data)

                _save('part_data.txt', data)
                _save('identifier_data.txt', parts)

    return data, urls

def main():

    car_make = ['Aixam', 'Alfa Romeo', 'Asia Motors', 'Aston Martin',
                'Audi', 'Bentley', 'BMW', 'Bristol', 'Cadillac', 'Caterham',
                'Chevrolet', 'Chrysler', 'Citroen', 'Dacia', 'Daewoo',
                'Daihatsu', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'FSO',
                'Great Wall', 'Honda', 'Hummer', 'Infiniti', 'Isuzu', 'Iveco',
                'Jaguar/Daimler', 'Jeep', 'Jensen', 'Kia', 'Lada', 'Lamborghini',
                'Lancia', 'Land Rover', 'LDV', 'Lexus', 'Ligier', 'Lotus', 'LTI',
                'Mahindra', 'Marcos', 'Maserati', 'Maybach', 'Mazda', 'MCW',
                'Mercedes Benz', 'MG', 'Microcar', 'Mini', 'Mitsubishi', 'Morgan',
                'Nissan', 'Noble', 'Opel', 'Perodua', 'Peugeot', 'Piaggio',
                'Porsche', 'Proton', 'Reliant', 'Renault', 'Rolls Royce', 'Rover',
                'Saab', 'Santana', 'Sao', 'Seat', 'Skoda', 'Smart', 'Ssangyong',
                'Subaru', 'Talbot', 'Tata', 'Tesla', 'Think', 'Toyota', 'Triumph',
                'TVR', 'UMM', 'Vauxhall', 'Volkswagen', 'Volvo', 'Westfield',
                'Yugo']

    try:
        part_data = _load('part_data.txt')
        identifier_data = _load('identifier_data.txt')
        print('Loading from Saved Data')

    except:
        part_data = []
        identifier_data = []
        print('Loading from Start')

    checkpoint = input('Start on A Specific Car? (Y/N): ')

    while True:
        if checkpoint.upper() == 'Y':
            check_make = input('Which Car? See List Above: ')

            while True:
                try:
                    make_index = car_make.index(check_make)
                    for make in car_make[make_index:]:
                        part_data, url_data = get_data(make, part_data, identifier_data)
                        columns = ['name', 'brand', 'part', 'price', 'stock',
                                   'store', 'image', 'category', 'description']
                        final_df = pd.DataFrame(part_data, columns=columns)
                        final_df.to_csv('{}_data.csv'.format(make), index=False)
                    break

                except:
                    print('Query not Understood. Try Again.')
            break

        elif checkpoint.upper() == 'N':
            print('Scraping All Makes and Models.')
            for make in car_make:
                part_data, url_data = get_data(make, part_data, identifier_data)
                columns = ['name', 'brand', 'part', 'price', 'stock',
                           'store', 'image', 'category', 'description']
                final_df = pd.DataFrame(part_data, columns=columns)
                final_df.to_csv('{}_data.csv'.format(make), index=False)
            break

        else:
            print('Query not Understood. Try Again.')


if __name__ == '__main__':
    main()