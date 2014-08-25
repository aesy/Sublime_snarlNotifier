import sublime, sublime_plugin, socket
from os.path import basename

class SnarlNotifier(sublime_plugin.EventListener):

	def __init__(self):
		self.icon = '%s\\snarlNotifier\\sublime.png' % (sublime.packages_path())

	def _send(self, request):
		request = request.encode('utf-8')
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect(('127.0.0.1', 9887))
		self.sock.send(request)
		recv = self.sock.recv(1024)
		recv = recv.decode('utf-8').rstrip('\r\n')
		self.sock.close()

	def _process(self, data, args):
		param = ''
		for key in data:
			if key in args:
				data[key] = args[key]
		for key, val in data.items():
			if val:
				param += '&' + key + '=' + val
		request = 'snp://notify' + param.replace('&', '?', 1)
		self._send(request + '\r\n')

	def notify(self, **args):
		data = {'title': '',
				'text': '',
				'icon': '',
				'callback': '',
				'timeout': '',
				'priority': ''}
		self._process(data, args)

	def on_post_save(self, view):
		filename = basename(view.file_name())
		self.notify(title=filename, text='Changes have been saved.', icon=self.icon)
