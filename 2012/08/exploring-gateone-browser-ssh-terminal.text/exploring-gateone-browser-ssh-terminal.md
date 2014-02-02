Title: Exploring GateOne Browser SSH terminal
Date: 2012-08-01 12:09
Author: John Hogenmiller 

I came across a program called [Gate One] by LiftOff Software that
just amazed me. This is an open-source, web-based ssh terminal. It is
capable of multiple users, sessions, and bookmarks. I've tried a number
of AJAX terminals or Java applet based ones in the past. The javascript
ones usually did not have very good terminal emulation, while the Java
apps worked, but worked just like a local desktop app (making it's own
connection to port 22). Gate One uses WebSockets, allowing for full
duplex communication through your web browser over the same port 80 or
443 used to serve up the web page.

Installation
------------

Gate One is a python application using the [Tornado framework]. As
such, at runs independently of an existing web server and handles
connections from browsers internally. If you already have a web server
running on your system, you will need to tell Gate One to use a
different IP or a different port.

Installation using pre-built binaries or the source is fairly
straightforward and detailed in the [documentation].

The installer creates a directory of /opt/gateone and places all
necessary files there. You can run it by changing to that directory and
running gateone.py as root.

    johnh@puppet2:/opt/gateone$ sudo ./gateone.py
    [W 120801 13:52:06 terminal:166] Could not import the Python Imaging Library (PIL) so images will not be displayed in the terminal
    [W 120801 13:52:06 gateone:2232] dtach command not found.  dtach support has been disabled.
    [I 120801 13:52:06 gateone:1800] No authentication method configured. All users will be ANONYMOUS
    [I 120801 13:52:06 gateone:1876] Loaded plugins: bookmarks, help, logging, logging_plugin, notice, playback, ssh
    [I 120801 13:52:06 gateone:2329] Listening on https://*:443/

At this point, gateone is running in the foreground and you can view as
connections occur and any errors. Pressing Ctrl If you conect to gateone
using your webbrowser, you are logged in as user ANONYMOUS and can
connect to any ssh host, either localhost or something remote.

If you edit /opt/gateone/server.conf, you can change authentication to
"pam" or "google". Using pam will perform a Basic HTTP style
authenication requiring a system-level username and password. Using
google will log you in with your google account. Both of these "just
work" without complicated setup.

### Running as a Non-Root

Before I put something like this in production, I wanted to apply some
additional security. First off, I want to see if I can get this to run
as a non-root user.

Since gateone ran as root user initially, it has files owned by rootOnly UID 0 can open ports below 1024.gateone may need permission to write to system directories

To solve the first one, I chowned the /opt/gateone directory to my
username. In the future, I'll want to run it under its own user, but
I'll use mine for now for simplicity. To solve the second and third, I
edited server.conf.

    johnh@puppet2:/opt/gateone$ sudo chown -R johnh:johnh .
    johnh@puppet2:/opt/gateone$ vi server.conf# change/add the following lines appropriatelyport = 2443session_dir = "/opt/gateone/tmp/gateone"pid_file = "/opt/gateone/tmp/gateone.pid"uid = 1000gid = 1000
    johnh@puppet2:/opt/gateone$ ./gateone.py
    [W 120801 14:06:01 terminal:166] Could not import the Python Imaging Library (PIL) so images will not be displayed in the terminal
    [W 120801 14:06:01 gateone:2232] dtach command not found.  dtach support has been disabled.
    [I 120801 14:06:01 gateone:1802] No authentication method configured. All users will be ANONYMOUS
    [I 120801 14:06:01 gateone:1876] Loaded plugins: bookmarks, help, logging, logging_plugin, notice, playback, ssh
    [I 120801 14:06:01 gateone:2329] Listening on https://*:2443/

Authentication
--------------

Running as a lower uid, you can use authentication of None or "google"
without issue. If you use "pam", you discover you can only login with
the username that gateone is running under. If you are the only intended
user of the service, this may not be an issue. But if you want to allow
other users, this becomes an issue. If you are fine with running as root
or using Google as your authentication provider, you can ignore this
next step.

