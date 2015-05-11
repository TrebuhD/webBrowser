from Toolbox import Toolbox

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
        clear_button = gtk.ToolButton(gtk.STOCK_CLEAR)
        refresh_button = gtk.ToolButton(gtk.STOCK_REFRESH)
        go_button = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        back_button = gtk.ToolButton(gtk.STOCK_GO_BACK)

        # The address bar needs to be split because Toolbar only accepts ToolItems.
        addressbar_item = gtk.ToolItem()
        addressbar = gtk.Entry()
        addressbar.connect('key_press_event', self.on_key_press, webview)
        addressbar.set_width_chars(100)
        addressbar_item.add(addressbar)

        # Let's give the buttons a purpose:
        go_button.connect('clicked', self.go, webview, addressbar)
        clear_button.connect('clicked', Toolbox.clear_text, addressbar)
        back_button.connect('clicked', Toolbox.go_back, webview)
        refresh_button.connect('clicked', Toolbox.refresh, webview)

        # Assemble the toolbar:
        # toolbar.insert(newTb, 0)
        toolbar.insert(back_button, 0)
        toolbar.insert(refresh_button, 1)
        toolbar.insert(addressbar_item, 2)
        toolbar.insert(clear_button, 3)
        toolbar.insert(go_button, 4)

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
            address = Toolbox.add_http_prefix(address)
            widget.set_text(address)
            print("Opening: " + address)
        # If the user clicked a button:
        else:
            address = addressbar.get_text()
            address = Toolbox.add_http_prefix(address)
            addressbar.set_text(address)
            print("Opening: " + address)
        web_view.open(address)

if __name__ == "__main__":
    WebBrowser()
    gtk.main()