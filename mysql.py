import pymysql
db=pymysql.connect(host='localhost',user='root',password='root',port=3306,db='spiders')
cursor=db.cursor();
cursor.execute('select version()');
print(cursor.fetchone())

#cursor.execute("CREATE DATABASE spiders DEFAULT CHARACTER SET utf8")
#sql = ' CREATE TABLE IF NOT EXISTS students (id VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, age INT NOT NULL, PRIMARY KEY (id ))'
#cursor.execute(sql)

data={
    "id":1,
    "name":'张三',
    "age":23

}
table="students"
keys=','.join(data.keys())
values=','.join(['%s']*len(data))
#插入
# sql2='insert into {table}({keys}) values({values})'.format(table=table,keys=keys,values=values)
#
# try:
#     cursor.execute(sql2,tuple(data.values()));
#     db.commit()
# except Exception as e:
#     print(e)
#     db.rollback()

#重复则更新
sql3='insert into {table}({keys}) values({values}) on duplicate key update '.format(table=table,keys=keys,values=values)

update=','.join('{key}=%s'.format(key=key) for key in data.keys())
sql3+=update
try:
    cursor.execute(sql3,tuple(data.values())*2)
    db.commit()
except Exception as e:
    print('failed!',e)
    db.rollback()

print(sql3)

#查询
cursor.execute('select * from students where age>10');
row=cursor.fetchone();
while row:
    print(row,type(row))
    row=cursor.fetchone()

cursor.close();



import pymongo
client=pymongo.MongoClient(host='localhost',port=27017)
db=client.test
collection=db.students
print(client)
print(db)
print(collection)


s1={
    "id":"20122222",
    'name':"张三",
    'age':22

}
#插入
result=collection.insert_one(s1);
#查询
result2=collection.find({'name':'张三'})
result21=collection.find_one({'age':{'$gt':20}})
print(result2.count())
#删除
#result3=collection.delete_many({'name':'张三'})
#print(result3.deleted_count)
print(result.inserted_id)
print(result21,result2.count())
for r in result2:
    print(r)


condition={'age':22}
result26=collection.find_one(condition)
print('result26',result26)
result26['age']=26
#更新
result31=collection.update(condition,result26)
result32=collection.update_many({'age':22},{'$set':{'age':27}})#update students set age=27 where age=22
print(result31)
print(result32.matched_count,result32.modified_count)




from redis import StrictRedis
redis=StrictRedis(host='localhost',port=6379,db=0,password='')
redis.set('a','rf')


print(redis.get('a'))
#redis.flushall()