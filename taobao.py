from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote

# chrome_options=webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# browser=webdriver.Chrome(chrome_options=chrome_options)
browser=webdriver.Chrome()
wait=WebDriverWait(browser,10)
KEYWORD='iPad'
def index_page(page):
    '''
    抓取索引页
    :param page:页码
    :return:
    '''
    print('正在爬取第',page,'页')
    try:
        url='https://s.taobao.com/search?q='+quote(KEYWORD)
        browser.get(url)
        if page>1:
            input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form > input')))#页码输入框
            submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager div.form > span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager li.item.active > span'),str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.m-itemlist .items .item')))
        get_products()
    except TimeoutException:
        index_page(page)


from pyquery import PyQuery as pq

def get_products():
    '''
    提取商品信息
    :return:
    '''
    html=browser.page_source
    doc=pq(html)
    items=doc('.m-itemlist .items .item').items()
    for item in items:
        product={
        'image': item.find('.pic .img').attr('data-src'),
        'price': item.find('.price strong').text(),
        'deal': item.find('.deal-cnt').text() ,
        'title': item.find('.title').text(),
        'shop': item.find('.shop').text() ,
        'location': item.find('.location').text()
        }
        print(product)
        insert_mysql(product)

import pymysql
db = pymysql.connect(host='localhost', db='spiders', user='root', password='root')
cursor = db.cursor()

def insert_mysql(dict):
    table='product'
    keys=','.join(dict.keys())
    values=','.join(['%s']*len(dict.values()))
    sql = 'insert into {table}({keys}) values({values})'.format(table=table,keys=keys,values=values)
    print(sql)
    try:
        cursor.execute(sql,tuple(dict.values()))
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()

if __name__ == '__main__':
    for i in range(1,101):
        index_page(i)