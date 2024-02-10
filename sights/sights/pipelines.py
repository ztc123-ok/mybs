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
from dbutils.pooled_db import PooledDB
import pymysql

class SightsPipeline:

    # 开始处理数据 item就是传递过来的数据
    def process_item(self, item, spider):
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
        if(len(item['heat_score']) == 0):
            item['heat_score'] = '0.0'
        if(len(item['comment_count']) == 0):
            item['comment_count'] = '0'

        # 插入景点数据
        if (len(rest) == 0):
            # 创建sql语句
            # 字符串要自己加引号，非字符串不能加，时间要加引号，评论带表情字符集设置为utf8mb4
            sql = "INSERT INTO xc_sight (name,url,comment_score,comment_count,heat_score,address,open_state,open_time,phone,photos,introduction,discount,create_time,update_time) VALUES ('{}','{}',{},{},{},'{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                item['name'], item['url'], item['comment_score'], item['comment_count'], item['heat_score'],
                item['address'], item['open_state'], item['open_time'], item['phone'], item['photos'],
                item['introduction'], item['discount'],
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
            sql = "UPDATE xc_sight SET name='{}',url='{}',comment_score={},comment_count={},heat_score={},address='{}',open_state='{}',open_time='{}',phone='{}',photos='{}',introduction='{}',discount='{}',update_time='{}' where id={}".format(
                item['name'], item['url'], item['comment_score'], item['comment_count'], item['heat_score'],
                item['address'], item['open_state'], item['open_time'], item['phone'], item['photos'],
                item['introduction'], item['discount'],
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

        # min_len = min(len(item['comments_user']), len(item['comments']), len(item['comments_ip']),
        #               len(item['comments_pic']), len(item['comments_time']))
        min_len = min(len(item['comments_user']), len(item['comments']),
                      len(item['comments_pic']), len(item['comments_time']))
        if(len(item['comments_user']) != min_len or len(item['comments']) != min_len or len(item['comments_ip']) != min_len or len(item['comments_pic']) != min_len or len(item['comments_time']) != min_len):
            with open("erro.txt", "a", encoding='utf-8') as f:
                f.writelines(f"{len(item['comments_user'])}, {len(item['comments'])}, {len(item['comments_ip'])}, {len(item['comments_pic'])}, {len(item['comments_time'])},"+ str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+"\n")
        # 插入时间排序评论
        for i in range(min_len):
            sql = "select id from xc_sight where url = '{}'".format(item['url'])
            cursor.execute(sql)

            rest = cursor.fetchall()

            print("count", rest)
            if (min_len > 0 and len(rest) > 0):
                if(i >= len(item['comments_ip'])):
                    ip = '未知'
                else:
                    ip = item['comments_ip'][i]
                sql = "INSERT INTO xc_comments (sight_id,comments_user,comments,comments_ip,comments_pic,comments_time,create_time) VALUES ({},'{}','{}','{}','{}','{}','{}')".format(
                    rest[0][0], item['comments_user'][i], item['comments'][i], ip,
                    item['comments_pic'][i], item['comments_time'][i],
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                )
                try:
                    print("正在插入智能排序评论数据。。。")
                    cursor.execute(sql)
                    connect.commit()
                except BaseException as e:
                    print('插入智能的评论有误',e)
                    mystr = str(rest[0][0]) + "," + item['comments_user'][i] + "," + item['comments'][i] + "," + \
                            ip + "," + item['comments_pic'][i] + "," + item['comments_time'][
                                i] + "," + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

                    with open("erro.txt", "a", encoding='utf-8') as f:
                        f.writelines(mystr + "\n"+str(e)+"\n")

        # min_len = min(len(item['comments_user_timesort']), len(item['comments_timesort']), len(item['comments_ip_timesort']),
        #               len(item['comments_pic_timesort']), len(item['comments_time_timesort']))
        min_len = min(len(item['comments_user_timesort']), len(item['comments_timesort']),
                      len(item['comments_pic_timesort']), len(item['comments_time_timesort']))
        if (len(item['comments_user_timesort']) != min_len or len(item['comments_timesort']) != min_len or len(
                item['comments_ip_timesort']) != min_len or len(item['comments_pic_timesort']) != min_len or len(
                item['comments_time_timesort']) != min_len):
            with open("erro.txt", "a", encoding='utf-8') as f:
                f.writelines(
                    f"{len(item['comments_user_timesort'])}, {len(item['comments_timesort'])}, {len(item['comments_ip_timesort'])}, {len(item['comments_pic_timesort'])}, {len(item['comments_time_timesort'])}," + str(
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "\n")
        # 插入智能排序评论
        for i in range(min_len):
            sql = "select id from xc_sight where url = '{}'".format(item['url'])
            cursor.execute(sql)

            rest = cursor.fetchall()

            print("count", rest)

            if (min_len > 0 and len(rest) > 0):
                if(i >= len(item['comments_ip_timesort'])):
                    ip = '未知'
                else:
                    ip = item['comments_ip_timesort'][i]
                sql = "INSERT INTO xc_comments_timesort (sight_id,comments_user,comments,comments_ip,comments_pic,comments_time,create_time) VALUES ({},'{}','{}','{}','{}','{}','{}')".format(
                    rest[0][0], item['comments_user_timesort'][i], item['comments_timesort'][i],
                    ip, item['comments_pic_timesort'][i],
                    item['comments_time_timesort'][i],
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                )
                try:
                    print("正在插入时间排序评论数据。。。")
                    cursor.execute(sql)
                    connect.commit()
                except BaseException as e:
                    print('插入时间的评论有误',e)
                    mystr = str(rest[0][0]) + "," + item['comments_user_timesort'][i] + "," + \
                            item['comments_timesort'][i] + "," + ip + "," + \
                            item['comments_pic_timesort'][i] + "," + item['comments_time_timesort'][i] + "," + str(
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    with open("erro.txt", "a", encoding='utf-8') as f:
                        f.writelines(mystr + "\n"+str(e)+"\n")
        cursor.close()
        connect.close()

        # 返回Item
        return item




