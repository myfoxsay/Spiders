
#https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D
import requests
import urllib.parse

import time
def get_html(offset):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'cookie': 'tt_webid=6711131915825432076; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16bcfaa537b73c-0d5a693a83f1df-5e173617-1fa400-16bcfaa537cd02; s_v_web_id=d934f7b220675d18c47216ae2a57cfcc; CNZZDATA1259612802=2007846243-1562554543-https%253A%252F%252Fwww.baidu.com%252F%7C1562554543; __tasessionId=ej6qkdmbi1562569327075; csrftoken=95a4f6064ca4ecbf4fdefde5bfda6169; tt_webid=6711131915825432076'

    }
    paramter = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': time.time()
    }
    url = 'https://www.toutiao.com/api/search/content/?' + urllib.parse.urlencode(paramter, encoding='utf-8')
    response = requests.get(url, headers=headers)
    print(response.content.decode('utf-8'))
    return response

import os
def parse_data(response):
    print(response.status_code)
    if response.json().get('data')==None:
        print('没有数据')
        return
    for i in response.json().get('data'):
        if not i.get('title')==None:

            save_image(i)




from hashlib import md5
def save_image(i):
    title = i.get('title')
    title = validateTitle(title)  # 去除非法文件名
    title='images/'+title;
    if not os.path.exists(title):
        os.mkdir(title)
    image_list = i.get('image_list');

    for image in image_list:
        url=image.get('url')
        response=requests.get(url)
        path='{0}/{1}.jpg'.format(title,md5(response.content).hexdigest())
        if not os.path.exists(path):
            with open(path,'wb') as f:
                print('正在保存...'+path)
                f.write(response.content)
        else:
            print('该图片已存储')

import re

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|...]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


def main(offset):
    response=get_html(offset)
    parse_data(response)

from multiprocessing.pool import Pool

if __name__ == '__main__':
    #多线程
    group_start=0
    group_end=20
    pool=Pool()
    group=([x*20 for x in range(group_start,group_end)])
    print(group)
    pool.map(main,group)
    pool.close()
    pool.join()



    # for i in range(0,20):
    #     main(i*20)



