# -*- coding: utf-8 -*-

#import tornado.ioloop
import tornado.web
import views

class Query(tornado.web.RequestHandler):
    def get(self):
        if self.get_argument('q', default=None):
            data = views.resultJson(self.get_argument('q'))
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(data)
        else:
            raise tornado.web.HTTPError(404)
            
class WinxinPost(tornado.web.RequestHandler):
    def get(self):
        if views.valid(self.get_argument('signature'),
                       self.get_argument('timestamp'),
                       self.get_argument('nonce')):
            self.write(self.get_argument('echostr'))
    
    def post(self):
        if views.valid(self.get_argument('signature'),
                       self.get_argument('timestamp'),
                       self.get_argument('nonce')):
            data = views.processXml(self.request.body)
            self.set_header("Content-Type", "application/xml; charset=UTF-8")
            self.write(data)

application = tornado.web.Application([
    (r"/query", Query),
    (r"/wx", WinxinPost),
    (r"/", tornado.web.RedirectHandler, dict(url="https://github.com/zhu327/wechatfund")),
], debug=True)

#if __name__ == "__main__":
#    application.listen(8888)
#    tornado.ioloop.IOLoop.instance().start()