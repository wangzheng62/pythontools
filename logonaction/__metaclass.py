import pymssql,CONFIG
#服务器
class Mssqlserver():
	SEVERCONFIG=CONFIG.DBSERVER
	def getconn(self):
		conn=pymssql.connect(*self.SEVERCONFIG)
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
		sql='SELECT Name FROM Master..SysDatabases ORDER BY Name;'
		res=self.getdata(sql)
		return res
#数据库
class MssqlDbMetaclass(type):
	def __new__(cls,name,bases,attrs):
		attrs['dbname']=name
		return type.__new__(cls,name,bases,attrs)
class MssqlDb(Mssqlserver,metaclass=MssqlDbMetaclass):
	def getUsertable(self):
		sql='use %s;Select Name From SysObjects Where XType=\'U\' order By Name;'%self.dbname
		t=self.getdata(sql)
		l=[]
		for tp in t:
			l.append(tp[0])
		return l
#表
class MssqlTableMetaclass(MssqlDbMetaclass):
	def __new__(cls,name,bases,attrs):
		attrs['tablename']=name
		return type.__new__(cls,name,bases,attrs)
class MssqlTableBase(metaclass=MssqlTableMetaclass):
	#获取列名
	def getcolname(self):
		sql='use %s;select name from syscolumns where id = object_id(\'%s\') order by colorder;'%(self.dbname,self.tablename)
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
		sql='use %s;select * from %s %s;'%(self.dbname,self.tablename,condition)
		res=self.getdata(sql)
		return res
class MssqlTable(MssqlTableBase):
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
		sql='use %s;insert into %s%s values %s;'%(self.dbname,self.tablename,names,values)
		self.changedata(sql)
	def update(self):
		'isexist is True'
		'all unique is null'
		data=''
		sql='UPDATE %s SET %s %s;'%(self.tablename,data,condition)
		self.changedata(sql)
	def delete(self):
		'isexist is True'
		condition=''
		if len(kw)==0:
			return False
		else:
			condition='where '
			for key in kw:
				temp='%s =\'%s\' and '%(key,kw[key])
				condition=condition+temp
			condition=condition[:-4]
			sql='use %s;delete from %s %s;'%(self.dbname,self.tablename,condition)
			self.changedata(sql)
			return True	
			
			
#______例子_______________________________________________
#数据库示例
class Manager(MssqlDb):
	pass
		
#表示例
class Userlist(MssqlTable,Manager):
	'aaaa'
	pass
#测试
if __name__=='__main__':
	db=Manager()
	print(db.getUsertable())
	tb=Userlist(passwd='123456')
	print(tb.info)
	print(tb.getkw())
	print(tb.isexist())
	t1=Userlist(loginname='huoyubei',passwd='123456',endtime='2017-07-01',auth='3',creator='test')
	#t1.delete(loginname='huoyubei')
	print(tb.iscolumnexist('passwd'))
	print(t1.iscolumnexist('loginname'))