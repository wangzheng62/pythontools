import mysql.connector,logging,os,CONFIG
#服务器

class Mysqlservermetaclass(type):
	def __new__(cls,name,bases,attrs):
		try:
			from CONFIG import MYSQLDBSERVER
			conn=mysql.connector.connect(**MYSQLDBSERVER)
			logging.basicConfig(filename=CONFIG.INFOLOG,level=logging.INFO)
			logging.info('数据库服务器测试连接成功')
		except Exception as e:
			logging.basicConfig(filename=CONFIG.ERRORLOG,level=logging.INFO)
			logging.error('数据库服务器测试连接失败')
			logging.error(e)
		return type.__new__(cls,name,bases,attrs)

class Mysqlserver(metaclass=Mysqlservermetaclass):
	SERVER={'user':'root','password':'12345678','host':'127.0.0.1'}
	
	def getdblist(self):
		conn=mysql.connector.connect(**self.SERVER)
		cr=conn.cursor()
		sql='show databases;'
		cr.execute(sql)
		t=cr.fetchall()
		res=[]
		for tp in t:
			res.append(tp[0])
		return res
			
#数据库
