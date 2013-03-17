#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'John Hogenmiller'
AUTHOR_EMAIL = u'john@hogenmiller.net'
SITENAME = u'Pelican Test Site'
SITEURL = 'http://pelican.yourtech.us'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

PLUGINS = ['pelican.plugins.gravatar',]

# Theme it
THEME = "themes/pelican-bootstrap-responsive-theme"
# THEME = "notmyidea"

# Blogroll
LINKS =  (
          ('id Graphics', 'http://www.idgraphics.net'),
          ('Bedford County Amateur Radio Society', 'http://bcars.org'),
	  ('Everett, PA', 'http://www.everettpa.net'),
 	  ('Raystown Wireless', 'http://www.raystownwireless.net'),
         )
# Social widget
SOCIAL = (('Myself', 'http://www.facebook.com/johnhogenmiller/'),
          ('Robin', 'http://www.facebook.com/robin.hogenmiller/'),
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

