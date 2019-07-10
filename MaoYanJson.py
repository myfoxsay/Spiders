import requests
import requests.exceptions
import re
import json
def get_one_page(url):
    try:

        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
        }
        result=requests.get(url,headers=headers)
        if result.status_code==200:
            return result.text
        return None
    except requests.exceptions.RequestException as e:
        return None

def parse_one_page(html):
    pattern=re.compile('<dd.*?board-index.*?>(.*?)</i>.*?<img.*?data-src="(.*?)".*?<p class="name"><a.*?>(.*?)</a></p>.*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>.*?<p class="score"><i class="integer">(.*?)</i><i class="fraction">(.*?)</i></p>',re.S)
    list=re.findall(pattern,html)
    for item in list:
        yield {
            'index':item[0],
            'image':item[1],
            'name':item[2],
            'actors':item[3].strip()[3:],
            'time':item[4][5:],
            'score':item[5]+item[6]
        }


def main(offset,list):
    url='https://maoyan.com/board/4?offset='+str(offset*10)
    html=get_one_page(url);
#    print(html)
    dicts=parse_one_page(html)
    for dict in dicts:
        print(dict)
        list.append(dict)

def write_to_file_json(content):
    print("写入中...")
    with open('maoyan.json','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False,indent=2)+'\n')



if __name__ == '__main__':
    list = []
    for i in range(0,10):
        main(i,list)
    write_to_file_json(list)