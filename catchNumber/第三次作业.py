words = "abcdefghi"
print(words[2:7:2])
print(words[5]+words[4]+words[6])
print(words[::-1])
print(words[::2])
print(words[::-4])
# ceg
# feg
# ihgfedcba
# acegi
# iea

str1 = 'hello 你好 我是大聪明 你是小聪明'
print(str1.index('大聪明'))
str2 = str1.replace('你好', '我叫小明')
print(str2)
list1 = str1.split(' ')
print(list1)
# 11
# hello 我叫小明 我是大聪明 你是小聪明
# ['hello', '你好', '我是大聪明', '你是小聪明']

list1 = [1, 11, 43, 67, 5, 6]
list1[list1.index(67)] = '小明'
print(list1)
print(list1.index(43))
list1 = [1, 11, 43, 67, 5, 6]
list1.sort()
print(list1)
list1.reverse()
print(list1)
list1.remove(5)
print(list1)
# [1, 11, 43, '小明', 5, 6]
# 2
# [1, 5, 6, 11, 43, 67]
# [67, 43, 11, 6, 5, 1]
# [67, 43, 11, 6, 1]

a = '周天成'
b = '21'
c = '学生'
str1 = "你好，我叫{}！我今年{}岁，是一名{}。"
print(str1.format(a,b,c))
# 你好，我叫周天成！我今年21岁，是一名学生。
