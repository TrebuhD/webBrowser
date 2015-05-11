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

        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_TOP)

        self.initialize_components()
        self.show_all()

    def initialize_components(self):
        # The big box to hold them all:
        box = gtk.VBox(False, 2)
        self.add(box)

        # The browser engine container:
        webview = webkit.WebView()

        # A toolbar with all the necessary controls:
        toolbar = gtk.Toolbar()
        toolbar.set_style(gtk.TOOLBAR_ICONS)

        # Buttons and stuff:
        # newtab_button = gtk.ToolButton(gtk.STOCK_NEW)
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
        # newtab_button.connect('clicked', )

        # Assemble the toolbar:
        toolbar.insert(back_button, 0)
        toolbar.insert(refresh_button, 1)
        toolbar.insert(addressbar_item, 2)
        toolbar.insert(clear_button, 3)
        toolbar.insert(go_button, 4)
        # toolbar.insert(newtab_button, 5)

        # Put it all in a box:
        box.pack_start(toolbar, False, False, 0)
        box.pack_start(self.notebook)
        self.notebook.show()

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
        # if self.notebook.get_n_pages() == 0:
        self.append_page(web_view)
        web_view.open(address)

    def append_page(self, web_view):
        # Scrollable window acting as a container for WebView:
        scroller = gtk.ScrolledWindow()
        scroller.add(web_view)
        scroller.show_all()

        # Create the components for a tab header:
        header = gtk.HBox()
        title_label = gtk.Label()
        web_view.connect("title-changed", Toolbox.changetitle, title_label)
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        close_button = gtk.Button()
        close_button.set_image(image)
        close_button.set_relief(gtk.RELIEF_NONE)

        close_button.connect("clicked", self.remove_page, scroller)

        header.pack_start(title_label,
                          expand=True, fill=True, padding=0)
        header.pack_end(close_button,
                        expand=False, fill=False, padding=0)
        header.show_all()

        self.notebook.append_page(scroller, header)

    def remove_page(self, widget, child):
        pagenum = self.notebook.page_num(child)
        if pagenum != -1:
            self.notebook.remove_page(pagenum)
            child.destroy()
            if self.notebook.get_n_pages() == 1:
                self.set_property('show-tabs', False)
        # Refresh the widget
        # self.notebook.queue_draw_area(0, 0, -1, -1)

if __name__ == "__main__":
    WebBrowser()
    gtk.main()