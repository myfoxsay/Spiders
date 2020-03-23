import datetime,requests
#https://www.jianshu.com/p/339c90c8a493
# m3u8是本地的文件路径

def get_ts_urls(m3u8_path,base_url):
    urls = []
    with open(m3u8_path,"r") as file:
        lines = file.readlines()
        for line in lines:
            if line.endswith(".ts\n"):
                urls.append(base_url+line.strip("\n"))
    return urls


def download(ts_urls,download_path):
    for i in range(len(ts_urls)):
        ts_url = ts_urls[i]
        file_name = ts_url.split("/")[-1]
        print("开始下载 %s" %file_name)
        start = datetime.datetime.now().replace(microsecond=0)
        try:
            response = requests.get(ts_url,stream=True,verify=False)
        except Exception as e:
            print("异常请求：%s"%e.args)
            return
        #ts_path = download_path+"/{0}.ts".format(i)
        ts_path = download_path+"/"+file_name
        with open(ts_path,"wb+") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        end = datetime.datetime.now().replace(microsecond=0)
        print("耗时：%s"%(end-start))

import os

from os import path

def file_walker(path):
    file_list = []
    for root, dirs, files in os.walk(path): # 生成器
        for fn in files:
            p = str(root+'/'+fn)
            file_list.append(p)
    print(file_list)
    return file_list

def combine(ts_path, combine_path, file_name):
    file_list = file_walker(ts_path)
    file_path = combine_path + file_name + '.ts'
    with open(file_path, 'wb+') as fw:
        for i in range(len(file_list)):
            fw.write(open(file_list[i], 'rb').read())

if __name__ == '__main__':
    #urls = get_ts_urls("index.m3u8","https://cdn3.yuan-baidu.com/850k/m3u8/201906/27/7d5e2fac9d61/")
    #print(urls)
    #download(urls,"./tsfiles")
    combine("./tsfiles","d:/ts","haha")