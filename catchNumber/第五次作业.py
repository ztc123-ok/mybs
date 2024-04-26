name = input('请输入姓名：')
age = int(input('请输入年龄：'))
if age > 64:
    print('已到退休年龄，可以退休了')
else:
    print('骚年好好加油，多多创造自身价值吧！')

money = int(input('请输入账户余额：'))
if money >= 5000:
    print('可以旅游')
elif money >= 2000 and money < 5000:
    print('可以购物')
elif money >= 500 and money < 2000:
    print('只能日常消费')
else:
    print('需要节省')

age = int(input('请输入年龄：'))
is_student = input('是否是学生：')

if age < 18 and is_student == '是':
    print('可以获得电影票的学生折扣')
else:
    print('不能获得电影票的学生折扣')
