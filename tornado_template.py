import os
import sys

from tornado import web
import tornado
from tornado.web import template

root = os.path.dirname(os.path.abspath(__file__))


class MainHandler(web.RequestHandler):
	def get(self, *args, **kwargs):
		word = "hello boy"
		# 以下方式为直接
		# t = template.Template("<h1>{{ word }}</h1>")
		# self.finish(t.generate(word=word))
		# 以下方式为从文件中读取
		# loader = template.Loader(os.path.join(root, "templates"))
		# self.finish(loader.load("hello.html").generate(word=word))
		# 以下方式为常用的渲染方式，需要在 settings 中定义 template 路径
		self.render("hello.html",word=word)

class PeopleIdHandler(web.RequestHandler):
	async def get(self, id, *args, **kwargs):
		self.write("People Id :{}".format(id))


class PeopleInfoHandler(web.RequestHandler):
	async def get(self, name, age, gender, *args, **kwargs):
		self.write("Name:{} Age:{} Gender:{}".format(name, age, gender))


class PeopleUserCenter(web.RequestHandler):
	def initialize(self, name):  # **kwargs 中的参数会映射进来
		self.db_name = name

	async def get(self, age, name, *args, **kwargs):
		print(self.db_name)
		self.write("Usercenter of {}:Age:{}".format(name, age))


people_db = {
	"name": "people"
}

urls = [
	(r'/', MainHandler),
	(r'/people/(\d+)/?', PeopleIdHandler),
	# 不指定对应参数，后面的问号可以在链接没有'/'的时候补全
	(r'/people/(\w+)/(\d+)/(\w+)/?', PeopleInfoHandler),
	# 直接通过 web 中的 URLSpec 实例化，好处是可以传入 name，在 redirect 的时候比较方便
	tornado.web.URLSpec(r'/people/(?P<name>\w+)/center/(?P<age>\d+)/?', PeopleUserCenter, people_db, name="usercenter"),
]

settings = {
	"template_path":"templates",
	"debug":True
}

if __name__ == "__main__":
	app = web.Application(urls,**settings)
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()
