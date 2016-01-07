# -*- coding: utf-8 -*-
from newspaper import Article as NewsPaperArticle

import html2text    # convert html to text
html2text.BODY_WIDTH = 0  # prevent random new lines all over the show: http://stackoverflow.com/questions/12839143/python-html2text-adds-random-n
# import markdown2    # convert text to html


class NewsArticleMixin(object):
    """
    Allow capability to extract article images
    """
    def html_to_markdown(self, content):
        """
        convert html text to markdown
        """
        return html2text.html2text(content, bodywidth=0)

#     def markdown_to_html(self, markdown):
#         """
#         convert markdown text to html
#         """
#         return markdown2.markdown(markdown)

#     def _clean_html(self, content):
#         """
#         strip ugly bad html to markdown
#         convert back form plain markdown to clean html
#         """
#         return self.markdown_to_html(self.html_to_markdown(content))

#     def article(self, content):
#         if content:
#             _article_store = Article(html=content)
#             _article_store.parse()

#             return _article_store
#         return None

#     def _extract_images(self, content):
#         # @TODO store this variable at the instance level
#         # so we can do other thing to the content
#         return self.article(content=content).images


#class Article(NewsArticleMixin, NewsPaperArticle):
class Article(NewsPaperArticle):
    """
    Override the newspaper article libraries Article class, which assumes
    we will always load from a url and enable provision of html directly
    This class provides image and other extractor services for content
    """
    def __init__(self, html, **kwargs):
        # Dummy this url as we already have the html
        # and we just want its parsing capabilities
        kwargs['url'] = 'http://example.com'
        super(Article, self).__init__(**kwargs)
        # now set the html with the data we ahve
        self.set_html(html)
        # set lookup props required to make it work
        self.is_downloaded = True
