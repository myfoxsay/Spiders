import json
str1='''
[{ "name":"Geek"
}]
'''
j1=json.loads(str1)
print(j1,type(j1))
str2=json.dumps(j1,indent=2)
print(str2,type(str2))

with open('maoyan.json','r',encoding='utf-8') as f:
    st=f.read();
    print(st)
    j2=json.loads(st);
    print(j2,type(j2))
    print(j2[0].get('name'))


import csv

with open('data.csv ','w', encoding='utf-8 ',newline='') as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(["100",'good',66])
    writer.writerow(["200", '刘丽', 25])


with open('data.csv ','a', encoding='utf-8 ',newline='') as csvfile:
    fieldnames = ['id','name','age']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'id' : '10005' , 'name':'王伟','age':22 })

with open('data.csv','r',encoding='utf-8') as csvfile:
    reader=csv.reader(csvfile)
    print(type(reader))
    for r in reader:
        print(r)