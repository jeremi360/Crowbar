from extensions.extension import Extension
from gi.repository import Gtk
import pyfox

Name = "WikiWand"
shortDes = "Modern Wikipedia"
Descrption = "Redirect you from Wikipedia to WikiWand (unofficial)"
Author = "Jeremi 'jeremi360' Biernacki"
url_1 = "https://github.com/jeremi360/pyfox"
url_2 = "/blob/master/pyfox/extensions/wikiwand.py"
url = "".join((url_1, url_2))
Icon = "gtk-info"
wand = "http://www.wikiwand.com"

class ToTop(Extension):
    def __init__(self, UI):
        super(ToTop, self).__init__(
                                    UI, Name, shortDes,
                                    Descrption, Author,
                                    url
                                    )

        self.get_icon().set_from_icon_name(Icon, 4)


    def work(self):
        w = "wikipedia.org"
        u = pyfox.geturl()
        if w in u:
            if "?oldformat=true" in u:
                n = "?".split(u)[0]
            else:
                region = w.split(u)[0]
                article = "/".split(u)[-1]
                n = "/".join([wand, region, article])
            
            pyfox.loadUrl(n)
        else:
            pyfox.loadUrl(u)







