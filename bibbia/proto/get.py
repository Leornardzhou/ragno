import utils
import requests
import re



def get_pages():

#     url = 'http://www.vatican.va/archive/ITA0001/_INDEX.HTM'
    url = 'http://www.vatican.va/archive/ENG0839/_INDEX.HTM'

    r = requests.get(url)
    a = re.findall(r'<a href=(__P.*?)>', r.text)
    print(a)

    # print(r.text)
    # driver = utils.start_driver('chrome')

    # open_url(driver, url)

    # for elem in driver.find_elements_by_xpath('//a[starts-with(@href, __)]')

    # driver.close()

get_pages()
