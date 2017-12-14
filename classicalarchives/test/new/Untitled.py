
# coding: utf-8

# tips:
#
# tables:
# composer: {id, name, year, country, num_midi, num_work}
# work: {id, grp_id, name, num_midi, num_page, }
#
#
# ids:
# - composer_id, work_id and contributor_id (page number) are fixed
# - group_id are not fixed
# - composer > work > contributor > track (= midi_id unique to avoid redownload)
# - place order > download > clear history > repeat
#
# xpath
# .// anywhere under current node
# //xxx//yyy somewhere under xxx and then under yyy
# .//li[@class="toggle"]  select li tag with class="toggle"
# .//li[contains(@id, "work_")]  select li tag with id containing "work_"
# .//li[starts-with(@id, "work_")]   select li tag with id starting with "work_"
#
# css_selector
# li[@id*=work]   select li tag with id containing work
# li[@id^=work]   select li tag with id starting with work
# li[@id$=work]   select li tag with id ending with work
#
# https://stackoverflow.com/questions/34315533/can-i-find-an-element-using-regex-with-python-and-selenium
#

# #

# In[345]:


import requests
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
import cma


# In[352]:


driver.implicitly_wait(5)


# In[410]:


USERNAME = 'joeyfuerimmer@gmail.com'
PASSWORD = '0.567359Zy'


# In[328]:


def login_cma(driver, username, password):
    login_url = cma.domain_url + '/secure/login.html'
    driver.get(login_url)
    login_username = driver.find_element_by_id('email')
    login_username.send_keys(username)
    login_password = driver.find_element_by_id('password')
    login_password.send_keys(password)
    login_button = driver.find_element_by_xpath('//*[@id="signinbtn"]//button')
    login_button.click()
    print('> successful login as {}'.format(username))


# In[329]:


def logout_cma(driver, username):
    logout_url = cma.domain_url + '/secure/logout.html'
    driver.get(logout_url)
    print('> successful logout as {}'.format(username))


# In[330]:


def is_login(driver, username):
    account_url = cma.domain_url + '/secure/youraccount.html'
    driver.get(account_url)
    try:
        email = driver.find_element_by_xpath('//*[@id="dispEmail"]').text.strip()
        if username in email:
            print('> currently login as {}'.format(username))
            return True
        else:
            print('> currently login as another user: ' + email +
                  ' (try logout and login again)')
            return False
    except NoSuchElementException:
        print('> currently not login')
        return False


# In[394]:


def download_midi(driver, out_prefix='', clear_history=True):

    if out_prefix:
        out_prefix += '.'

    download_url = cma.domain_url + '/secure/downloads.html'
    driver.get(download_url)

    # find all files to download at this page
    download_list = driver.find_elements_by_xpath('//td[@class="dlButton"]//a[@href]')
    if len(download_list) == 0:
        print('> Nothing to download, quit.')
        return

    # get download url and start download
    for download in download_list:
        download_url = download.get_property('href')
        download_fname = out_prefix + download_url.split('/')[-1]
        print('> downloading {}\n> to local file {}'.format(download_url, download_fname))
        with open(download_fname,'wb+') as f:
            f.write(requests.get(download_url).content)

    # clear all downloaded tracks
    if clear_history:

        # clear history
        clear_button = driver.find_element_by_xpath('//span[@id="clearBtnBot"]//button[@type="button"]')
        clear_button.click()

        # confirm
        confirm_box = driver.find_element_by_id('ConfDBox')
        # yui-gen0-button
        for confirm_button in confirm_box.find_elements_by_tag_name('button'):
            if confirm_button.text == 'Yes':
                print('> Clearing history of downloaded files.')
                confirm_button.click()


# # Common tasks

# In[392]:


is_login(driver, 'joeyfuerimmer@gmail.com')


# In[360]:


login_cma(driver, 'joeyfuerimmer@gmail.com', '0.567359Zy')


# In[320]:


logout_cma(driver, 'joeyfuerimmer@gmail.com')


# In[391]:


download_midi(driver, '.', 'temp.prefix', clear_history=True)


# In[393]:


driver.save_screenshot('foo.png')


# # Developing section

# In[409]:


