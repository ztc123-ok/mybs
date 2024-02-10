import pymysql

connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou",
                          charset="utf8")
cursor = connect.cursor()

sql = "SELECT id,heat_score FROM xc_sight"

cursor.execute(sql)
# connect.commit()
rest = cursor.fetchall()
rest = dict(rest)
print(rest[1])
