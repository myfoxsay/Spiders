import urllib.parse

r=urllib.parse.urlparse("baidu.com/p;user?a=1#comment",scheme="https",allow_fragments=True);
print(type(r))
print(r)

ba={
    'name':"王贺",
    "age":33

}

print("http://www.baidu.com?"+urllib.parse.urlencode(ba))
print(urllib.parse.parse_qs('name=%E7%8E%8B%E8%B4%BA&age=33'))
import requests
r2=requests.get("http://www.baidu.com")
print(type(r2),type(r2.text),type(r2.cookies),r2.text,sep='\n')

r3=requests.get("http://httpbin.org/get")
print(r3.text)
print(r3.json())


import re
headers = {
'User-Agent':'Mozilla/5 .0 (Macintosh; Intel Mac 05 X 10_11_4) AppleWebKit/537.36 (KHTML, lik e Gecko)Chrome/52 .0.2743. 116 Safari/53 7.36'
}
r =requests.get("https://www.zhihu.com/explore",headers=headers)
pattern =re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)
titles = re. findall(pattern , r.text)
for i in titles:
    print(i)




image=requests.get("https://github.githubassets.com/images/modules/site/integrators/google.png")
print(image.text)
print(image.content)
with open('google.png','wb') as f:
    f.write(image.content)


r4=requests.get("http://baidu.com")
exit() if not r4.status_code==requests.codes.ok else print('success')

# 文件上传
files={'file':open('google.png','rb')}
r5=requests.post("http://httpbin.org/post",files=files)
print(r5.text)


import re
a=re.match('\d+','1111')
print(a)
print(a.group())
print(a.span())


