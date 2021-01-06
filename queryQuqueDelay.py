from selenium import webdriver
import time
import xlrd
import re
from selenium.webdriver.common.by import By


# Google Chrome	87.0.4280.88 (正式版本) (x86_64) mac
def query():
    driver = webdriver.Chrome('./chromedriver')
    driver.get("http://192.168.3.70:8131/#/kafka/lag")
    workbook = xlrd.open_workbook(r'./queue.xls')
    # 根据sheet索引或者名称获取sheet内容
    sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
    url = sheet.cell_value(1, 0)
    driver.get(url)
    time.sleep(3)
    for rown in range(sheet.nrows):
        if rown == 0:  # 忽略第一行标题
            continue
        topic = sheet.cell_value(rown, 1)
        groupIdsText = sheet.cell_value(rown, 2)
        if len(topic) == 0:
            print('kafka:topic不可为空')
            return
        if len(groupIdsText) == 0:
            print('kafka:groupId不可为空')
            return
        if str(groupIdsText).__contains__('，'):
            print('kafka:有中文逗号,请检查文本：', groupIdsText)
            return
        groupIds = groupIdsText.split(',')
        threshold = float(sheet.cell_value(rown, 3))
        thresholdPercent = float(sheet.cell_value(rown, 4))
        driver.find_element_by_id('topic').clear()
        driver.find_element_by_id('topic').send_keys(topic)
        for groupId in groupIds:
            driver.find_element_by_id('group').clear()
            driver.find_element_by_id('group').send_keys(groupId)
            time.sleep(1)
            driver.find_element_by_xpath('//*[@type="submit"]').click()
            time.sleep(2)
            # 判断是否已返回页面
            waiting = True
            while waiting:
                table = driver.find_element_by_tag_name('tbody')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                if len(rows) == 0:
                    answer = input('kafka:Consumer Group:{},Topic:{} 未查询到数据，是否跳过？(y/n)'.format(groupId, topic))
                    if answer == 'y' or answer == 'yes':
                        break
                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, 'td')
                    # Consumer Group
                    htmlGroup = cols[0].text
                    # 判断页面Consumer Group是否已修改来判断是否已成功返回
                    if not str(htmlGroup).__contains__(groupId):
                        print('kafka:等待页面响应中...')
                        time.sleep(1)
                        break
                    else:
                        waiting = False
                        cols = row.find_elements(By.TAG_NAME, 'td')
                        # 消费延迟(延迟%)
                        htmlThresholdText = cols[4].text
                        htmlThresholdList = re.findall(r"(\d+)\((\d+.\d+)%\)", htmlThresholdText)
                        if float(htmlThresholdList[0][0]) > threshold or float(
                                htmlThresholdList[0][1]) > thresholdPercent:
                            print('kafka延迟报警：Consumer Group:{},Topic:{},分区:{},消费延迟(延迟%):{}'.
                                  format(cols[0].text, cols[2].text, cols[3].text, htmlThresholdText))


if __name__ == '__main__':
    query()
