#https://m.weibo.cn/u/3545186430
import requests
import urllib.parse
from pyquery import PyQuery
import pymysql

db = pymysql.connect(host='localhost', db='spiders', user='root', password='root')
cursor = db.cursor()

def insert_mysql(dict):
    table='weibo'
    keys=','.join(dict.keys())
    values=','.join(['%s']*len(dict.values()))
    sql = 'insert into {table}({keys}) values({values})'.format(table=table,keys=keys,values=values)
    print(sql)
    try:
        cursor.execute(sql,tuple(dict.values()))
        db.commit()
        print('已存入')
    except Exception as e:
        print(e)
        db.rollback()


def get_html(page):
    global response
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
        'x-requested-with': 'x-requested-with'

    }
    paramter = {
        'type': 'uid',
        'value': "3545186430",
        'containerid': '1076033545186430',
        'page': page
    }
    return requests.get('https://m.weibo.cn/api/container/getIndex?' + urllib.parse.urlencode(paramter),
                            headers=headers);


def parse_data(response):
    for cards in response.json().get('data').get('cards'):
        mblog=cards.get('mblog')
        weibo={}
        weibo['id']=mblog.get('id')
        weibo['comments_count']=mblog.get('comments_count')#评论数
        weibo['attitudes_count']=mblog.get('attitudes_count')#点赞数
        weibo['reposts_count']=mblog.get('reposts_count')#转发数
        weibo['text']=PyQuery(mblog.get('text')).text()
        yield weibo

if __name__ == '__main__':
    for i in range (1,11):
        response=get_html(i)
        dicts=parse_data(response)
        # 存入mysql
        for dict in dicts:
            insert_mysql(dict)

