#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'John Hogenmiller'
AUTHOR_EMAIL = u'john@hogenmiller.net'
SITENAME = u'Pelican Test Site'
SITEURL = 'http://pelican.yourtech.us'

SITEABOUT = "Welcome to the website. This currently is a placeholder, but it will describe me, link to a contact page, my sotrey, and various other assorted sundries."

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
SOCIAL = (('My Facebook', '//www.facebook.com/johnhogenmiller/'),
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

