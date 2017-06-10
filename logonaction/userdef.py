class TableMetaclass(type):
	def __new__(cls,name,bases,attrs):
		print(attrs)
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