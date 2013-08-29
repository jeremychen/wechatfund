# 基金查查 #

[@Timmy](http://weibo.com/zhu327)

## 功能 ##

1. 微信公众账号基金净值查询与订阅;
2. 基金净值查询api.

## 部署 ##
### 环境 ###

SAE(Sina App Engine) python tornado环境,kvDB开启支持.

### 部署 ###

需要修改的文件:

    weichatfund
        |--views.py
        
该文件TOKEN字符串该为微信公众号申请时填写的TOKEN.
        
## 开发 ##
### 结构 ###

    wechatfund
        |--config.yaml    SAE的配置文件
        |--index.wgsi     tornado main文件
        |--query.py       抓取新浪基金信息
        |--saedb.py       sae kvdb封装
        |--views.py       视图函数
        |--wxxml.py       微信xml处理

### 设计 ###

#### 功能1 ####

注册微信公众号试,填写url必须为http://yourhost/wx
1. 输入基金代码直接查询基金净值
2. 输入a+基金代码订阅基金,数据存入kvdb,key为用户id,value为通过cPickle序列化后的list
3. 输入r+基金代码取消订阅,kvdb直接删除该基金代码
4. 输入c查询订阅基金,遍历用户id对应的list

#### 功能2 ####

请求方式为:
http://yourhost/query?q=基金代码1|基金代码2

返回JSON格式:

    {
        "resultcode": 200,                                      # 返回结果码,200正常,101输入不正确,201基金不存在
        "result": [
            {
                "code": "000001",   # 基金代码
                "name": "\u534e\u590f\u6210\u957f\u6df7\u5408", # 基金名称
                "daygrowrate": "-1.27%",                        # 基金涨幅
                "newnet": "1.0860"                              # 基金净值
            }
        ]
        ...
    }
