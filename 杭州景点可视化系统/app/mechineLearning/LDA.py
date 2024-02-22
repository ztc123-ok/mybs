import os
import re
import jieba
import jieba.posseg as psg
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import emoji
import pymysql
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from django.core.files.storage import FileSystemStorage
from django.conf import settings
def clean(list,restr=''):
    # 过滤表情,我还得专门下个emoji的库可还行，数据库字段设utf8mb4好像也行,字段里含有‘和“写sql也会错
    # 谁家取昵称还带表情啊
    try:
        co = re.compile(
            u'['u'\U0001F300-\U0001F64F'u'\U00010000-\U0010ffff' u'\U0001F680-\U0001F6FF'u'\u2600-\u2B55]+')
    except re.error:
        co = re.compile(
            u'('u'\ud83c[\udf00-\udfff]|'u'[\uD800-\uDBFF][\uDC00-\uDFFF]'u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'u'[\u2600-\u2B55])+')
    if (isinstance(list, str)):
        list = co.sub(restr, list)
        list = emoji.replace_emoji(list, restr)
        list = list.replace("'", restr)
        list = list.replace('"', restr)
        list = list.replace(' ',restr)
        list = list.replace('\n',restr)
        list = list.replace('\\', restr)
    else:
        for i in range(len(list)):
            list[i] = co.sub(restr, list[i])
            list[i] = emoji.replace_emoji(list[i], restr)
            list[i] = list[i].replace("'", restr)
            list[i] = list[i].replace('"', restr)
            list[i] = list[i].replace(' ',restr)
            list[i] = list[i].replace('\n',restr)
            list[i] = list[i].replace('\\', restr)

    return list
def read_data(sight_id,enviroment = None):

    connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou",
                                           charset="utf8")
    cursor = connect.cursor()

    get_comments = "SELECT comments FROM xc_comments where sight_id = {}".format(sight_id)
    get_comments_timesort = "SELECT comments FROM xc_comments_timesort where sight_id = {}".format(sight_id)

    cursor.execute(get_comments)
    comments = [row[0] for row in cursor.fetchall()]
    cursor.execute(get_comments_timesort)
    comments_timesort = [row[0] for row in cursor.fetchall()]
    print(comments[:2])
    print(comments_timesort[:2])

    stop = []  # 停用词表
    texts = []  # 评论
    texts_timesort = []  # 时间排序评论

    if enviroment != None:
        file_stop = 'topic_stopwords.txt'  # 停用词表
    else:
        file_stop = 'app/mechineLearning/topic_stopwords.txt'  # 停用词表

    with open(file_stop, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()  # lines是list类型
        for line in lines:
            lline = line.strip()  # line 是str类型,strip 去掉\n换行符
            stop.append(lline)  # 将stop 是列表形式
    print("stop[]:", stop[:20])

    for comment in comments:
        words = []  # 存放切词后、去除停用词后的句子词组
        # 使用jieba对评论进行分词
        for word in jieba.lcut(comment):
            # 若切出来的词语 不属于停用词表， 加入词组中
            if word not in stop:
                words.append(word)
        words = ''.join(words)
        texts.append(words)
    for comment in comments_timesort:
        words = []  # 存放切词后、去除停用词后的句子词组
        # 使用jieba对评论进行分词
        for word in jieba.lcut(comment):
            # 若切出来的词语 不属于停用词表， 加入词组中
            if word not in stop:
                words.append(word)
        words = ''.join(words)
        texts_timesort.append(words)

    cursor.close()
    connect.close()

    return texts,texts_timesort

def keep_noun_split_words(text):
    seg_list = psg.cut(text)
    # 词性筛选
    #flag_list = ['n','an','v','a','b','nr','vn']
    #flag_list = ['n', 'v', 'a']
    flag_list = ['n'] # 景点特色
    word_list = []
    for seg_word in seg_list:
        if seg_word.flag in flag_list and len(seg_word.word) > 1:
            word_list.append(seg_word.word)
    return ' '.join(word_list)

def keep_adj_split_words(text):
    seg_list = psg.cut(text)
    # 词性筛选
    #flag_list = ['n','an','v','a','b','nr','vn']
    #flag_list = ['n', 'v', 'a']
    flag_list = ['a','v'] # 游客感受
    word_list = []
    for seg_word in seg_list:
        if seg_word.flag in flag_list and len(seg_word.word) > 1:
            word_list.append(seg_word.word)
    return ' '.join(word_list)

def get_pic_words(texts,sight_id):

    flag_list = ['n','an','v','a','b','nr','vn','nrfg']
    word_list = {}
    for words in texts:
        seg_list = psg.cut(words)
        for seg_word in seg_list:
            if seg_word.flag in flag_list and len(seg_word.word) > 1:
                word_list[seg_word.word] = word_list.get(seg_word.word, 0) + 1

    # 以下部分需在系统中展示，这里是测试演示，系统展示本部分需要删除

    # 按词频从高到低排序
    counts = sorted(word_list.items(), key=lambda x: x[1], reverse=True)
    # 输出前10个
    if len(counts) < 10:
        return counts
    for i in range(10):
        word, count = counts[i]
        print('{:<10}{:>5}'.format(word, count))
    # 绘制柱状图
    x_word = []
    y_count = []
    for i in range(10):
        word, count = counts[i]
        x_word.append(word)
        y_count.append(count)
    # 设置显示中文
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 设置图片大小
    plt.figure(figsize=(20, 15))
    plt.bar(range(len(y_count)), y_count, color='r', tick_label=x_word, facecolor='#9999ff', edgecolor='white')
    # 这里是调节横坐标的倾斜度，rotation是度数，以及设置刻度字体大小
    plt.xticks(rotation=45, fontsize=20)
    plt.yticks(fontsize=20)
    # plt.legend()
    plt.title("景点 {} 评论词频统计".format(sight_id), fontsize=24)
    # plt.savefig('bar_result_{}.jpg'.format(sight_id)) # 保存词频柱状图
    #plt.show()
    # counts[('不错',1422),('值得',766)...]
    return counts


# 绘制词云图
def drawcloud(texts,sight_id,enviroment=None):
    strs = ""
    flag_list = ['n', 'an', 'v', 'a', 'b', 'nr', 'vn']
    for words in texts:
        seg_list = psg.cut(words)
        for seg_word in seg_list:
            if seg_word.flag in flag_list and len(seg_word.word) > 1:
                strs = strs + " " + seg_word.word
    # 生成对象
    wc = WordCloud(font_path="msyh.ttc",
                             width=1000,
                             height=700,
                             background_color='white',
                             max_words=100).generate(strs)
    # 显示词云图
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    #plt.show()
    # 保存文件
    if enviroment != None:
        wc.to_file(os.path.join(r"D:\www\mybs\杭州景点可视化系统\media\WordCloud", "WordCloud_{}.png".format(sight_id)))
    else:
        wc.to_file(os.path.join(os.path.join(settings.MEDIA_ROOT, 'WordCloud'),"WordCloud_{}.png".format(sight_id)))

def print_top_words(model, feature_names, n_top_words):
    tword = []
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        topic_w = " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words -1:-1]])
        tword.append(topic_w)
        print(topic_w)
    return tword


def get_id():
    connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou",
                                           charset="utf8")
    cursor = connect.cursor()
    get_id = "SELECT id FROM xc_sight"
    cursor.execute(get_id)
    list_id = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connect.close()
    return list_id

