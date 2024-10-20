from PySide6.QtWidgets import QPlainTextEdit, QTextEdit, QCompleter, QMenu
from PySide6.QtCore import Qt, QRect, QSize, QStringListModel, QTimer, Signal
from PySide6.QtGui import QColor, QTextFormat, QPainter, QTextCursor, QAction
from highlighter import Highlighter
from line_number_area import LineNumberArea

class CodeEditor(QPlainTextEdit):
    # Define a custom signal to emit when text changes for preview
    text_changed_for_preview = Signal()

    def __init__(self, parent=None):  
        super().__init__(parent) 
        self.line_number_area = LineNumberArea(self)

        # Connect signals
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.textChanged.connect(self.handle_text_changed)

        # Initialize line number area
        self.update_line_number_area_width(0)
        self.highlight_current_line()

        # Initialize Syntax Highlighter with default theme
        self.current_theme = 'dark'
        self.highlighter = Highlighter(self.document(), 'html', theme=self.current_theme)

        # Initialize Auto-Completion
        self.completer = QCompleter(self)
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)

        # List of HTML tags and attributes
        html_keywords = [
            'html', 'head', 'title', 'base', 'link', 'meta', 'style', 'script', 'noscript',
            'body', 'section', 'nav', 'article', 'aside', 'h1', 'h2', 'h3', 'h4', 'h5',
            'h6', 'header', 'footer', 'address', 'main', 'p', 'hr', 'pre', 'blockquote',
            'ol', 'ul', 'li', 'dl', 'dt', 'dd', 'figure', 'figcaption', 'div', 'a', 'em',
            'strong', 'small', 's', 'cite', 'q', 'dfn', 'abbr', 'data', 'time', 'code',
            'var', 'samp', 'kbd', 'sub', 'sup', 'i', 'b', 'u', 'mark', 'ruby', 'rt', 'rp',
            'bdi', 'bdo', 'span', 'br', 'wbr', 'ins', 'del', 'picture', 'source', 'img',
            'iframe', 'embed', 'object', 'param', 'video', 'audio', 'track', 'map', 'area',
            'table', 'caption', 'colgroup', 'col', 'tbody', 'thead', 'tfoot', 'tr', 'td',
            'th', 'form', 'fieldset', 'legend', 'label', 'input', 'button', 'select',
            'datalist', 'optgroup', 'option', 'textarea', 'keygen', 'output', 'progress',
            'meter', 'details', 'summary', 'menuitem', 'menu'
        ]
        self.model = QStringListModel()
        self.model.setStringList(html_keywords)
        self.completer.setModel(self.model)

        # Define Snippets
        self.snippets = {
            'html': "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>Document</title>\n</head>\n<body>\n    \n</body>\n</html>",
            'table': "<table>\n    <tr>\n        <th>Header 1</th>\n        <th>Header 2</th>\n    </tr>\n    <tr>\n        <td>Data 1</td>\n        <td>Data 2</td>\n    </tr>\n</table>",
            'div': "<div>\n    \n</div>",
            # Add more snippets as needed
        }

        # Initialize Timer for Debouncing Preview Updates
        self.preview_timer = QTimer()
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self.emit_preview)

    def handle_text_changed(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor) 
        current_word = cursor.selectedText()
        if current_word:
            self.completer.complete()

        # Start/restart the timer for preview update
        self.preview_timer.start(300)  # 300 ms delay

    def emit_preview(self):
        # Emit the custom signal
        self.text_changed_for_preview.emit()

    def keyPressEvent(self, event):
        if self.completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape,
                               Qt.Key_Tab, Qt.Key_Backtab):
                event.ignore()
                return

        # Handle completion
        is_shortcut = (event.modifiers() & Qt.ControlModifier) and event.key() == Qt.Key_Space
        if is_shortcut:
            self.completer.complete()
            return

        # Check for snippet trigger (e.g., typing "html" and pressing Tab)
        if event.key() == Qt.Key_Tab:
            cursor = self.textCursor()
            cursor.select(QTextCursor.WordUnderCursor)
            word = cursor.selectedText()
            if word in self.snippets:
                cursor.insertText(self.snippets[word])
                return

        super().keyPressEvent(event)

    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        menu.addSeparator()
        snippet_menu = menu.addMenu("Snippets")
        for key in self.snippets:
            action = QAction(key, self)
            action.triggered.connect(lambda checked, k=key: self.insert_snippet(k))
            snippet_menu.addAction(action)
        menu.exec(event.globalPos())

    def insert_snippet(self, key):
        if key in self.snippets:
            cursor = self.textCursor()
            cursor.insertText(self.snippets[key])

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.line_number_area.width()-5, self.fontMetrics().height(),
                                 Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()  
            line_color = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def set_theme(self, theme):
        self.current_theme = theme
        self.highlighter.set_theme(theme)
