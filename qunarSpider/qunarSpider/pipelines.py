# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from .items import QunarspiderItem, CatchOneItem
import pymysql
import time
class QunarspiderPipeline:
    def process_item(self, item, spider):
        if(not isinstance(item,QunarspiderItem)):
            print("跳过一次处理")
            return item
        print("运行到QunarspiderPipeline了")
        print("从item中拿到para_name:",item['para_name'])
        connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou",
                                       charset="utf8")
        cursor = connect.cursor()

        print("开始向数据库插入景点数据。。。。")
        sql = "select id from xc_sight where url = '{}'".format(item['url'])
        cursor.execute(sql)

        rest = cursor.fetchall()
        print("count", rest)
        # count [{'id': 16}]

        # 数据类型为空异常处理
        if(len(item['comment_score']) == 0):
            item['comment_score'] = '0.0'

        # 插入景点数据
        if (len(rest) == 0):
            # 创建sql语句
            # 字符串要自己加引号，非字符串不能加，时间要加引号，评论带表情字符集设置为utf8mb4
            sql = "INSERT INTO qn_sight (name,url,comment_score,ticket,travel_time,transportation,tip_time,create_time,update_time) VALUES ('{}','{}',{},'{}','{}','{}','{}','{}','{}')".format(
                item['name'], item['url'], item['comment_score'], item['ticket'], item['travel_time'],
                item['transportation'], item['tip_time'],
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            # 执行sql语句
            try:
                cursor.execute(sql)
                connect.commit()
            except BaseException as e:
                print('插入景点有误:',e)
                with open("erro.txt", "a", encoding='utf-8') as f:
                    f.writelines("景点url:" + item['url'] + "\n"+str(e)+"\n")
        # 更新景点数据
        else:
            # 创建sql语句
            sql = "UPDATE xc_sight SET name='{}',url='{}',comment_score={},ticket='{}',travel_time='{}',transportation='{}',tip_time='{}',update_time='{}' where id={}".format(
                item['name'], item['url'], item['comment_score'], item['ticket'], item['travel_time'],
                item['transportation'], item['tip_time'],
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                rest[0][0])
            # 执行sql语句
            try:
                cursor.execute(sql)
                connect.commit()
            except BaseException as e:
                print('更新景点有误',e)
                with open("erro.txt", "a", encoding='utf-8') as f:
                    f.writelines("景点url:" + item['url'] + "\n"+str(e)+"\n")

        return item

class CatchOnePipeline:
    def process_item(self, item, spider):
        if(not isinstance(item,CatchOneItem)):
            print("跳过一次处理")
            return item
        print("运行到CatchOnePipeline了")
        print("从item中拿到para_name:",item['para_name'])
        return item