def get_composer_works(driver, driver2, url, download_set):
    t1 = time.time()

    # not login version
    driver.get(url)

    # composer id
    composer_id = url.split('/')[-1].split('.')[0]

    # get comopser name
    composer_info = driver.find_element_by_xpath('//h1[@class="composer"]').text

    # number of midi
    wMidi = driver.find_element_by_xpath('//div[@id="wMidi"]')
    total_num_midi = int(wMidi.find_element_by_xpath('.//li[@class="counts"]').text.split()[1].replace(',',''))

    print('> composer_id={} composer_info={} num_midi={}'
          .format(composer_id, composer_info, total_num_midi))

    # loop through all works (collect work_id, group_id, work_name, num_midi)
    for work in wMidi.find_elements_by_xpath('.//li[starts-with(@id, "grp_")]')[:3]:

        group_id = work.get_attribute('id')
        num_midi = int(work.find_element_by_xpath('.//div[@class="infolabel"]').text.split()[0])
        work_toggle = work.find_element_by_xpath('.//a[starts-with(@id, "work_")]')
        work_name = work_toggle.text
        work_id = work_toggle.get_attribute('id').replace('work_','')

        print('>> work_id={} group_id={} work_name={} num_midi={}'
              .format(work_id, group_id, work_name, num_midi))

        # keep the group "toggle expanded"
        if (work.get_attribute('class') == 'toggle'):
            work_toggle.click()

        # staring from page 1
        first_page = work.find_element_by_xpath('.//*[@class="yui-pg-first"]')
        first_page.click()

        # go through all pages
        page_items = {}
        while True:
            page_id = int(work.find_element_by_xpath('.//span[@class="yui-pg-current-page yui-pg-page"]').text)

            # get contributor
            contributor = work.find_element_by_xpath('.//div[@class="details"]//a')
            contributor_url = contributor.get_attribute('href')
            contributor_id = contributor_url.split('/')[-1].split('.')[0]
            contributor_name = contributor.text
            num_track = work.find_element_by_xpath('.//div[@class="buy"]//p').text
            num_track = int(num_track.split()[0])

            # get track list
            track_list = work.find_elements_by_xpath('.//table[@class="trackList"]//tr')
            track_prefix = ''
            track_id = 0
            for track in track_list:
                # faster way to check if the first tag is <th>
                tmp_html = track.get_attribute('innerHTML').strip()
                if tmp_html.startswith('<th '):
                    track_prefix = track.find_element_by_xpath('.//th').text
                    continue
                # a formal track with download button
                track_id += 1
                track_name = (track_prefix + " " +
                              track.find_element_by_xpath('.//td[@class="tlTitle"]').text)
                track_length = track.find_element_by_xpath('.//td[@class="tlLen"]').text

                download_id = '{}.{}.{}.{}.{}'.format(composer_id, work_id, contributor_id, page_id, track_id)

                track_download = track.find_element_by_xpath('.//td[@class="tlAdd"]//a[@class="dl dlMIDI1"]')
                # track_download.click()


                # go to download midi
#                 download_midi()

                print('>>> contributor_id={} contributor_name={} num_track={}'
                      .format(contributor_id, contributor_name, num_track))
                print(composer_id, work_id, contributor_id, track_id,
                     track_name, track_length)

            # check if reaching the last page
            next_page = work.find_element_by_xpath('.//*[@class="yui-pg-next"]')
            if not next_page.get_attribute('href'):
                break
            # turn the page
            next_page.click()


    t2 = time.time()
    print('> done in {} seconds'.format(t2-t1))


# # Testing section

# In[411]:


driver_browse = webdriver.PhantomJS()
driver_browse.implicitly_wait(5)
driver_down = webdriver.PhantomJS()
driver_down.implicitly_wait(5)


# In[425]:


login_cma(driver_browse, USERNAME, PASSWORD)


# In[427]:


login_cma(driver_down, USERNAME, PASSWORD)


# In[429]:


is_login(driver_browse, USERNAME)


# In[430]:


is_login(driver_down, USERNAME)


# In[432]:


driver_down.current_url


# In[433]:


driver_down.get('https://www.classicalarchives.com/midi/composer/2156.html')


# In[434]:


driver_browse.get('https://www.classicalarchives.com/midi/composer/156.html')


# In[435]:


driver_down.current_url


# In[436]:


driver_browse.current_url


# In[408]:


get_composer_works(driver, 'https://www.classicalarchives.com/midi/composer/2156.html')


# In[397]:


wMidi = driver.find_element_by_xpath('//div[@id="wMidi"]')


# In[398]:


wMidi.find_element_by_xpath('.//li[@class="counts"]').text


# In[357]:


download_url = cma.domain_url + '/secure/downloads.html'
driver.get(download_url)


# In[356]:


