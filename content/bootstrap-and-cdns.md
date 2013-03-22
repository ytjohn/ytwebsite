Title: Bootstrap and CDNs
Date: 2012-09-18 18:26
Author: John Hogenmiller
 
Often when creating a "modern" web page, it's very common to find yourself reinventing the wheel over and over again. I know any time I wanted to create a two-column layout, I would have to look at previous works of mine or search the Internet for a decent example. However, I recently came across Twitter's [Bootstrap] framework. At it's core, it's just a css file that divide your web page into a 12-column "[grid]". You create a "row" div, and inside that row you place your "span*" columns. Each span element spans from 1 to 12 columns, and should always add up to 12 for each row. You can also offset columns. There are css classes for large displays (1200px or higher), normal/default displays (980px), and smaller displays such as tablets (768px) or phones (480px). Elements can be made visible or hidden based on the device acessing the site (phone, tablet, or desktop). There is also a [javascript] component you can use for making the page more interactive.

[bootstrap]: http://twitter.github.com/bootstrap/index.html "Twitter Bootstrap"
[grid]: http://twitter.github.com/bootstrap/scaffolding.html#grid
[javascript]: http://twitter.github.com/bootstrap/javascript.html "Bootstrap Javascript"

If you download bootstrap, you get a collection of files to choose from. There's js/bootstrap.js, img/glyphicons-halflings.png, img/glyphicons-halflings-white.png, css/bootstrap.css, css/bootstrap-responsive.css. There is also a compress .min. version of the javascript and css files. You can read further about the [responsive] version of the css, or how to use the [icons].

[responsive]:	http://twitter.github.com/bootstrap/scaffolding.html#responsive
[icons]:			http://twitter.github.com/bootstrap/base-css.html#icons

Normally, one would take these downloaded files and put them into their own web application directory tree. However, there is a better way. Unless you are planning to use this on an Intranet with limited Internet access, you can use a copy of these files hosted on a "content delivery network (CDN)". A good example of this is the [jQuery] library hosted on Google's CDN. Google has a number of [hosted libraries] on their network. This has several advantages, one of which being caching. If everyone is pointing at a common hosted library, that library gets cached on the end-user's machine instead of being reloaded on every site that uses that library. 

[jquery]:	http://jquery.org/
[hosted libraries]: https://developers.google.com/speed/libraries/devguide

While bootstrap is not hosted on google, there is another CDN running on [CloudFlare] called [cdnjs] that provides a lot of the "less popular" frameworks, including bootstrap. Here are the URLs to the most current version of bootstrap files (they have version 2.0.0 through 2.1.1 currently).

[cdnjs]:		http://cdnjs.com/
[cloudflare]: 	http://www.cloudflare.com

* http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.1.1/css/bootstrap.css
* http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.1.1/css/bootstrap.min.css
* http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.1.1/css/bootstrap-responsive.css
* http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.1.1/css/bootstrap-responsive.min.css
* http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.1.1/bootstrap.js
* http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.1.1/bootstrap.min.css
* http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.1.1/img/glyphicons-halflings-white.png
* http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.1.1/img/glyphicons-halflings.png

All one has to do in order to use these is to add the css and the javascript (optional) to their page. Since most CDNs support both http and https, you can leave the protocol identifier out.

	<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.1.1/css/bootstrap.min.css">
	<script src="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.1.1/bootstrap.min.js">
	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>

Here's an example you can use on your own.

	<!DOCTYPE html>
	<html lang="en">

	<body>
	<div class="container-fluid">
			<div class="row-fluid">
			 <div class="span12 label label-info">
					<h1>Header</h1>
			 </div>
			</div>

			<div class="row-fluid">
			 <div class="span2">
					left column
					<i class="icon-arrow-left"></i>
			 </div>
			 <div class="span6">

					<p>center column

					<i class="icon-tasks"></i></p>

					<div class="hero-unit">
					 <h1>This is hero unit</h1>
					 <p>It is pretty emphasized</p>
					</div>

					<p>still in the center, but not so heroic</p>

			 </div>
			 <div class="span4">
					right column
					<i class="icon-arrow-right"></i>
			 </div>
			</div>
	</div><!-- end container -->

	<!-- load everything at end for fast content loading -->
	<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.1.1/css/bootstrap.min.css">
	<script src="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.1.1/bootstrap.min.js">
	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
	</body>
	</html>

	
Finally, I found that [NetDNA] also hosts bootstrap on their CDN at [www.bootstrapcdn.com]. I would say that either CDN would be fairly reliable, as they are both sponsored by their CDN they are running on. One advantage of this site is that they provide a lot more than just the basic bootstrap hosting such as custom themes and fonts.

To use them, you can simply swap out your css and js scripts.

	<link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/css/bootstrap-combined.min.css" rel="stylesheet">
	<script src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/js/bootstrap.min.js"></script>
	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
	

[www.bootstrapcnd.com]:	http://www.bootstrapcdn.com/
[NetDNA]:	http://www.netdna.com/

**UPDATE:** I added jquery into the above examples because several parts of bootstrap rely on it (such as the Modal dialogs).



20120918

