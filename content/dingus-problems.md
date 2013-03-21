Title: dingus problems
Date: 2012-09-20 12:50
Author: John Hogenmiller (john@hogenmiller.net)

Yesterday, I ran into a small, but confusing issue converting from
markdown to html for a post. A markdown process will convert html in a
code block to html escaped entities. That way, when you use the
resulting html, your html example code doesn't get interpreted as html.

For example:

~~~~ {.prettyprint}
<p>This is a <strong>strong</strong> example.</p>
~~~~

Gets converted to:

~~~~ {.prettyprint}
<pre><code>&lt;p&gt;This is a &lt;strong&gt;strong&lt;/strong&gt; example.&lt;/p&gt;</code></pre>
~~~~

In the "dingus" I made, this didn't appear to be happening. The above
example rendered as:

~~~~ {.prettyprint}
<pre><code>This is a <strong>strong</strong> example.</p></code></pre>
~~~~

Furthermore, it worked perfectly fine using the "official" php-markdown
[dingus][]. I was using their library, and it's incredibly simple to
implement. After some digging, I discovered that in my dingus, the code
was being converted properly in my preview section, but not in my HTML
Source textarea. I was printing the same `$render` variable in both
sections, but getting different results in my browser.

As it turns out, most html elements are "CDATA" and a textarea is
"PCDATA". When all is said and done, this means that instead of needing
to send `&lt;`, I need to send `&amp;lt;` to the browser. Fortunately,
php has a function called `htmlspecialchars()` that does this for me.
For my HTML Output, I just needed to change `print $render` to
`print htmlspecialchars($render)`.

20120920

  [dingus]: http://michelf.ca/projects/php-markdown/dingus/
