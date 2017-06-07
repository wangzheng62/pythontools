from userdef import User
def check(user,callback,*checkactions):
	def auth(func):
		def wrapper(*args,**kw):
			for f in checkactions:
				if f(user):
					return func(*args,**kw)
				else:
					break
			return callback()
		return wrapper
	return auth
def f1(user):
	if user.test1=='test1':
		return True
	else:
		return False
def f2(user):
	if user.test2=='test2':
		return True
	else:
		return False
def f3(user):
	if user.test3=='test3':
		return True
	else:
		return False
def err():
	print('条件失败')
if __name__=='__main__':
	u=User('a','1',test1='test1',test2='test2',test3='test3')
	@check(u,err,*(f1,f2,f3))
	def do():
		print('条件成功')
	do()
	