import os
import re
import jieba
import jieba.posseg as psg
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import emoji
import pymysql

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
def read_data(sight_id):

    connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou",
                                           charset="utf8")
    cursor = connect.cursor()

    get_comments = "SELECT comments FROM xc_comments where sight_id = {}".format(id)
    get_comments_timesort = "SELECT comments FROM xc_comments_timesort where sight_id = {}".format(id)

    cursor.execute(get_comments)
    comments = [row[0] for row in cursor.fetchall()]
    cursor.execute(get_comments_timesort)
    comments_timesort = [row[0] for row in cursor.fetchall()]
    print(comments[:2])
    print(comments_timesort[:2])

    stop = []  # 停用词表
    texts = []  # 评论
    texts_timesort = []  # 时间排序评论

    file_stop = './stopwords/hit_stopwords.txt'  # 停用词表
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
        texts.append(words)
    for comment in comments_timesort:
        words = []  # 存放切词后、去除停用词后的句子词组
        # 使用jieba对评论进行分词
        for word in jieba.lcut(comment):
            # 若切出来的词语 不属于停用词表， 加入词组中
            if word not in stop:
                words.append(word)
        texts_timesort.append(words)

    cursor.close()
    connect.close()

    return texts,texts_timesort

pwd_path = r'2021-test/'

fileList = os.listdir(pwd_path)

def keep_noun_split_words(text):
    seg_list = psg.cut(text)
    flag_list = ['n', 'nz', 'vn']
    word_list = []
    for seg_word in seg_list:
        if seg_word.flag in flag_list and len(seg_word.word) > 1:
            word_list.append(seg_word.word)
    return ' '.join(word_list)


df = pd.DataFrame(fileList)
df.columns = ['file']

for line in range(len(df)):
    fileNM = df.loc[line, 'file']
    with open(pwd_path + fileNM, 'r', encoding='utf-8') as file:
        df.loc[line, 'text'] = file.read()

df['content'] = df['text'].apply(del_stopwords_keep_charactersCN).apply(keep_noun_split_words)

a = df['content'].tolist()

tf_vectorizer = CountVectorizer(max_df=0.95, min_df=5, max_features=1000)
tf = tf_vectorizer.fit_transform(a)

lda = LatentDirichletAllocation(n_components=10, max_iter=50, learning_method='batch', random_state=12345)
lda.fit(tf)

def print_top_words(model, feature_names, n_top_words):
    tword = []
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        topic_w = " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words -1:-1]])
        tword.append(topic_w)
        print(topic_w)
    return tword

print_top_words(lda, tf_vectorizer.get_feature_names(), 5)

def get_id():
    connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou",
                                           charset="utf8")
    cursor = connect.cursor()
    get_id = "SELECT id FROM xc_sight"
    cursor.execute(get_id)
    list_id = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connect.close()
    return  list_id
if __name__ == "__main__":
    sight_id = 2

    if sight_id == None:
        list_id = get_id()
    else:
        list_id = [sight_id]

    for id in list_id:
        texts, texts_timesort = read_data(id)