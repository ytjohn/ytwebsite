Title: Back into programming, monitoring notes
Date: 2009-08-25
Author: John Hogenmiller 

I have been out of the programming circuit for a few years and have been
looking at getting back into it.  My traditional programming style is an
ssh window into my server and all my editing takes place on a
development server, in vi.  
  
Recently, I've been trying to decent work out a way to determine how the
world sees your connectivity from within your network.  Essentially, I
wanted to simulate accessing one of my locally connected machines from
the Internet.  Typically, you have to subscribe to a third party service
to perform this service for you.  Coincidentally, I have been reading up
on [Google App Engine][] and saw the potential in using GAE for my
purpose.  I could envision writing a monitoring system that runs
entirely on the GAE.  Unfortunately, I had no programming experience in
Python or Java.  I did see that [PHP has been ported to Java][] and
someone got [PHP running on GAE][].  The possibility of either creating
a new monitoring system in PHP (or modifying an existing PHP-based
monitoring system) entered my mind.  
  
I decided that rather than stay with PHP, I would use this project as a
method to learn Python.  I started digging into Python resources and
contemplating how I would want my monitoring system to work.  Ultimately
though, I decided I didn't want to create a brand-new monitoring system
(even a basic one) when existing ones such as Nagios and Zabbix do
perfectly well. In my research, I found a project called
[mirrorrr][]that used GAE as a web-proxy.    
  
This solution was immediately obvious.  My existing monitoring system
(Zabbix) has support for fetching web pages.  I could place a file with
the word "OK" on my local web server and then fetch it through GAE.   I
could even determine through the returned page whether my server was
down or if GAE was down.  
  
I set to work testing out the mirrorrr code under my own account.  The
major issue I observed is that mirrorrr is configured to cache pages,
meaning that when I changed my OK to FAIL, mirrorrr never updated the
page.  In the closed-source world, that is the end of the story. 
However, since this is an open-source project, this was an opportunity.  
  
I've been wanting to get back into programming, and I when I start back,
I want to be familiar with using an IDE (namely Eclipse).  In
preparation for creating a monitoring system, I had setup a development
station in (\*gasp\*) Windows Server 2003.  I connect to this via remote
desktop and generally leave Eclipse running 24x7. I had also gone
through the steps of installing the PyDev plugin, the GAE plugins, and
SVN plugins.  
  
**The Process**  
  
I downloaded a copy of the code using SVN checkout and set to work
editing the mirror.py file to disable CACHE.  I call this the "dive in
and learn to swim later" process.  Here, I could make changes to
existing code and test them out immediately.  In fact, the SDK for GAE
works as a sort of mini-server.  Once I run the code within the SDK, any
change I make to the source affects the running instance.    
  
I was able to read through and alter the code to allow me to switch
between caching and non-caching.  I ran into an issue with their "recent
urls" feature.  This shows the last 5 urls you have visited.  When you
are not caching your data, this never gets sets and starts throwing
errors.  I realized I would have to improve that section of the code
before I could truly implement a configurable "enable cache" option.  
  
At this point, I backed out of my file and considered my options.  I
wanted to make two distinct changes to the source, one of which requires
the other.  The author of the project hasn't maid a change to his(her?)
code since December of 2008.  However, I did see recent entries in the
Wiki, indicating this wasn't an abandoned project.  I realized that to
truly make my changes worthwhile, I should try and get them included
back in the upstream.  To do so, I should submit each change separately.
That required more tracking than I had been doing.  
  
So, I took care of another todo list item.  I went ahead and setup an
"official" repository server for YourTech, checked out a fresh copy of
mirrorrr, and then imported it into mine.  Now I could work.  I imported
the project from my repo server into Eclipse and started recreating my
work.  First I added added a feature to disable the recent urls.  At the
same time, I made an improvement by moving a chunk of code into a
self-contained method (which is apparently what python calls functions,
as near I can tell at this juncture).  Once this was committed, I went
ahead and proceeded with recreating my work on disabling the cache.   
  
Once I was done, you could enable or disable each feature separately. 
However, if you disabled the cache but left recent urls enabled, your
recent urls would never update.  On the flip side, if recent urls were
recorded before disabling the cache, then you could see the most recent
urls before caching was disabled.  Some person may want that feature --
they could start up the mirrorrr, visit several links, then disable the
cache, preserving those links on the main page forever.  
  
At this point, the only remaining task was to submit my changes to the
project maintainer.  I opened issues [6][] & [7][] and now I await
response.  
  
**Conclusion**  
  
The more I use Eclipse, the more I like it.  The ability to perform
every step of the process in one program is extremely useful.  Steps
like comparing history or checking out a specific version is much easier
to grasp than when you are tooling around the command line.  In the
shell, I would typically have most of my files open as a background
task.  Reverting a file from subversion required switching back to the
file, closing it, then reverting.  In Eclipse, it's a right-click
operation, regardless of whether the file is open or not.  
  
Python's syntax is a bit weird coming from a Perl and PHP background,
but it's learn-able.   As I plan to make several more improvements to
mirrorrr, I hope to become proficient in this language as well. 
However, I may be picking up a Perl project in the near future using the
[Mojo toolkit][], so everything is up in the air.

  [Google App Engine]: https://appengine.google.com/
  [PHP has been ported to Java]: http://www.caucho.com/resin-3.0/quercus/
  [PHP running on GAE]: http://www.webdigi.co.uk/blog/2009/run-php-on-the-google-app-engine/
  [mirrorrr]: http://code.google.com/p/mirrorrr/
  [6]: http://code.google.com/p/mirrorrr/issues/detail?id=6
  [7]: http://code.google.com/p/mirrorrr/issues/detail?id=7
  [Mojo toolkit]: http://mojolicious.org/
