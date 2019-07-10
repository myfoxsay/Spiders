import requests
import urllib.parse
print(requests.get("http://192.168.99.100:8050/render.html?url=https://www.baidu.com&wait=5").text)
print(requests.get("http://192.168.99.100:8050/render.png?url=https://www.baidu.com&wait=5&width=1000&height=500").text)
print(requests.get("http://192.168.99.100:8050/render.json?url=https://www.baidu.com&wait=1&html=1&png=1&har=1").text)


lua='''
function main(splash)
    return 'hello'
end
'''
print(requests.get('http://192.168.99.100:8050/execute?lua_source='+urllib.parse.quote(lua)).text)