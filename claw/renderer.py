"""MD rendering helper"""
# pylint: disable=invalid-name,W0702,W0622
import mistune

renderer = None
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import html

    class HighlightRenderer(mistune.Renderer):
        """pygments wrapper for mistune"""
        def block_code(self, code, lang):
            if not lang:
                return '\n<pre><code>%s</code></pre>\n' % \
                    mistune.escape(code)
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = html.HtmlFormatter(linenos="table")
            return highlight(code, lexer, formatter)
    renderer = HighlightRenderer()
except:
    pass

markdown=mistune.Markdown(renderer=renderer)

def render(markdown_data):
    """Render MD"""
    return markdown.render(markdown_data)
