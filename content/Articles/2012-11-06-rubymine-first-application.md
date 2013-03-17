Title: Rubymine First Application

Unfortunately, I ran out of any free time on the weekend, and this turned into a Tuesday evening project.

After my last post, I went ahead and told RubyMine to create a new rails application called "rubyweb2". The first issue I ran across was complaints about not having a JavaScript runtime. A very quick google search led me to [therailsblog.com](http://www.therailsblog.com/2011/09/could-not-find-javascript-runtime-see.html) where I was told to add two lines to the Gemfile in my project and run "bundle install". In fact, this is a cautionary note in the [getting started](http://guides.rubyonrails.org/getting_started.html) guide as well.

	gem "execjs"
	gem "therubyracer"

You can run `bundle install` from the project directory, or you can use RubyMine's Tools -> Bundler -> Install menu option. Once this was completed, I was able to run the application and got a default rails page on port http://localhost:3000/ - not bad.

Now, running the app will serve up my index.html, but it's nothing that I want yet. I'll start working through the [tutorial](http://guides.rubyonrails.org/getting_started.html#say-hello-rails) guide to setup some models, views, and controllers.


