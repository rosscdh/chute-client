# -*- coding: utf-8 -*-
from newspaper import Article as NewsPaperArticle


class Article(NewsPaperArticle):
    """
    Override the newspaper article libraries Article class, which assumes
    we will always load from a url and enable provision of html directly
    This class provides image and other extractor services for content
    """
    def __init__(self, html, **kwargs):
        # Dummy this url as we already have the html
        # and we just want its parsing capabilities
        kwargs['url'] = 'http://staging.manualone.com'
        super(Article, self).__init__(**kwargs)
        # now set the html with the data we ahve
        self.set_html(html)
        # set lookup props required to make it work
        self.is_downloaded = True
