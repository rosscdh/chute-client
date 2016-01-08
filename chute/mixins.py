# -*- coding: utf-8 -*-
import config as settings

from .article import Article, NewsArticleMixin

import HTMLParser
import feedparser
import slugify
import json

htmlParser = HTMLParser.HTMLParser()

# {
#   "pk": 3,
#   "project": {
#     "is_facebook_feed": true,
#     "detail_url": "/project/bienertit-0ced/",
#     "slug": "bienertit-0ced",
#     "name": "bienert.it",
#     "url": "https://www.facebook.com/bienert.it",
#     "date_created": "2015-12-07T13:35:15.224Z"
#   },
#   "feed": [
#     {
#       "pk": 1,
#       "name": "sonoGDT Partner",
#       "message": "Wir sind ab sofort sonoGDT Partner. Was bedeutet das im Einzelnen für Sie als Kunden? Sie möchten gerne Ihr Ultraschallgerät mit Ihrer vorhandenen Praxissoftware benutzen, so dass die Ultraschallbilder automatisch unter der Patientenkarteikarte gespeichert werden? Auch ist es möglich dem Ultraschallgerät die Patientendaten zu übergeben, wie zum Beispiel Name des…",
#       "description": "Wir sind ab sofort sonoGDT Partner. Was bedeutet das im Einzelnen für Sie als Kunden? Sie möchten gerne Ihr Ultraschallgerät mit Ihrer vorhandenen Praxissoftware benutzen, so dass die Ultraschallbilder automatisch unter der Patientenkarteikarte gespeichert werden? Auch ist es möglich dem…",
#       "picture": "http://bienert.it/wp-content/uploads/2015/11/bit-foto-sonogdt.jpg",
#       "video": null,
#       "video_transcode_status": null,
#       "updated_at": "2015-11-23T20:27:17Z",
#       "absolute_url": "/project/bienertit-0ced/feed/1/",
#       "template_name": "basic",
#       "post_type": "link",
#       "url": "http://magnificent.de/api/v1/feed/1/",
#       "slug": "53719e19a7944716b6efaa01d8972bfe",
#       "provider_crc": "742d37c15ff2d8021ff90f5290d737c4",
#       "wait_for": 3,
#       "template": 1,
#       "updated_time": "2015-12-07T14:29:14.353Z"
#     }
#   ]
# }


class RssReaderMixin(NewsArticleMixin, object):
    """
    Mixin to talk with rss feeds
    """
    _article_store = None

    def article(self, content):
        if content:
            _article_store = Article(html=content)
            _article_store.parse()

            return _article_store
        return None

    def extract_images_from_content(self, content):
        # @TODO store this variable at the instance level
        # so we can do other thing to the content
        return self.article(content=content).images

    def get_template_from_tags(self, tags):
        template = None
        for tag in tags:
            if 'template-' in tag:
                template = tag.split('template-')[1]
                break
        return template if template else 'basic'

    def get_rss_from_wordpress(self, **kwargs):
        category = kwargs.get('category', getattr(settings, 'WORDPRESS_RSS_CATEGORY', None))
        number_of_items = kwargs.get('number_of_items', getattr(settings, 'WORDPRESS_RSS_NUM_ITEMS', 100))

        feed_url = getattr(
            settings,
            'WORDPRESS_RSS_BASE_URL',
            'http://sektor-m.com'
        )
        if category:
            feed_url += '/category/'
            feed_url += str(category)

        feed_url += '/feed/'
        wordpress_feed = feedparser.parse(feed_url)

        title = unicode(wordpress_feed.feed.title)
        slug = slugify.slugify(title.lower())

        project = {
            "slug": slug,
            "name": title,
            "url": wordpress_feed.feed.title_detail.base,
            "is_facebook_feed": False,
            "detail_url": wordpress_feed.feed.link,
            "date_created": wordpress_feed.feed.updated
        }
        feed = []
        for item in wordpress_feed.entries[:number_of_items]:
            #print item

            tags = [t.get('term') for t in item.get('tags')]
            summary_detail = self.html_to_markdown(content=unicode(item.get('summary_detail').get('value')))
            title = htmlParser.unescape(unicode(item.get('title')))

            try:
                images = self.extract_images_from_content(content=unicode(item.content[0].value))
                image = images[0]
            except:
                images = []
                image = None

            try:
                rss_item = {
                    "pk": item.id,
                    "name": title,
                    "message": summary_detail,
                    "description": summary_detail,
                    "picture": image,
                    "video": None,
                    "video_transcode_status": None,
                    "updated_at": "2015-11-23T20:27:17Z",
                    "absolute_url": item.link,
                    "template_name": self.get_template_from_tags(tags=tags),
                    "post_type": "link",
                    "url": item.link,
                    "slug": slugify.slugify(title.lower()),
                    "provider_crc": None,
                    "wait_for": self.calculate_wait_for(corpus='%s %s' % (item.title, summary_detail)),
                    "template": None,
                    "updated_time": item.published
                }

                feed.append(rss_item)
            except AttributeError:
                pass
        return json.dumps({
            "pk": None,
            "project": project,
            "feed": feed
        })

