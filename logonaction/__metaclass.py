import pymssql
#服务器
class Mssqlserver():
	SEVERCONFIG=['127.0.0.1','sa','12345678']
	def getconn(self):
		conn=pymssql.connect(*self.SEVERCONFIG)
		return conn
	def getsysdata(self,sql):
		conn=self.getconn()
		cr=conn.cursor()
		cr.execute(sql)
		t=cr.fetchall()
		if t==None:
			return None
		if type(t[0])==tuple:
			l=[]
			for tp in t:
				l.append(tp[0])
			return l
		return t
	def getdblist(self):
		sql='SELECT Name FROM Master..SysDatabases ORDER BY Name;'
		res=self.getsysdata(sql)
		return res
#数据库
class MssqlDbMetaclass(type):
	def __new__(cls,name,bases,attrs):
		attrs['dbname']=name
		return type.__new__(cls,name,bases,attrs)
class MssqlDb(Mssqlserver,metaclass=MssqlDbMetaclass):
	def getUsertable(self):
		sql='use %s;Select Name From SysObjects Where XType=\'U\' order By Name;'%self.dbname
		res=self.getsysdata(sql)
		return res
#表
class MssqlTableMetaclass(MssqlDbMetaclass):
	def __new__(cls,name,bases,attrs):
		attrs['tablename']=name
		return type.__new__(cls,name,bases,attrs)
class MssqlTable(metaclass=MssqlTableMetaclass):
	def getcolname(self):
		sql='use %s;select name from syscolumns where id = object_id(\'%s\') order by colorder;'%(self.dbname,self.tablename)
		res=self.getsysdata(sql)
		return res
	def getvalue(self):
		sql='use %s;select * from %s where loginname=\'%s\' and passwd=\'%s\';'%(self.dbname,self.tablename,self.username,,self.passwd)
#数据库示例
class Manager(MssqlDb):
	pass
		
#表示例
class Userlist(MssqlTable,Manager):
	pass
if __name__=='__main__':
	db=Manager()
	print(db.getUsertable())
	tb=Userlist()
	print(tb.getcolname())