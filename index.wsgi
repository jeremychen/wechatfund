# -*- coding: utf-8 -*-

#import tornado.ioloop
import tornado.web
import handlers
            
class WechatHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            if handlers.valid(self.get_argument('signature'),
                        self.get_argument('timestamp'),
                        self.get_argument('nonce')):
                self.write(self.get_argument('echostr'))
        except tornado.web.HTTPError:
            self.write('')
    
    def post(self):
        try:
            if handlers.valid(self.get_argument('signature'),
                        self.get_argument('timestamp'),
                        self.get_argument('nonce')):
                data = handlers.processXml(self.request.body)
                self.set_header("Content-Type", "application/xml; charset=UTF-8")
                self.write(data)
        except tornado.web.HTTPError:
            self.write('')

application = tornado.web.Application([
    (r"/wechatfund", WechatHandler),
    (r"/", tornado.web.RedirectHandler, dict(url="https://github.com/zhu327/wechatfund")),
], debug=True)

#if __name__ == "__main__":
#    application.listen(8888)
#    tornado.ioloop.IOLoop.instance().start()
