from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
#网易邮件登录
#Google Chrome	87.0.4280.88 (正式版本) (x86_64) mac
driver=webdriver.Chrome('./chromedriver')
driver.get("https://mail.163.com/")
driver.find_element_by_id('lbNormal').click()
driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
driver.find_element_by_name('email').send_keys('user11111')
driver.find_element_by_name('password').send_keys('pass11111')
driver.find_element_by_id('dologin').click()
#验证码
for i in range(0,16):
    print(15-i)
    time.sleep(1)

#已删除
driver.find_element_by_xpath('//*[@title="已删除"]').click()
while True:
    try:
        time.sleep(1)
        driver.find_element_by_xpath('//span[@role="checkbox"]/span').click()#点击全选
        driver.find_element_by_xpath('//div[@role="toolbar"]/div[2]/div[1]/span').click()#点击彻底删除
        driver.find_element_by_xpath('//div[@class="nui-msgbox-ft"]/div[2]/div[1]/span').click()#点击确认
    except Exception as e:
        print(e)
        print("结束")
        break
