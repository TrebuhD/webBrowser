# coding=utf-8
__author__ = 'hubert'

import gtk
import gtk.gdk
import webkit


def go(widget):
    add = addressbar.get_text()
    if not add.startswith("http://"):
        add = "http://" + add
    addressbar.set_text(add)
    web_view.open(add)

def on_key_press(widget, event):
    # If enter was pressed
    if event.keyval == 65293:
        print("enter key pressed")
        go(widget)

# The main program window:
win = gtk.Window()
win.connect('destroy', lambda w: gtk.main_quit())

# The big box to hold all them lil' boxes:
box = gtk.VBox()
win.add(box)

# A wee box for all the necessary controls:
top_bar_box = gtk.HBox()
box.pack_start(top_bar_box, False)

addressbar = gtk.Entry()
addressbar.connect('key_press_event', on_key_press)
top_bar_box.pack_start(addressbar)

gobutton = gtk.Button("GO")
top_bar_box.pack_end(gobutton, False)
gobutton.connect('clicked', go)

# The browser engine container:
web_view = webkit.WebView()

# Scrollable box for the WebView:
scroller = gtk.ScrolledWindow()
box.pack_start(scroller)
scroller.add(web_view)

# Make the window not tiny:
win.set_default_size(1024, 768)
win.show_all()
gtk.main()