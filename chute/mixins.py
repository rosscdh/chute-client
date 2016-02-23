# -*- coding: utf-8 -*-
import config as settings

from .article import Article, NewsArticleMixin

import HTMLParser
import feedparser
import slugify
import json
import re

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
        _article_store = Article(html=content)
        _article_store.parse()

        return _article_store

    def get_template_from_tags(self, tags):
        template = None
        for tag in tags:
            if 'template-' in tag:
                template = tag.split('template-')[1]
                break
        return template if template else 'basic'

    def extract_timing(self, text):
        # Extract Seconds
        res = re.search("\#(?P<time_length>\d+)(?P<time_type>(?:s|m|h))", text)
        seconds = None
        if res:
            time_length = res.group('time_length')
            time_type = res.group('time_type')
            seconds = 30
            if time_type == 's':
                seconds = time_length
            elif time_type == 'm':
                seconds = time_length/60
            elif time_type == 'h':
                seconds = time_length/3600
            else:
                raise Exception('Not a valid Time type must be #{time_length}s or #{time_length}m or #{time_length}h'.format(time_length=time_length))
            # remove from title
            return text.replace('#{seconds}{time_type}'.format(seconds=seconds, time_type=time_type), '')
        return text, seconds

    def get_title(self, text):
        text, seconds = self.extract_timing(text=text)
        return text, seconds

    def get_video(self, article, item):
        try:
            video = article.movies[0]
        except:
            videos = [video for video in re.findall("https?://(?:[a-z0-9\-]+\.)+[a-z0-9]{2,6}(?:/[^/#?]+)+\.(?:m4v|mp4|mov|avi)", item.content[0].value)]
            try:
                video = videos[0]
            except:
                video = None
        return video

    def get_rss_from_wordpress(self, **kwargs):
        category = kwargs.get('category', getattr(settings, 'WORDPRESS_RSS_CATEGORY', None))
        number_of_items = kwargs.get('number_of_items', getattr(settings, 'WORDPRESS_RSS_NUM_ITEMS', 100))

        feed_url = getattr(
            settings,
            'WORDPRESS_RSS_BASE_URL',
            'http://sektor-m.com'
        )

        wordpress_feed = feedparser.parse(feed_url)

        if wordpress_feed.get('bozo', None) in [1]:
            raise Exception('No Url Could be decoded: {url}, check internet connection?'.format(url=feed_url))

        feed_title = htmlParser.unescape(unicode(wordpress_feed.feed.title))
        slug = slugify.slugify(feed_title.lower())

        project = {
            "slug": slug,
            "name": feed_title,
            "url": wordpress_feed.feed.title_detail.base,
            "is_facebook_feed": False,
            "detail_url": wordpress_feed.feed.link,
            "date_created": wordpress_feed.feed.updated,
            "location": {
                "location": settings.CONFIG_JSON.get('location', "-31.9546516,115.8351524"),
                "woeid": "",
                "unit": settings.CONFIG_JSON.get('unit', "c"),
            }
        }
        feed = []

        short_codes = '(\!)?\[(.*?)\]\((.*?)\)'

        for item in wordpress_feed.entries[:number_of_items]:
            article = self.article(content=unicode(item.content[0].value))

            tags = [t.get('term') for t in item.tags]

            summary = self.html_to_markdown(content=unicode(item.summary))
            summary = re.sub(short_codes, '', summary).strip()

            summary_detail = self.html_to_markdown(content=unicode(item.summary_detail.value))
            summary_detail = re.sub(short_codes, '', summary_detail).strip()

            title, seconds = self.get_title(text=htmlParser.unescape(unicode(wordpress_feed.feed.title)))

            try:
                image = article.images[0]
            except:
                image = None

            video = self.get_video(article=article,
                                   item=item)
            if video:
                # If we have a video then its going to be fullscreen no matter what
                title = None
                summary = None

            try:
                rss_item = {
                    "pk": item.id,
                    "name": title,
                    "message": summary_detail,
                    "description": summary if summary != summary_detail else None,
                    "picture": image,
                    "video": video,
                    "video_transcode_status": None,
                    "updated_at": item.published,
                    "absolute_url": item.link,
                    "template_name": self.get_template_from_tags(tags=tags),
                    "post_type": "link",
                    "url": item.link,
                    "slug": slugify.slugify(title.lower()),
                    "provider_crc": None,
                    "wait_for": seconds if seconds else self.calculate_wait_for(corpus='%s %s' % (item.title, summary_detail)),
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

