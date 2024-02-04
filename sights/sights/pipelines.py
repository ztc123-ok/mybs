# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymysql import cursors
from twisted.enterprise import adbapi
import time
import copy

class SightsPipeline:

    # 初始化函数
    def __init__(self, db_pool):
        self.db_pool = db_pool

    # 从settings配置文件中读取参数
    @classmethod
    def from_settings(cls, settings):
        # 用一个db_params接收连接数据库的参数
        db_params = dict(
            host='localhost',
            user='root',
            password='root',
            port=3307,
            database='hangzhou',
            charset='utf8',
            use_unicode=True,
            # 设置游标类型
            cursorclass=cursors.DictCursor
        )
        # 创建连接池
        db_pool = adbapi.ConnectionPool('pymysql', **db_params)

        # 返回一个pipeline对象
        return cls(db_pool)

    # 处理item函数
    def process_item(self, item, spider):
        # 对象拷贝，深拷贝  --- 这里是解决数据重复问题！！！
        asynItem = copy.deepcopy(item)

        # 把要执行的sql放入连接池
        query = self.db_pool.runInteraction(self.insert_into, asynItem)

        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error, item, spider)

        # 返回Item
        return item

    # 处理sql函数
    def insert_into(self, cursor, item):
        # SQL 查询语句，查询user表中name字段中的数据
        sql = "select id from xc_sight where url = '{}'".format(item['url'])
        cursor.execute(sql)

        rest = cursor.fetchall()
        print("count",rest)
        #count [{'id': 16}]

        #插入景点数据
        if(len(rest) == 0):
            # 创建sql语句
            # 字符串要自己加引号，非字符串不能加，时间要加引号，评论带表情字符集设置为utf8mb4
            sql = "INSERT INTO xc_sight (name,url,comment_score,comment_count,heat_score,address,open_state,open_time,phone,photos,introduction,discount,create_time,update_time) VALUES ('{}','{}',{},{},{},'{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                item['name'], item['url'], item['comment_score'], item['comment_count'], item['heat_score'],item['address'],item['open_state'],item['open_time'],item['phone'],item['photos'],item['introduction'],item['discount'],
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            # 执行sql语句
            try:
                cursor.execute(sql)
            except:
                print('插入景点有误')
                with open("erro.txt", "a",encoding='utf-8') as f:
                    f.writelines("景点url:"+ item['url'] + "\n")

        else:
            # 创建sql语句
            sql = "UPDATE xc_sight SET name='{}',url='{}',comment_score={},comment_count={},heat_score={},address='{}',open_state='{}',open_time='{}',phone='{}',photos='{}',introduction='{}',discount='{}',update_time='{}' where id={}".format(
                item['name'], item['url'], item['comment_score'], item['comment_count'], item['heat_score'],item['address'],item['open_state'],item['open_time'],item['phone'],item['photos'],item['introduction'],item['discount'],
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                rest[0]['id'])
            # 执行sql语句
            try:
                cursor.execute(sql)
            except:
                print('更新景点有误')
                with open("erro.txt", "a",encoding='utf-8') as f:
                    f.writelines("景点url:"+ item['url'] + "\n")

        sql = "select id from xc_sight where url = '{}'".format(item['url'])
        cursor.execute(sql)

        rest = cursor.fetchall()

        print("count",rest)

        #插入智能排序评论数据
        if(len(item['comments']) > 0 and len(rest) > 0):
            for i in range(len(item['comments'])):
                sql = "INSERT INTO xc_comments (sight_id,comments_user,comments,comments_ip,comments_pic,comments_time,create_time) VALUES ({},'{}','{}','{}','{}','{}','{}')".format(
                    rest[0]['id'],item['comments_user'][i],item['comments'][i],item['comments_ip'][i],item['comments_pic'][i],item['comments_time'][i],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                )
                try:
                    cursor.execute(sql)
                except:
                    print('插入智能的评论有误')
                    mystr = str(rest[0]['id']) + "," + item['comments_user'][i] + "," + \
                            item['comments'][i] + "," + item['comments_ip'][i] + "," + \
                            +item['comments_pic'][i] + "," + item['comments_time'][i] + "," + str(
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    with open("erro.txt", "a", encoding='utf-8') as f:
                        f.writelines(mystr + "\n")

        # 插入时间排序评论数据
        if (len(item['comments_timesort']) > 0 and len(rest) > 0):
            for i in range(len(item['comments_timesort'])):
                sql = "INSERT INTO xc_comments_timesort (sight_id,comments_user,comments,comments_ip,comments_pic,comments_time,create_time) VALUES ({},'{}','{}','{}','{}','{}','{}')".format(
                    rest[0]['id'], item['comments_user_timesort'][i], item['comments_timesort'][i],item['comments_ip_timesort'][i],item['comments_pic_timesort'][i],item['comments_time_timesort'][i] ,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                )
                try:
                    cursor.execute(sql)
                except:
                    print('插入时间的评论有误')
                    mystr = str(rest[0]['id'])+","+item['comments_user_timesort'][i]+","+item['comments_timesort'][i]+","+item['comments_ip_timesort'][i]+","+item['comments_pic_timesort'][i]+","+item['comments_time_timesort'][i]+","+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    with open("erro.txt", "a",encoding='utf-8') as f:
                        f.writelines(mystr+ "\n")


    # 错误函数
    def handle_error(self, failure, item, spider):
        # #输出错误信息
        print("failure", failure)


