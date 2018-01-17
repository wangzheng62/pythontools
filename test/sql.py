#mysql 语法
SELECT='select {} {} from {} {} {};'.format(DISTINCT,COLNAMES,TABLES,WHERE,ORDER_BY)
INSERT='insert into {} {} values {};'.format(TABLES,COLNAMES,VALUES)
UPDATE='update {} set {} {};'.format(TABLES,KEYWORDS,WHERE)
DELECT='delete from {} {};'.format(TABLES,WHERE)
#
LIMIT='limit {};'.format(NUM)
LIKE='{} {} like {}'.format(COLNAMES,NOT,RE)
IN='in {}'.format(VALUES)
BETWEEN='between {} and {}'.format(VALUE1,VALUE2)
AS='as {}'.format(ALIASNAME)