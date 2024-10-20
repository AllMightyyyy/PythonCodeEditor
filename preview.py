from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

class LivePreview(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setHtml("<html><body><h1>Live Preview</h1></body></html>")

    def update_preview(self, html_content):
        self.setHtml(html_content, QUrl("file:///"))
