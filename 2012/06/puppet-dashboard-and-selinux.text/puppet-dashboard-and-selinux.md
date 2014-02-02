Title: Puppet Dashboard and selinux
Date: 2012-06-25
Author: John Hogenmiller 
Tags: puppet selinux

Once I got a rough handle on setting up Puppet, I decided to get [Puppet
Dashboard] working on my puppetmaster (a Centos 6 server) to have a
sort of web interface to view puppet statuses. Since I already have the
puppetlabs repositories setup from when I installed puppet, this was
almost as simple as running "yum install puppet-dashboard".

You then go to /usr/share/puppet-dashboard and follow the [install
guide] to get the database working. Then you can run it locally using
the "sudo -u puppet-dashboard ./script/server -e production" command or
starting the service (service puppet-dashboard start). I recommed
running it manually the first few times to make sure everything is
working.

At this point, I was able to browse to http://puppetmaster:3000/ and
view a nice looking dashboard with no hosts checked in. I then made sure
to add the following to puppetmaster's puppet.conf [master] section and
restart puppet.

    reports = http, store
    reporturl = http://localhost:3000/reports/upload

I performed a "puppet agent --test" on one of my puppets, and here is
where I ran into trouble. Everything appeared to work, but no report or
"pending task" showed up in the Dashboard. I ran the Dashboard locally
so I could see the http request coming in. No request. I double checked
my configuration, everything looked good.

Finally, I ran my puppetmaster in debug/no-daemonize mode.
(/usr/sbin/puppetmaster --debug --no-daemonize) so I could watch what
was happening. However, in this mode, it worked fine. I ran
/usr/sbin/puppetmaster without debugging and it still worked. The
reports would get submitted to dashboard if I ran puppetmaster directly,
but not if I started it with the init scripts.

I couldn't find any differences between how the init script was starting
puppetmaster vs me starting it manually. However, I did come across this
entry in /var/log/messages:


     Jul 25 10:15:16 puppetmasterj puppet-master[11988]: Compiled catalog for puppet2.lab in environment production in 1.16 seconds
     Jul 25 10:15:17 puppetmasterj puppet-master[11988]: Report processor failed: Permission denied - connect(2)


Which led me to the following entry in audit.log

     type=AVC msg=audit(1343225819.078:1582): avc:  denied  { name_connect } for  pid=11988 comm="puppetmasterd" dest=3000 scontext=unconfined_u:system_r:puppetmaster_t:s0 tcontext=system_u:object_r:ntop_port_t:s0 tclass=tcp_socket

This was an selinux issue. I quickly ascertained that turning enforcing
off in selinux allowed my reports to get through. I couldn't find anyone
else online encountering this issue. However, many people disable
selinux enforcing early on and I guess the cross-section of
puppet-dashboard users and those using selinux enforcing is somewhat
small.

How to fix this? There is a set of python programs called "audit2why"
and "audit2allow" as part of the policycoreutils-python package. These
tools will parse entries from the audit.log and either explain why an
action was denied or provide a solution. You can get these tools by
doing a "yum install policycoreutils-python".

Now we can use audit2allow to parse our audit.log error. You'll want to
run the tool, paste in your log entry, and then hit Ctrl+D on a blank
line.

     [root@puppetmasterj tmp]# audit2allow -m puppetmaster
     type=AVC msg=audit(1343232143.497:1617): avc:  denied  { name_connect } for  pid=12552 comm="puppetmasterd" dest=3000 scontext=unconfined_u:system_r:puppetmaster_t:s0 tcontext=system_u:object_r:ntop_port_t:s0 tclass=tcp_socket
     module puppetmaster 1.0;
     require {
         type puppetmaster_t;
         type ntop_port_t;
         class tcp_socket name_connect;
     }
     #============= puppetmaster_t ==============
     allow puppetmaster_t ntop_port_t:tcp_socket name_connect;


The above gives you a textual view of a module you can create to allow
puppetmaster to make an outbound connection. audit2allow will even
generate that module with the -M option.

     [root@puppetmasterj tmp]# audit2allow -M puppetmaster
     type=AVC msg=audit(1343232143.497:1617): avc:  denied  { name_connect } for  pid=12552 comm="puppetmasterd" dest=3000 scontext=unconfined_u:system_r:puppetmaster_t:s0 tcontext=system_u:object_r:ntop_port_t:s0 tclass=tcp_socket
     ******************** IMPORTANT ***********************
     To make this policy package active, execute:
     semodule -i puppetmaster.pp


That generated the module "puppetmaster.pp". Despite the pp extension,
this is not a puppet manifest, but an selinux binary module. Let's
install it.

     [root@puppetmasterj tmp]# semodule -i puppetmaster.pp

With that, puppetmaster can communicate with dashboard and reports are
flowing. The only remaining thing left to do is to file a bug report. As
it happened, someone had posted a bug report similar to this for
documentation on the puppetdb project. I decided to append to that
issue, but I suggested migrating the issue to the main puppet project.
Issue [#15567].

  [Puppet Dashboard]: http://projects.puppetlabs.com/projects/dashboard
    "Puppet Dashboard"
  [install guide]: http://docs.puppetlabs.com/dashboard/manual/1.2/bootstrapping.html
    "Puppet Install Guide"
  [#15567]: http://projects.puppetlabs.com/issues/15567
    "Issue 15567 selinux"
