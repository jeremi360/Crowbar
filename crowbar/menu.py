from gi.repository import Gtk
import os

r = os.path.realpath(__file__)
r = os.path.dirname(r)
r = os.path.dirname(r)

try:
    from crowbar.tab import Tab
    from crowbar import variable
    print("Eclipse way")
except:
    from tab import Tab
    import variable
    print("Normal way")

try:
    import grabbo
    from grabbo import granite
except:
    print("Please first install Grabbo in your python path or copy to crowbar dir")
    print("Grabbo can be download from https://github.com/jeremi360/Grabbo")
    exit()

Menu_UI = os.path.join(r, 'ui', 'Menu.xml')
class Menu(grabbo.Builder):
    def __init__(self, current_tab):
        grabbo.Builder.__init__(self, Menu_UI)
        self.ctab = current_tab
        self.Home = self.ui.get_object("Home")
        self.NewWin =  self.ui.get_object("NewWin")
        self.NewPriv = self.ui.get_object("NewPriv")
        self.Open = self.ui.get_object("Open")
        self.Save = self.ui.get_object("Save")
        self.Print = self.ui.get_object("Print")
        self.Settings = self.ui.get_object("Settings")
        self.Addons = self.ui.get_object("Addons")
        self.Tools = self.ui.get_object("Tools")

    def on_home(self, button):
        self.ctab.load_url(variable.home)

    def get(self):
        return self.ui.get_object("grid")

