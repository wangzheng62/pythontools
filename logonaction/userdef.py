def mssqlgetcol(**kw):
	pass
def mysqlgetcol(**kw):
	pass
class TableMetaclass(type):
	def __new__(cls,name,bases,attrs):
		print(attrs)
		print(bases)
		print(name)
		if attrs['dbtype']=='mssql':
			attrs['__slot__']=mssqlgetcol(db=attrs['db'],tablename=attrs['tablename'])
		if attrs['dbtype']=='mysql':
			attrs['__slot__']=mysqlgetcol(db=attrs['db'],tablename=attrs['tablename'])
		return type.__new__(cls,name,bases,attrs)
class Table(dict,metaclass=TableMetaclass):
	dbtype='mssql'
	db='manager'
	tablename='userlist'
	def __init__(self):
		pass
if __name__=='__main__':
	t=Table()
	print(t.__slot__)
	a=1
	b=1
	if a is b:
		print(1)
	c=[]
	d=[]
	if c is b:
		print('[]')
	n='123456789'
	print(n[0])
	bt=bytes('abc','utf8')
	print(bt)
	s1='abc'
	bt1=s1.encode()
	print(bt1)
	print(bt.decode())