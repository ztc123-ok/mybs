person = {}
person['name'] = '露比'
person['age'] = 13
person['address'] = "美琪喵喵窝"
print(person)
# {'name': '露比', 'age': 13, 'address': '美琪喵喵窝'}
person['address'] = "迪士尼"
print(person)
# {'name': '露比', 'age': 13, 'address': '迪士尼'}
print(person.pop('name'))
# 露比
print(person)
# {'age': 13, 'address': '迪士尼'}

set1 = {'java','python','c++','php','mysql'}
set1.remove('python')
print(set1)
# {'c++', 'php', 'mysql', 'java'}
set1.add('css')
print(set1)
# {'c++', 'php', 'css', 'mysql', 'java'}
list1 = ["灰太狼", "红太狼", "抓不到羊", "我一定会回来的"]
for x in list1:
    set1.add(x)
print(set1)
# {'c++', '我一定会回来的', '抓不到羊', '灰太狼', 'php', 'css', '红太狼', 'mysql', 'java'}
