class User(object):
	__type=''
	def __init__(self,username,passwd,**kw):
		self.__username=username
		self.passwd=passwd
		for key in kw:
			exec('self.%s=kw[key]'%key)
	@property
	def username(self):
		return self.__username
if __name__=='__main__':
	u=User('test','123456')
	print(u.username,u.passwd)
	u.passwd='aaa'
	print(u.username,u.passwd)