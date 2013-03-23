#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'John Hogenmiller'
AUTHOR_EMAIL = u'john@hogenmiller.net'
SITENAME = u'ytjohn'
# SITEURL = 'http://pelican.ytnoc.net'
SITEURL = 'http://www.yourtech.us'

# SITEABOUT = "Welcome to the website. This currently is a placeholder, but it will describe me, link to a contact page, my story, and various other assorted sundries."
SITEABOUT = "soawesomejohn :: yourtechjohn :: ytjohn :: johnh :: squegie"
TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

DEFAULT_CATEGORY = ('posts')

# Go to google.com/cse to build a custom search

# blog.yourtech.us:  008176316909509740226:lgxj0_nm9mu
# pelican.ytnoc.net: 008176316909509740226:yycjdi2wzp0
# www.yourtech.us:   008176316909509740226:1osf0ptylds

GOOGLE_CX = '008176316909509740226:1osf0ptylds'

from pelican.plugins import gravatar
PLUGINS = [gravatar,]

# Theme it
THEME = "theme/ytjohn-bootstrap2"
# THEME = "notmyidea"

ARTICLE_URL = '/{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}.html'
PAGE_URL = '/pages/{slug}.html'
PAGE_SAVE_AS = 'pages/{slug}.html'

# add any extra files (robots.txt, favicon.ico)
FILES_TO_COPY = (
                 ('extra/favicon.ico', 'favicon.ico'),
                )

# Blogroll
LINKS =  (
          ('id Graphics', 'http://www.idgraphics.net'),
          ('Bedford County Amateur Radio Society', 'http://bcars.org'),
	  ('Everett, PA', 'http://www.everettpa.net'),
 	  ('Raystown Wireless', 'http://www.raystownwireless.net'),
         )
# Social widget
SOCIAL = (('GitHub/ytjohn', '//github.com/ytjohn'),
          ('My Google+', '//plus.google.com/107348408305555858514'),
         )

DEFAULT_PAGINATION = 10

PLUGINS=['pelican.plugins.sitemap',]

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

