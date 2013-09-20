# -*- coding:utf-8 -*-

import urllib2, HTMLParser, gzip, StringIO

class FundParser(HTMLParser.HTMLParser):
    """ 定义了html解析的方法
        根据新浪基金网页找对应的标签以及属性值
    """
    def __init__(self):
        self.tags = ['h1', 'span']
        self.f = 0
        self.data = {}
        HTMLParser.HTMLParser.__init__(self)
    def handle_starttag(self, tag, attrs):
        if tag in self.tags:
            if len(attrs) == 0: pass
            else:
                for name,value in attrs:
                    if name == "class":
                        if value == "title":
                            self.f = 1
                        elif value == "asset-value":
                            self.f = 2
                        elif value in ("asset-amt red", "asset-amt green"):
                            self.f = 3
                        elif value == "code":
                            self.f = 4
    def handle_data(self, data):
        if self.f == 1:
            self.data['name'] = data.decode('gb2312')
        elif self.f == 2:
            self.data['newnet'] = data.decode('gb2312')
        elif self.f == 3:
            self.data['daygrowrate'] = data.decode('gb2312')
        elif self.f == 4:
            self.data['code'] = data[1:-1].decode('gb2312')
    def handle_endtag(self, tag):
        if tag in self.tags:
            self.f = 0

def getRsponse(code):
    """ 获取基金代码在新浪基金对应的html,输入为基金代号
        新浪的网页默认gzip压缩，这里对其解压缩
    """
    url = "http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=%s&country=fund"    
    full_url = url % code
    response = urllib2.urlopen(full_url)
    headers = response.info()
    data = response.read()
    if 'gzip' == headers.get('Content-Encoding'):
        tmp = StringIO.StringIO(data)
        gz = gzip.GzipFile(fileobj=tmp)
        data = gz.read()
        gz.close()
    return data
    
def getResult(codes):
    """ 输入参数为列表,遍历列表生成净值字典,并附带处理状态码
        resultcode:
        200 返回正常
        101 基金代码非数字
        201 基金代码不存在
    """
    result = dict.fromkeys(['resultcode', 'result'])
    def _xFun(s):
        return s.isdigit()
    if False in map(_xFun, codes):
        result["resultcode"] = 101
        return result
    data = list()
    for code in codes:
        r = getRsponse(code)
        fp = FundParser()
        fp.feed(r)
        if 4 != len(fp.data):
            result["resultcode"] = 201
            return result
        data.append(fp.data)
    result["resultcode"] = 200
    result["result"] = data
    return result

