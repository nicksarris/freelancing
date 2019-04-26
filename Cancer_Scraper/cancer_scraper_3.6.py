__author__ = 'Nick Sarris (ngs5st)'

import pandas as pd
from bs4 import BeautifulSoup
import requests

sessions = requests.session()
site_6 = 'http://www.chictr.org.cn/searchprojen.aspx'

def scrape_hindawi():

    print('')
    authors = []
    email_ids = []

    hindawi_index = 1
    while True:

        print('Scraping Hindawi, on Page {} / 387'.format(hindawi_index))
        response = sessions.get('https://www.hindawi.com/search/all/cancer/' + str(hindawi_index))
        soup = BeautifulSoup(response.text, "lxml")
        data = (soup.find_all('li')[9:])

        if not data:
            break

        else:

            for entry in data:
                author_val = str(entry.contents[1])
                author_val = author_val.lstrip(', ')
                author_val = author_val.rstrip()
                list.append(authors, author_val)

            for entry in data:
                list.append(email_ids, '')

        hindawi_index += 1

    hindawi_data = pd.DataFrame()
    hindawi_data['authors'] = authors
    hindawi_data['email_ids'] = email_ids
    hindawi_data.to_csv('hindawi_data.csv', index=False)

def scrape_tf():

    print('')
    authors = []
    email_ids = []

    tandf_index = 1
    while True:

        print('Scraping Taylor/Francis, on Page {} / 2580'.format(tandf_index))
        response = sessions.get('http://www.tandfonline.com/action/doSearch?AllField=Cancer&'
                                'pageSize=100&subjectTitle=&startPage=' + str(tandf_index - 1))
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all('div', {'class': 'author'})

        if str(data[0]) == '<div class="author">' \
                      '<span class="hlFld-ContribAuthor"><a href="/author/Ferrucci%2C+Leah+M"> Leah M.   Ferrucci   PhD, MPH </a></span>  , ' \
                      '<span class="hlFld-ContribAuthor"><a href="/author/Cartmel%2C+Brenda"> Brenda   Cartmel   PhD </a></span>  , ' \
                      '<span class="hlFld-ContribAuthor"><a href="/author/Turkman%2C+Yasemin+E"> Yasemin E.   Turkman   APRN, PMHNP-BC, MSN, MPH </a></span>  , ' \
                      '<span class="hlFld-ContribAuthor"><a href="/author/Murphy%2C+Maura+E"> Maura E.   Murphy   MSN, CPNP </a></span>  , ' \
                      '<span class="hlFld-ContribAuthor"><a href="/author/Smith%2C+Tenbroeck"> Tenbroeck   Smith   MA </a></span>  , ' \
                      '<span class="hlFld-ContribAuthor"><a href="/author/Stein%2C+Kevin+D"> Kevin D.   Stein   PhD </a></span>   &amp; ' \
                      '<span class="hlFld-ContribAuthor"><a href="/author/McCorkle%2C+Ruth"> Ruth   McCorkle   PhD, FAAN </a></span> </div>' and tandf_index != 1:
            break

        else:
            for entry in data:
                entry_authors = []
                data_authors = entry.find_all('span', {'class': 'hlFld-ContribAuthor'})
                for val in data_authors:

                    try:
                        del val.a['href']

                        val_ = str(val.a.contents)
                        val_ = str(val_.replace('   ',' '))
                        val_ = str(val_.replace('"',''))
                        val_ = str(val_.lstrip("[' "))
                        val_ = str(val_.rstrip(" ']"))

                        if '<span class=single_highlight_class onclick=highlight()>Cancer</span>' in val_:
                            continue
                        else:
                            list.append(entry_authors, val_)

                    except:
                        continue

                list.append(authors, (', '.join(entry_authors)))
                list.append(email_ids, '')

        tandf_index += 1

    tandf_data = pd.DataFrame()
    tandf_data['authors'] = authors
    tandf_data['email_ids'] = email_ids
    tandf_data.to_csv('tandf_data.csv', index=False)

def scrape_sagepub():

    print('')
    authors = []
    email_ids = []

    sage_index = 1
    while True:

        print('Scraping SagePub, on Page {} / 1390'.format(sage_index))
        response = sessions.get('http://journals.sagepub.com/action/doSearch?AllField=Cancer'
                                '&pageSize=100&startPage=' + str(sage_index - 1))
        soup = BeautifulSoup(response.text, "lxml")
        data = (soup.find_all('li')[36:136])
        title = soup.find_all('article', {'data-title': 'Interval cancers in a national colorectal cancer screening programme'})

        if title and sage_index != 1:
            break

        else:
            for entry in data:
                entry_authors = []
                data_authors = entry.find_all('a', {'class': 'entryAuthor'})

                val_index = 0
                for val in data_authors:
                    if val_index % 5 == 0:

                        val_ = str(val.contents)
                        val_ = str(val_.lstrip("[' "))
                        val_ = str(val_.rstrip("']"))
                        list.append(entry_authors, val_)

                    val_index += 1

                list.append(authors, (', '.join(entry_authors)))
                list.append(email_ids, '')

        sage_index += 1

    sage_data = pd.DataFrame()
    sage_data['authors'] = authors
    sage_data['email_ids'] = email_ids
    sage_data.to_csv('sage_data.csv', index=False)

def scrape_chictr():

    print('')
    authors = []
    email_ids = []

    chictr_index = 1
    while True:

        print('Scraping Chictr, on Page {} / 1157'.format(chictr_index))
        response = sessions.get('http://www.chictr.org.cn/searchprojen.aspx?title=&officialname=&subjectid=&secondaryid='
                                '&applier=&studyleader=&ethicalcommitteesanction=&sponsor=&studyailment=&studyailmentcode='
                                '&studytype=0&studystage=0&studydesign=0&minstudyexecutetime=&maxstudyexecutetime='
                                '&recruitmentstatus=0&gender=0&agreetosign=&secsponsor=&regno=&regstatus=0&country='
                                '&province=&city=&institution=&institutionlevel=&measure=&intercode=&sourceofspends='
                                '&createyear=0&isuploadrf=&whetherpublic=&btngo=btn&page=' + str(chictr_index))

        if response.status_code != 200:
            break
        
        else:    
            soup = BeautifulSoup(response.text, "lxml")
            data = soup.find_all('a', href=True)[33:52]
    
            for entry in data:
                data_url = entry['href']
                if 'showprojen' in data_url:
                    response = sessions.get('http://www.chictr.org.cn/' + data_url)
                    soup = BeautifulSoup(response.text, "lxml")
                    author = str(soup.find_all('p', {'class': "en"})[12].contents)
                    author = author.replace("\\xa0']",'')
                    author = author.replace("['\\r\\n                            ",'')
                    list.append(authors, author)
    
                    email = str(soup.find_all('td', {'style': 'width: 300px;'})[4].contents)
                    email = email.replace("['\\r\\n                        ", '')
                    email = email.replace("\\xa0\\r\\n                    ']",'')
                    list.append(email_ids, email)
    
        chictr_index += 1

    chictr_data = pd.DataFrame()
    chictr_data['authors'] = authors
    chictr_data['email_ids'] = email_ids
    chictr_data.to_csv('chictr_data.csv', index=False)

if __name__ == '__main__':
    scrape_chictr()
