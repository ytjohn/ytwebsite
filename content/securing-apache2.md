Title: Securing Apache2
Date: 2010-01-02
Author: John Hogenmiller (john@hogenmiller.net)

 A client wanted to make files available available to the web browser
from within their LAN and a handful of static IPs without requiring any
sort of username or password.  This is the web equivalent of a shared,
read only folder.  This is no big issue, you can create an .htaccess
file like so:  
  

> **Order deny,allow  
> Deny from all  
> Allow from 10.10.0.1/16  
> Allow from 127.0.0.1/32  
> Allow from 1.1.1.1/32**

  
However, they would also like to access it from a remote location with a
username and password.  
  
First, we need to create a password file.  In the old days, you would
use "AuthType Basic", but a more secure method is the Digest method.  To
use this, you must have the auth\_digest module loaded into your Apache
configuration.  If you are running a Debian or Ubuntu version, you can
do this by executing "**sudo a2enmod auth\_digest**".  Using digest
authentication prevents your username and password from being sent in
the clear (however, I always recommend that any site requiring
authentication should utilize https).  
  
Next,  you create your htdigest file:  

> **htdigest -c .htdigest *authname username***

When prompted, you would enter a password for *username*.  
  
Finally, you need to modify your .htaccess file to allow either method:  
  

> **Order deny,allow  
> Deny from all  
> AuthName "authname"  
> AuthType Digest  
> AuthUserFile /var/www/.htpasswd  
> require valid-userAllow from 10.10.0.1/16  
> Allow from 127.0.0.1/32  
> Allow from 1.1.1.1/32  
> Satisfy Any**  

Now, a user can come from the 10.10.x.x network, localhost, or 1.1.1.1
without requiring authentication.  If they later come from an
unrecognized IP, they can enter their username and password and be
granted access.  
  
--  
Securing Apache2 by IP or Username By YourTech John on January 2, 2010
8:40 AM
