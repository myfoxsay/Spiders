import urllib.request
import socket
import urllib.error
import urllib.parse
response=urllib.request.urlopen('http://www.baidu.com')
##print(response.read().decode('utf-8'))
print(type(response))
print(response.status)
print(response.getheaders())
print(response.getheader("Server"))

try:
    response2=urllib.request.urlopen("http://httpbin.org",timeout=0.1)
except urllib.error.URLError as e:
    if isinstance(e.reason,socket.timeout):
        print("Time out!")


headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'

    }

request=urllib.request.Request('https://www.python.org',headers=headers)
response3=urllib.request.urlopen(request)
print(response3.read().decode('utf-8'))




url = 'http://httpbin.org/post'
headers = {
'User-Agent': 'Mozilla/4.0 (compatible; MSIE S. S; Windows NT)',
'Host':'httpbin.org'
}
dict={
'name':"Tom"

}

data= bytes(urllib.parse.urlencode(dict), encoding='utf8')
req = urllib.request.Request(url=url, data=data, headers=headers, method ='POST')
response = urllib.request.urlopen(req)
print(response. read(). decode('utf-8'))






