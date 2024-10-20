from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import Qt
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.token import Token

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent, language='html', theme='dark'):
        super().__init__(parent)
        self.lexer = get_lexer_by_name(language)
        self.theme = theme
        self.formatters = self.get_formatters()

    def get_formatters(self):
        if self.theme == 'dark':
            return {
                Token.Keyword: self._format(QColor("#569CD6"), QFont.Bold),          # Blueish
                Token.Name.Tag: self._format(QColor("#4EC9B0")),                    # Teal
                Token.Name.Attribute: self._format(QColor("#9CDCFE")),              # Light Blue
                Token.String: self._format(QColor("#CE9178")),                      # Peach
                Token.Comment: self._format(QColor("#6A9955"), italic=True),         # Green
                Token.Operator: self._format(QColor("#D4D4D4")),                    # Light Gray
                Token.Punctuation: self._format(QColor("#D4D4D4")),                # Light Gray
                Token.Text: self._format(QColor("#D4D4D4")),                        # Light Gray
            }
        elif self.theme == 'light':
            return {
                Token.Keyword: self._format(QColor("#0000FF"), QFont.Bold),          # Blue
                Token.Name.Tag: self._format(QColor("#800000")),                    # Maroon
                Token.Name.Attribute: self._format(QColor("#FF00FF")),              # Magenta
                Token.String: self._format(QColor("#008000")),                      # Green
                Token.Comment: self._format(QColor("#808080"), italic=True),         # Gray
                Token.Operator: self._format(QColor("#000000")),                    # Black
                Token.Punctuation: self._format(QColor("#000000")),                # Black
                Token.Text: self._format(QColor("#000000")),                        # Black
            }
        else:
            # Default to dark theme if unknown
            return {
                Token.Keyword: self._format(QColor("#569CD6"), QFont.Bold),
                Token.Name.Tag: self._format(QColor("#4EC9B0")),
                Token.Name.Attribute: self._format(QColor("#9CDCFE")),
                Token.String: self._format(QColor("#CE9178")),
                Token.Comment: self._format(QColor("#6A9955"), italic=True),
                Token.Operator: self._format(QColor("#D4D4D4")),
                Token.Punctuation: self._format(QColor("#D4D4D4")),
                Token.Text: self._format(QColor("#D4D4D4")),
            }

    def _format(self, color, font_weight=QFont.Normal, italic=False):
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        fmt.setFontWeight(font_weight)
        fmt.setFontItalic(italic)
        return fmt

    def set_theme(self, theme):
        self.theme = theme
        self.formatters = self.get_formatters()
        self.rehighlight()

    def highlightBlock(self, text):
        for token, content in lex(text, self.lexer):
            fmt = self.formatters.get(token, self.formatters.get(Token.Text, QTextCharFormat()))
            start = text.find(content)
            while start != -1:
                self.setFormat(start, len(content), fmt)
                start = text.find(content, start + len(content))