download_list = driver.find_elements_by_xpath('.//td[@class="dlButton"]//a[@href]')
len(download_list)


# In[350]:


for dl in download_list:
    print(dl.get_property('href'))


# In[343]:


track_url = 'https://www.classicalarchives.com/d/oJ15_kmJyD8TjjxAWa-ZC2csPCE5Xmp_uciZAnZSPLHqUwAT_9zpLweoIRfc3buOXynmgfUaKBFVeGvZ1zmpw_7og1_c9ul-jyT3uxHo-_eMCsczK6Jrlcq3KXRQO-Lizs_rd3qJGQH8HfSvVGlbrg/bVg-g53z0zzmfETYwpGFzw/bach565.mid'


# In[346]:


with open(track_url.split('/')[-1],'wb+') as f:
    f.write(requests.get(track_url).content)


# In[ ]:


with open('/Users/ehco/Desktop/img/'+name+'.png','wb+') as f:
    f.write(requests.get(img_url).content)


# In[371]:


clear_button = driver.find_element_by_xpath('//span[@id="clearBtnBot"]//button[@type="button"]')


# In[372]:


clear_button.click()


# In[389]:


driver.save_screenshot('confirmdelete.png')


# In[388]:


# confirm_button = driver.find_element_by_xpath('//button[@id="yui-gen0-button"]')
# confirm_button = driver.find_element_by_xpath('//div[@id="ConfDBox_c"]//button[@id="yui-yui-gen0-button-button"]')
confirm_box = driver.find_element_by_id('ConfDBox')
# yui-gen0-button
for btn in confirm_box.find_elements_by_tag_name('button'):
    if btn.text == 'Yes':
        btn.click()
        break


# In[148]:


get_composer_works(url)


# In[255]:


url = 'https://www.classicalarchives.com/midi/composer/2113.html'


# In[256]:


driver = webdriver.PhantomJS()


# In[257]:


driver.implicitly_wait(5) # seconds


# In[258]:


driver.get(url)


# In[276]:


# a = driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div[1]/h1')
driver.find_element_by_xpath('//h1[@class="composer"]').text


# In[260]:


wMidi = driver.find_element_by_xpath('//div[@id="wMidi"]')


# In[261]:


int(wMidi.find_element_by_xpath('.//li[@class="counts"]')
    .text.split()[1].replace(',',''))


# In[266]:


len(wMidi.find_elements_by_css_selector('li[id^="grp_"]'))


# In[277]:


# grp_r6eaja1f only 1 page, grp_vjaf53p5 20 pages
# the grp_id changes dynamically!!!

for work in wMidi.find_elements_by_xpath('.//li[starts-with(@id, "grp_")]'):
    toggle = work.find_element_by_xpath('.//a[starts-with(@id, "work_")]')
    work_name = toggle.text
    work_id = toggle.get_attribute('id')
    if work_id != 'work_2363':
        continue
    if work.get_attribute('class') == 'toggle':
        toggle.click()

    # start from page 1
    first_page = work.find_element_by_xpath('.//*[@class="yui-pg-first"]')
    first_page.click()

    # go through the pages
    while True:
        current_page = int(work.find_element_by_xpath('.//span[@class="yui-pg-current-page yui-pg-page"]').text)
        next_page = work.find_element_by_xpath('.//*[@class="yui-pg-next"]')

        contributor = work.find_element_by_xpath('.//div[@class="details"]//a')
        contributor_url = contributor.get_attribute('href')
        contributor_id = contributor_url.split('/')[-1].split('.')[0]
        contributor_name = contributor.text
        num_track = work.find_element_by_xpath('.//div[@class="buy"]//p').text
        num_track = int(num_track.split()[0])

        print(current_page, contributor_url, contributor_name, contributor_id, num_track)

        # get track list
        track_list = work.find_elements_by_xpath('.//table[@class="trackList"]//tr')
        track_prefix = ''
        index = 1

        for track in track_list:
            tmp_html = track.get_attribute('innerHTML').strip()
            if tmp_html.startswith('<th '):
                track_prefix = track.find_element_by_xpath('.//th').text
                continue
            track_name = (track_prefix + " " +
                          track.find_element_by_xpath('.//td[@class="tlTitle"]').text)
            track_length = track.find_element_by_xpath('.//td[@class="tlLen"]').text
            print(index, track_name, track_length)
            index += 1

        # check if reaching the last page
        if not next_page.get_attribute('href'):
            break
        next_page.click()



# In[358]:


driver.save_screenshot('foo.png')
