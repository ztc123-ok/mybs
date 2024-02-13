import json

my_dict = {'Apple': 4, 'Banana': 2, 'Orange': 6, 'Grapes': 11}
# 保存文件
tf = open("myDictionary.json", "w")
json.dump(my_dict, tf)
tf.close()
# 读取文件
tf = open("myDictionary.json", "r")
new_dict = json.load(tf)
print(new_dict)
