#数据库类的示例
import pymssql
from __sqlstatement import USERLIST
def mssqlgetcol(**kw):
	print(kw)
	sql=USERLIST['获取列名']%(kw['db'],kw['tablename'])
	print(sql)
	SEVERCONFIG=['127.0.0.1','sa','12345678']
	conn=pymssql.connect(*SEVERCONFIG)	
	cr=conn.cursor()
	cr.execute(sql)
	t=cr.fetchall()
	print(t)
	l=[]
	for tp in t:
		l.append(tp[0])
	return l
def mysqlgetcol(**kw):
	pass
class TableMetaclass(type):
	def __new__(cls,name,bases,attrs):
		print(attrs)
		print(bases)
		print(name)
		if attrs['dbtype']=='mssql':
			attrs['__slot__']=mssqlgetcol(db=attrs['db'],tablename=attrs['tablename'])
			print(attrs['__slot__'])
		if attrs['dbtype']=='mysql':
			attrs['__slot__']=mysqlgetcol(db=attrs['db'],tablename=attrs['tablename'])
		return type.__new__(cls,name,bases,attrs)
	
class Table(dict,metaclass=TableMetaclass):
	dbtype='mssql'
	db='manager'
	tablename='dbo.userlist'
	def __init__(self):
		pass
		
#mssql数据库
class Mssqlserver():
	import pymssql
	SEVERCONFIG=['127.0.0.1','sa','12345678']
	def getconn(self):
		conn=pymssql.connect(*self.SEVERCONFIG)
		return conn
	def getsysdata(self,sql):
		conn=self.getconn()
		cr=conn.cursor()
		cr.execute(sql)
		t=cr.fetchall()
		l=[]
		for tp in t:
			l.append(tp[0])
		return l
	def getdblist(self):
		sql='SELECT Name FROM Master..SysDatabases ORDER BY Name;'
		res=self.getsysdata(sql)
		return res
		
class MssqlDb(Mssqlserver):
	db='manager'
	def getUsertable(self):
		sql='use %s;Select Name From SysObjects Where XType=\'U\' order By Name;'%self.db
		res=self.getsysdata(sql)
		return res
class MssqlTable(MssqlDb):
	tablename='userlist'
	def getcolname(self):
		sql=USERLIST['获取列名']%(self.db,self.tablename)
		res=self.getsysdata(sql)
		return res
if __name__=='__main__':
	t=Table()
	print(t.db)
	s1=Mssqlserver()
	print(s1.SEVERCONFIG)
	print(s1.getdblist())
	db=MssqlDb()
	print(db.getUsertable())
	tb=MssqlTable()
	print(tb.getcolname())