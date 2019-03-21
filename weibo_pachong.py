# encoding:UTF-8
import pymysql
import re
import time
import requests

weibo_id = '4160547165300149'
url='https://m.weibo.cn/api/comments/show?id=' + weibo_id+'&page={}'
headers = {
    'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
    'Accept' : 'application/json, text/plain, */*',
    'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding' : 'gzip, deflate, br',
    'Referer' : 'https://m.weibo.cn/detail/' + weibo_id,
    'Cookie' : '_T_WM=2c84be31e095e5aee9092d5cbd74dfac; ALF=1555551358; SUHB=0la18ys8kHAqDV; SSOLoginState=1553165160; MLOGIN=1; XSRF-TOKEN=e22661',
    'DNT' : '1',
    'Connection' : 'keep-alive',
    }

i = 0
comment_num = 1
while True:

    r = requests.get(url.format(i), headers=headers)
    comment_page = r.json()['data']['data']

    if r.content:

        print('正在读取第 %s 页评论：' % i)
        for j in range(0,len(comment_page)):
            print('第 %s 条评论' % comment_num)
            user = comment_page[j]
            comment_id = user['user']['id']
            print(comment_id)
            user_name = user['user']['screen_name']
            print(user_name)
            created_at = user['created_at']
            print(created_at)
            text = re.sub('<.*?>|回复<.*?>:|[\U00010000-\U0010ffff]|[\uD800-\uDBFF][\uDC00-\uDFFF]','',user['text'])
            print(text)
            likenum = user['like_counts']
            print(likenum)
            source = re.sub('[\U00010000-\U0010ffff]|[\uD800-\uDBFF][\uDC00-\uDFFF]','',user['source'])
            print(source + '\r\n')
            conn =pymysql.connect(host='127.0.0.1',db='weibo_nlp',user='root',password='1234',charset="utf8",use_unicode = False)
            cur = conn.cursor()
            sql = "insert into weibo_text(comment_id,user_name,created_at,text,likenum,source) values(%s,%s,%s,%s,%s,%s)"
            param = (comment_id,user_name,created_at,text,likenum,source)
            try:
                A = cur.execute(sql,param)
                conn.commit()
            except Exception as e:
                print(e)
                conn.rollback()
            comment_num+=1
        i += 1
        time.sleep(3)
    else:
        break
