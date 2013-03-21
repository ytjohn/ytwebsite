Title: Sending messages using xmpppy
Date: 2011-04-05
Author: John Hogenmiller (john@hogenmiller.net)

In continuing working with XMPP and Python, I managed to get xmpppy
working.  
  
This proved to be particularly tricky because xmpppy uses some outdated
modules like md5 and sha.  It also relies on some dns functions which no
longer seem to work.  
  

> I was able to use the sample script "[xsend.py][]" that the project
> provides.  The big thing is that I had to specify talk.google.com and
> the port number directly in the connect command.

  
If I did not specify the servername, I would get the error:  
 An error occurred while looking up \_xmpp-client.\_tcp.example.com  
  
NOTE: DNS is configured correctly for the domain I was practicing with,
but the xmpppy code was not able to resolve it.  
  
To run the script, simply execute;  
  

> ./xblast.py destination@example.com  text to send

  
The Script:  

> \#!/usr/bin/python  
> \# \$Id: xsend.py,v 1.8 2006/10/06 12:30:42 normanr Exp \$  
> import sys,os,xmpp,time  
>   
> if len(sys.argv) \< 2:  
>     print "Syntax: xsend JID text"  
>     sys.exit(0)  
>   
> tojid=sys.argv[1]  
> text=' '.join(sys.argv[2:])  
>   
> jidparams={}  
>   
> jidparams['jid']='system@example.com'  
> jidparams['password'] = '123456'  
>   
> jid=xmpp.protocol.JID(jidparams['jid'])  
> cl=xmpp.Client(jid.getDomain(),debug=True)  
>   
> con=cl.connect(('talk.google.com',5222),  use\_srv=False)  
>   
> if not con:  
>     print 'could not connect!'  
>     sys.exit()  
> print 'connected with',con  
> auth=cl.auth(jid.getNode(),jidparams['password'],resource=jid.getResource())  
> if not auth:  
>     print 'could not authenticate!'  
>     sys.exit()  
> print 'authenticated using',auth  
>   
> \# cl.SendInitPresence(requestRoster=0)   \# you may need to uncomment
> this for old server  
> id=cl.send(xmpp.protocol.Message(tojid,text))  
> print 'sent message with id',id  
>   
> time.sleep(1)   \# some older servers will not send the message if you
> disconnect immediately after sending  
>   
> cl.disconnect()

  
  
---

  [xsend.py]: http://xmpppy.sourceforge.net/examples/xsend.py
