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
	def getcolname(self):
		sql='use %s;select name from syscolumns where id = object_id(\'%s\') order by colorder;'%(self.dbname,self.tablename)
		t=self.getdata(sql)
		l=[]
		for tp in t:
			l.append(tp[0])
		return l
class MssqlTable(MssqlTableBase):
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
	def __init__(self,**kw):
		self.info=kw
		self.colname=self.getcolname()
		self.value=self.getvalue(**kw)
	def getkw(self):
		kw={}
		for name in self.colname:
			kw[name]=[]
		for row in self.value:
			colnum=0
			for cell in row:
				kw[self.colname[colnum]].append(cell)
				colnum+=1
		return kw
#______________________________________________________
#数据库示例
class Manager(MssqlDb):
	pass
		
#表示例
class Userlist(MssqlTable,Manager):
	'aaaa'
	def isexist(self):
		if len(self.value)==0:
			return False
		else:
			return True
#测试
if __name__=='__main__':
	db=Manager()
	print(db.getUsertable())
	tb=Userlist(passwd='123456')
	print(tb.colname)
	print(tb.value)
	print(tb.info)
	print(tb.getkw())
	print(tb.isexist())
	