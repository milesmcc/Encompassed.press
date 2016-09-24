import tornado.ioloop
import tornado.web
import json

class PrettyHandler(tornado.web.RequestHandler):
    def get(self):
        with open("top.json") as data_file:
            top = json.load(data_file)
        self.set_header("Content-Type", "application/json")
        self.write(unicode(json.dumps(top, sort_keys=True, indent=4)))
class ApiHandler(tornado.web.RequestHandler):
    def get(self):
        with open("top.json") as data_file:
            top = json.load(data_file)
        self.set_header("Content-Type", "application/json")
        self.write(unicode(json.dumps(top, separators=(",", ":"))))
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        with open("top.json") as data_file:
            top = json.load(data_file)
        self.render("page.html", article = top)
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/api", ApiHandler),
    (r"/pretty", PrettyHandler)
    ])
api = tornado.web.Application([(r"/", MainHandler),])
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

# tornado is a beautiful thing....
