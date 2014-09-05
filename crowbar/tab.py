from gi.repository import Gtk, WebKit
import os


try:
	import grabbo
except:
	print("Please first install Grabbo in your python path or copy to crowbar dir")
	print("Grabbo can be download from https://github.com/jeremi360/Grabbo")
	exit()

class Hb_TabButton(grabbo.TabButton):
	def on_close(self, button):
		grabbo.TabButton.on_close(self, button)
		w = self.n.get_width() - 220
		self.n.set_width(w)

UI_Tab = os.path.join('..', 'ui', 'Tab.xml')

class Tab(grabbo.Builder):
	def __init__(self, notebook, url = None):
		super(Tab, self).__init__(UI_Tab)
		self.back_url = None
		self.next_url = None

		#get objects from UI_Tab
		#main tab toolbar
		self.back = self.ui.get_object("back")
		self.next = self.ui.get_object("next")
		self.urlen = self.ui.get_object("urlen")
		self.fresh = self.ui.get_object("fresh")
		self.zoomin = self.ui.get_object("zoomin")
		self.zoomres = self.ui.get_object("zoomres")
		self.zoomout = self.ui.get_object("zoomout")
		self.find = self.ui.get_object("find")
		self.book = self.ui.get_object("book")
		self.ExtBox = self.ui.get_object("ExtBox")

		#findbox
		self.findbox = self.ui.get_object("findbox")
		self.closefb = self.ui.get_object("closefb")
		self.findfb = self.ui.get_object("findfb")
		self.backfb = self.ui.get_object("backfb")
		self.nextfb = self.ui.get_object("nextfb")

		#this UI elements are hide until is not in use
		self.findbox.hide()

		#create WEBVIEW
		self.webview = WebKit.WebView()
		self.scroll = self.ui.get_object("scroll")
		self.scroll.add(self.webview)

		#connect WEBVIEW signals with methods
		self.webview.connect("title-changed", self.title_chang)
		self.webview.connect("icon-loaded", self.load_icon)
		self.webview.connect("load-finished", self.finish_load)
		self.webview.connect("load-progress-changed", self.progress_load)

		#connect UI elements with methods

		#main tab toolbar
		self.back.connect("clicked", self.go_back)
		self.next.connect("clicked", self.go_next)
		self.fresh.connect("clicked", self.on_fresh)
		self.find.connect("toggled", self.on_findbox)
		self.zoomin.connect("clicked", self.zoom_in)
		self.zoomout.connect("clicked", self.zoom_out)
		self.zoomres.connect("clicked",  self.reset_zoom)

		#findbox
		self.findfb.connect("activate", self.on_find)
		self.backfb.connect("clicked", self.find_back)
		self.nextfb.connect("clicked", self.find_next)

		#last settings
		self.webview.set_full_content_zoom(True)

		if url:
			self.urlen.set_text(url)
			self.webview.load_uri(url)

		#show
		self.webview.show()
		self.notebook = notebook
		self.tb = Hb_TabButton(self.notebook, self.get())


	def get(self):
		return self.ui.get_object("box")

	def reset_zoom(self, button):
		self.webview.set_zoom_level(1.0)

	def go_back(self, button):
		self.next_url = self.webview.get_uri()
		self.webview.go_back()
		b = self.webview.get_uri()
		self.urlen.set_text(b)

	def go_next(self, button):
		self.back_url = self.webview.get_uri()
		self.webview.load_uri(self.next_url)
		self.urlen.set_text(self.next_url)

	def on_fresh(self, button):
		self.webview.reload()

	def zoom_in(self, button):
		self.webview.zoom_in()

	def zoom_out(self, button):
		self.webview.zoom_out()


	def on_find(self, button):
		self.webview.search_text(
								self.findfb.get_text(),
								False, True, True
								)

	def find_back(self, button):
		self.webview.search_text(
								self.findfb.get_text(),
								False, False, True
								)

	def find_next(self, button):
		self.webview.search_text(
								self.findfb.get_text(),
								False, True, True
								)

	def on_book(self, button):
		pass

	def on_findbox(self, button):
		if self.find.get_active():
			self.findbox.show()
		else:
			self.findbox.hide()

	def url_active(self, widget):
		url = widget.get_text()
		if not "://" or  not "." in url:
			url = "http://www.google.pl/search?q=" + url
		elif not "://" in url:
			url = "http://" + url
		self.webview.load_uri(url)

	def title_chang(self, webview, frame, title):
		short = ""

		if len(title) > 26:
			for i in range(26):
				try:
					short += title[i]
				except:
					pass

			self.tb.button.set_label(short)
		else:
			self.tb.button.set_label(title)

		self.notebook.group.set_title(title)

	def load_icon(self, webview, url):
		try:
			pixbuf = webview.get_icon_pixbuf()
			self.urlen.set_icon_from_pixbuf(Gtk.EntryIconPosition.PRIMARY, pixbuf)
			self.tb.button.get_image().set_from_pixbuf(self.urlen.get_icon_pixbuf(Gtk.EntryIconPosition.PRIMARY))

		except:
			self.urlen.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "applications-internet")
			self.tb.button.get_image().set_from_name("applications-internet")

	def progress_load(self, webview, amount):
		self.urlen.set_progress_fraction(amount / 100.0)

	def finish_load(self, webview, frame):
		self.urlen.set_text(webview.get_uri())
		self.urlen.set_progress_fraction(0.0)

