import pymysql

# connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou",
#                           charset="utf8")
# cursor = connect.cursor()
#
# sql = "SELECT comments_time FROM xc_comments_timesort WHERE sight_id=29999"
#
# cursor.execute(sql)
# # connect.commit()
# rest = cursor.fetchall()
# latest_date = max(rest)
# print(latest_date)
list = [1,2,3,4,5,6]
print(list[:1])
