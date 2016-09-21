import tornado.ioloop
import tornado.web
import json



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        with open("top.json") as data_file:
            top = json.load(data_file)
        self.render("page.html", article = top)
application = tornado.web.Application([(r"/", MainHandler),])
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

# tornado is a beautiful thing....
