import mysql.connector,logging,os,CONFIG

#元类
class Mysqlservermetaclass(type):
	def __new__(cls,name,bases,attrs):
		try:
			from CONFIG import MYSQLDBSERVER
			conn=mysql.connector.connect(**MYSQLDBSERVER)
			attrs['DBSERVER']=MYSQLDBSERVER
			logging.basicConfig(filename=CONFIG.INFOLOG,level=logging.INFO)
			logging.info('数据库服务器测试连接成功')
		except Exception as e:
			logging.basicConfig(filename=CONFIG.ERRORLOG,level=logging.INFO)
			logging.error('数据库服务器测试连接失败')
			logging.error(e)
		return type.__new__(cls,name,bases,attrs)

class MysqlDBmetaclass(Mysqlservermetaclass):
	def __new__(cls,name,bases,attrs):
		attrs['db_name']=name
		attrs['dbconn']={'database':name}
		return type.__new__(cls,name,bases,attrs)
		
class MysqlTableMetaclass(MysqlDBmetaclass):
	def __new__(cls,name,bases,attrs):
		attrs['table_name']=name
		return type.__new__(cls,name,bases,attrs)
		
#基类		
class MysqlserverBase(metaclass=Mysqlservermetaclass):
	def __getconn(self):
		conn=mysql.connector.connect(**self.DBSERVER)
		return conn
	@property
	def databases(self):
		return __databases
	@databases.getter
	def databases(self):
		conn=self.__getconn()
		cr=conn.cursor()
		sql='show databases;'
		cr.execute(sql)
		t=cr.fetchall()
		__databases=[]
		for tp in t:
			__databases.append(tp[0])
		return __databases
class MysqlDBBase(metaclass=MysqlDBmetaclass):
	def __getconn(self):
		LOCALDB=dict(self.DBSERVER,**self.dbconn)
		conn=mysql.connector.connect(**LOCALDB)
		return conn
	def getdata(self,sql):
		conn=self.__getconn()
		cr=conn.cursor()
		cr.execute(sql)
		t=cr.fetchall()
		return t
	def changedata(self,sql):
		conn=self.__getconn()
		cr=conn.cursor()
		cr.execute(sql)
		conn.commit()
	@property
	def tables(self):
		return __tables
	@tables.getter
	def tables(self):
		conn=self.__getconn()
		cr=conn.cursor()
		sql='show tables;'
		cr.execute(sql)
		t=cr.fetchall()
		__tables=[]
		for tp in t:
			__tables.append(tp[0])
		return __tables
class MysqlTableBase(metaclass=MysqlTableMetaclass):
	@property
	def desc(self):
		return __desc
	@desc.getter
	def desc(self):
		t0=('Field','Type','Null','Key','Default','Extra')
		sql='desc %s;'%self.table_name
		__desc=self.getdata(sql)
		__desc.insert(0,t0)
		return __desc
	#获取列名
	@property
	def colnames(self):
		return __colnames
	@colnames.getter
	def colnames(self):
		sql='desc %s;'%self.table_name
		t=self.getdata(sql)
		__colnames=[]
		for tp in t:
			__colnames.append(tp[0])
		return __colnames
	
	
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
		sql='select * from %s %s;'%(self.table_name,condition)
		res=self.getdata(sql)
		return res
#类
class Mysqlserver(MysqlserverBase):
	pass
class MysqlDB(MysqlDBBase):
	pass
class MysqlTable(MysqlTableBase):
	def __init__(self,**kw):
		for key in kw:
			assert key in self.colnames,"当前表中没有->{}<-列".format(key)
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
	#DML增删改
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
			sql='insert into %s%s values %s;'%(self.table_name,names,values)
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
			sql='UPDATE %s SET %s where %s;'%(self.table_name,data,condition)
			self.changedata(sql)
			return True
	def delete(self):
		'isexist is True'
		condition='where '
		for key in self.info:
			temp='%s =\'%s\' and '%(key,self.info[key])
			condition=condition+temp
		condition=condition[:-4]
		sql='delete from %s %s;'%(self.table_name,condition)
		self.changedata(sql)
		return True	
	#DDL
	'''alter table table_name [add,drop,modify] colname datatype [unique,not null]'''
	def __alter(self,colname,action='',datatype='varchar(10)',constraint=''):
		sql='alter table %s %s %s %s %s;'%(self.table_name,action,colname,datatype,constraint)
		print(sql)
	def coladd(self,colname,datatype='varchar(10)',constraint=''):
		self.__alter(colname,action='add',datatype='varchar(10)',constraint='')
	def coldrop(self,colname):
		self.__alter(colname,action='drop',datatype='')

if __name__=='__main__':
	class DBserver(Mysqlserver):
		pass
	class Groupdata1(MysqlDB,DBserver):
		pass
	class Group10(MysqlTable,Groupdata1):
		'aaaa'
		pass
	db=DBserver()
	l=Group10(**{"名字":123})
	print(l.info)
	print(db.databases)
	print(l.DBSERVER)
	print(l.db_name)
	print(l.table_name)
	print(l.databases)
	print(l.tables)
	print(l.colnames)
	print(l.desc)
	print(l.coldrop('hahhaa1'))