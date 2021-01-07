from selenium import webdriver
import time
import xlrd
import re
from selenium.webdriver.common.by import By
import sys
from webdriver_manager.chrome import ChromeDriverManager

# 改browser
browser = webdriver.Chrome(ChromeDriverManager().install())

if sys.version_info < (3, 0):
    # Python 2
    import Tkinter as tk
else:
    # Python 3
    import tkinter as tk
root = tk.Tk()

root.title("Sandwich")

root.geometry('500x300')


# tk.Button(root, text="Make me a Sandwich").pack()


# Google Chrome	87.0.4280.88 (正式版本) (x86_64) mac
def query():
    driver = browser
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
            count = 0
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
                    # Topic
                    htmlTopic = cols[2].text
                    # 判断页面Consumer Group是否已修改来判断是否已成功返回
                    if not (str(htmlGroup).__contains__(groupId) and str(htmlTopic) == topic):
                        print('kafka:等待页面响应中...')
                        count = count + 1
                        if count % 3 == 0:
                            driver.find_element_by_xpath('//*[@type="submit"]').click()
                            time.sleep(1)
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


query()
print("统计完成！关闭弹框即可退出")

tk.mainloop()
# 本地测试
# if __name__ == '__main__':
#     query()
# mac下打包教程：
# https://www.jianshu.com/p/01fdb93aa7ad
# https://blog.csdn.net/mangxunmeng4980/article/details/106420587

#安装好依赖后
#pip3 install py2app
#py2applet --make-setup queryQuqueDelay.py

#生成setup.py
#修改其中的
# OPTIONS = {'includes': [
#     'selenium', 'time', 're','webdriver_manager','xlrd']
# }
#python3 setup.py py2app
#就会生成build文件夹和dist文件夹
# 打包好后将 queue.xls拷贝到Resources下 本机地址举例：/Users/用户名/PycharmProjects/Spiders/dist/queryQuqueDelay.app/Contents/Resources/
#启动目录：右键-显示包内容-Contents-MacOS-queryQuqueDelay  本机地址举例:/Users/用户名/PycharmProjects/Spiders/dist/queryQuqueDelay.app/Contents/MacOS/queryQuqueDelay