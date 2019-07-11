from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
EMAIL ='test@test . com'
PASSWORD = '123456'
class CrackGeetest ():

    def _init_(self):
        self. url = 'https://auth.geetest.com/login/'
        self.browser = webdriver .Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD

    def get_geetest_button(self):
        '''
        获取初始验证按钮
        :return: 按钮对象
        '''
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'geetest_radar_tip')))
        return button

