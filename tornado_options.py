from tornado import web
import tornado
from tornado.options import define, options

define('port', 8080, help="Run on this port", type=int)
define('debug', True, help="Turn debug model", type=bool)
# 通过命令行加载参数
options.parse_command_line()
# 通过文件加载参数
options.parse_config_file('conf.cfg')


class MainHandler(web.RequestHandler):
    async def get(self, *args, **kwargs):
        # print("in main handler")
        # self.write("hello boy")
        # 如果有多于一个的值，直接传入即可，reverse_url 会将正则一起返回
        self.redirect(self.reverse_url('usercenter', 'evan', 19))

class PeopleIdHandler(web.RequestHandler):
    async def get(self, id, *args, **kwargs):
        self.write("People Id :{}".format(id))

class PeopleInfoHandler(web.RequestHandler):
    async def get(self, name, age, gender, *args, **kwargs):
        self.write("Name:{} Age:{} Gender:{}".format(name, age, gender))

class PeopleUserCenter(web.RequestHandler):
    def initialize(self, name):# **kwargs 中的参数会映射进来
        self.db_name = name

    async def get(self, age, name, *args, **kwargs):
        print(self.db_name)
        self.write("Usercenter of {}:Age:{}".format(name, age))

people_db = {
    "name":"people"
}

urls = [
    (r'/', MainHandler),
    (r'/people/(\d+)/?', PeopleIdHandler),
    # 不指定对应参数，后面的问号可以在链接没有'/'的时候补全
    (r'/people/(\w+)/(\d+)/(\w+)/?', PeopleInfoHandler),
    # 直接通过 web 中的 URLSpec 实例化，好处是可以传入 name，在 redirect 的时候比较方便
    tornado.web.URLSpec(r'/people/(?P<name>\w+)/center/(?P<age>\d+)/?', PeopleUserCenter, people_db ,name="usercenter"),
]

if __name__ == "__main__":
    app = web.Application(urls,debug=options.debug)
    print(options.debug)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


