#userlist操作
USERLIST={'检查用户名':'select loginname from manager.dbo.userlist where loginname=\'%s\';','获取列名':'use %s;select name from syscolumns where id = object_id(\'%s\') order by colorder;','获取用户信息':'select * from manager.dbo.userlist where loginname=\'%s\' and passwd=\'%s\';','增加用户':'insert into manager.dbo.userlist values %s','更改用户':'update manager.dbo.userlist set passwd=\'%s\',endtime=\'%s\',contact=\'%s\' where loginname=\'%s\';','删除用户':'delete from manager.dbo.userlist where loginname=\'%s\' and creator=\'%s\';'}
#onlinelist操作
ONLINELIST={'检查登录信息':'select loginname,logintime from manager.dbo.onlinelist where loginname=\'%s\';','插入登录信息':'insert into manager.dbo.onlinelist values (\'%s\',%s);','删除登录信息':'delete from manager.dbo.onlinelist where loginname=\'%s\';'}