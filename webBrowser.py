__author__ = 'hubert'

import gtk
import webkit


class WebBrowser(gtk.Window):
    def __init__(self):
        super(WebBrowser, self).__init__()

        self.set_title("Web Browser 9000")
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(16800, 16800, 16920))
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("destroy", gtk.main_quit)
        self.set_size_request(1024, 768)

        self.initialize_components()
        self.show_all()

    def initialize_components(self):
        # The big box to hold them all:
        box = gtk.VBox(False, 2)
        self.add(box)

        # The browser engine container:
        webview = webkit.WebView()

        # Scrollable box for the WebView:
        scroller = gtk.ScrolledWindow()
        scroller.add(webview)

        # A toolbar with all the necessary controls:
        toolbar = gtk.Toolbar()
        toolbar.set_style(gtk.TOOLBAR_ICONS)

        # Buttons and stuff:
        # newTb = gtk.ToolButton(gtk.STOCK_NEW)
        clearTb = gtk.ToolButton(gtk.STOCK_CLEAR)
        refreshTb = gtk.ToolButton(gtk.STOCK_REFRESH)
        goTb = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        goBackTb = gtk.ToolButton(gtk.STOCK_GO_BACK)

        # The address bar needs to be split because Toolbar only accepts ToolItems.
        addressItem = gtk.ToolItem()
        addressbar = gtk.Entry()
        addressbar.connect('key_press_event', self.on_key_press, webview)
        addressbar.set_width_chars(100)
        addressItem.add(addressbar)

        # Let's give the buttons a purpose:
        goTb.connect('clicked', self.go, webview, addressbar)
        clearTb.connect('clicked', self.clear_text, addressbar)
        goBackTb.connect('clicked', self.go_back, webview)
        refreshTb.connect('clicked', self.refresh, webview)

        # Assemble the toolbar:
        # toolbar.insert(newTb, 0)
        toolbar.insert(goBackTb, 0)
        toolbar.insert(refreshTb, 1)
        toolbar.insert(addressItem, 2)
        toolbar.insert(clearTb, 3)
        toolbar.insert(goTb, 4)

        # Put it all in a box:
        box.pack_start(toolbar, False, False, 0)
        box.pack_start(scroller)

    def on_key_press(self, widget, event, webview):
        # If enter was pressed:
        if event.keyval == 65293:
            self.go(widget, webview)

    def go(self, widget, web_view, addressbar=None):
        # If called from address bar by pressing enter:
        if hasattr(widget, 'get_text'):
            address = widget.get_text()
            address = self.add_http_prefix(address)
            widget.set_text(address)
            print("Opening: " + address)
        # If the user clicked a button:
        else:
            address = addressbar.get_text()
            address = self.add_http_prefix(address)
            addressbar.set_text(address)
            print("Opening: " + address)
        web_view.open(address)

    @staticmethod
    def add_http_prefix(addr):
        if not addr.startswith("http://"):
            return "http://" + addr
        else:
            return addr

    @staticmethod
    def go_back(widget, web_view):
        web_view.go_back()

    @staticmethod
    def refresh(widget, web_view):
        web_view.reload()

    @staticmethod
    def clear_text(widget, addressbar):
        addressbar.set_text("")

if __name__ == "__main__":
    WebBrowser()
    gtk.main()