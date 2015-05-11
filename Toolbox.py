__author__ = 'hubert'


class Toolbox(object):
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


