
# coding: utf-8

# tips:
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

# In[144]:


from selenium import webdriver
import time


# In[147]:


def get_composer_works(url):
    t1 = time.time()
    
    # not login version
    driver = webdriver.PhantomJS()
    driver.get(url)
    
    # composer id
    composer_id = url.split('/')[-1].split('.')[0]
    
    # get comopser name
    composer_info = driver.find_element_by_xpath('//h1[@class="composer"]').text
        
    # number of midi
    wMidi = driver.find_element_by_xpath('//div[@id="wMidi"]')
    total_num_midi = int(wMidi.find_element_by_xpath('.//li[@class="counts"]')
                         .text.split()[1].replace(',',''))

    # loop through all works (collect work_id, group_id, work_name, num_midi)
    for work in wMidi.find_elements_by_xpath('.//li[starts-with(@id, "grp_")]')[:10]:
        group_id = work.get_attribute('id')
        num_midi = int(work.find_element_by_xpath('.//div[@class="infolabel"]').text.split()[0])
        work_toggle = work.find_element_by_xpath('.//a[starts-with(@id, "work_")]')
        work_name = work_toggle.text
        work_id = work_toggle.get_attribute('id')
        # keep the group "toggle expanded"
        if (work.get_attribute('class') == 'toggle'):
            work_toggle.click()
        # staring from page 1, go through all pages
        first_page = work.find_element_by_xpath('.//*[@class="yui-pg-first"]')
        first_page.click()
        print(group_id, work_id, work_name, num_midi)
            
            
            
    # close browser
    driver.close()
    
    t2 = time.time()
    print('> done in {} seconds'.format(t2-t1))


# In[148]:


get_composer_works(url)


# In[2]:


url = 'https://www.classicalarchives.com/midi/composer/2113.html'


# In[3]:


driver = webdriver.PhantomJS()


# In[4]:


driver.get(url)


# In[88]:


# a = driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div[1]/h1')
driver.find_element_by_xpath('//h1[@class="composer"]').text


# In[69]:


a.text


# In[122]:


wMidi = driver.find_element_by_xpath('//div[@id="wMidi"]')


# In[123]:


num_midi = int(wMidi.find_element_by_xpath('.//li[@class="counts"]')
               .text.split()[1].replace(',',''))


# In[158]:


print(len(wMidi.find_elements_by_css_selector('li[id^="grp_"]')))


# In[162]:


# for work in wMidi.find_elements_by_xpath('.//li[starts-with(@id, "grp_")]')[:3]:
for work in wMidi.find_elements_by_css_selector('li[id^="grp_"]')[:3]:
    print(work.get_attribute('class'))
    print(work.find_element_by_xpath('.//a[starts-with(@id, "work_")]').text)


# In[174]:


# grp_r6eaja1f only 1 page, grp_vjaf53p5 20 pages
for work in wMidi.find_elements_by_xpath('.//li[starts-with(@id, "grp_vjaf53p5")]')[:10]:
    toggle = work.find_element_by_xpath('.//a[starts-with(@id, "work_")]')
    if work.get_attribute('class') == 'toggle':
        toggle.click()
    # start from page 1
    first_page = work.find_element_by_xpath('.//*[@class="yui-pg-first"]')
    first_page.click()
    # determine number of pages
    while True:
        current_page = int(work.find_element_by_xpath('.//span[@class="yui-pg-current-page yui-pg-page"]').text)
        next_page = work.find_element_by_xpath('.//*[@class="yui-pg-next"]')
        print(current_page)
        
        # check if reaching the last page
        if not next_page.get_attribute('href'):
            break
        next_page.click()
    
#    print(work.find_elements_by_tag_name('a')[1].get_property('id'))
    # print(work.find_element_by_xpath('.//a[contains(@id, "work_")]').get_property('id'))


# In[97]:


driver.find_element_by_xpath('//div[@id="wMidi"]//li[@class="counts"]').text.split()[1].replace(',','')


# In[119]:


x = driver.find_element_by_xpath('//div[@id="wMidi"]')


# In[120]:


x.find_element_by_xpath('.//li[@class="counts"]').text


# In[98]:


a=driver.find_elements_by_xpath('//div[@id="wMidi"]//li[@class="toggle"]')


# In[141]:


for b in a[:3]:
    print(b.get_property('innerHTML'))
#    print(b.find_element_by_xpath('.//*[contains(@id, "work_")]').get_property('id'))
    print(b.find_element_by_xpath('.//div[@class="infolabel"]').text.split()[0])
#     group_id = b.get_property('id')
#     work_id = b.find_element_by_xpath('//a[@id="work_962"]').get_property('id')
#     print(group_id, work_id)


# In[92]:


b.text


# In[152]:


driver.save_screenshot('foo.png')


# In[63]:


n = midi_tag.find_element_by_xpath('//*[@class="counts"]')


# In[64]:


n.text


# In[25]:


a.text


# In[50]:


n.text


# In[39]:


for x in n:
    print(x.text.strip().split())


# In[75]:


driver.page_source

