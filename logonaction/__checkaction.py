#装饰器
def check(user,callback,checkactions):
	def auth(func):
		def wrapper(*args,**kw):
			n=1
			for f in checkactions:
				bool=f(user)
				if bool:
					n+=1
				else:
					break
			if	bool:	
				return func(*args,**kw)
			else:
				return callback(n)
		return wrapper
	return auth
if __name__=='__main__':
	from __mssqlmetaclass import MssqlDb,MssqlTable
	class Manager(MssqlDb):
		pass
	class Userlist(MssqlTable,Manager):
		pass
	def login(user):
		if user.isexist():
			return True
		else:
			return False
	def auth(user):
		if user.getkw()['auth'][0]==2:
			return True
		else:
			return False
	def date(user):
		if user.getkw()['endtime'][0]=='2017-07-01':
			return True
		else:
			return False
	def err(n):
		return '条件%s失败'%n
	u=Userlist(loginname='huoyubei',passwd='1234')
	@check(Userlist(loginname='huoyubei',passwd='123'),err,(login,auth,date))
	def do():
		print('条件成功')
	do()
	