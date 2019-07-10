from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

browser=webdriver.Chrome()
try:
    browser.get('https://www.baidu.com')
    input=browser.find_element_by_id('kw')
    input.send_keys('Python')
    input.send_keys(Keys.ENTER)
    wait=WebDriverWait(browser,10)
    wait.until(expected_conditions.presence_of_element_located((By.ID,'content_left')))
    print(browser.current_url)
    print(browser.get_cookies())
    print(browser.page_source)
finally:
    browser.close()

browser=webdriver.Chrome()
browser.get("https://www.taobao.com")
print(browser.page_source)
browser.close()


browser= webdriver.Chrome()
browser. get ('https://www.zhihu.com/explore')
browser . execute_script('window.scrollTo(0, document.body.scrollHeight )')
#browser . execute_script('alert("Hello World")')
input=browser.find_element_by_class_name('zu-top-add-question')
print(input.id)
print(input.location)
print(input.tag_name)
print(input.size)
print(input.get_attribute('id'))
browser.close()

print('-----------------------')
driver=webdriver.PhantomJS()
driver.get('https://baidu.com')
print(driver.current_url)