Title: Nagios and XMPP
Date: 2011-02-28
Author: John Hogenmiller 

I found that someone has written a perl script geared towards sending
alerts from Nagios to XMPP usernames.  
  
http://www.gridpp.ac.uk/wiki/Nagios\_jabber\_notification  
  
I have downloaded this, but have not yet got it working as of yet, but
it does look promising.  It took me a while to update all the
dependencies for it, but if those were in place, the installation itself
is rather simple.  That is, the notification script works, but I haven't
actually configured nagios as of yet.  
  
This script has a shortcoming in that it only accepts the username
portion of the JID and not the domain name -- and this means that
notifications can only be sent between users of the same domain.  
  
To illustrate, user@example.net can not send a message to
user@example.com, but user1 and user2 on example.net can send to each
other.  
  

> \# this command will fail:  
> ytjohn@monitor:/usr/local/bin\$ ./notify\_by\_jabber.pl
> yourtech\\@example.com testing    
> \# while this one works  
> ytjohn@monitor:/usr/local/bin\$ ./notify\_by\_jabber.pl yourtech
> testing

  
  
And in the perl script, you have to specify the login credentials and
server you're connecting to:  
  
  

> \#\# Configuration  
> \# my \$username = 'system@example.com';   \# does not work  
> my \$username = 'system';  
> my \$password = "password";  
> my \$resource = "nagios";  
> \#\# End of configuration  
>   
>   
> my \$len = scalar @ARGV;  
> if (\$len ne 2) {  
>    die "Usage...\\n \$0 [jabberid] [message]\\n";  
> }  
> my @field=split(/,/,\$ARGV[0]);  
> \#------------------------------------  
>   
> \# Google Talk & Jabber parameters :  
>   
> my \$hostname = 'talk.google.com';  
> my \$port = 5222;  
> \# componentname is the second half of your JID:  
> my \$componentname = 'example.com';  
> my \$connectiontype = 'tcpip';  
> my \$tls = 1;

  
Originally posted: February 28, 2011 6:23 PM   

