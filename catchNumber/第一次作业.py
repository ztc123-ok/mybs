import  pymysql

connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou", charset="utf8")
cursor = connect.cursor()

sql = "select id,comments from xc_comments_timesort where sight_id = {} and (positive IS NULL OR positive = '')".format(1)
cursor.execute(sql)
rest = cursor.fetchall()
print(rest)
cursor.close()
connect.close()

