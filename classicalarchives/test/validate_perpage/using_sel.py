from selenium import webdriver

def foo(url):

    res = {}

    driver = webdriver.PhantomJS()
    driver.get(url)

    # get composer info
    res['info'] = driver.find_element_by_xpath('//*[@id="content"]//*/h1[@class="composer"]')
    ['info'] = driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div[1]/h1')



    driver.close()

    with open('test.json', 'w') as f:
        print(json.dumps(res, sort_keys=True, indent=4), file=f)

foo('https://www.classicalarchives.com/midi/composer/2113.html')
