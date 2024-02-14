import pymysql

connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou",
                          charset="utf8")
cursor = connect.cursor()
sql = "select id from xc_sight"
cursor.execute(sql)
results = [row[0] for row in cursor.fetchall()]
print(list(results))
