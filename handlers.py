# -*- coding:utf-8 -*-

import time
from jsquery import query, queryAny
from xml import toDict, toXml
from saedb import SaeDb
from hashlib import sha1

TOKEN = '' # 微信公众号 TOKEN

def valid(signature, timestamp, nonce):
        li = []

        li.append(TOKEN)
        li.append(nonce)
        li.append(timestamp)

        li.sort()

        tmpWord = ''.join(li)
        tmpWord = sha1(tmpWord).hexdigest()


        if tmpWord == signature:
            return True
        else:
            return False
    
def processXml(xml):

    help = u'''使用指南:
1 查询净值 000001
2 基金订阅 a000001
3 查询订阅 c
4 取消订阅 r000001
5 <a href="https://me.alipay.com/zhu327">点击赞助</a>
'''

    xdict = toDict(xml)
    if xdict['MsgType'] == 'event':
        if xdict['Event'] == 'subscribe':
            # 返回欢迎订阅，与帮助信息
            text = u"欢迎订阅基金查查"
            text = '\n'.join([text, help])
        elif xdict['Event'] == 'unsubscribe':
            db = SaeDb(xdict['FromUserName'])
            db.delete()
            return None
    elif xdict['MsgType'] == 'text':
        t = xdict['Content']
        if t.isdigit():
            data = query(t)
            if data:
                # data['result'][t]信息渲染xml模版返回
                text = u"%s\n净值: %s\n涨幅: %s" % (data['name'], data['newnet'], data['daygrowrate'])
            else:
                # 返回基金代码错误
                text = u'基金代码错误'
        elif t.startswith('a') and t[1:].isdigit():
            data = query(t[1:])
            if data:
                # t[1:]基金代码存入xdict['FromUserName']订阅数据库字典
                db = SaeDb(xdict['FromUserName'])
                if db.len() < 5:
                    db.append(t[1:])
                    text = u'订阅成功,输入c查询'
                else:
                    text = u'最多订阅5支'
            else:
                # 返回基金代码错误
                text = u'基金代码错误'
        elif t.startswith('r') and t[1:].isdigit():
            # 如果数据库中有t[1:]则删除，返回删除成功
            db = SaeDb(xdict['FromUserName'])
            db.remove(t[1:])
            text = u'取消订阅成功'
        elif t == 'c':
            # 查询xdict['FromUserName']订阅字典
            # data = getResult(list)
            # 渲染结果
            db = SaeDb(xdict['FromUserName'])
            codes = db.get()
            if codes:
                data = queryAny(codes)
                l = list()
                for d in data:
                    text = u"%s\n代码: %s\n净值: %s\n涨幅: %s" % (d['name'], \
                    d['code'], d['newnet'], d['daygrowrate'])
                    l.append(text)
                text = '\n'.join(l)
            else:
                text = u'请订阅后再查询'
        else:
            # 返回帮助信息
            text = help
    else:
        # 返回帮助信息
        text = help
    kw = dict.fromkeys(['ToUserName', 'FromUserName', 'CreateTime', 'Content'])
    kw['ToUserName'] = xdict['FromUserName']
    kw['FromUserName'] = xdict['ToUserName']
    kw['CreateTime'] = int(time.time())
    kw['Content'] = text
    return toXml(kw)
    
