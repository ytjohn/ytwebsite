Title: Markdown Blogging
Date: 2012-08-06
Author: John Hogenmiller 

I recently have started a process of migrating my website over to
[blogger.com][]. One of the main reasons for this was because in my last
server move, I had broken my Movable Type installation, and found myself
too busy to fix it. I found I didn't want to spend my time fixing and
updating blogging software. I wanted to work on my projects, write them
up, and post them. It was time to move my content to an existing
platform that handled the back end. I looked at a few, and decided
blogger.com would be as good as any other service.  
It only took a short time to setup a blog, point a CNAME at it, and then
to import my existing posts. When I started creating some new posts, I
immediately ran into some limitations.  

1.  You used to be able to edit permalinks on blogger. Now, you can only
    do that before you publish. The only way to change a permalink after
    publishing is to create a new post with the desired permalink and
    delete the old one.
2.  Blogger has no built in formatting for code blocks. So if I want to
    show a config file, source code, or terminal session log, I have to
    fiddle with changing fonts, size, and "blockquote" to get it
    presentable. Even then, you run the risk of strange formatting of
    your raw text.

  
  
  
I found a solution that other bloggers use called [SyntaxHighlighter][].
This is a combination of javascript and css code that takes text within
your   

    ; tags and gives you nice looking blocks of code, highlighted and (optionally) with line numbers. The catch is that your pre tags need to have a class name, along with the language (perl/c/bash/text) "brush" to use. If you go with pre tags, you have to change any angle bracks to their HTML escaped equivalents of < and >. They have a work-around using SCRIPT/CDATA, but it takes some getting used to. Adding this to your blog only requires a few steps.

  
I rather liked syntaxhighlighter, but it still seemed like I had to do a
lot of manual work with the code. Also, I had to select the brush each
time. Couldn't it guess? Notepad++ and some others will guess at what
language you're using and highlight accordingly. I found something
called [prettify][] that does just that. You only need to load one js
file and one css file. Prettify works off of either   

     or  tags and has similar limitations to SyntaxHighlighter regarding html tags. However, it has the advantage of being able to guess the language automatically.

  
Being able to use this code made my posts look much nicer, but the
entire process got me thinking. The way I "document" most of projects
typically invole using a notepad editor like [Geany][prettify] or
[Notepad++][]. As I work, I add notes, copy in source code or shell
comands, and do everything in a plain text editor. Later, I add
commentary and clean up the document. I take this and paste it into the
WYSIWYG editor on blogger. Finally, I have to keep switching between
compose and html mode to get my text looking suitable. There are too
many steps for me to want to do this consistently. All I really want to
do is take my text file, add a little formatting in a few spots, a few
hyperlinks in others, and post it.  
Enter [markdown][]. *Markdown is a text-to-HTML conversion tool for web
writers. Markdown allows you to write using an easy-to-read,
easy-to-write plain text format, then convert it to structurally valid
XHTML (or HTML)*. I have used this before, but didn't pay it close
enough attention. It's used on github and reddit, there are plugins for
it in dokuwiki and redmine. The idea is you write in text, adding
formatting using the markdown syntax. This format is both human readable
and machine readable. When read by the appropriate library, clean html
is generated. It also has a feature for wrapping blocks of code inside
of   

    &;lt;code> tags and html-escaping html inside of those tags.

  
Within the MarkDown project is a paged called "[dingus][]" which means
"placeholder". You can paste your markdown text into one textarea and
get the generated html plus a preview back. I tested pasting that
generated html into Blogger's HTML box and it seems to work perfectly
fine. What this means is that I can type up my documentation completely
within my text editor of choice, save it locally, and then generate my
html code to paste into blogger.  
Some of you may have realized that my   

     tags are missing that class name (. Well, I copy the generated html, do a search and replace of  with  and then paste it, but that's adding more steps. Instead, I sought to make my own dingus that does this automatically. I found that there is an extension of markdown called Markdown Extra written in PHP. Extra adds a few features such as simple tables, but remains consistent with original Markdown formatting. Using that library, I was able to create my own dingus rather easily and alter the  tag with one line of code $render2 = str_replace("<pre>", "<pre class=\"prettyprint linenums\">", $render);. In my experimentation, I made a parser that reads a text file and outputs html, and three dingus parsers. Dingus1 does straightforward conversion of markdown extra to html. Dingus2 and 3 provide the class names for prettified code, with #3 going the extra step of applying stylesheets for the preview.

  
With this setup, I can quickly paste in my text document and pull html
code to paste into blogger.com's html edit box. With some more research,
I can modify the dingus to interact with blogger's API and post on my
behalf. There are also some WYSIWYM live editors that show you an
instant render of your markdown as you type (you type in a textarea
while your html renders in a nearby div). This would be a good way to do
some tweaking to the markdown text before posting the html to the web.
My next plans are to make a better dingus, possibly with a live preview
and a "post to blogger" option.  
Some other links:  

-   http://balupton.github.com/jquery-syntaxhighlighter/demo/
-   http://code.google.com/p/pagedown/wiki/PageDown
-   http://markitup.jaysalvat.com/examples/markdown/

  [blogger.com]: http://www.blogger.com/
  [SyntaxHighlighter]: http://alexgorbatchev.com/SyntaxHighlighter/
  [prettify]: http://www.geany.org/ "Geany"
  [Notepad++]: http://notepad-plus-plus.org/ "Notepad++"
  [markdown]: http://daringfireball.net/projects/markdown/
    "Markdown intro"
  [dingus]: http://daringfireball.net/projects/markdown/dingus