def save_topic(tword,sight_id):
    topics = ";".join(tword)
    connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou",
                                           charset="utf8")
    cursor = connect.cursor()
    update_topic = "UPDATE xc_sight SET topic = '{}' where id = {}".format(topics,sight_id)
    cursor.execute(update_topic)
    connect.commit()

    cursor.close()
    connect.close()

def doLDA(id):
    texts, texts_timesort = read_data(id)

    texts = texts_timesort + texts

    data = pd.DataFrame({
        'content': texts  # 实际的评论文本
    })
    # 词频统计
    word_list = get_pic_words(texts,id)
    # 绘制词云图
    drawcloud(texts,id)

    data["content_noun"] = data.content.apply(keep_noun_split_words)
    data["content_adj"] = data.content.apply(keep_adj_split_words)

    tf_vectorizer_noun = CountVectorizer(max_df=0.95, min_df=5, max_features=1000)
    tf_vectorizer_adj = CountVectorizer(max_df=0.95, min_df=5, max_features=1000)
    tf_noun = tf_vectorizer_noun.fit_transform(data["content_noun"].tolist())
    tf_adj = tf_vectorizer_adj.fit_transform(data["content_adj"].tolist())

    # 看下来2个效果比较好，一个是景点特色，一个是游客感受
    lda = LatentDirichletAllocation(n_components=1, max_iter=60, learning_method='batch', random_state=12345)
    lda.fit(tf_noun)
    # 景点特色
    tword_noun = print_top_words(lda, tf_vectorizer_noun.get_feature_names_out(), 8)
    lda.fit(tf_adj)
    # 游客感受
    tword_adj = print_top_words(lda, tf_vectorizer_adj.get_feature_names_out(), 8)
    tword = tword_noun + tword_adj
    # save_topic(tword,id)

    return ";".join(tword)

if __name__ == "__main__":
    # sight_id = 12
    my_list = list(range(371, 1861))
    for id in my_list:
        texts, texts_timesort = read_data(id,"外部运行")

        texts = texts_timesort + texts
        data = pd.DataFrame({
            'content': texts  # 实际的评论文本
        })
        # 词频统计
        word_list = get_pic_words(texts,id)
        if len(word_list) == 0:
            continue
        # 绘制词云图
        drawcloud(texts,id,"外部运行")

        data["content_noun"] = data.content.apply(keep_noun_split_words)
        data["content_adj"] = data.content.apply(keep_adj_split_words)

        tf_vectorizer_noun = CountVectorizer(max_df=0.95, min_df=5, max_features=1000)
        tf_vectorizer_adj = CountVectorizer(max_df=0.95, min_df=5, max_features=1000)

        try:
            tf_noun = tf_vectorizer_noun.fit_transform(data["content_noun"].tolist())
            tf_adj = tf_vectorizer_adj.fit_transform(data["content_adj"].tolist())

            # 看下来2个效果比较好，一个是景点特色，一个是游客感受
            lda = LatentDirichletAllocation(n_components=1, max_iter=60, learning_method='batch', random_state=12345)
            lda.fit(tf_noun)
            # 景点特色
            tword = print_top_words(lda, tf_vectorizer_noun.get_feature_names_out(), 8)
            lda.fit(tf_adj)
            # 游客感受
            tword = tword + print_top_words(lda, tf_vectorizer_adj.get_feature_names_out(), 8)
            save_topic(tword,id)
        except:
            pass