Fortunately, pam is highly configurable. You aren't required to
authenticate against shadow passwords. You can also authenticate against
db4 files with pam_userdb, msyql, or even htpasswd files. To start off,
I'm going to use htpasswd files. Note that Ubuntu doesn't provide
pam_pwdfile.so by default. You need to install libpam-pwdfile ("sudo
apt-get install libpam-pwdfile").

# Note - in testing, I discovered gateone uses Crypt encryption while htpasswd defaults to MD5. Use -d to switch to crypt encryption.

    johnh@puppet2:/opt/gateone$ htpasswd -c -d users.passwd user1
    New password:
    Re-type new password:
    Adding password for user user1
    johnh@puppet2:/opt/gateone$ cat users.passwd
    user1:KKEPyZtUf9sadf9

Create a pam module called gateone under /etc/pam.d

    johnh@puppet2:/opt/gateone$ cat /etc/pam.d/gateone
    #%PAM-1.0
    # Login using a htpasswd file
    @include common-sessionauth    
    required pam_pwdfile.so          pwdfile /opt/gateone/users.passwdaccount 
    required pam_permit.so

Modify server.conf to use pam and pam_service of gateone:

    auth = "pam"
    pam_service = "gateone"

Now start gateone and log in.

    johnh@puppet2:~/g1/gateone$ ./gateone.py
    [W 120801 14:59:16 terminal:168] Could not import the Python Imaging Library (PIL) so images will not be displayed in the terminal
    [W 120801 14:59:16 gateone:2577] dtach command not found.  dtach support has been disabled.
    [I 120801 14:59:16 gateone:2598] Connections to this server will be allowed from the following origins: 'http://localhost https://localhost http://127.0.0.1 https://127.0.0.1 https://puppet2 https://127.0.1.1 https://puppet2:2443'
    [I 120801 14:59:16 gateone:2023] Using pam authentication
    [I 120801 14:59:16 gateone:2101] Loaded plugins: bookmarks, help, logging, logging_plugin, mobile, notice, playback, ssh
    [I 120801 14:59:16 gateone:2706] Listening on https://*:2443/
    [I 120801 14:59:16 gateone:2710] Process running with pid 32591
    [I 120801 14:59:17 gateone:949] WebSocket opened (user1@gateone).

One additional nice feature with authentication enabled is the ability
to resume sessions - even across different computers or browsers.

Reverse Proxy
-------------

(I failed on this part, but felt it was worth recording)

Once I got it working in single user mode, I wanted to go ahead and set
this up under a reverse proxy under Apache. This would allow me to
integrate it into my existing web server under a sub-directory.

First, I edited server.conf to use a URL prefix of /g1/

Second, I tried setting up a ReverseProxy in Apache.

    # GateOne 
    ProxySSLProxyEngine 
    OnProxyPass /g1/ https://localhost:2443/g1/
    ProxyPassReverse /g1/ https://localhost:2443/g1/
    ProxyPassReverseCookieDomain localhost localhost
    ProxyPassReverseCookiePath / /g1/

This almost worked. I had no errors, but the resulting page was
unreadable. However, at the bottom was a clue. "The WebSocket connection
was closed. Will attempt to reconnect every 5 seconds... NOTE: Some web
proxies do not work properly with WebSockets." The problem was Apache
not properly proxying my websocket connection. People have managed to
get this working under nginx, but not Apache.

Searching for a solution led me to a similar question on ServerFault, an
apache-websocket module on github, and a websocket tcp proxy based on
that module.

-   http://serverfault.com/questions/290121/configuring-apache2-to-proxy-websocket
-   https://github.com/disconnect/apache-websocket
-   http://blog.alex.org.uk/2012/02/16/using-apache-websocket-to-proxy-tcp-connection/

In order to get this work, I'll need to download and compile some code.
The apxs command requires the apache-prefork-dev package in
Debian/Ubuntu. Install it with "sudo apt-get install
apache-prefork-dev".

Now we are ready to download the code and install the module:

    johnh@puppet2:~$ git clone https://github.com/disconnect/apache-websocket.git
    Cloning into 'apache-websocket'..... done
    johnh@puppet2:~$ wget http://blog.alex.org.uk/wp-uploads/mod_websocket_tcp_proxy.tar.gz
    johnh@puppet2:~$ cd apache-websocket
    johnh@puppet2:~/apache-websocket$ sudo apxs2 -i -a -c mod_websocket.c*snip*
    johnh@puppet2:~/apache-websocket$ sudo apxs2 -i -a -c mod_websocket_draft76.c*snip*
    johnh@puppet2:~$ cd examples
    johnh@puppet2:~$ tar -xzvf ../../mod_websocket_tcp_proxy.tar.gzmod_websocket_tcp_proxy.c
    johnh@puppet2:~$ cd apache-websocket/examples/
    johnh@puppet2:~/apache-websocket/examples$ sudo apxs2 -c -i -a -I.. mod_websocket_tcp_proxy.c
    *snip*
    chmod 644 /usr/lib/apache2/modules/mod_websocket_tcp_proxy.so
    [preparing module `websocket_tcp_proxy' in /etc/apache2/mods-available/websocket_tcp_proxy.load]
    Enabling module websocket_tcp_proxy.To activate the new configuration, you need to run:service apache2 restart
    johnh@puppet2:~$

Before we restart, I want to remove my Proxy lines and replace them with
the mod_websocket_tcp_proxy lines.

    SetHandler websocket-handler        
    WebSocketHandler  /usr/lib/apache2/modules/mod_websocket_tcp_proxy.so tcp_proxy_init        
    WebSocketTcpProxyBase64 on        
    WebSocketTcpProxyHost 127.0.0.1        
    WebSocketTcpProxyPort 2443        
    WebSocketTcpProxyProtocol base64    

Despite all this, I was still unable to get this to work. I even
attempted using the web root (/) as my location. If the Location matches
and your HTTP request is handled by mod_websocket, you get a 404. If
you use Proxy, then your websocket request is handled by mod_proxy.
Mod_proxy wins out over Location matches. Perhaps you can modify
gateone code to have one URL for the web interface and one for
websockets (or maybe it's already in place and we just need to know),
but I don't see a way at this time to get this working under Apache. I
may be able to work with the gateone author and the
mod_websocket_tcp_proxy.c author to come up with a solution. Or I
could try installing nginx. In the meantime, I can continue to run Open
Gate as a non-root user on a non-standard port. Alternatively, I could
find a wrapper to bring port 443 to 2443.

  [Gate One]: http://liftoffsoftware.com/Products/GateOne
  [Tornado framework]: http://www.tornadoweb.org/
  [documentation]: http://liftoff.github.com/GateOne/About/index.html
