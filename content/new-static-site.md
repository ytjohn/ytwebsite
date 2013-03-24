Title: New Static Site
Date: 2013-03-24

I had mentioned previously that I had taken up [markdown blogging](|filename|markdown-blogging.md). At that time, I was writing my post in markdown, converting it to HTML, and then injecting it into [blogger](http://www.blogger.com). This last week, I have done a good bit of work to convert my site to a "static site" using [Pelican](http://www.getpelican.com/). A static site is made up entirely of static files - no database, no php includes, just your basic collection of html, javascript, css, and images. I write content in Markdown on my laptop. I develop my theme locally as well. Then I run "make html" and pelican will process my configuration file, my content, and my theme to generate all of the pages, posts, archive pages, and various rss feeds. The end result is a directory full of files that can be dropped onto pretty much any webserver.

There were a few hic-cups. Many of my older pages were not originally written in markdown, but rather using whatever CMS editor I had at the time. Pelican has an import feature, but some things got lost in translation. Any preformated code blocks had to be re-created manually (amusingly enough, copying and pasting from the old web page into vim, then indenting them properly).

The biggest loss is a search engine. A CMS like Wordpress or a hosted solution like Blogger stores your content in a database and provides a search interface to that content. With static pages, not so much. Most of the web gets around this using Google's [CSE](http://www.google.com/cse), which I am trying as well. As of yet, almost nothing appears to be indexing on this page. If this continues, I will setup a stanadlone search engine that simply indexes the pages on this site. I'm still researching possibilities on that. Ten years ago, [ht://dig](http://www.htdig.org/) was the premier application to use, but development on that seems to have stopped in 2004. [Sphider](http://www.sphider.eu/) looks like a good product, but again, development stopped in 2007. Small search engine development seems to have dropped off significantly with the rise of Google's popularity. 

A copy of the website content and theme can be tracked on [github](http://www.github.com/ytjohn/ytwebsite). 


