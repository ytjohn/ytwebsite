Title: Starting with Ruby and AWS
Date: 2012-11-02 23:29
Author: John Hogenmiller (john@hogenmiller.net)

This weekend I decided to takle both learning Ruby and working with AWS
via the Ruby API. Having only played with both of these in the past,
this presents two learning challenges at once. However, from past
projects, this is how I learn best. I am somewhat familiar with AWS
terms and once made a script in Python to fire up an instance. This was
before Amazon came out with their management console, so I imagine
things have come a long way since then (hopefully easier). I also played
with Ruby for a while, but didn't have a decent project for it. Having a
project with goals will hopefully keep me on track and give me a way to
measure my progress.

My goals for this project are as follows:

1.  Utilize a web based interface. Using rails seems to be the popular
    way to do this, and I'd like to base my template interface off of
    [boilerstrap5], a combination of twitter-bootstrap and
    html5boilerplate. This will probably have the most trial and error
    to get it right.
2.  Connect to the AWS api and pull some basic information such as my
    account name.
3.  Fetch details about an AMI image. Maybe I'll be able to parse a list
    of public images, or maybe I can just punch in an image ID and pull
    up the details.
4.  Start an instance from an AMI image. This might require some steps
    like setting up a an S3 bucket -- we'll see.
5.  List my running instances.
6.  Control a running instance - ie, power cycle it.
7.  Destroy an instance.
8.  BONUS: Do something similar with S3 buckets - create, list, destroy.

First off, I need to setup a ruby development environment. Since I have
used [PyCharm] in the past, I will try JetBrain's [RubyMine] for my
editor environment. After installing this, the first thing I learned is
that rails is not installed. I could install using apt-get, but
Jetbrains recommends using [RVM]. It looks like a nice way to manage
different versions of Ruby, rails, and gems. I know when I have
installed Ruby applications requiring gems, gem versions was always a
source of concern. It is very easy to get mismatched gem versions in the
wild.

RVM install locally to \~/.rvm on linux, which is nice - you don't mess
up any system wide ruby installations and keep everything local to your
development environment. After installation, I had to figure out a
couple bits with rvm.

-   `rvm install 1.9.2` \# installs ruby 1.9.2
-   `rvm list` \# lists versions of ruby installed
-   `rvm use 1.8.7` \# use ruby 1.8.7

First, your terminal has to be setup as a login shell. This tripped me
up for a while until I changed the settings in my terminal emulator.
[terminator] has this as checkmark option.

    ytjohn@freshdesk:~$ rvm list
    
    rvm rubies
    
       ruby-1.8.7-p371 [ x86_64 ]
       ruby-1.9.2-p320 [ x86_64 ]
    
    # => - current
    # =* - current && default
    #  * - default
    
    ytjohn@freshdesk:~$ rvm use 1.8.7
    
    RVM is not a function, selecting rubies with 'rvm use ...' will not work.
    
    You need to change your terminal emulator preferences to allow login shell.
    Sometimes it is required to use `/bin/bash --login` as the command.
    Please visit https://rvm.io/integration/gnome-terminal/ for a example.
 

After switching to login

    ytjohn@freshdesk:~$ rvm use 1.8.7
    Using /home/ytjohn/.rvm/gems/ruby-1.8.7-p371

Finally, once you get ruby and rails working, you can create your rails
project. I'm starting with a rails project because it's "all the rage"
and gives you a decent running start. Later, I'll work on switching the
supplied templates with boilerplate + bootstrap based ones.

This gets me started. Next up, I'll actually create the project from
within RubyMine and just work on basic web functionality.

  [boilerstrap5]: https://github.com/ytjohn/boilerstrap5
  [PyCharm]: http://blog.yourtech.us/feeds/posts/www.jetbrains.com/pycharm/
  [RubyMine]: http://www.jetbrains.com/ruby/
  [RVM]: 
  [terminator]: http://software.jessies.org/terminator
