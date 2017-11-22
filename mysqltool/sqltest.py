import mysql.connector
SERVER={'user':'root','password':'12345678','host':'127.0.0.1'}
conn=mysql.connector.connect(**SERVER)
cr=conn.cursor()
sql='show databases;'
cr.execute(sql)
t=cr.fetchall()
print(t)
sql01='create database tt1;'
cr.execute(sql01)