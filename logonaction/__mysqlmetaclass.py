import mysql.connector,CONFIG
#服务器
class Mysqlserver():
	SEVERCONFIG=CONFIG.MYSQLDBSERVER
	def getconn(self):
		conn=mysql.connector.connect(**self.SEVERCONFIG)
		return conn
	def getdata(self,sql):
		conn=self.getconn()
		cr=conn.cursor()
		cr.execute(sql)
		t=cr.fetchall()
		return t
	def changedata(self,sql):
		conn=self.getconn()
		cr=conn.cursor()
		cr.execute(sql)
		conn.commit()
	def getdblist(self):
		sql='show databases;'
		conn=self.getconn()
		cr=conn.cursor()
		cr.execute(sql)
		t=cr.fetchall()
		res=[]
		for tp in t:
			res.append(tp[0])
		return res
#数据库
class MysqlDbMetaclass(type):
	def __new__(cls,name,bases,attrs):
		attrs['dbname']=name
		def getconn(self):
			self.SEVERCONFIG['database']=name
			conn=mysql.connector.connect(**self.SEVERCONFIG)
			return conn
		attrs['getconn']=getconn
		sql='show databases;'
		conn=self.getconn()
		cr=conn.cursor()
		cr.execute('show databases;')
		t=cr.fetchall()
		res=[]
		for tp in t:
			res.append(tp[0])
		
		if name not in res and not name=='MysqlDb':
			sql='create database %s;'%name
			conn=mysql.connector.connect(**self.SEVERCONFIG)
			cr=conn.cursor()
			cr.execute(sql)
			conn.commit()
		return type.__new__(cls,name,bases,attrs)
class MysqlDb(Mysqlserver,metaclass=MysqlDbMetaclass):
	def getUsertable(self):
		sql='show tables;'
		t=self.getdata(sql)
		l=[]
		for tp in t:
			l.append(tp[0])
		return l
	
#表
class MysqlTableMetaclass(MysqlDbMetaclass):
	def __new__(cls,name,bases,attrs):
		attrs['tablename']=name
		return type.__new__(cls,name,bases,attrs)
class MysqlTableBase(metaclass=MysqlTableMetaclass):
	#获取列名
	def getcolname(self):
		sql='select column_name from information_schema.columns where table_schema =\'%s\' and table_name = \'%s\' ;'%(self.dbname,self.tablename)
		t=self.getdata(sql)
		l=[]
		for tp in t:
			l.append(tp[0])
		return l
	#获取列值
	def getvalue(self,**kw):
		condition=''
		if len(kw)==0:
			pass
		else:
			condition='where '
			for key in kw:
				temp='%s =\'%s\' and '%(key,kw[key])
				condition=condition+temp
			condition=condition[:-4]
		sql='select * from %s %s;'%(self.tablename,condition)
		res=self.getdata(sql)
		return res
class MysqlTable(MysqlTableBase):
	def __init__(self,**kw):
		self.info=kw
	#辅助功能
	def isexist(self):
		values=self.getvalue(**self.info)
		if len(values)==0:
			return False
		else:
			return True
	def iscolumnexist(self,key):
		if eval('self.getvalue(%s=\'%s\')'%(key,self.info[key])):
			return True
		else:
			return False			
	def getkw(self):
		kw={}
		colnames=self.getcolname()
		values=self.getvalue(**self.info)
		for name in colnames:
			kw[name]=[]
		for row in values:
			colnum=0
			for cell in row:
				kw[colnames[colnum]].append(cell)
				colnum+=1
		return kw
	#增删改
	def insert(self):
		'isexist is False'
		'all unique is null'
		if self.isexist():
			return False
		else:
			colnames=self.getcolname()
			names=[]
			values=[]
			for key in colnames:
				if key in self.info:
					names.append(key)
					values.append(self.info[key])
			names=str(tuple(names))
			names=names.replace('\'','')
			values=str(tuple(values))
			sql='insert into %s%s values %s;'%(self.tablename,names,values)
			self.changedata(sql)
			return True
	def update(self,**kw):
		'isexist is True'
		'all unique is null'
		if len(kw)==0 or not self.isexist():
			return False
		else:
			data=''
			for key in kw:
				temp='%s =\'%s\' ,'%(key,kw[key])
				data=data+temp
			data=data[:-1]
			condition=''
			for key in self.info:
				temp='%s =\'%s\' and '%(key,self.info[key])
				condition=condition+temp
			condition=condition[:-4]
			sql='UPDATE %s SET %s where %s;'%(self.tablename,data,condition)
			self.changedata(sql)
			return True
	def delete(self):
		'isexist is True'
		condition='where '
		for key in self.info:
			temp='%s =\'%s\' and '%(key,self.info[key])
			condition=condition+temp
		condition=condition[:-4]
		sql='delete from %s %s;'%(self.tablename,condition)
		self.changedata(sql)
		return True	
			
#______例子_______________________________________________
#数据库示例
class Groupdata1(MysqlDb):
	pass
		
#表示例
class Group10(MysqlTable,Groupdata1):
	'aaaa'
	pass
#测试
if __name__=='__main__':
	s=Group10()
	print(s.getdblist())
	print(s.SEVERCONFIG)
	print(s.getUsertable())
	print(s.getcolname())